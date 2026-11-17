#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 唯一代码入口（本地 LLM 唯一允许的动作）

架构原则（最高优先级）：
  本地大模型（LLM）在本技能中**唯一允许的动作**是调用本脚本，并把 stdout
  原样透传给终端用户。任何难度判定、附件预处理、Coze 调用、结果缝合均由本脚本内部代码完成。

正确流程（2026-09-25 修正）：
  1) 附件判断：>5MB 本地转 Markdown 后按 .md 附件上传；<5MB 原文件直接上传
     （两条路径统一走 doc_context 通道，Coze 端拿到的都是文件附件）
  2) 难度分级：仅判断 vague / non-vague
  3) vague → 本地澄清循环；non-vague → 直接发 Coze

用法（**唯一入口**，v1.3.19 起单一路径）：
  python scripts/entry.py --q "用户问题"
  python scripts/entry.py --q "用户问题" --attach "/path/to/file.docx"

  输出（v1.3.20 起：全程明文，无编码分支、无开关）：
    stdout = 明文答案 + <<<CT_ANSWER_END>>> + checksum + answer_file 行
    另落一份 <技能根>/_answers/<sha16>.md（UTF-8，数据真源）
  说明：标记与 checksum 只在 `_emit_plain` 这一个地方产生；编码恒为 UTF-8 字节
  （`stdout.buffer.write`），不看控制台代码页、不看环境变量。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import subprocess
import tempfile
import time
from pathlib import Path

