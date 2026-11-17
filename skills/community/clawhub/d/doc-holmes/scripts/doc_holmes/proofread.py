#!/usr/bin/env python3
"""C 级 LLM 错字校对（v2.3.0，plan T6.3）。

OCR 识别错误（错字/漏字/形近字）是扫描件翻译质量的头号损耗。本模块在重建
文本层之前，把 OCR 行文本分块送**用户自己配置的 LLM 端点**做"仅纠错不改写"
校对，修正后的行写回隐形文本层——译文源即修复后的文本。

设计约束：
- 行数守恒：LLM 返回行数与输入不一致时整块放弃（保守降级）；
- 优雅降级：任何网络/格式异常都回退原文，只记 stats，绝不阻塞翻译；
- 数据边界：文本只发用户自配端点（与翻译同一数据边界）。
"""

from __future__ import annotations

import json
import urllib.request

_PROMPT_HEAD = (
    "以下文本来自 OCR 扫描识别，可能含有识别错误（形近字、错字、漏字、多余空格）。\n"
    "请只修正明显的 OCR 识别错误，保持原意、语言、行数与换行位置完全不变。\n"
    "不要翻译、不要改写、不要增删内容、不要在段落之间插入空行、不要添加任何解释。"
    "直接输出修正后的全文。\n\n"
)


def _chunk_lines(lines, limit: int = 1500):
    """按字符数上限把行列表切成块（保留行边界）。"""
    blocks, cur, size = [], [], 0
    for ln in lines:
        ln_len = len(ln) + 1
        if cur and size + ln_len > limit:
            blocks.append(cur)
            cur, size = [], 0
        cur.append(ln)
        size += ln_len
    if cur:
        blocks.append(cur)
    return blocks


def _call_llm(text: str, base_url: str, api_key: str, model: str,
              timeout: int = 120) -> str:
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": _PROMPT_HEAD},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
        "max_tokens": max(1024, int(len(text) * 1.5)),
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=body, method="POST",
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        d = json.loads(resp.read().decode("utf-8", "ignore"))
    return d["choices"][0]["message"]["content"] or ""


def proofread_lines(lines, base_url: str, api_key: str, model: str,
                    timeout: int = 120, chunk_limit: int = 1500, llm_fn=None):
    """对 OCR 行列表做 LLM 错字校对。返回 (corrected_lines, stats)。

    任何失败都返回 (原 lines, {"error": ...})——绝不阻塞翻译流程。
    行数守恒：LLM 返回行数不一致的块整块放弃。
    """
    stats = {"blocks": 0, "blocks_failed": 0, "lines_changed": 0}
    if not lines:
        return list(lines), stats
    corrected_all = []
    for block in _chunk_lines(lines, chunk_limit):
        stats["blocks"] += 1
        try:
            text = "\n".join(block)
            resp = (llm_fn or _call_llm_checked)(text, base_url, api_key, model, timeout)
            fixed_lines = [l for l in resp.replace("\r\n", "\n").split("\n")]
            # 引擎侧常在末尾多一个空行/截断标记，容忍首尾空行
            while fixed_lines and not fixed_lines[-1].strip():
                fixed_lines.pop()
            while fixed_lines and not fixed_lines[0].strip():
                fixed_lines.pop(0)
            # LLM 常给段落间插空行：双侧空行 run 归一化后再比行数
            def _squeeze(seq):
                out, blank = [], False
                for l in seq:
                    if l.strip():
                        out.append(l)
                        blank = False
                    else:
                        if not blank:
                            out.append("")
                        blank = True
                while out and not out[-1].strip():
                    out.pop()
                return out
            if len(_squeeze(fixed_lines)) != len(_squeeze(block)):
                stats["blocks_failed"] += 1
                corrected_all.extend(block)
                continue
            changed = sum(1 for a, b in zip(block, fixed_lines) if a.strip() != b.strip())
            stats["lines_changed"] += changed
            corrected_all.extend(fixed_lines)
        except Exception as exc:
            stats["blocks_failed"] += 1
            stats.setdefault("error", str(exc)[:200])
            corrected_all.extend(block)
    return corrected_all, stats


def make_page_proofread(base_url: str, api_key: str, model: str,
                        timeout: int = 120, chunk_limit: int = 1500):
    """返回页级校对回调（rebuild_repaired_textlayer 的 line_proofread 参数）。

    回调契约：page_lines(list[str]) -> corrected(list[str])（长度一致）；
    任何失败返回原 lines（rebuild 侧按行数不一致整块放弃，等价降级原文）。
    累计统计挂在回调属性 .proofread_stats（dict）上，供审计读取。
    """
    stats = {"blocks": 0, "blocks_failed": 0, "lines_changed": 0,
             "pages_proofread": 0, "error": None}

    def _proofread(page_lines):
        if not page_lines:
            return list(page_lines)
        stats["pages_proofread"] += 1
        fixed, st = proofread_lines(page_lines, base_url, api_key, model,
                                    timeout=timeout, chunk_limit=chunk_limit,
                                    llm_fn=_call_llm_checked)
        for k in ("blocks", "blocks_failed", "lines_changed"):
            stats[k] = stats.get(k, 0) + st.get(k, 0)
        if st.get("error"):
            stats["error"] = st["error"]
        return fixed

    _proofread.proofread_stats = stats
    return _proofread


def _call_llm_checked(text: str, base_url: str, api_key: str, model: str,
                      timeout: int = 120) -> str:
    """带截断检测的 LLM 调用：finish_reason=length 视为失败（截断文本不能进校对层）。"""
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": _PROMPT_HEAD},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
        "max_tokens": _max_tokens_for(text),
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=body, method="POST",
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        d = json.loads(resp.read().decode("utf-8", "ignore"))
    choice = d["choices"][0]
    if choice.get("finish_reason") == "length":
        raise ValueError("LLM 输出被截断（finish_reason=length），块放弃")
    return choice["message"]["content"] or ""


def _max_tokens_for(text: str) -> int:
    """CJK 字符 token 比率更高：按 CJK 占比取 1.5~3.0 系数。"""
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    ratio = cjk / max(len(text), 1)
    factor = 3.0 if ratio > 0.3 else 1.5
    return max(1024, int(len(text) * factor))
