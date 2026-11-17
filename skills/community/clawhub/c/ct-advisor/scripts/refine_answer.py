#!/usr/bin/env python3
"""ct-advisor answer refiner entry point (called by the agent).

Reads 3 variables (JSON). Source priority (in-memory pipeline first, zero temp files):
  1) --payload-inline <JSON string> — zero file I/O, the agent's preferred path
  2) stdin pipe `echo '{...}' | python refine_answer.py` — no temp files, cross-platform safe
  3) positional arg (file path, legacy, avoid when possible)
Variables: query_meta (incl. query_origin machine id), original_question, draft_answer
Calls build_refiner().refine() to get the final answer, prints it to stdout.

query_meta is a JSON string with three fields:
  - difficulty: vague | forwarded (2026-09-26 binary gate; legacy simple/middle/complex
                values are still accepted for payload compatibility but carry no meaning —
                the Coze server always re-judges difficulty with its own LLM)
  - category:   question category (e.g. methodology:B / design / compliance:D)
  - accuracy:   self-rated accuracy good | normal (good = precise, normal = generic)

Robustness: any exception falls back to printing draft_answer and exits 0, so the agent
always gets a usable answer and the conversation never breaks due to a script crash.
By default it calls the Coze refiner with a single call and a conditional timeout — 90s default
(`refiner.timeout`), widened to 300s (`refiner.long_timeout`) for long tasks (route.timeout_tier
== "long" on the forwarded question / template-type category / follow-up with packed conversation
history). On Coze timeout/error it degrades to the local draft as a fault fallback — there is no
local-only mode; the stderr fallback line reports the *actual* resolved timeout, not a hardcoded
value.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Set

# ── Windows 子进程无控制台窗口（2026-10-15）─────────────────────────────────
# python.exe 是控制台子系统程序：父进程自身没有控制台时（如 WorkBuddy 桌面端
# 宿主直接拉起本脚本），下方 handle_need_tool 子进程会让 Windows 新建控制台
# → 屏幕闪出前台弹窗。CREATE_NO_WINDOW（+ STARTF_USESHOWWINDOW / SW_HIDE
# 双保险）令子进程完全后台运行；capture_output 管道捕获不受影响。
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

# 代码旁路模式（--ship）最终答案定界符：脚本输出唯一权威答案，agent 只做原样透传。
ANSWER_START = "<<<CT_ANSWER_START>>>"
ANSWER_END = "<<<CT_ANSWER_END>>>"
# 2026-10-22（v1.3.20）：本模块输出**明文**。v1.3.9 的 base64 ASCII-safe 信封已删除
# ——抗 cp936 乱码的职责上移到 entry._emit_plain（UTF-8 字节写 + 答案文件），
# 内部再加一层编码只会多出「谁负责解码」的分支。标记/checksum 只在 entry 出口产生。
NEED_PARAMS_MARKER = "<<<CT_NEED_PARAMS>>>"
INSTALL_MARKER = "<<<CT_INSTALL_REQUIRED>>>"

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters import build_refiner, RefineRequest, RefineResult, MissingDependencyError
from scripts.i18n import t  # noqa: E402  (user-facing prompts EN/ZH, locale-resolved)
# 复用入口预判（模式 B 前端高置信预取）：--ship 的 need_tool 分支用其补全真实参数，
# 避免纯 --ship 路径下任意 need_tool 都 100% 落到 need_params（Coze 仅判类别、不抽真实入参）。
from route_tool import (predict as _predict_tool, suggest_footer,  # noqa: E402
                        complexity_hint_text, complexity_hint_prefix,
                        has_complexity_hint)

def _load_auto_approve_endpoints(config_path: str) -> Set[str]:
    """从 config.json 加载 auto_approve_endpoints 白名单。"""
    try:
        cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
        return set(cfg.get("auto_approve_endpoints", []) or [])
    except Exception:
        return set()


def _get_endpoint_from_config(config_path: str) -> str:
    """从 config.json 读取 refiner.endpoint。"""
    try:
        cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
        return (cfg.get("refiner", {}) or {}).get("endpoint", "")
    except Exception:
        return ""


# Session-scoped in-memory authorization (resets per script invocation).
_SESSION_AUTHORIZED_ENDPOINTS: Set[str] = set()


def _check_outbound_authorization(endpoint: str, config_path: str) -> bool:
    """检查出站授权：返回 True 表示已授权可继续，False 表示未授权需拦截。"""
    # 1. 会话内存中已授权
    if endpoint in _SESSION_AUTHORIZED_ENDPOINTS:
        return True
    # 2. config.json 白名单中
    if endpoint in _load_auto_approve_endpoints(config_path):
        return True
    # 3. 未授权：输出机器信号 + 随 locale 切换的用户提示，agent 应展示给用户确认
    sys.stderr.write(
        f"[ct-advisor][AUTH-BLOCK] outbound to {endpoint} requires user confirmation.\n"
        f"\n{t('auth.coze_outbound', endpoint=endpoint)}\n"
    )
    return False

# On Chinese Windows the console defaults to cp936:
#  - stdin decoded as cp936 would corrupt the UTF-8 JSON piped in (the agent's main usage is piping JSON);
#  - stdout encoded as cp936 may raise UnicodeEncodeError on CJK/emoji/℃, and the consumer decoding as UTF-8 would get garbage.
# Fix all three standard streams to UTF-8 for consistent cross-platform, cross-console encoding behaviour.
# stdout 恒 LF（2026-10-15）：源头输出 LF；本模块不再算校验和（出口在 entry）。
for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace", newline="\n")  # type: ignore[attr-defined]
    except Exception:
        pass


def _detect_lang(text: str) -> str:
    """按 CJK 占比检测提问语言（≥15% → 'zh-CN'，否则 'en'）。

    2026-08-21：语言参数化——表格表头 / 来源标签随提问语言切换，
    保证英文提问交付全英文（结构化单元格数据保持原文不翻译）。
    """
    if not text:
        return "zh-CN"
    import re as _re
    cjk = len(_re.findall(r"[\u4e00-\u9fff]", text))
    return "zh-CN" if cjk >= max(1, len(text) * 0.15) else "en"


# §20.15：用户可经提示词关闭 message 置顶提示（逐次关键词本轮回退，关闭意图不回传 coze 端）
_MESSAGE_DISMISS_ZH = ("关闭提示", "不显示提示", "隐藏提示", "隐藏系统提示", "关闭系统提示",
                       "不要提示", "关掉提示", "别显示提示", "去掉提示", "屏蔽提示")
_MESSAGE_DISMISS_EN = ("no notice", "hide message", "hide notice", "disable tips",
                       "disable message", "suppress tips", "turn off notice",
                       "dismiss notice", "no message", "hide tips")


def _is_message_dismissed(question: str) -> bool:
    """判断用户本轮回传的提问是否要求关闭 message 置顶提示。

    仅匹配明确关闭意图关键词，避免误伤正常提问（§20.15）。关闭意图不回传 coze 端。
    """
    if not question:
        return False
    q = question.lower()
    return any(k in q for k in _MESSAGE_DISMISS_EN) or any(k in question for k in _MESSAGE_DISMISS_ZH)


def _format_message_banner(msg: dict, lang: str = "zh-CN") -> str:
    """§20.15：把归一化后的 message 渲染为置顶 banner 文本（Prepend 到答案最前）。

    level 仅影响样式前缀（tip/info/notice/warning），位置一律最前。
    dismissible=True 时附「回复 X 可隐藏」提示。
    """
    text = (msg.get("text") or "").strip()
    if not text:
        return ""
    level = msg.get("level", "notice")
    zh = lang == "zh-CN"
    prefix = {
        "tip": "💡 提示" if zh else "💡 Tip",
        "info": "ℹ️ 说明" if zh else "ℹ️ Note",
        "notice": "📌 提示" if zh else "📌 Notice",
        "warning": "⚠️ 提醒" if zh else "⚠️ Heads-up",
    }.get(level, "📌 提示" if zh else "📌 Notice")
    sep = "：" if zh else ": "  # 中文全角冒号无空格；英文半角冒号后空格，符合各自排版习惯
    banner = f"**{prefix}**{sep}{text}"
    if msg.get("dismissible", True):
        hint = "（回复「关闭提示」可隐藏此提示）" if zh else '(reply "no notice" to hide)'
        banner = f"{banner}\n\n{hint}"
    return banner


def _render_registry_landscape(res: dict, lang: str = "zh-CN") -> str:
    """把 ct-registry 聚合结果（landscape）渲染为用户友好 markdown 表格。

    2026-08-21：README 示例 2 实测——裸 JSON 块对用户不友好；改为
    「试验数汇总 + 分期/地域/申办方 三张两列表格 + xlsx 提示」。
    **表头/文案随提问语言（lang）切换，单元格检索数据（PHASE 3 / United States /
    Novo Nordisk 等）保持原文不翻译**（用户明确口径，2026-08-21）。
    """
    ls = res.get("landscape") or {}
    parts: list = []
    zh = lang == "zh-CN"
    n = ls.get("n_trials")
    if n is not None:
        raw = ls.get("raw_total")
        if zh:
            dedup = f"（去重后 {n} 条原始记录）" if raw is not None and raw != n else ""
            parts.append(f"**检索到 {n} 项注册试验**{dedup}")
        else:
            dedup = f" ({n} raw records)" if raw is not None and raw != n else ""
            parts.append(f"**{n} registered trials found**{dedup}")
    for field, (zh_t, en_t) in (
            ("phase_mix", ("**分期分布**", "**Phase distribution**")),
            ("region_mix", ("**地域分布**", "**Region distribution**")),
            ("top_sponsors", ("**主要申办方**", "**Top sponsors**"))):
        arr = ls.get(field)
        if isinstance(arr, list) and arr:
            rows = "\n".join(
                f"| {str(it.get('k', ''))} | {it.get('n', '')} |"
                for it in arr if isinstance(it, dict))
            title = zh_t if zh else en_t
            head = "| 类别 | 数量 |" if zh else "| Category | Count |"
            parts.append(f"{title}\n\n{head}\n|---|---|\n{rows}")
    excel = res.get("excel")
    if excel:
        parts.append(
            f"📊 完整试验清单（名称 / 阶段 / 地区 / 申办方）已导出：`{excel}`"
            if zh else
            f"📊 Full trial list (name / phase / region / sponsor) exported: `{excel}`")
    note = res.get("note")
    if note:
        parts.append(f"> {note}")
    if parts:
        return "\n\n".join(parts)
    # 无结构化字段可渲染时回退裸 JSON
    try:
        return json.dumps(res, ensure_ascii=False, indent=2)
    except Exception:
        return str(res)


def _render_skill_result(result, lang: str = "zh-CN") -> str:
    """把 need_tool 技能主产物渲染为可读文本（确定性，无 LLM）。"""
    # 2026-08-21：ct-registry 聚合 → 用户友好表格（README 示例 2 实测，替代裸 JSON）
    if isinstance(result, dict) and isinstance(result.get("landscape"), dict):
        return _render_registry_landscape(result, lang)
    if isinstance(result, (dict, list)):
        try:
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception:
            return str(result)
    return str(result) if result is not None else ""


def _stitch_hint(zh: bool) -> str:
    """回程汇总提示（2026-11-09，由代码生成，非 LLM 追加）。

    handoff 是单向的；用户分别跑完技能后，需要一条同样由代码驱动的回填路径，
    否则混合调用没有「回程」。提示给出可直接执行的入口与 spec 格式。
    """
    spec = ('{"question":"<原问题>","results":[{"tool":"ct-registry",'
            '"files":["<产物路径>"]}]}')
    if zh:
        return ("\n\n---\n\n💡 *回程汇总：上述技能跑完后，可把产物路径交给 "
                "`entry.py --stitch '<JSON>'`（或 `@spec.json`），由代码在本地缝合；"
                "默认不出站、不经 LLM、不改写数值。*\n\n格式：`" + spec + "`"
                "\n\n*如需对结果做方法学解释，在 spec 里加 `\"interpret\":true`："
                "仅把字段白名单内的**脱敏纯数值摘要**与代码构造的方法学问题发往 Coze，"
                "原始产物、药名、方案名、受试者数据与原问题均不出域；未授权或无白名单数值时"
                "自动只交付本地汇总。*")
    spec_en = spec.replace("<原问题>", "<question>").replace("<产物路径>", "<path>")
    return ("\n\n---\n\n*Return path: once the skills above have run, pass their output "
            "paths to `entry.py --stitch '<JSON>'` (or `@spec.json`). The summary is "
            "stitched locally by code — no egress by default, no LLM, no numeric rewriting.*"
            "\n\nFormat: `" + spec_en + "`"
            "\n\n*For a methodology interpretation of the results, add `\"interpret\":true` "
            "to the spec: only allowlisted **sanitized numeric values** and a code-built "
            "methodology question are sent to Coze. Raw outputs, drug/protocol names, "
            "subject data and the original question never leave this machine; if the "
            "endpoint is unauthorised or no allowlisted values exist, only the local "
            "summary is delivered.*")


def _complexity_tools(tool_out: dict) -> list:
    """从执行结果归一化出本次涉及的兄弟技能列表（多工具信号，纯代码）。

    deferred_tools 在真实执行流中是 [{tool, params, ...}] 字典列表，需取 tool 字段；
    need_tools 内也可能夹带字典，统一归一化为字符串。
    """
    if not isinstance(tool_out, dict):
        return []
    tool = tool_out.get("tool")
    deferred = tool_out.get("deferred_tools") or []
    tools = list(tool_out.get("need_tools") or [])
    if not tools and tool:
        names = [tool]
        for d in deferred:
            if isinstance(d, dict):
                if d.get("tool"):
                    names.append(d["tool"])
            elif d:
                names.append(d)
        tools = names
    norm = []
    for t in tools:
        if isinstance(t, dict):
            t = t.get("tool")
        if t:
            norm.append(t)
    return norm


def _complexity_hint(tool_out: dict, lang: str = "zh-CN") -> str:
    """兼容旧调用：返回「末尾追加式」提示文本（出口层现已统一改用前置版）。

    文本由 route_tool.complexity_hint_text 统一生成（单一真相源，避免两端措辞漂移）。
    """
    return complexity_hint_text(_complexity_tools(tool_out), lang)


def _prepend_complexity(answer: str, tool_out: dict, lang: str = "zh-CN") -> str:
    """复杂混合调用安全提示前置到答案**最前**（2026-11-10 修复，幂等）。

    原实现把提示追加在缝合答案末尾；若混合调用在扣子端卡死 / 超时回落，
    ``_merge_answer`` 根本不执行，提示永不出现。前置后只要执行结果显示多工具，
    提示就会随结果一并返回，用户第一眼即可看到「长时间无反馈请拆分重问」。
    """
    prefix = complexity_hint_prefix(_complexity_tools(tool_out), lang)
    if not prefix or has_complexity_hint(answer or "", at_start=True):
        return answer
    return prefix + (answer or "")


def _complexity_prefix_from_q(question: str, lang: str = "zh-CN",
                              with_separator: bool = True) -> str:
    """基于本地预判（零联网）直接由问题算出提示，供「调用之前 / 回落」场景使用。

    本地 route_tool 预判即可判定多工具，**不依赖扣子端是否返回 complexity_hint
    字段，也不依赖 _merge_answer 是否执行**。返回空串表示非复杂混合调用。
    """
    try:
        pred = _predict_tool(question)
        tools = (pred.get("need_tools") or []) if isinstance(pred, dict) else []
    except Exception:  # noqa: BLE001
        tools = []
    return complexity_hint_prefix(tools, lang, with_separator=with_separator)


def _with_q_prefix(text: str, prefix: str) -> str:
    """幂等前置：答案里已有提示（如 --card-inline 子进程已加）则不重复添加。"""
    if not prefix or has_complexity_hint(text or "", at_start=True):
        return text
    return prefix + (text or "")


def _pre_call_complexity(question: str, lang: str = "zh-CN") -> str:
    """「调用之前发出」+ 返回可前置到答案的前缀（两路同源，纯代码）。

    HARD GATE 下本进程是同步子进程，stdout 在进程结束前不会被读取，故「调用之前」
    能落地的最早通道是 stderr（调用前即写出，即便后续卡死也已留痕）；「与结果
    一并返回」由返回值前缀在最终出口完成。
    """
    prefix = _complexity_prefix_from_q(question, lang, with_separator=True)
    if prefix:
        notice = _complexity_prefix_from_q(question, lang, with_separator=False)
        if notice:
            sys.stderr.write(
                "[ct-advisor] 复杂混合调用预警（调用之前发出）：\n" + notice + "\n")
    return prefix


def _render_deferred_cards(tool_out: dict, lang: str = "zh-CN") -> str:
    """混合跨技能：把 deferred_tools 渲染成**可直接调用的 @skill 卡片列表**（纯代码）。

    2026-11-09：客户端已可直接调用本机注册技能。此前多源问题只在信封里带
    deferred_tools、答案正文却只有主技能一张卡片，其余技能对用户完全不可见
    （test_cross_skill_handoff.py B 组 8 条曾全部 FAIL）。这里让每个技能都带上
    mention / 已按各自白名单拆分的参数 / 缺失参数 / 交付物 / B 档保密等级，
    用户可分别一键调用，不必等 advisor「再逐个调用」。
    """
    deferred = tool_out.get("deferred_tools") or []
    if not deferred:
        return ""
    zh = lang == "zh-CN"
    lines = []
    for d in deferred:
        if not isinstance(d, dict):
            continue
        tool = d.get("tool") or ""
        mention = d.get("mention") or ("@skill:%s" % tool)
        p = d.get("params") or {}
        p_txt = ("；" if zh else ", ").join(f"{k}={v}" for k, v in p.items()) \
            or ("（无）" if zh else "(none)")
        missing = d.get("missing") or []
        miss_txt = "/".join(str(m) for m in missing) or ("无" if zh else "none")
        deliv = d.get("deliverables") or ""
        # 英文路径不复用中文交付物文案（避免中英混杂）
        show_deliv = bool(deliv) and (
            zh or not any("\u4e00" <= c <= "\u9fff" for c in str(deliv)))
        conf = bool(d.get("confidential"))
        # 本机未注册的技能不得伪装成可直接调用的 @skill 卡片（反幻觉 / 反误导）。
        # 兼容旧执行卡信封：缺省 client_callable 视为可调用。
        if d.get("client_callable", True) is False:
            if zh:
                lines.append(f"- `{tool}`：⚠️ 该技能当前**本机未注册**，客户端尚无法直接调用；"
                             "请先在近端运行环境准备该技能。")
            else:
                lines.append(f"- `{tool}`: not registered locally; the client cannot invoke "
                             "it directly yet — prepare the skill in the local runtime first.")
            continue
        if zh:
            line = f"- `{mention}`" + (f"：{deliv}" if show_deliv else "")
            line += f"｜已识别参数：{p_txt}｜需补齐：{miss_txt}"
            if conf:
                line += "｜⚠️ B 档涉密，请在本机执行"
        else:
            line = f"- `{mention}`" + (f": {deliv}" if show_deliv else "")
            line += f" | params: {p_txt} | missing: {miss_txt}"
            if conf:
                line += " | Tier-B: run locally, confidential input"
        hint = d.get("hint") if zh else (d.get("hint_en") or d.get("hint"))
        if hint:
            line += ("｜💡 " + hint) if zh else (" | " + hint)
        lines.append(line)
    if not lines:
        return ""
    has_callable = any(
        isinstance(d, dict) and d.get("client_callable", True) is not False
        for d in deferred)
    if zh:
        if has_callable:
            return ("\n\n### 其余可直接调用的技能\n\n"
                    "本次提问还涉及下列技能，可分别按卡片直接调用（各自参数已随附；"
                    "标注「本机未注册」的需先在近端准备该技能）：\n"
                    + "\n".join(lines))
        return ("\n\n### 其余技能（当前本机未注册）\n\n"
                "本次提问还涉及下列技能，但本机尚未注册，客户端暂时无法直接调用：\n"
                + "\n".join(lines))
    if has_callable:
        return ("\n\n### Other skills you can invoke directly\n\n"
                "This question also involves the skills below; invoke each from the client "
                "with the params already extracted (items marked not registered must be "
                "prepared in the local runtime first):\n" + "\n".join(lines))
    return ("\n\n### Other skills (not registered locally)\n\n"
            "The question also involves the skills below, which are not registered "
            "locally yet and cannot be invoked from the client:\n" + "\n".join(lines))


def _merge_answer(coze_answer: str, tool_out: dict, lang: str = "zh-CN") -> str:
    """确定性缝合：Coze 原答案 + 补充信息（含来源标签）。纯代码，不依赖 LLM。

    lang（2026-08-21）：来源标签 / 文案随提问语言切换（zh-CN → 中文，en → 英文），
    结构化数据内容（表格单元格等）保持原文。
    """
    tool = tool_out.get("tool") or "ct-tool"
    status = tool_out.get("status")
    if status == "ok":
        res = _render_skill_result(tool_out.get("result"), lang)
        extra = _render_deferred_cards(tool_out, lang)
        # 2026-09-10（用户要求）：调用兄弟技能后，缝合层追加一行「建议直接用该技能」——
        # 缝合结果是可读摘要，用户若要核实 / 获取更详细的原始输出，应直接运行该技能本身。
        # 2026-11-09：混合跨技能时，其余技能也各自附上可直调的 @skill 卡片。
        if lang == "zh-CN":
                return (f"{coze_answer}\n\n---\n\n## 补充信息（来源：{tool}）\n\n{res}"
                        f"\n\n💡 *以上为该技能结果的可读摘要；如需可复算结果或文件交付物，"
                        f"请在客户端直接调用 `@skill:{tool}`。*") + extra
        return (f"{coze_answer}\n\n---\n\n## Supplementary data (Source: {tool})\n\n{res}"
                        f"\n\n💡 *The above is a readable summary of this skill's result; "
                        f"for reproducible results or file deliverables, invoke `@skill:{tool}` directly.*") + extra
    if status == "handoff":
        # 2026-11-09（客户端已可直接调用兄弟技能）：代码产出 @skill 卡片，
        # 把执行权交回技能本体，避免用户只拿到 advisor 缝合的纯文本摘要。
        # 🔴 卡片是答案正文的一部分，由 entry.py 单一出口输出；本地 LLM 不参与生成、
        #    不得改写，也不得据此自行发起技能调用（SKILL.md HARD GATE）。
        rp = tool_out.get("result") or {}
        rp = rp if isinstance(rp, dict) else {}
        mention = rp.get("mention") or f"@skill:{tool}"
        pms = rp.get("params") or {}
        missing = rp.get("missing") or []
        purpose = rp.get("purpose") or ""
        deliverables = rp.get("deliverables") or ""
        confidential = bool(rp.get("confidential"))
        zh = lang == "zh-CN"
        param_txt = ("；" if zh else ", ").join(f"{k}={v}" for k, v in pms.items()) \
            or ("（无）" if zh else "(none)")
        # 英文路径不复用中文 payload（2026-09-10 unreleased_b 同款修复）：
        # purpose / deliverables 来自 tool_mapping.json，恒为中文，直接拼会中英混杂。
        def _ascii_only(text: str) -> bool:
            return not any("\u4e00" <= c <= "\u9fff" for c in str(text))
        p_line = ""
        d_line = ""
        if purpose and (zh or _ascii_only(purpose)):
            p_line = f"- 用途：{purpose}\n" if zh else f"- Purpose: {purpose}\n"
        if deliverables and (zh or _ascii_only(deliverables)):
            d_line = (f"- 完整交付物：{deliverables}\n" if zh
                      else f"- Full deliverables: {deliverables}\n")
        miss_block = ""
        if missing:
            items = "\n".join(f"- {m}" for m in missing)
            miss_block = (f"\n\n调用前建议补齐：\n{items}" if zh
                          else f"\n\nSuggested params to supply:\n{items}")
        guard = ""
        if confidential:
            guard = ("\n\n⚠️ 该技能属 B 档（输入涉密）：请在本机用它处理真实方案 / 受试者数据，"
                     "不要把资料发往公共检索端点或 Coze 通道（F33 出域红线）。"
                     if zh else
                     "\n\n⚠️ Tier-B skill (confidential input): run it locally against real "
                     "protocols / subject data; never send those materials to public endpoints.")
        extra = _render_deferred_cards(tool_out, lang)
        back = _stitch_hint(zh)
        if zh:
            return (f"{coze_answer}\n\n---\n\n## 可直接调用：{mention}\n\n"
                    f"该技能已在本机注册，客户端可直接调用；ct-advisor 不再代跑 CLI，"
                    f"以免只拿到速览摘要。\n"
                    f"{p_line}"
                    f"- 已识别参数：{param_txt}\n"
                    f"{d_line}"
                    f"{miss_block}{guard}\n\n"
                    f"以上为本技能按自身能力给出的方法学回答；真实数据、可复算结果与文件"
                    f"请以上述技能的实际输出为准。") + extra + back
        return (f"{coze_answer}\n\n---\n\n## Invoke directly: {mention}\n\n"
                f"This skill is registered locally and can be called from the client; "
                f"ct-advisor does not run its CLI on your behalf, so you get the full "
                f"deliverable instead of a brief summary.\n"
                f"{p_line}"
                f"- Params identified: {param_txt}\n"
                f"{d_line}"
                f"{miss_block}{guard}\n\n"
                f"The answer above is ct-advisor's own methodology answer; rely on the "
                f"skill's actual output for real data, reproducible results and files.") + extra + back
    if status == "need_params":
        mp = tool_out.get("result") or {}
        missing = mp.get("missing", []) if isinstance(mp, dict) else []
        miss_txt = "\n".join(f"- {m}" for m in missing) or "(详见执行器输出)"
        if lang == "zh-CN":
            return (f"{coze_answer}\n\n---\n\n{NEED_PARAMS_MARKER}\n"
                    f"以下补充信息需要先由你向用户追问并补齐参数后才能获取：\n{miss_txt}")
        return (f"{coze_answer}\n\n---\n\n{NEED_PARAMS_MARKER}\n"
                f"Additional data requires you to ask the user for these missing params first:\n{miss_txt}")
    if status == "referral":
        # F1, 2026-09-03：referral-only 技能（如 meta-analysis）不经 need_tool 自动调用；
        # 缝合层把 Coze 原答案 + 显式调用引导一起透出，而不是当作错误。
        rp = tool_out.get("result") or {}
        msg = rp.get("message", "") if isinstance(rp, dict) else str(rp)
        mention = rp.get("mention", f"@{tool}") if isinstance(rp, dict) else f"@{tool}"
        if lang == "zh-CN":
            return (f"{coze_answer}\n\n---\n\n## 需显式调用的本地技能：{tool}\n\n"
                    f"{msg}\n\n请使用：{mention}")
        return (f"{coze_answer}\n\n---\n\n## Local skill to invoke explicitly: {tool}\n\n"
                f"{msg}\n\nUse: {mention}")
    if status == "install_required":
        # 2026-09-10 A/B 档门控：A 档技能未安装。
        # 🔴 安装姿态（同日第二轮，用户要求）：安装要下载并写入本地技能目录，**可能触发本机
        # 安全警告**，故默认 `install_mode="suggest"` —— **只建议、不执行**：向用户说明用途 +
        # 给出命令，由用户自行执行；仅当用户给出**明确授权**（卡片 install_consent="approved"
        # 重跑 → install_mode="authorized"）才可由 agent 代为执行。拒绝 → 带
        # install_consent="declined" 重跑（由代码产出未取数兜底答案）。
        rp = tool_out.get("result") or {}
        rp = rp if isinstance(rp, dict) else {}
        purpose = rp.get("purpose") or ""
        # 2026-09-10 修正：安装通道统一为 SkillHub。
        # `install_command` 由 handle_need_tool._install_command() 生成（含 --dir 与完整
        # 解释器路径，实测可执行）；**不得**渲染裸 `skillhub install` —— PATH 中无该命令
        # （~/.local/bin/skillhub 在本机不存在，其 bash 启动器另有 Windows 路径 bug）。
        sid = rp.get("skillhub") or tool
        cmd = rp.get("install_command") or ""
        hint = rp.get("install_hint") or ""
        note = rp.get("install_note") or ""
        authorized = rp.get("install_mode") == "authorized" or bool(rp.get("install_authorized"))
        missing = rp.get("missing") or []
        miss_txt = "\n".join(f"- {m}" for m in missing) if missing else ""
        if lang == "zh-CN":
            tail = f"\n若安装后仍需补参数，请一并提供：\n{miss_txt}" if missing else ""
            cmd_line = f"- 安装命令：`{cmd}`\n" if cmd else ""
            how_line = f"- 取包说明：{hint}\n" if hint else ""
            note_line = f"- ⚠️ {note}\n" if note else ""
            if authorized:
                act = ("用户**已明确授权**安装（install_consent=approved）→ 执行上述安装命令；"
                       "成功后带**原执行卡**重跑，由代码调用该技能并缝合。")
            else:
                act = ("🔴 **只建议、不执行**：向用户说明该技能用途，把上面的安装命令原样给出"
                       "（**用户可自行执行**），并说明「安装会写入本地技能目录、可能触发本机"
                       "安全提示」。**在用户明确授权前，不得代为执行该命令**；"
                       "用户回复授权安装 → 在卡片加 \"install_consent\": \"approved\" 重跑。")
            return (f"{coze_answer}\n\n---\n\n{INSTALL_MARKER}\n"
                    f"需调用 A 档技能「{tool}」补充信息，但本地尚未安装"
                    f"（{'用户已授权安装' if authorized else '**建议安装**'}）。\n"
                    f"- 用途：{purpose}\n"
                    f"- SkillHub 标识：`{sid}`\n"
                    f"{cmd_line}{how_line}{note_line}\n"
                    f"{act}"
                    + ("" if authorized else
                       "用户拒绝 → 在卡片加 \"install_consent\": \"declined\" 重跑，"
                       "以自身能力作答并标注「数据未取数」。")
                    + tail)
        tail = f"\nIf params are still needed after install:\n{miss_txt}" if missing else ""
        cmd_line = f"- Install command: `{cmd}`\n" if cmd else ""
        how_line = f"- How to fetch: {hint}\n" if hint else ""
        note_line = f"- ⚠️ {note}\n" if note else ""
        if authorized:
            act = ("The user has **explicitly authorised** the install (install_consent=approved) "
                   "→ run the install command above; on success re-run with the original card so "
                   "code executes the skill and stitches.")
        else:
            act = ("🔴 **Suggest only — do not execute**: tell the user what the skill does and "
                   "hand them the install command verbatim (**they may run it themselves**), noting "
                   "that installing writes into the local skills directory and may trigger a local "
                   "security prompt. **Do not run it on their behalf before explicit authorisation**; "
                   "if they authorise it, re-run with \"install_consent\": \"approved\" added to the card.")
        return (f"{coze_answer}\n\n---\n\n{INSTALL_MARKER}\n"
                f"The Tier-A skill \"{tool}\" is needed for the supplementary data but is not "
                f"installed (**{'installation authorised by the user' if authorized else 'installation suggested'}**).\n"
                f"- Purpose: {purpose}\n"
                f"- SkillHub name: `{sid}`\n"
                f"{cmd_line}{how_line}{note_line}\n"
                f"{act}"
                + ("" if authorized else
                   " Decline → re-run with \"install_consent\": \"declined\" added; the answer is "
                   "then produced from own capability and marked \"data not retrieved\".")
                + tail)
    if status == "unreleased_b":
        # 2026-09-10 A/B 档门控；2026-11-09 口径：仅当技能**本机未注册**时走这里，
        # 直接说明「本机未注册 / 不经公共市场分发」+ 用自身能力作答。已注册技能走 handoff。
        # 英文路径自带英文文案（payload 的 message / purpose_note 恒为中文，直接复用会让
        # 英文答案夹中文——2026-09-10 修）。
        rp = tool_out.get("result") or {}
        rp = rp if isinstance(rp, dict) else {}
        tier = rp.get("tier") or "B"
        registered = rp.get("registered", True)
        purpose = rp.get("purpose") or ""
        if lang == "zh-CN":
            msg = rp.get("message") or f"{tool} 属 B 档技能（输入涉密），当前本机未注册、客户端无法直接调用。"
            note = rp.get("purpose_note") or ""
            return (f"{coze_answer}\n\n---\n\n## 需调用的 B 档技能：{tool}（本机未注册）\n\n"
                    f"{msg}\n\n{note}\n\n"
                    f"以上回答基于 ct-advisor 自身能力与方法学框架给出；该技能的深度分析未实际执行，"
                    f"涉及需用真实方案 / 数据运行才能得出的结论请以本地技能结果为准。")
        if registered:
            msg = (f'The Tier-B skill "{tool}" (confidential input: subject data / protocol / CRF) '
                   f'is not distributed through public marketplaces and is **not registered '
                   f'locally**, so the client cannot invoke it directly.')
        else:
            msg = (f'"{tool}" is not in ct-advisor\'s skill registry and is treated as Tier B by '
                   f'default — it is not registered locally and cannot be invoked here.')
        note = (f"The skill's capability (e.g. in-depth protocol review / statistical review / data QC) "
                f"must run in its own local environment against real data; ct-advisor does not "
                f"impersonate it.")
        p = f"- Purpose: {purpose}\n" if purpose else ""
        return (f"{coze_answer}\n\n---\n\n## Tier-B skill required: {tool} (not registered locally)\n\n"
                f"{msg}\n{p}\n{note}\n\n"
                f"The answer above is based on ct-advisor's own capability and methodology framework; "
                f"the skill's in-depth analysis was not actually executed. For conclusions that require "
                f"running against real protocols / data, rely on the local skill's output.")
    if status == "unpublished_a":
        # 2026-09-10 A/B 档门控：A 档（输入非涉密）但尚未发布 → 当前不可安装。
        # 与 install_required 分开：不给安装地址（未上架 / 空仓库装完仍不可用）、不征询同意；
        # 与 local_fallback 分开：不是用户拒绝，而是上游尚未公开。
        # 只渲染面向用户的字段（message / purpose / next_step）；result.hint 是给 agent 的
        # 处置指引，**不得混进用户可见正文**（2026-09-10 修）。
        # 英文路径自带英文文案（payload 里的 message 由代码生成、恒为中文，直接复用会让
        # 英文答案夹中文——2026-09-10 修，unreleased_b 同此处理）。
        rp = tool_out.get("result") or {}
        rp = rp if isinstance(rp, dict) else {}
        purpose = rp.get("purpose") or ""
        if lang == "zh-CN":
            msg = rp.get("message") or f"{tool} 属 A 档技能，未在 SkillHub 上架且当前本机未注册。"
            nxt = rp.get("next_step") or (
                "可先分别调用已上架的兄弟技能（ct-registry / ct-safety / ct-literature）取数，"
                "再由 ct-advisor 就地缝合；待该技能正式发布后再由它统一编排。")
            p = f"- 该技能用途：{purpose}\n" if purpose else ""
            return (f"{coze_answer}\n\n---\n\n## 需调用的 A 档技能：{tool}（本机未注册）\n\n"
                    f"{msg}\n{p}"
                    f"以上回答基于 ct-advisor 自身能力与方法学框架给出；该技能未实际执行，"
                    f"凡需其取数或运行才能确认的内容（试验登记号、安全信号数值、文献条目、"
                    f"竞品情报评分等）均未经核验，请勿直接引用为事实。\n{nxt}")
        msg = (f'The Tier-A skill "{tool}" (non-confidential input) is not listed on SkillHub '
               f'and is **not registered locally**, so the client cannot invoke it now.')
        nxt = rp.get("next_step_en") or (
            f"If the skill is available in your client, invoke @{tool} directly; otherwise "
            "call ct-registry / ct-safety / ct-literature separately and have ct-advisor "
            "stitch the results.")
        p = f"- Purpose: {purpose}\n" if purpose else ""
        return (f"{coze_answer}\n\n---\n\n## Tier-A skill required: {tool} (not registered locally)\n\n"
                f"{msg}\n{p}"
                f"The answer above is based on ct-advisor's own capability and methodology framework; "
                f"the skill was not executed, so anything requiring its data or runtime (registry IDs, "
                f"safety-signal values, literature records, competitive-intel scores) is unverified — "
                f"do not cite it as fact.\n{nxt}")
    if status == "local_fallback":
        # 2026-09-10 A/B 档门控：用户拒绝安装 → 自身能力作答，明确标注未取数（反幻觉红线）。
        rp = tool_out.get("result") or {}
        rp = rp if isinstance(rp, dict) else {}
        msg = rp.get("message") or f"未调用 {tool} 取数。"
        hint = rp.get("hint") or ""
        if lang == "zh-CN":
            return (f"{coze_answer}\n\n---\n\n## 数据未取数说明\n\n"
                    f"{msg}\n\n{hint}\n\n"
                    f"⚠️ 本回答未调用 {tool} 实际取数：试验登记号、安全信号数值、文献条目等"
                    f"需检索才能确认的内容均未经核验，请勿直接引用为事实。")
        return (f"{coze_answer}\n\n---\n\n## Data not retrieved\n\n"
                f"{msg}\n\n{hint}\n\n"
                f"⚠️ {tool} was not called, so nothing was retrieved: identifiers, safety-signal "
                f"values, literature records and similar items are unverified — do not cite them as fact.")
    err = tool_out.get("result") or ""
    if lang == "zh-CN":
        return (f"{coze_answer}\n\n---\n\n## 补充信息获取失败（来源：{tool}）\n\n"
                f"Coze 建议调用的本地技能执行出错，已保留 Coze 原答案：\n{err}")
    return (f"{coze_answer}\n\n---\n\n## Supplementary data retrieval failed (Source: {tool})\n\n"
            f"The local skill Coze requested failed; Coze's original answer is kept:\n{err}")


def _run_handle_need_tool(card: dict) -> dict:
    """在代码内机械执行 need_tool 执行卡（subprocess 调 handle_need_tool.py）。"""
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "handle_need_tool.py"),
             "--card", json.dumps(card, ensure_ascii=False)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300, **_hidden_kwargs()
        )
        if proc.returncode != 0:
            return {"tool": card.get("need_tool"), "status": "error",
                    "result": f"rc={proc.returncode}: {(proc.stderr or '')[:1500]}"}
        return json.loads(proc.stdout)
    except subprocess.TimeoutExpired:
        return {"tool": card.get("need_tool"), "status": "error",
                "result": "技能执行超时（>300s）"}
    except Exception as e:  # noqa: BLE001
        return {"tool": card.get("need_tool"), "status": "error",
                "result": f"{type(e).__name__}: {e}"}


def _ensure_deferred(tool_out: dict, card: dict) -> dict:
    """card-inline / ship 路径的混合调用兜底（2026-11-09，纯代码）。

    执行卡若在传递中丢了 need_tools，handoff 就只剩主技能一张卡片。
    复用 handle_need_tool.ensure_deferred 现场补齐；任何异常都原样返回，
    绝不因兜底失败影响主答案。
    """
    try:
        from handle_need_tool import ensure_deferred
        return ensure_deferred(tool_out, card)
    except Exception:  # noqa: BLE001
        return tool_out


def _emit_plain(text: str) -> None:
    """把最终答案以**明文**写 stdout（2026-10-22 v1.3.20：内部无编码包裹）。

    历史：v1.3.9 起本函数输出 base64 ASCII-safe 信封（`ANSWER_B64_*`）以抗
    cp936 乱码；该防护已上移到 `entry._emit_plain`（UTF-8 字节写 + 答案文件），
    本函数只把正文交给调用方（`entry._run_card_inline` 直接读 stdout）。
    标记与 checksum 不在本层产生——唯一产生点是 entry 出口。
    """
    sys.stdout.write((text or "").replace("\r\n", "\n"))


def _extract_draft(raw: str) -> str:
    """Best-effort extract draft_answer from raw input, for fallback on parse failure."""
    try:
        return json.loads(raw).get("draft_answer", "") or ""
    except Exception:
        m = re.search(r'"draft_answer"\s*:\s*"((?:[^"\\]|\\.)*)"', raw, re.S)
        return m.group(1) if m else ""


def _record_latency(mode: str, round_id: str, threshold: int) -> None:
    """F 可观测化（2026-08-23）：纯本地统计每轮工具往返数。

    每次 refine_answer.py 调用即一次 tool round-trip；按 --round-id 分组递增计数，
    超过 --latency-threshold 时 stderr 输出 [WARN]，提示可能 pre-fire 延迟复发
    （对应 #1 实测延迟失效模式）。计数器落 <ROOT>/.runtime/latency_<round_id>.json
    （gitignored 运行态副产物，纯本地、无外部依赖）。度量失败绝不影响主流程。
    """
    try:
        runtime_dir = ROOT / ".runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        cf = runtime_dir / f"latency_{round_id}.json"
        try:
            data = json.loads(cf.read_text(encoding="utf-8"))
        except Exception:
            data = {"count": 0}
        data["count"] = int(data.get("count", 0)) + 1
        cf.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        trips = data["count"]
        sys.stderr.write(f"[ct-advisor][latency] round={round_id} mode={mode} trips={trips}\n")
        if trips > threshold:
            sys.stderr.write(
                f"[ct-advisor][latency][WARN] round={round_id} trips={trips} exceeds guard "
                f"threshold {threshold} — possible pre-fire delay regression (check Step 0/1 ordering)\n"
            )
    except Exception as _e:  # noqa: BLE001  # 度量失败绝不影响主流程
        sys.stderr.write(f"[ct-advisor][latency] record skipped: {_e}\n")


# ── 2026-10-25 本地域码守卫（反 SDTM 域幻觉，如编造 'IM' 影像发现域）────
# 设计原则：① 仅作**输出前校验**，不作答、不引入知识（符合 Coze-only 架构）；
# ② 上下文感知——仅当两字母码被显式框定为 SDTM 域时才校验，绝不误伤普通缩写
#    （如 (PI) 研究者、(QC) 质控、IN/ON/US 等）；③ 防御式——任何异常都跳过、不阻断主流程；
# ④ allowlist 缺失时**禁用**守卫（宁可漏检也不对真实标准域误报）。
# 命中非标准域码时在答案末尾追加本地校验警告（不修改 Coze 原答案语义）。
_SDTM_ALLOW_CACHE: dict = {}

# 上下文感知：仅当码被显式框定为 SDTM 域时才校验（避免误伤普通缩写）。
_SDTM_DOMAIN_PATTERNS = [
    re.compile(r"\b([A-Z]{2})\s*(?:标准)?域\b"),                            # X域 / X标准域
    re.compile(r"(?:SDTM|SDTMIG)\s*[:：]?\s*([A-Z]{2})\s*(?:域|[（(])"),     # SDTM X域 / SDTM X（
    re.compile(r"(?:归入|放入|应归入|派入|分流到|分流至|落到|落入|置于|记录于|存放于|建议放入|默认归入)\W{0,6}([A-Z]{2})\s*(?:(?:标准)?域|[（(])"),  # 动词 X域/( / X标准域
    re.compile(r"[（(][^）)]{0,40}?\b([A-Z]{2})\b[^）)]{0,40}?(?:影像|imaging|Imaging|Findings|发现)[）)]"),  # (…X…影像/发现)
    re.compile(r"(?:影像|发现)\W{0,6}[（(]\s*([A-Z]{2})\b"),               # 影像/发现（X
    re.compile(r"\bdomain\s+([A-Z]{2})\b"),                                # domain X
]


def _load_sdtm_allowlist() -> dict:
    """载入 SDTMIG v3.4 标准域 allowlist（scripts/sdtm_domain_allowlist.json）。

    失败则禁用守卫（返回空 dict）——绝不对真实标准域误报。
    """
    global _SDTM_ALLOW_CACHE
    if _SDTM_ALLOW_CACHE:
        return _SDTM_ALLOW_CACHE
    p = ROOT / "scripts" / "sdtm_domain_allowlist.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as _e:  # noqa: BLE001
        sys.stderr.write(f"[ct-advisor] sdtm_domain_allowlist load failed: {_e} (guard disabled)\n")
        data = {}
    _SDTM_ALLOW_CACHE = data
    return data


def _scan_sdtm_domain_codes(text: str, valid: Set[str]) -> list:
    """返回答案中被框定为 SDTM 域、但不在标准 allowlist 中的两字母码列表。"""
    found: list = []
    for pat in _SDTM_DOMAIN_PATTERNS:
        for m in pat.finditer(text):
            code = m.group(1)
            if code in valid:
                continue
            if code not in found:
                found.append(code)
    return found


def _validate_sdtm_domains(answer: str, lang: str = "zh-CN") -> str:
    """输出前 SDTM 域码守卫：通用负向闸门，拦截一切不在 SDTMIG v3.4 标准域目录中的域码断言。

    本质不是「拦截某个特定码」，而是「凡被框定为 SDTM 域、却不在标准域目录里的两字母码一律拦截」。
    IM 等仅作为已知高频幻觉的加料纠错示例（见 curated_hallucinations），allowlist 才是判定依据。
    命中时在答案末尾追加本地校验警告；任何异常均原样返回、不阻断主流程。
    """
    if not answer or not answer.strip():
        return answer
    try:
        allow = _load_sdtm_allowlist()
        if not allow:
            return answer  # allowlist 缺失 → 禁用守卫
        valid = set(allow.get("domains", {})) | set(allow.get("non_standard_codes", []))
        if not valid:
            return answer
        found = _scan_sdtm_domain_codes(answer, valid)
        # curated_hallucinations 兜底强匹配：对已知高频幻觉码（如 IM），即便未触发上述强模式、
        # 只要出现在影像/域语境也拦。这是 allowlist 之外的加料纠错，绝不改变「非标准码即拦」的主体逻辑。
        for code, _note in (allow.get("curated_hallucinations") or {}).items():
            mm = re.search(r"\b" + re.escape(code) + r"\b", answer)
            if not mm:
                continue
            ctx = answer[max(0, mm.start() - 20): mm.end() + 20]
            if re.search(r"影像|imaging|Imaging|Findings|发现|SDTM|域|domain", ctx):
                if code not in found:
                    found.append(code)
        if not found:
            return answer
        known = allow.get("curated_hallucinations") or {}
        reasons = []
        for code in found:
            if code in known:
                reasons.append(f"{code}：{known[code]}")
            elif lang == "zh-CN":
                reasons.append(
                    f"{code} 不在 SDTMIG v3.4 标准域清单；若为申办方自定义（sponsor）域，"
                    f"请按项目 SDTM 映射规范（SDTM spec）核实，勿当作 CDISC 标准域引用。")
            else:
                reasons.append(
                    f"{code} is not in the SDTMIG v3.4 standard domain list; if it is a "
                    f"sponsor-defined custom domain, verify against the project SDTM specification "
                    f"and do not cite it as a CDISC standard domain.")
        if lang == "zh-CN":
            block = (
                "\n\n> ⚠️ **本地域码自动校验（ct-advisor）**：答案中出现的 SDTM 域代码 "
                + "、".join(f"`{c}`" for c in found)
                + " 不在 SDTMIG v3.4 标准域目录中。\n>\n"
                + "\n".join(f"> - {r}" for r in reasons)
                + "\n>\n> 请以 CDISC SDTMIG v3.4 官方域目录及项目 SDTM spec 为准。"
            )
        else:
            block = (
                "\n\n> ⚠️ **Local SDTM domain-code check (ct-advisor)**: the following SDTM "
                "domain code(s) in the answer are NOT in the SDTMIG v3.4 standard domain "
                "directory: " + ", ".join(f"`{c}`" for c in found) + ".\n>\n"
                + "\n".join(f"> - {r}" for r in reasons)
                + "\n>\n> Refer to the official CDISC SDTMIG v3.4 domain list and the project SDTM spec."
            )
        sys.stderr.write(f"[ct-advisor] sdtm domain guard flagged: {found}\n")
        return answer + block
    except Exception as _e:  # noqa: BLE001  # 守卫失败绝不影响主流程
        sys.stderr.write(f"[ct-advisor] sdtm domain guard skipped: {_e}\n")
        return answer


def main() -> None:
    ap = argparse.ArgumentParser(description="ct-advisor answer refiner (Coze polish, single call)")
    ap.add_argument("payload", nargs="?", help="path to JSON file with the 3 variables (deprecated: use stdin or --payload-inline)")
    ap.add_argument("--payload-inline", help="inline JSON payload string (highest priority, avoids temp files)")
    ap.add_argument("--config", default=str(ROOT / "config.json"),
                     help="path to config.json (defaults to the skill package config.json, "
                          "independent of the current working directory)")
    ap.add_argument("--fire-only", action="store_true",
                    help="race early-fire mode: step 2 background call, sends only original_question, "
                         "returns Coze result or empty string (no draft fallback on Coze failure), writes race cache on success")
    ap.add_argument("--collect", action="store_true",
                    help="race collect mode: step 3 call, reads the race cache written by --fire-only; "
                         "hit returns Coze result (Coze wins, local interrupted), miss returns empty (local wins)")
    ap.add_argument("--wait", type=float, default=None,
                    help="--collect gather wait cap in seconds; defaults to config refiner.race_window")
    ap.add_argument("--forward", action="store_true",
                    help="全量直发主链路（2026-08-14）：单次调用 Coze，返回结构化 RefineResult JSON。"
                         "本地大模型原则上不回答——本模式只转发；need_tool 分支透出执行卡供本地执行技能。"
                         "失败/超时回退 draft_answer（final_answer 字段），由调用方判定本地兜底")
    ap.add_argument("--ship", action="store_true",
                    help="代码旁路主链路（2026-08-15）：单次调用 Coze，若 need_tool 则在代码内直接调 "
                         "handle_need_tool.py 执行并对结果做确定性缝合；最终答案以**明文**输出"
                         "（v1.3.20：标记/checksum 由 entry.py 出口统一添加）。本地大模型只做原样透传"
                         "（pipe），不重写/重排/补充。此模式用于跳过大模型重组。")
    ap.add_argument("--card-inline", default=None,
                    help="need_params 重试路径（与 --ship 配合）：跳过 Coze 直发，直接用给定执行卡 JSON 运行 "
                         "handle_need_tool.py 并缝合（用于补齐参数后重试，避免重复调用 Coze）")
    # P0-B 语气写作：注入 tone_matcher.py 生成的 tone_profile.json（仅风格、无事实）
    ap.add_argument("--tone", default=None,
                    help="path to tone_profile.json (from scripts/tone_matcher.py); injects style-only tone into Coze prompt")
    # P1-D 本地用户记忆：注入 memory_manager.py 维护的 ct-advisor-memory.json 上下文
    ap.add_argument("--memory", default=None,
                    help="path to ct-advisor-memory.json (from scripts/memory_manager.py); injects local user memory context")
    # F 可观测化（2026-08-23）：可选延迟护栏度量——统计每轮工具往返数，纯本地、无外部依赖。
    # 仅在显式传 --latency-report 时启用；计数器落 <ROOT>/.runtime/（gitignored，运行态副产物）。
    ap.add_argument("--latency-report", action="store_true",
                    help="F observability: emit a per-invocation latency event to stderr and tally "
                         "tool round-trips per --round-id (default round key 'default'); pure-local, no network")
    ap.add_argument("--round-id", default="default",
                    help="latency-report grouping key: pass a stable id per question so trips are counted per round "
                         "(e.g. a question hash); omit to accumulate under the 'default' key")
    ap.add_argument("--latency-threshold", type=int, default=10,
                    help="latency-report guard threshold: when a round's trip count exceeds this, emit a [WARN] "
                         "line signalling possible pre-fire delay regression (default 10)")
    ap.add_argument("--latency-reset", action="store_true",
                    help="latency-report helper: clear the .runtime latency counter for --round-id and exit")
    args = ap.parse_args()

    # F 可观测化（2026-08-23）：延迟护栏度量。必须在所有分派前执行，以覆盖每种调用模式。
    # 纯本地、无外部依赖：计数器落 <ROOT>/.runtime/latency_<round_id>.json（gitignored 运行态副产物）。
    if args.latency_reset:
        try:
            cf = ROOT / ".runtime" / f"latency_{args.round_id}.json"
            if cf.exists():
                cf.unlink()
            sys.stderr.write(f"[ct-advisor][latency] reset round={args.round_id}\n")
        except Exception as _e:  # noqa: BLE001
            sys.stderr.write(f"[ct-advisor][latency] reset failed: {_e}\n")
        sys.exit(0)
    if args.latency_report:
        _mode = "serial"
        if args.fire_only:
            _mode = "fire-only"
        elif args.collect:
            _mode = "collect"
        elif args.ship:
            _mode = "ship"
        elif args.forward:
            _mode = "forward"
        _record_latency(_mode, args.round_id, args.latency_threshold)

    # --card-inline 重试路径（与 --ship 配合）：跳过 Coze 直发，直接用执行卡在代码内跑 handle_need_tool 并缝合。
    # 必须在读 payload 之前处理，避免空 stdin 触发 payload 解析回退。
    if args.card_inline:
        try:
            card = json.loads(args.card_inline)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[ct-advisor] card-inline JSON 解析失败: {e}\n")
            sys.exit(1)
        coze_answer = card.get("draft_answer") or ""
        tool_out = _ensure_deferred(_run_handle_need_tool(card), card)
        _q = card.get("original_question") or ""
        _lang = _detect_lang(_q)
        # 2026-11-10 修复：调用之前预警 + 与结果一并返回最前（幂等，双来源互补）
        _q_prefix = _pre_call_complexity(_q, _lang)
        _emit_plain(_with_q_prefix(
            _prepend_complexity(
                _merge_answer(coze_answer, tool_out, lang=_lang), tool_out, _lang),
            _q_prefix))
        sys.exit(0)

    # Read priority (in-memory pipeline first, zero temp files):
    #   1) --payload-inline: pass the JSON string directly, zero file I/O
    #   2) stdin pipe: `echo '{...}' | python refine_answer.py`
    #   3) file path (positional, legacy, avoid when possible)
    if args.payload_inline:
        raw = args.payload_inline
    elif args.payload:
        p = Path(args.payload)
        if not p.exists():
            # Explicit path given but missing: fail loudly, do NOT silently fall back to stdin
            # (otherwise it would hang or misread an empty payload)
            sys.stderr.write(f"[ct-advisor] payload file not found: {args.payload} / payload 文件未找到: {args.payload}\n")
            sys.exit(2)
        raw = p.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    draft = _extract_draft(raw)
    try:
        obj = json.loads(raw)
        req = RefineRequest(
            query_meta=obj.get("query_meta", ""),
            original_question=str(obj.get("original_question", "")),
            draft_answer=str(obj.get("draft_answer", "")),
        )
        # P0-B 语气写作 / P1-D 本地记忆：注入 tone_profile / memory_context（CLI 优先，其次 payload 内联）。
        # 两者均为纯本地生成的风格/上下文，仅随契约外发给 Coze，符合风格硬闸与记忆 TTL 设计。
        if args.tone:
            try:
                tp = json.loads(Path(args.tone).read_text(encoding="utf-8"))
                if isinstance(tp, dict):
                    req.tone_profile = tp
                    sys.stderr.write(f"[ct-advisor] tone profile injected: {args.tone}\n")
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"[ct-advisor] tone profile load failed: {e}\n")
        elif isinstance(obj.get("tone_profile"), dict):
            req.tone_profile = obj["tone_profile"]
        if args.memory:
            try:
                mc = json.loads(Path(args.memory).read_text(encoding="utf-8"))
                if isinstance(mc, dict):
                    req.memory_context = mc
                    sys.stderr.write(f"[ct-advisor] memory context injected: {args.memory}\n")
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"[ct-advisor] memory context load failed: {e}\n")
        elif isinstance(obj.get("memory_context"), dict):
            req.memory_context = obj["memory_context"]
        # query_origin is auto-stamped into query_meta by normalize(); no top-level field.
        # 类型 B 跨轮连续性（2026-08-25 硬弃用本地 is_followup 正则 + 字符串缝合）：
        # 非 --collect 模式（真实转发路径）下，永远把有界历史经 conversation_history 外发给 Coze，
        # 由远端 LLM 判"是否追问 / 继承哪些前情"。本地不再用正则猜追问、不再做字符串前缀缝合
        # （stitch 属脆弱分类器，会漏判长句式设计演进）。唯一本地职责：结构闸门（is_ctx_valid）
        # + 24h 硬上限 + 有界裁剪（pack_history_for_coze 内部 prune_history）。
        if not args.collect:
            try:
                sys.path.insert(0, str(ROOT / "scripts"))
                import context_stitch as _cs
                _orig = req.original_question or ""
                _raw_orig = _orig  # 保留原始问题（供缓存，防多轮嵌套）
                _cache = _cs.load_cache()
                if _cs.is_ctx_valid(_cache):
                    _hist = _cs.pack_history_for_coze(_cache)
                    if _hist:
                        req.conversation_history = _hist
                        # is_followup 现由"有无历史"确定性派生（非正则猜），
                        # 供远端 refiner 走 long_timeout（300s）避免多轮上下文追问被截断。
                        req.is_followup = True
                        sys.stderr.write(
                            f"[ct-advisor] conversation_history packed: {len(_hist)} rounds\n")
            except Exception as _e:  # noqa: BLE001  # 打包失败不影响主流程
                sys.stderr.write(f"[ct-advisor] history pack skipped: {_e}\n")
    except Exception as e:
        # JSON parse failed: distinguish --collect mode (cache lookup) from other modes
        if args.collect:
            # --collect mode: payload parse failure means the cache path cannot be located;
            # tell the agent explicitly "local wins", do NOT confuse it with "cache miss"
            sys.stderr.write(
                t("error.payload_invalid",
                  error=f"{type(e).__name__}; collect: cache path cannot be located -> LOCAL WINS, do NOT wait for Coze")
                + "\n"
            )
            sys.stdout.write("")
            sys.exit(0)
        # Other modes (fire-only / serial): cannot self-heal; warn clearly + fall back to draft
        sys.stderr.write(
            t("error.payload_invalid", error=f"{type(e).__name__} (invalid JSON)") + "\n"
        )
        sys.stdout.write(draft)
        sys.exit(0)

    # Contract self-heal: fill missing/invalid fields, eliminating the "invalid payload -> silent fallback" root cause
    heal_notes = req.normalize()
    if heal_notes:
        sys.stderr.write(
            t("error.payload_healed", notes="; ".join(heal_notes)) + "\n"
        )

    try:
        req.validate()  # Should pass after self-heal; only fails in extreme cases (both orgq and draft empty)
    except ValueError as e:
        sys.stderr.write(
            t("error.payload_invalid", error=f"contract validation failed: {e}") + "\n"
        )
        # Fallback: when the draft is also empty, emit an explicit prompt instead of a silent empty answer
        if not draft or not draft.strip():
            sys.stdout.write(t("error.empty_question") + "\n")
        else:
            sys.stdout.write(draft)
            sys.exit(0)

    # ── 2026-11-10 修复：复杂混合调用安全提示 ──────────────────────────────
    # 在**任何出站 / 技能调用之前**由本地零联网预判发出（stderr 实时预警），并返回
    # 可前置到答案的前缀。各明文输出分支用 _with_q_prefix 幂等前置，覆盖扣子端
    # 成功慢回 / 超时回落 / 未授权 / 缓存短路 —— 不再依赖 _merge_answer 是否执行，
    # 也不依赖扣子端是否回传 complexity_hint 字段。结构化 JSON 与竞速（fire-only /
    # collect）路径不注入正文以保持协议，但预警已在调用前发出。
    _q_prefix = _pre_call_complexity(req.original_question,
                                     _detect_lang(req.original_question))

    # ── 2026-09-23 改进（诊断报告落地）：转发前本地守卫 ──
    # 范围路由 / 大文档压缩 / 同 origin 去重；fire_only·collect 路径 no-op（遵守 race 硬闸门）。
    # 防御式：任何守卫异常都跳过，绝不阻断主流程（与 context_stitch 同策略）。
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import forward_guards as _fg
        _mode = ("fire_only" if args.fire_only else "collect" if args.collect
                 else "ship" if args.ship else "forward" if args.forward else "serial")
        _go = _fg.apply_guards(req, _mode)
        if _go.notes:
            sys.stderr.write("[ct-advisor] forward_guards: " + "; ".join(_go.notes) + "\n")
        if _go.short_circuit:
            # 缓存重放同样走明文出口（2026-10-22）：内部全程明文，标记与 checksum
            # 由 entry 出口统一产生；来源提示走 stderr，不污染 stdout。
            sys.stderr.write(
                "[ct-advisor] dedup short-circuit: replayed local cached answer "
                "(no new Coze call sent)\n"
            )
            _emit_plain(_with_q_prefix(_go.answer, _q_prefix))
            sys.exit(0)
    except Exception as _ge:  # noqa: BLE001
        sys.stderr.write(f"[ct-advisor] forward_guards skipped: {_ge}\n")

    if args.ship:
        # 代码旁路主链路（2026-08-15）：单次调用 Coze；need_tool 分支在代码内执行 + 确定性缝合；
        # 最终答案以**明文**输出（v1.3.20），本地大模型原样透传（pipe），不重写。
        if not _check_outbound_authorization(
            _get_endpoint_from_config(args.config), args.config
        ):
            # 未授权出站：无法获取 Coze 答案，明确告知 agent 走本地兜底
            _emit_plain(_with_q_prefix(
                "⚠️ 未授权出站到 Coze，无法获取精校答案。请确认允许后重试。"
                "「答案未经过 Coze 精校，请谨慎使用」。", _q_prefix))
            sys.exit(0)
        try:
            result = build_refiner(config_path=args.config).refine_forward(req)
        except MissingDependencyError:
            sys.stderr.write(
                t("error.dependency_fatal",
                  cmd='python -m pip install "requests==2.32.3"') + "\n"
            )
            sys.exit(1)
        except Exception as e:  # noqa: BLE001
            # Coze 失败：无精校答案，交给本地兜底，包裹明确警告
            sys.stderr.write(
                f"[ct-advisor] ship 失败（{type(e).__name__}）：Coze 不可用，需本地兜底\n"
            )
            # 2026-11-10 修复：即便扣子端卡死/不可用，复杂混合调用提示仍须随
            # 回落文案一并返回（本地预判独立保证，不依赖扣子端返回该字段）。
            _emit_plain(_with_q_prefix(
                "⚠️ 无法连接 Coze 服务，答案未经过精校。请稍后重试。", _q_prefix))
            sys.exit(0)
        coze_answer = result.final_answer or ""
        need_tool = result.need_tool
        if need_tool:
            # P1 修复（2026-08-15）：Coze 仅判工具类别、不抽真实入参（只给 max/top 等默认值）。
            # 用本地 route_tool 预判补全真实参数（cond/drug/topic/test/p1/p2），覆盖 Coze 默认值，
            # 使「代码跳过大模型」在 need_tool 场景也成立——避免任意 need_tool 都 100% 弹参数追问。
            params = dict(result.params or {})
            pred = _predict_tool(req.original_question)
            if pred.get("need_tool") == need_tool:
                for k, v in (pred.get("params") or {}).items():
                    if v not in (None, ""):
                        params.setdefault(k, v)
            # 2026-11-09：ship 路径也要带上混合技能列表（Coze 侧 + 本地预判），
            # 否则「代码跳过大模型」的直缝路径同样只剩单一技能卡片。
            mixed_tools = list(dict.fromkeys(
                list(getattr(result, "need_tools", None) or [])
                + list(pred.get("need_tools") or [])
                + ([need_tool] if need_tool else [])))
            card = {
                "need_tool": need_tool,
                "need_tools": mixed_tools,
                "params": params,
                "draft_answer": coze_answer,
                "original_question": req.original_question,
            }
            tool_out = _ensure_deferred(_run_handle_need_tool(card), card)
            # 2026-08-21：缝合文案/标签随提问语言（结构化单元格数据保持原文）
            _lang = _detect_lang(req.original_question)
            # 2026-11-10 修复：复杂混合调用提示前置到答案最前（与结果一并返回，
            # 覆盖扣子端成功慢回 / 超时回落；本地预判即能独立保证，不依赖扣子端返回）。
            merged = _prepend_complexity(
                _merge_answer(coze_answer, tool_out, lang=_lang), tool_out, _lang)
        else:
            merged = coze_answer
        if not merged.strip():
            merged = "⚠️ Coze 返回为空，请稍后重试。"
        # 更新会话上下文（供下一轮类型 B 追问拼接）：累积多轮历史（q + 结论摘要）。
        # 保留规则（2026-08-24 修订，OR + 24h 硬上限）：在 2h 内 OR 总数 ≤10 任一即留，
        # 再 AND 未超 24h（任何超 24h 记录必丢，防孤立旧记录污染）。裁剪统一由
        # context_stitch.prune_history 负责，此处不再内联，避免规则分散。
        # 2026-08-24：① 新增 answer_summary（Coze 结论首段），使下一轮 stitch 能携带已定设计实体；
        # ② 改为累积式 history（不再 rounds=0 覆盖），2h 内连续调用可跨轮关联同一试验设计；
        # ③ rounds 自增（仅作兜底上限），不再每轮归零。
        try:
            sys.path.insert(0, str(ROOT / "scripts"))
            import context_stitch as _cs2
            _cache_src = locals().get("_raw_orig") or (req.original_question or "")
            _prev_cache = _cs2.load_cache()
            # 顶层缓存失效（is_ctx_valid=False：超 24h 或 超 2h 且超 10 轮）则丢弃旧 history，开启新会话
            _history = _prev_cache.get("history", []) if _cs2.is_ctx_valid(_prev_cache) else []
            _entry = {
                "ts": _cs2.time.time(),
                "q": _cache_src,
                "summary": _cs2.extract_summary(_cache_src, coze_answer),
                "answer_summary": _cs2.extract_summary(_cache_src, coze_answer),
            }
            _history.append(_entry)
            # 统一裁剪（OR + 24h 硬上限）
            _history = _cs2.prune_history(_history)
            _cs2.save_cache({
                "rounds": int(_prev_cache.get("rounds", 0)) + 1,
                "history": _history,
                "q": _cache_src,
                "summary": _entry["summary"],
                "answer_summary": _entry["answer_summary"],
            })
        except Exception:  # noqa: BLE001  # 缓存写入失败不影响主流程
            pass
        # §20.15：Coze 顶层 message 字段 → 置顶 banner（用户提示词可关闭；仅抑显示，意图不回传 coze）
        if getattr(result, "message", None) and not _is_message_dismissed(req.original_question):
            _banner = _format_message_banner(result.message, _detect_lang(req.original_question))
            if _banner:
                merged = f"{_banner}\n\n---\n\n{merged}"
        # 缓存来源声明（2026-09-09，彤 规范）：命中云计算缓存 → 答案最前明示，非本次实时计算
        if getattr(result, "cache_hit", False):
            _lang = _detect_lang(req.original_question)
            _decl = (
                "📦 本答案来自云计算缓存（历史运行结果，非本次实时计算）。如需最新结果，请追问要求重新生成。"
                if _lang == "zh-CN"
                else "📦 This answer is from the cloud cache (a previous run, not freshly computed for this request). Ask again for a fresh generation if needed."
            )
            merged = f"> {_decl}\n\n{merged}"
        # 2026-09-10（第十四轮，用户要求）：**先自身作答，末尾再建议**兄弟技能。
        # 未自动调用任何兄弟技能、但问题与某技能沾边（弱命中 / 咨询意图）时，
        # 在最终答案**最末**追加一行软建议；不阻断、不改写答案。
        if not need_tool:
            _st = (_predict_tool(req.original_question).get("suggest_tools") or [])
            if _st:
                merged = merged + suggest_footer(
                    _st, lang=_detect_lang(req.original_question))
        # 2026-09-23 改进：超范围前置转介 + 回写去重库（防御式）
        try:
            import forward_guards as _fg3
            _sh = getattr(req, "scope_hint", "")
            if _sh:
                merged = _fg3.apply_scope_referral(merged, _sh)
            if merged.strip():
                _fg3.record_answer(((req.query_meta or {}) or {}).get("query_origin", ""),
                                   req.original_question, merged)
        except Exception:  # noqa: BLE001
            pass
        # 2026-10-25：输出前 SDTM 域码守卫（通用负向闸门：凡不在 SDTMIG v3.4 标准域目录的域码断言即拦；IM 等仅示例）；防御式、不阻断。
        merged = _validate_sdtm_domains(merged, lang=_detect_lang(req.original_question))
        _emit_plain(_with_q_prefix(merged, _q_prefix))
        sys.exit(0)

    if args.forward:
        # 全量直发主链路（2026-08-14）：单次调用 Coze，返回结构化 RefineResult JSON。
        # 不做难度分流、不生成本地草稿（本地大模型原则上不回答）；need_tool 分支透出执行卡。
        # 失败/超时：final_answer 回退 draft（调用方判定走本地知识库兜底），并输出 FALLBACK 标记。
        if not _check_outbound_authorization(
            _get_endpoint_from_config(args.config), args.config
        ):
            # 未授权出站：输出兜底结果（final_answer=draft）+ 明确标记
            sys.stdout.write(json.dumps({
                "final_answer": draft, "need_tool": None, "cache_hit": False,
                "fallback": "auth_blocked",
            }, ensure_ascii=False))
            sys.exit(0)
        try:
            result = build_refiner(
                config_path=args.config,
            ).refine_forward(req)
        except MissingDependencyError as e:
            sys.stderr.write(
                t("error.dependency_fatal",
                  cmd='python -m pip install "requests==2.32.3"') + "\n"
            )
            sys.exit(1)
        except Exception as e:  # noqa: BLE001
            # 兜底：任何异常 → draft + FALLBACK 标记（本地知识库兜底由调用方触发）
            sys.stderr.write(
                f"[ct-advisor] forward 失败（{type(e).__name__}）：本次本地兜底；"
                f"若持续失败可运行 `python scripts/check_coze.py` 诊断代理/网络。\n"
            )
            result = RefineResult(final_answer=draft, need_tool=None)
        out = {
            "final_answer": result.final_answer,
            "cached_answer": result.cached_answer,
            "cache_hit": result.cache_hit,
            "need_tool": result.need_tool,
            "params": result.params or {},
            "run_id": result.run_id,
            "message": result.message,  # §20.15：顶层可选 message 字段，供消费端（如工作台）置顶渲染
        }
        # 失败回退标记（stderr 同时输出，供调用方提示用户）
        if result.need_tool is None and not result.cache_hit and not result.final_answer.strip():
            sys.stderr.write("[ct-advisor][FALLBACK] Coze 返回空/失败，无法生成答案\n")
        # 2026-09-23 改进：超范围前置转介 + 回写去重库（防御式）
        try:
            import forward_guards as _fg3
            _sh = getattr(req, "scope_hint", "")
            if _sh and out.get("final_answer"):
                out["final_answer"] = _fg3.apply_scope_referral(out["final_answer"], _sh)
            if out.get("final_answer", "").strip():
                _fg3.record_answer(((req.query_meta or {}) or {}).get("query_origin", ""),
                                   req.original_question, out["final_answer"])
        except Exception:  # noqa: BLE001
            pass
        # 2026-10-25：输出前 SDTM 域码守卫（反域幻觉）；final_answer 内联校验。
        if out.get("final_answer"):
            out["final_answer"] = _validate_sdtm_domains(
                out["final_answer"], lang=_detect_lang(req.original_question))
        sys.stdout.write(json.dumps(out, ensure_ascii=False))
        sys.exit(0)

    if args.fire_only:
        # Race early-fire mode (step 2 background call): draft left empty, only original_question.
        # Coze wins -> stdout is its result; fail/timeout -> empty string, agent uses the local draft as a fault fallback in step 4.
        # Outbound authorization check: if not authorized, output empty (local wins) + stderr notice.
        if not _check_outbound_authorization(
            _get_endpoint_from_config(args.config), args.config
        ):
            sys.stdout.write("")
            sys.exit(0)
        try:
            final = build_refiner(
                config_path=args.config,
            ).refine_fire_only(req)
        except MissingDependencyError as e:
            sys.stderr.write(
                t("error.dependency_fatal",
                  cmd='python -m pip install "requests==2.32.3"') + "\n"
            )
            sys.exit(1)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(
                f"[ct-advisor] race fire-only 失败（{type(e).__name__}）：本次本地兜底；"
                f"若持续失败可运行 `python scripts/check_coze.py` 诊断代理/网络。\n"
            )
            final = ""
        # 2026-08-23 F 加固：refine_fire_only() 在本环境可能返回 RefineResult 对象（而非纯字符串），
        # 统一取 .final_answer 以兼容两种返回形态，避免 (final or "").strip() 抛 AttributeError。
        if not isinstance(final, str):
            final = getattr(final, "final_answer", "") or ""
        sys.stdout.write(final or "")
        sys.exit(0)

    if args.collect:
        # Race collect mode (step 3): read the race cache written by step 2 --fire-only.
        # Hit (Coze returned first) -> return Coze result (Coze wins, local interrupted); else empty (local wins).
        # --collect does not make a network call, so no auth check needed.
        try:
            refiner = build_refiner(
                config_path=args.config,
            )
            final = refiner.collect_race(req, args.wait)
        except MissingDependencyError as e:
            sys.stderr.write(
                t("error.dependency_fatal",
                  cmd='python -m pip install "requests==2.32.3"') + "\n"
            )
            sys.exit(1)
        except Exception:  # noqa: BLE001
            final = ""
        sys.stdout.write(final or "")
        sys.exit(0)

    # Serial mode (foreground, complex/vague): outbound authorization check.
    # If not authorized, output draft directly + stderr notice.
    if not _check_outbound_authorization(
        _get_endpoint_from_config(args.config), args.config
    ):
        sys.stderr.write(t("auth.serial_blocked") + "\n")
        sys.stdout.write(_with_q_prefix(draft, _q_prefix))
        sys.exit(0)
    last_error = ""
    # 回退消息报告的实际有效超时（长任务 300s / 普通 60s）。先给默认值，避免 build_refiner 失败时未定义。
    eff_timeout = 90
    try:
        refiner = build_refiner(config_path=args.config)
        # 复用 refiner 的同一套条件化超时判定，避免消息硬编码 60s 与真实等待时长不符。
        try:
            eff_timeout = refiner.resolve_timeout(req)
        except Exception:  # noqa: BLE001  判定失败不阻断主流程，退回该 refiner 的默认超时
            eff_timeout = getattr(refiner, "timeout", 90)
        final = refiner.refine(req)
    except MissingDependencyError as e:
        # Missing dependency: fail explicitly, never silently fall back to draft (else the user thinks the answer came from Coze)
        sys.stderr.write(
            t("error.dependency_fatal",
              cmd='python -m pip install "requests==2.32.3"') + "\n"
        )
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        # Any non-dependency exception (network/timeout/Coze 5xx etc.) is labelled as fallback to avoid being mistaken for a Coze-refined answer
        last_error = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
        sys.stderr.write(
            t("error.fallback_local", reason=type(e).__name__, timeout=eff_timeout) + "\n"
        )
        final = draft
    # 2026-08-23 F 加固：refine() 在真实出域场景下可能返回 RefineResult 对象（而非纯字符串），
    # 统一取 .final_answer 以兼容两种返回形态，避免离线/无网回归时 (final or "").strip() 抛 AttributeError。
    if not isinstance(final, str):
        final = getattr(final, "final_answer", "") or ""
    # 2026-09-23 改进：超范围前置转介 + 回写去重库（防御式）
    try:
        import forward_guards as _fg3
        _sh = getattr(req, "scope_hint", "")
        if _sh:
            final = _fg3.apply_scope_referral(final, _sh)
        if (final or "").strip():
            _fg3.record_answer(((req.query_meta or {}) or {}).get("query_origin", ""),
                               req.original_question, final)
    except Exception:  # noqa: BLE001
        pass
    # 诊断兜底（2026-08-13）：Coze 失败且无本地草稿时输出友好询问（agent 应征得用户同意后
    # 自动运行 check_coze.py 诊断），而非空输出——空输出会被误判为"没有答案"。
    if not (final or "").strip():
        sys.stdout.write(_with_q_prefix(
            t("error.fallback_diagnose", error=last_error or "unknown") + "\n",
            _q_prefix))
    else:
        # 2026-10-25：输出前 SDTM 域码守卫（通用负向闸门：凡不在 SDTMIG v3.4 标准域目录的域码断言即拦；IM 等仅示例）；防御式、不阻断。
        final = _validate_sdtm_domains(final, lang=_detect_lang(req.original_question))
        sys.stdout.write(_with_q_prefix(final, _q_prefix))
    sys.exit(0)


if __name__ == "__main__":
    main()