# UTF-8 强制（三流统一）+ stdout 恒 LF（2026-10-15：控制台回传链路会把 \n
# 转 \r\n，源头输出 LF + 校验和按 LF 口径计算，双保险免疫 CRLF 损耗）
for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace", newline="\n")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
for _p in (str(SCRIPT_DIR), str(SKILL_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Windows 子进程无控制台窗口（2026-10-15）─────────────────────────────────
# python.exe 是控制台子系统程序：父进程自身没有控制台时（如 WorkBuddy 桌面端
# 宿主直接拉起本脚本），下方 office_to_md / clarify_loop / refine_answer 等
# 子进程会让 Windows 新建控制台 → 屏幕闪出前台弹窗。CREATE_NO_WINDOW
# （+ STARTF_USESHOWWINDOW / SW_HIDE 双保险）令子进程完全后台运行；
# 三处调用均为 capture_output 管道捕获，取值不受影响。
_CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)


def _hidden_kwargs() -> dict:
    """返回抑制控制台弹窗的 subprocess 关键字参数（非 Windows 平台返回 {}）。"""
    if not sys.platform.startswith("win"):
        return {}
    kw = {"creationflags": _CREATE_NO_WINDOW}
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        kw["startupinfo"] = si
    except Exception:
        pass
    return kw

# ── 下游代码模块 ──────────────────────────────────────────────────────────────
from route import is_vague
from orchestrate import ANSWER_END, run_orchestrate

# ── query_origin 透传（2026-11-11 修复：advisorlog 5/9 非法根因）─────────────
# ct-base §8.6 + cloud_brief §4 契约：query_origin 由本地客户端生成并两层透传，
# 服务端禁止兜底生成。此前 entry.py 主链路出站 payload 缺该字段 → Coze advisorlog
# 写入器拿不到合规 sha256，落 5/9 脏值，飞书日志归因与追踪价值受损。
# 规范生成器 = hardware_id.hardware_id()（主板级 UUID/ MachineGuid → sha256:<64hex>）；
# 异常时回退主机名哈希，保证永不崩、永不空（空值会被端点 §1.4 拒绝）。
def _query_origin() -> str:
    try:
        from hardware_id import hardware_id
        o = hardware_id()
        if o and o.startswith("sha256:") and len(o) == 71:
            return o
    except Exception:  # noqa: BLE001 - 生成器不可用绝不阻断主流程
        pass
    try:
        import hashlib, socket
        return "sha256:" + hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()
    except Exception:  # noqa: BLE001
        return "sha256:" + "0" * 64

# ── B1 task 推断（2026-10-08）：payload 增加 suggested_task 辅助 Coze 端标注 ──
# 2026-10-16 修复：suggested_task 此前被 orchestrate._build_request 静默丢弃。
# 现通过 query_meta.task_category 透传到 Coze（orchestrate.py 同步修改）。
TASK_KEYWORDS = {
    "pairwise_meta": ["meta分析", "荟萃分析", "meta-analysis", "pooled", "合并效应量", "森林图"],
    "subgroup_analysis": ["亚组", "subgroup", "分层分析"],
    "single_group_meta": ["单组率", "单组均值", "metaprop", "metamean"],
    "nma": ["网状meta", "network meta", "nma", "multiple treatments"],
    "metareg": ["元回归", "metareg", "meta-regression"],
    "samplesize": ["样本量", "sample power", "检验效能", "power"],
    "survival_meta": ["生存meta", "hr", "hazard ratio", "km曲线"],
    "diagnostic_meta": ["诊断meta", "灵敏度", "特异度", "auc", "roc"],
}

def _infer_task(question: str) -> str:
    q = (question or "").lower()
    for task, kws in TASK_KEYWORDS.items():
        if any(kw.lower() in q for kw in kws):
            return task
    return "unclassified"

# §16.9 适配层：常驻编排服务的本地 HTTP 客户端（出站 urllib 逻辑已下沉）
from adapters.local_service_client import run_orchestrate_via_server

# 定界符常量
TOOL_DELEGATE_START = "<<<CT_TOOL_DELEGATE>>>"
TOOL_DELEGATE_END = "<<<CT_TOOL_DELEGATE_END>>>"

# 5MB 体积门
MAX_FILE_BYTES = 5 * 1024 * 1024


def _plain_text(text: str) -> str:
    """内部通篇明文：只做行尾归一。标记与 checksum 只在出口产生一次。"""
    return (text or "").replace("\r\n", "\n")


# ── 2026-11-10：复杂混合调用安全提示（调用之前发出 + 与结果一并返回）─────────
# 原实现把提示追加在缝合答案**末尾**，而 _merge_answer 只在 Coze 调用与兄弟技能
# 执行全部完成后才运行：混合调用在扣子端卡死 / 超时回落时该分支根本不执行，提示
# 彻底消失。本层在 entry.py 单一出口统一收口：出站前用本地零联网预判写 stderr
# 预警，最终答案再把同一提示前置到最前（幂等），覆盖所有成功 / 回落 / 短路分支。
_EARLY_HINT = ""      # 前置版（带分隔线），出口层拼接答案用
_EARLY_NOTICE = ""    # 纯正文，出站前 stderr 实时预警用


def _complexity_hint_pair(question: str) -> tuple:
    """本地零联网预判 → (纯正文 notice, 前置版 prefix)，非复杂混合调用返回 ("","")。

    只依赖 route_tool 的规则表，不触网、不依赖扣子端回传 complexity_hint 字段。
    """
    try:
        from route_tool import predict as _pred, complexity_hint_prefix
        p = _pred(question or "")
        tools = (p.get("need_tools") or []) if isinstance(p, dict) else []
        lang = "zh-CN" if re.search(r"[\u4e00-\u9fff]", question or "") else "en"
        return (complexity_hint_prefix(tools, lang, with_separator=False),
                complexity_hint_prefix(tools, lang, with_separator=True))
    except Exception:  # noqa: BLE001 - 提示是附加安全信息，异常绝不阻断主流程
        return ("", "")


def _with_complexity_prefix(output: str, prefix: str) -> str:
    """出口层去重 + 前置：全文恰好一次提示，且必在答案最前。

    2026-11-10 v1.63：云端 `GraphOutput.complexity_hint` 已改为**纯布尔标记**
    （v1.62 曾为提示文案，现已撤销），正常链路下本地 `refiner.py` 不解析、不渲染，
    因此不会出现两次；但为兼容仍在跑的旧端点、并杜绝任何未来重复源（v1.62 文案
    被消费端渲染进正文 / Coze LLM 自行写出同款提示 / --card-inline 子进程已前置 /
    缓存答案里带着旧提示），这里统一先剥净正文里所有同款提示段，再前置一次。
    无论上游怎么变，用户只看到一次；提示文本唯一真相源是本地 route_tool。
    """
    if not prefix:
        return output
    try:
        from route_tool import strip_complexity_hint
        body = strip_complexity_hint(output or "")
    except Exception:  # noqa: BLE001 - 极端兜底：剥离不可用时退化为「已前置则不重复」
        try:
            from route_tool import has_complexity_hint
            if has_complexity_hint(output or "", at_start=True):
                return output
        except Exception:  # noqa: BLE001
            pass
        body = output or ""
    return prefix + body


# ── 对外出口（2026-10-22 单一路径 · 唯一产生点）─────────────────────────────
# 形态：明文正文 + <<<CT_ANSWER_END>>> + checksum 行 + answer_file 行（纯 ASCII）。
# 结束标记放**尾部**：被通道截断时标记与 checksum 一起消失，失败一眼可辨。
PLAIN_END_MARK = "<<<CT_ANSWER_END>>>"

#: 答案文件目录（相对技能根，全 ASCII）＝数据真源。stdout 里给的是**相对路径**，
#: 避免用户名/目录含中文时路径本身在 cp936 控制台再次变成乱码。
ANS_DIR_NAME = "_answers"

#: 兜底目录（首选 `_answers/` 写不进去时用，如网络共享 ACL 拒绝）。作用只有一个：
#: 保证「终端乱码时还有一份完整明文可读」这条通道不会因为写盘失败而消失。
ANS_FALLBACK_DIR = Path(tempfile.gettempdir()) / "ct-advisor"


def _checksum16(text: str) -> str:
    """答案正文（LF 口径）的 sha256 前 16 位。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _answer_body(output: str) -> str:
    """从出口载荷取正文：剥掉尾部标记与其后的 checksum 行（内部已无编码包裹）。"""
    s = _plain_text(output)
    idx = s.rfind(PLAIN_END_MARK)
    if idx >= 0:
        s = s[:idx]
    s = re.sub(r"(?m)^[ \t]*checksum:[ \t]*[0-9a-f]{16}[ \t]*$", "", s)
    return s.strip("\n")


def _answer_ref(p: Path, is_primary: bool) -> str:
    """`answer_file:` 的取值：优先**绝对 POSIX 路径**，让 agent 一次 Read 就能取回原文。

    为什么不是相对路径：相对路径要求 agent 自己拼技能根，多一步就可能拼错或
    拼不到（cwd 不同）；而绝对路径是自解释的。

    唯一的约束是**这一行必须保持纯 ASCII**——它是乱码终端里唯一的指路牌，
    一旦含非 ASCII 就会和控制台一起坏掉。所以绝对路径含非 ASCII（如中文用户名）
    时，退回相对技能根的形式（全 ASCII），由 agent 拼上已知的技能根。
    """
    abs_posix = p.as_posix()
    if abs_posix.isascii():
        return abs_posix
    return f"{ANS_DIR_NAME}/{p.name}" if is_primary else abs_posix


def _write_answer_file(payload: str, cs: str) -> str:
    """把答案落到磁盘，返回 `answer_file:` 行的取值；两处都写不进去才返回空串。

    1) **同名且内容相同 → 跳过写入**。技能目录在网络共享上，ACL 为 creator-owner，
       覆盖既有文件会抛 `PermissionError 13`；而同一答案重复运行必然撞同一个
       sha16（缓存重放 / 同一问题重问）。无脑重写会把兜底通道打成「无文件」，
       比乱码更糟——所以先比内容，一致就直接复用。
    2) 首选失败退 `%TEMP%/ct-advisor/`。首选目录给绝对路径（ASCII 时）；TEMP 只能
       给绝对路径，属最后手段。
    """
    name = f"{cs}.md"
    for idx, d in enumerate((SKILL_ROOT / ANS_DIR_NAME, ANS_FALLBACK_DIR)):
        p = d / name
        try:
            d.mkdir(parents=True, exist_ok=True)
            if p.exists() and p.read_text(encoding="utf-8") == payload:
                return _answer_ref(p, idx == 0)
            p.write_text(payload, encoding="utf-8")
            if idx:
                sys.stderr.write(f"[entry] 技能目录不可写，答案已改存 {p.as_posix()}\n")
            return _answer_ref(p, idx == 0)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[entry] 答案文件写入失败({d}): {type(e).__name__}: {e}\n")
    return ""


def _emit_plain(output: str, exit_code: int = 0) -> None:
    """唯一出口：写答案文件（UTF-8）→ 按 UTF-8 字节写 stdout → 退出。

    编码决策**不在这里做**：不看 isatty、不看 sys.stdout.encoding、不看环境变量，
    一律 `stdout.buffer.write(utf-8 字节)`——常量编码，没有协商分支，也没有开关。
    显示层（终端代码页）与本函数无关：数据真源是 `_answers/<sha16>.md`，
    stdout 末尾的 `answer_file:` 行是纯 ASCII，任何代码页下都读得出来。
    """
    body = _answer_body(output)
    cs = _checksum16(body + "\n")          # 校验口径 = 标记之前的全部字节（含尾换行）
    payload = f"{body}\n{PLAIN_END_MARK}\nchecksum: {cs}\n"

    ref = _write_answer_file(payload, cs)
    if ref:
        payload += f"answer_file: {ref}\n"

    try:
        sys.stdout.flush()
        sys.stdout.buffer.write(payload.encode("utf-8"))
        sys.stdout.buffer.flush()
    except Exception:  # noqa: BLE001
        sys.stdout.write(payload)
    sys.exit(exit_code)


def _handle_attachment_oversized(attach_path: str, question: str) -> tuple:
    """附件 >5MB：本地转 Markdown 后**按 .md 附件上传**（doc_context 通道）。

    返回 (question, doc_context)。Coze 端拿到的是一份标准 .md 文件
    （经 /upload_file → mode=file_id），与 <5MB 原文件上传同一条通道。
    解析失败 / 格式不支持时返回 (带 ⚠️ 提示的 question, "")。
    """
    p = Path(attach_path)
    ext = p.suffix.lower()

    if ext in (".docx", ".xlsx", ".pptx"):
        # 2026-10-16 修复：subprocess.run 的 TimeoutExpired / OSError 此前未被捕获，
        # 大附件转换卡住或拉起失败会让 main 直接崩溃（stdout 为空，agent 无从交代）。
        # 附件转换是**可选增强**，失败应降级为「带提示的无附件提问」继续主流程。
        try:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "office_to_md.py"), str(p)],
                capture_output=True, text=True, timeout=120, **_hidden_kwargs()
            )
        except Exception as _e:  # noqa: BLE001
            return question + (
                f"\n\n⚠️ 附件《{p.name}》本地转换失败（{type(_e).__name__}），未能上传。请精简内容至 5MB 以下后重试。"
            ), ""
        if result.returncode != 0:
            return question + f"\n\n⚠️ 附件《{p.name}》解析失败，未能上传: {result.stderr[:200]}", ""
        md = result.stdout
    elif ext in (".txt", ".md", ".csv", ".tsv", ".json"):
        md = p.read_text(encoding="utf-8", errors="replace")
    else:
        return question + (
            f"\n\n⚠️ 附件《{p.name}》体积超过 5MB，格式 {ext} 暂不支持本地转换。"
            f"请精简内容至 5MB 以下后重试，或另存为 .docx/.xlsx/.pptx/.txt/.md。"
        ), ""

    # 写出临时 .md，按 md 格式走统一上传通道（<5MB 同一套账）
    md_path = Path(tempfile.gettempdir()) / f"ctadv_{p.stem}_oversized.md"
    md_path.write_text(md, encoding="utf-8")
    sys.stderr.write(f"[entry] >5MB 已转 md: {md_path} ({md_path.stat().st_size / 1024:.1f} KB)\n")
    payload_json, doc_id = build_file_payload(
        path=str(md_path),
        instruction=question,
        allow_upload=True,
    )
    note = (
        f"\n\nℹ️ 附件《{p.name}》体积超过 5MB，已转换为 Markdown 版并随问题上传，"
        f"云端将基于转换后的 .md 全文作答。"
    )
    return question + note, payload_json


def _handle_attachment_normal(attach_path: str, question: str) -> str:
    """附件 <5MB：调用 build_file_payload 构建 doc_context（JSON 字符串）。

    allow_upload=True 强制走上传通道（mode=file_id）——Coze 端原生解析原始文件，
    保真度高于本地转 md；上传失败时 build_file_payload 内部自动降级老通道
    （mode=file 转发 base64），仍不可行返回空串。
    """
    payload_json, doc_id = build_file_payload(
        path=attach_path,
        instruction=question,
        allow_upload=True,
    )
    return payload_json


def _run_clarify(original_question: str, max_rounds: int = 3) -> dict:
    """调用 clarify_loop 获取澄清问题（纯本地，无网络）"""
    payload = json.dumps({
        "original_question": original_question,
        "previous_answers": [],
        "round": 0,
        "max_rounds": max_rounds,
    }, ensure_ascii=False)
    # 2026-10-16 修复：subprocess.run 的 TimeoutExpired / OSError 此前落在 try 之外，
    # clarify_loop 卡住或拉起失败会让 main 直接崩溃。澄清是**可选**增强步骤，
    # 任何失败都必须降级为「可直接作答」并继续主流程，绝不阻断。
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "clarify_loop.py"),
             "--payload-inline", payload],
            capture_output=True, text=True, timeout=30, **_hidden_kwargs()
        )
        return json.loads(result.stdout)
    except Exception as _e:  # noqa: BLE001
        sys.stderr.write(
            f"[entry] 澄清循环不可用（降级为直接作答）: {type(_e).__name__}: {_e}\n"
        )
        return {"status": "decidable", "ambiguous": False, "questions": []}


def _extract_call_info(card_json) -> tuple:
    """从委托卡抽取「实际调用的兄弟技能 + 调用方法」。无卡（非 handoff）→ 本地直接作答。

    返回 (called_tools: list, call_method: dict|str)。best-effort：任何异常 → 本地直接作答。
    """
    if not card_json:
        return [], "local-direct"
    try:
        _c = json.loads(card_json)
        if not isinstance(_c, dict):
            return [], "local-direct"
        _tools = _c.get("need_tools") or []
        if isinstance(_tools, list) and _tools:
            _primary = _c.get("need_tool") or _tools[0]
        else:
            _primary = _c.get("need_tool")
            _tools = [_primary] if _primary else []
        _params = _c.get("params") or _c.get("tool_params") or {}
        return _tools, {"primary": _primary, "params": _params}
    except Exception:  # noqa: BLE001
        return [], "local-direct"


def _extract_delegate_card(output: str) -> str | None:
    """从输出中提取 CT_TOOL_DELEGATE 块的 card JSON（若有）。

    2026-10-16 修复：此前 `output.index(TOOL_DELEGATE_END)` 在「有 START 无 END」
    （输出被截断 / 拼接异常）时抛 ValueError，而调用方没有 try → main 直接崩溃、
    stdout 为空。现整段包在 try 内，任何形态异常一律降级为 None（当作无委托处理，
    由上游的 B64 包裹校验兜底）。
    """
    try:
        if TOOL_DELEGATE_START not in output or TOOL_DELEGATE_END not in output:
            return None
        start = output.index(TOOL_DELEGATE_START) + len(TOOL_DELEGATE_START)
        end = output.index(TOOL_DELEGATE_END)
        if end <= start:
            return None
        card = json.loads(output[start:end].strip())
        return json.dumps(card, ensure_ascii=False)
    except Exception:  # noqa: BLE001
        return None


def _run_card_inline(card_json: str, config_path: str) -> str:
    """代码执行 ct 技能并缝合（跳过 LLM 决策）"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "refine_answer.py"),
         "--card-inline", card_json,
         "--config", config_path],
        capture_output=True, text=True, timeout=300, **_hidden_kwargs()
    )
    return result.stdout


# ── L1：常驻编排服务（减少重模块重复导入，2026-09-25）──────────────────────
# 出站（urllib）逻辑已全部下沉到 adapters/local_service_client.py（§16.9）；
# entry.py 仅保留一个薄封装调用，详见该适配器。
def _run_orchestrate(payload: str, config: str) -> str:
    """常驻编排服务薄封装（出站入口）。

    2026-10-22 重构：本地答案缓存 / 去重短路已上移到 main() 统一由 session_store
    负责（跨 entry / proxy 一致），本函数仅做「常驻服务 → 内联」转发，
    不再内部查 answer_cache（避免与 session_store 双重维护、且无法区分「是否真实出站」）。
    """
    return run_orchestrate_via_server(payload, config)


def main():
    global _EARLY_HINT, _EARLY_NOTICE
    ap = argparse.ArgumentParser(
        description="ct-advisor 唯一代码入口（本地 LLM 唯一允许动作）"
    )
    ap.add_argument("--q", default=None, help="用户问题（--stitch 回程汇总模式下可省略）")
    ap.add_argument("--stitch", default=None,
                    help="回程汇总：JSON spec 或 @spec.json，由代码在本地缝合多个兄弟技能的产物；"
                         "默认不触网。spec.interpret=true 时额外请求 L3 方法学解释，"
                         "仅外发字段白名单内的脱敏数值摘要（F33）")
    ap.add_argument("--attach", default=None, help="附件路径")
    ap.add_argument("--q-meta", default=None, help="可选 query_meta JSON")
    ap.add_argument("--config", default=str(SKILL_ROOT / "config.json"))
    ap.add_argument("--max-clarify", type=int, default=3, help="澄清轮数上限")
    ap.add_argument("--session", default="",
                    help="会话标识（跨轮上下文/去重键）：proxy 或飞书应传入稳定 ID；"
                         "缺失则退化为单轮（仍享全局答案缓存，仅无多轮上下文）")
    args = ap.parse_args()

    # ── 0a) 回程汇总模式（2026-11-09，纯代码；默认零出站）────────────────
    # 补齐混合 handoff 的「回程」：用户分别调用多个兄弟技能后，把产物路径交给
    # 本入口，由代码机械解析并确定性缝合。仍是 entry.py 单一出口、同一明文协议；
    # 不走 vague gate / 缓存 / 委托，产物内容全程留在本机（F33）。
    # spec.interpret=true（用户显式）→ 追加 L3 方法学解释：由 interpret_results.py
    # 仅外发白名单内的脱敏数值摘要 + 代码构造的纯方法学问题；用户原问题、
    # 原始产物文本 / 文件名 / 路径 / 药名 / 方案名 / ID 一律不出域。
    # 🔴 HARD GATE 不变：本地 LLM 的唯一动作依旧是运行 entry.py 并原样输出 stdout。
    if args.stitch:
        from stitch_results import run_stitch, load_spec
        _spec = load_spec(args.stitch)
        if bool(_spec.get("interpret")):
            from interpret_results import run_interpret
            sys.stderr.write(
                "[entry] stitch+interpret 模式：本地汇总 + 脱敏数值摘要出站解释（F33 白名单）\n")
            _emit_plain(run_interpret(_spec, run_stitch(args.stitch), args.config))
        else:
            sys.stderr.write("[entry] stitch 模式：本地代码汇总，不出站\n")
            _emit_plain(run_stitch(args.stitch))
        return
    if not args.q:
        ap.error("--q 为必填项（使用 --stitch 回程汇总模式时可省略）")

    # ── 0) 依赖预检（2026-10-15 修订：requests 已改为可选） ──
    # 传输层切换为 stdlib urllib（refiner._call_coze）后 requests 不再是必需依赖：
    # 「依赖缺失」作为一类用户可见失败被整体消灭。此处仅留痕，不再 fail-fast 退出——
    # 装了 requests 行为不变，没装也经 urllib 正常出站。
    try:
        import requests  # noqa: F401
    except ImportError:
        sys.stderr.write("[entry] 未检测到 requests，使用 stdlib urllib 传输（功能不受影响）\n")

    original_question = args.q
    # 2026-11-10：复杂混合调用提示在此（任何出站 / 技能调用之前）用本地零联网
    # 预判算好；预警实际写出放在 5a 真实出站前，前置到答案放在唯一出口 7。
    _EARLY_NOTICE, _EARLY_HINT = _complexity_hint_pair(original_question or "")
    # 2026-10-16 修复：非法 --q-meta JSON 此前会让 main 抛 JSONDecodeError 崩溃
    # （stdout 为空）。query_meta 只是可选元信息，解析失败应降级为空 dict 并继续。
    query_meta = {}
    if args.q_meta:
        try:
            _qm = json.loads(args.q_meta)
            if isinstance(_qm, dict):
                query_meta = _qm
            else:
                sys.stderr.write("[entry] --q-meta 不是 JSON 对象（已忽略）\n")
        except Exception as _e:  # noqa: BLE001
            sys.stderr.write(
                f"[entry] --q-meta 非法 JSON（已忽略）: {type(_e).__name__}: {_e}\n"
            )
    doc_context = ""

    # ── 1) 附件判断 ─────────────────────────────────────────────────────────
    if args.attach:
        # 延迟导入（性能修复）：doc_memory(45KB) 仅在确有附件时才加载，避免无附件提问被拖慢
        from doc_memory import build_file_payload
        p = Path(args.attach)
        if not p.exists():
            original_question += f"\n\n⚠️ 附件未找到: {args.attach}"
        else:
            file_size = p.stat().st_size
            sys.stderr.write(f"[entry] 附件: {args.attach}, 体积: {file_size / 1024:.1f} KB\n")

            if file_size > MAX_FILE_BYTES:
                # >5MB：本地转 md 后，按 .md 附件上传（doc_context 通道）
                sys.stderr.write("[entry] 附件 >5MB，转 md 后按 md 格式上传\n")
                original_question, doc_context = _handle_attachment_oversized(args.attach, original_question)
                if doc_context:
                    sys.stderr.write(f"[entry] md doc_context 构建完成 ({len(doc_context)} chars)\n")
            else:
                # <5MB：直接上传（doc_context 通道）
                sys.stderr.write("[entry] 附件 <5MB，构建 doc_context 直接上传\n")
                doc_context = _handle_attachment_normal(args.attach, original_question)
                if doc_context:
                    sys.stderr.write(f"[entry] doc_context 构建完成 ({len(doc_context)} chars)\n")
                else:
                    sys.stderr.write("[entry] doc_context 构建失败，回退为无附件模式\n")

    # ── 2) 难度分级（仅判断 vague）──────────────────────────────────────────
    vague = is_vague(original_question)
    sys.stderr.write(f"[entry] vague: {vague}\n")

    # ── 3) 构建 payload ─────────────────────────────────────────────────────
    # query_meta 仅保留 difficulty（non-vague 统一标记为 forwarded，Coze 端自行判断）
    query_meta["difficulty"] = "vague" if vague else "forwarded"

    # 2026-10-16 修复：scope_hint 主链路缺失。此前 scope_guard 仅在 forward_guards
    # 中生效（refine_answer 路径），entry.py 主链路不调用。现加入 payload，
    # 使 Coze 端能获得范围路由标签（如 medical_writing）。
    _scope_hint = ""
    try:
        from scope_guard import assess as _assess_scope, domain_hint as _domain_hint
        _in_scope, _tag, _ = _assess_scope(original_question)
        if not _in_scope and _tag:
            _scope_hint = _tag
            sys.stderr.write(f"[entry] scope_guard: out-of-scope tag={_tag}\n")
        # 2026-11-09：domain 走 query_meta.domain_hint 独立字段，**不写进 scope_hint**。
        # 云端 full_analysis_node._doc_prompt_directive 把非空 scope_hint 一律渲染成
        # 「可能超出本技能核心覆盖范围」，正常方法学问题若带 domain 会被错误标注。
        # Coze KB 检索实际靠 extract_question_keywords(原问题) + category，
        # scope_hint 从不参与路由（state.py 注明「仅透传，不参与检索」）。
        _dh = _domain_hint(original_question)
        if _dh:
            query_meta["domain_hint"] = _dh
            sys.stderr.write(f"[entry] scope_guard: domain_hint={_dh} -> query_meta\n")
    except Exception:
        pass

    # ── 3b) 注入会话上下文（P0-3 修复：主链路此前从未调用 context_stitch，
    # 导致 Coze 永远只拿到单轮问题，用户被迫在「承接上一轮」里手工复述背景）────
    session_id = (args.session or "").strip()
    conversation_history = []
    # 2026-10-30（缓存键分区接线）：上下文指纹必须在「本轮尚未写入历史」时算，
    # 与 session_store.record 内部自动推导的口径一致（写入前历史）。
    # 首轮独立问题 → "h0"（跨用户可复用）；追问 → 真实历史指纹（不写全局缓存）。
    _history_key = "h0"
    try:
        import session_store as _ss
        conversation_history = _ss.history(session_id)
        _history_key = _ss.hist_fingerprint(conversation_history)
        if conversation_history:
            sys.stderr.write(
                f"[entry] 注入会话上下文 {len(conversation_history)} 轮 "
                f"(P0-3 修复) · 缓存分区 {_history_key}\n")
    except Exception:  # noqa: BLE001
        _history_key = "h?"

    payload = json.dumps({
        "query_meta": query_meta,
        "original_question": original_question,
        "draft_answer": "",
        "doc_context": doc_context,
        "suggested_task": _infer_task(original_question),
        "scope_hint": _scope_hint,
        "conversation_history": conversation_history,
        # 2026-11-11：补 query_origin 透传（修复 advisorlog 脏值；合规 sha256:<64hex>）
        "query_origin": _query_origin(),
    }, ensure_ascii=False)

    # ── 4) vague → 澄清循环 ─────────────────────────────────────────────────
    if vague:
        sys.stderr.write("[entry] 进入澄清循环\n")
        clarify_result = _run_clarify(original_question, args.max_clarify)
        status = clarify_result.get("status", "decidable")
        if status == "need_clarify":
            questions = clarify_result.get("questions", [])
            q_text = "\n".join(f"  - {q}" for q in questions)
            sys.stderr.write(f"[entry] 需澄清 {len(questions)} 项\n")
            _emit_plain(
                f"在回答之前，需要澄清以下问题：\n\n{q_text}\n\n"
                f"请针对以上问题逐一回复后，我将基于您的补充信息继续分析。"
            )
        # decidable / forced_decide → 继续发 Coze

    # ── 5) 短路：近窗去重 + 全局答案缓存（P0-2 修复）────────────────────
    # 对所有路径生效：vague 的 need_clarify 已在步骤 4 提前 exit，不会误短路；
    # 此处仅对「真正会出站」的问题做本地复用（覆盖重复发送澄清类问题也省出站）。
    shortcut = False
    _output_format = query_meta.get("output_format", "") or ""
    try:
        import session_store as _ss
        _dh, _dans, _dsecs = _ss.dedup_check(session_id, original_question,
                                            output_format=_output_format,
                                            history_key=_history_key)
        if _dh and _dans:
            sys.stderr.write(
                f"[entry] 近窗重复命中（{_dsecs}s 前）→ 本地短路复用，不出站\n")
            output = _plain_text(_dans)
            shortcut = True
        else:
            _cached = _ss.cache_get(
                original_question, doc_context,
                query_meta.get("difficulty", ""),
                output_format=_output_format,
                history_key=_history_key)
            if _cached:
                sys.stderr.write(
                    "[entry] 全局答案缓存命中 → 本地短路复用，不出站\n")
                output = _plain_text(_cached)
                shortcut = True
    except Exception:  # noqa: BLE001
        pass

    if not shortcut:
        # ── 5a) 真实出站 ───────────────────────────────────────────────
        # 2026-11-10 修复：安全提示必须在**出站 / 兄弟技能调用之前**发出。HARD GATE
        # 下本进程是同步子进程，stdout 在进程结束前不会被读取，故最早可落地通道是
        # stderr（调用前即写出，扣子端卡死时也已留痕）；最终答案另在出口把同一
        # 提示前置到最前，双路保证「调用之前」与「与结果一并返回」。
        if _EARLY_NOTICE:
            sys.stderr.write(
                "[entry] 复杂混合调用预警（出站/技能调用之前发出）：\n"
                + _EARLY_NOTICE + "\n")
        sys.stderr.write("[entry] 进入编排（出站 Coze）...\n")
        try:
            output = _run_orchestrate(payload, args.config)
        except Exception as e:
            sys.stderr.write(f"[entry] orchestrate 异常: {type(e).__name__}: {e}\n")
            output = _plain_text(
                f"⚠️ Coze 服务暂时不可用（{type(e).__name__}），"
                f"请稍后重试或检查网络连接。"
            )

        # ── 6) 检测 CT_TOOL_DELEGATE → 代码自动执行 card-inline ──────
        card_json = _extract_delegate_card(output)
        if card_json:
            sys.stderr.write("[entry] 检测到工具委托，代码自动执行 card-inline\n")
            # 2026-11-11：将合规 query_origin 注入委托卡（Coze 未必回显，
            # 本地兜底确保 handle_need_tool → 子技能透传 origin 一致、飞书归因不断链）
            try:
                _card_obj = json.loads(card_json)
                if isinstance(_card_obj, dict) and not _card_obj.get("query_origin"):
                    _card_obj["query_origin"] = _query_origin()
                    card_json = json.dumps(_card_obj, ensure_ascii=False)
            except Exception:  # noqa: BLE001 - 解析失败则维持原卡，不阻断
                pass
            _ci_out = ""
            try:
                _ci_out = _run_card_inline(card_json, args.config)
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"[entry] card-inline 异常: {type(e).__name__}: {e}\n")
            if _ci_out.strip():
                output = _ci_out
            else:
                sys.stderr.write("[entry] card-inline 产物为空，降级为人读提示\n")
                output = _plain_text(
                    "⚠️ 技能结果缝合失败：委托执行的本地技能未能返回有效结果。\n\n"
                    "可能原因：技能参数不完整、技能执行超时或该技能当前不可用。\n"
                    "请补充必要信息后重试；若持续失败，请把本条提示与上方 stderr 反馈给技能维护者。"
                )

        # ── 6a) 回传真实答案 + 调用方法到 Coze（2026-11-11 Fix B / Fix C）─────
        # Fix B：handoff 路径下，Coze 初始写的 advisorlog 只有路由决策（空/非实质答案）；
        # 本地产出真实答案后回调 /advisor_outcome，由 Coze upsert 单条权威记录。
        # Fix C（2026-11-11）：闸门从 `if card_json:` 扩展到 **所有真实答案**。服务端
        # async_feishu_write 是后台 daemon 线程，在 Serverless 容器回收场景下可能被
        # 掐断导致 batch_create 静默丢失（缺陷 A）；本地对非 handoff 答案同样回传
        # /advisor_outcome，服务端已有幂等跳过（行已含 outcome_reported 则跳过初始写，
        # async_feishu_writer.py:642-652），不会产生重复行，且保证每条真实答案必有
        # 记录、本地可观测成败。best-effort：异常一律吞掉，绝不阻断交付。
        try:
            from adapters.advisor_outcome import report_outcome
            from adapters.refiner import _skill_version
            from refine_answer import _get_endpoint_from_config
            _endpoint = _get_endpoint_from_config(args.config)
            if _endpoint:
                _called_tools, _call_method = _extract_call_info(card_json)
                report_outcome(_endpoint, {
                    "query_origin": _query_origin(),
                    "original_question": original_question,
                    "final_answer": output,
                    "called_tools": _called_tools,
                    "call_method": _call_method,
                    "skill_version": _skill_version(),
                })
                sys.stderr.write("[entry] advisor_outcome 回传已发起\n")
        except Exception as _e:  # noqa: BLE001
            sys.stderr.write(f"[entry] advisor_outcome 回传异常（忽略）: {type(_e).__name__}: {_e}\n")

        # ── 6b) 记录会话历史（仅真实出站；短路命中不重复记轮）────────
        try:
            import session_store as _ss
            _plain = _answer_body(output)
            if _plain.strip():
                _ss.record(
                    session_id, original_question, answer=_plain,
                    difficulty=query_meta.get("difficulty", ""),
                    doc_context=doc_context,
                    output_format=_output_format,
                    history_key=_history_key,
                )
        except Exception:  # noqa: BLE001
            pass

    # ── 7) 出口（唯一形态、唯一产生点；无开关）──────────────────────────
    # 2026-11-10：复杂混合调用提示前置到答案最前（幂等）。无论 Coze 成功慢回、
    # 超时回落、未授权、委托 card-inline 还是缓存短路，都随结果一并返回。
    _emit_plain(_with_complexity_prefix(output, _EARLY_HINT))


if __name__ == "__main__":
    # 顶层兜底（主流程出口契约）：任何未被内部捕获的异常此前都会让 Python 打印
    # traceback 并**留下空 stdout**——agent 只能看到「empty stdout」，无法向用户
    # 交代任何原因。这里统一转成合法的人读提示（明文 + 尾部校验），保证 stdout
    # 永远可交付、且与正常出口同一形态（2026-10-22 单一路径）。
    try:
        main()
    except SystemExit:
        raise
    except BaseException as _e:  # noqa: BLE001
        try:
            sys.stderr.write(f"[entry] 未捕获异常: {type(_e).__name__}: {_e}\n")
            _msg = (
                "⚠️ 技能执行出现未预期错误，无法生成答案。\n\n"
                f"{type(_e).__name__}: {_e}\n\n"
                "请稍后重试；若持续出现，请把本条提示与上方 stderr 反馈给技能维护者。"
            )
            _emit_plain(_with_complexity_prefix(_msg, _EARLY_HINT), exit_code=1)
        except BaseException:  # noqa: BLE001
            pass
        sys.exit(1)
