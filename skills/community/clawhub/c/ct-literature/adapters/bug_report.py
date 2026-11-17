#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bug_report.py — ct- 系列「技能错误报告」共享适配器模板 (ct-base §20.3)

功能（供各 ct- 叶子技能复制到自身 adapters/ 目录后使用，§16.9 出站目录）：
  1. detect_error_signal(): 会话内错误信号判定（工具化；触发规则仍以 SKILL.md agent 规则为准）
  2. build_report(): 组装「脱敏」错误报告（固定白名单信封；description 为自由文本问题描述）
  3. render_report_text(): 渲染为可读文本，供用户两阶段确认（①展示并提议 → ②确认发送）
  4. confirm_prompt(): 双语一次性提议文案（i18n 提示，中英）
  5. send_to_endpoint(): POST 到「统一 bug-report coze 端点」（仅 action=report）；返回含 history（同 query_origin 上一条历史记录 JSON 或 ""）
  6. confirm_thanks() / build_followup() / parse_history(): 发送成功后「历史回执」文案生成（§20.3 历史回执：2.1 感谢 + 2.2 已修复通知 / 2.3 未修复通知）
  7. save_local_report(): 本地兜底（无 coze 调用时生成 md + 作者邮箱，数据不出域）

【职责边界】本文件是「报告客户端」，只负责上报：
  - 唯一动作 = report（写一条脱敏报告到统一端点）。
  - get / update / download / delete 属「治理动作」，由 ct-update 技能（作者侧）专用，
    本文件与叶子技能一律不实现、不调用（§20.3.5 治理归属）。

设计约束：
  - 报告信封为「硬白名单」：只允许 REPORT_SCHEMA 字段，build 时自动剔除一切额外键
    ——未列入信封的用户数据键（原始数据表、受试者记录等）一律不进报告（§20.3.2 脱敏铁律）。
  - description 是唯一自由文本字段，用于帮助作者定位问题：**写「现象 / 复现步骤 / 期望 vs 实际 /
    所用算法或函数（如 Schoenfeld 公式、ss_survival_logrank）/ 错误消息原文」，必要时可写数值与
    研究设计内容（如 HR=0.75、power=0.85、1:1 分配比）**——以能复现问题为准。
    唯一硬边界：不写可识别个人/机构/受试者的身份信息（姓名、ID、邮箱、单位、受试者编号）。
    内容最终由用户在两阶段确认①检视把关（用户同意才发送）。
  - 仅标准库；端点是占位符，叶子技能接入时替换为真实统一端点 URL。
  - 出站鉴权：send 前必须经技能既有出站授权闸门（§5）确认；本文件不自行授权。
  - query_origin（§8.6）：sha256(hostname)，随每个报告发送，服务端归因/限流。
"""

import hashlib
import io
import json
import os
import socket
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

# ── §8.6 硬件绑定机器标识：统一从本技能 scripts/hardware_id.py 导入（ct-base 共享件 vendored 副本）──
# 任何叶子技能复制本文件时，须配套复制 scripts/hardware_id.py。取不到时回退主机名（保证永不崩）。
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "scripts"))
try:
    from hardware_id import hardware_id as _hardware_id
except Exception:  # pragma: no cover
    _hardware_id = None

# ── 报告信封：硬白名单字段（§20.3.2 脱敏铁律）───────────────────────────
# 只允许这些键；值类型固定。任何未列入信封的用户数据键（原始数据表/受试者记录）都会在 sanitize 时被剔除。
# description 例外：唯一自由文本字段，用户把关制披露——可写现象/复现/期望 vs 实际/所用算法或函数/
# 错误消息原文，必要时可含数值与研究设计；唯一边界=不写可识别身份信息；用户确认②把关；空串允许（省略键）。
REPORT_SCHEMA = {
    "skill": str,            # 技能名（如 "ct-samplesize"）
    "skill_version": str,    # 技能版本（如 "4.0.7"）
    "test": str,             # 出错检验（如 "ttest_ind"）；未知为 "unknown"
    "error_type": str,       # error | engine_error | numerical_suspect | crash
    "error_code": str,       # 技能定义的错误码（如 "COZE_UNREACHABLE"）；无则 ""
    "engine_status": str,    # 引擎状态摘要（如 "coze ok" / "r_engine error"）；无则 ""
    "description": str,      # 用户把关制问题描述（现象/复现/算法或函数/可含数值与研究设计；不含可识别身份信息）
    "locale": str,           # 会话语言（"zh"/"en"）
    "query_origin": str,     # §8.6 客户端标识（硬件绑定 sha256，跨账号/主机名稳定）
    "session_hash": str,      # 会话指纹（硬件标识+日期），不含会话内容
    "attempts": int,         # 同检验重试次数（1 = 首次失败）
}

# ── 统一报告端点（已发布 2026-08-21，ct-bugreport 正式域名）──────────────
# 全库共用一个端点（§20.3.5）：接收 → 校验 → 飞书表格落库 → 通知。
DEFAULT_ENDPOINT = "https://ct-bugreport.coze.site/run"
AUTHOR_EMAIL = "medstatstar@gmail.com"  # §13.2 联系方式（本地兜底）

# ── 端点访问 token：公共凭据（§5 公用凭据最低线 = XOR+base64 混淆内嵌）──
# 用户授权（2026-08-21）：该 token 绑定公开端点、无个人归属，可随技能发布；
# OBFUSCATION 非加密（密钥随脚本、可逆），仅防明文扫描/误读，不得宣称安全存储。
# 与 ct-samplesize 同源同键（§5 全家族共用一份公共凭据）。
_OBFUSCATION_KEY = b"ct-bugreport-coze-obf-v1-3c9e"
_EMBEDDED_SECRETS = {
    "ct_bugreport_coze": (
        "Bg1nChcgEQw_BjgneBkmSytEJhEvQAJBd3AqDywOLR4sISUeKB02Cjh6MhY0V2AbLCFkDnxuA1Z3HzEeYTU4VTwhExUrI2cPNgAOHjULLBRYVFR5E1pWLh1iCz8IFi0iGBEOQhUjSCNaDjFTRxQCXV8vVCsWPUQVHD4qMxsmGARPKgQwMWAVMC1JMVlMYghJCwYyXQsjMTQSIyo7QH5THz8GHC0yPFcgSHQDWm8sD0ReKxgxRgYzJkQ7aSoXNyFkXSwMSkV_R1BWdjYUHUw1M1c7Dx8XPA5KUCIQBh8gNi8cOnJnSQduLAo7RCgPBDUJHTUfIRsvFkMNTigJE3RECBtpMAwPAR0UURdUOBcSKEscdyVWCj9qORcCahoBSGBaST8nGx4sHwRAKBoIQDpXIl83D2BaLDJsQ395dhlwDBQdTlE_DTsPHwYTIxgKDUkzWDUkX0USaX9cOwsjCS0fNA8EQ1xADUAAQQEDQxV3Kw1VYxxSH34JUlQsIHxTODM_UT4rEQNiNzYDLENfTAAYEHdXdi5dVwcaSgwEIUUQPCQ1QFkxJw0RXzkTVGE3Z3xBCQgNIEdaFTMpBC4IOj8ATyA5TlNMGjAqdxxlTEs3ZiQKBwAaFgUALkUdRTtKFScuLncLGj9iQWlXZCReKws9QlRFIR5WRCgDFmUbGSg2Zh0XEBRACXVmTnQNVwdoUww-O1E3CQobSjEWShN5DAQHewRyZH4waSQmHVw4Ig0ZUzMwNERMJSJOV1VWVjNoJGFjejB7KCkeX1sRVxopKgYeE2oTBRwEb102IHk3XB50AE43FjBlDCIAIRU1NxsseDkcOzxeOFAWQhRFGFcoU10gQXQmLTA8UD0EFxh1UiANL3gIMSheJlB1VjJTJzkwWToxMEFSICQeA0ExWjgSYRYDCmgUUkYCC3UJJDBoFjo9IlAlPjkgYCIGQ1x5XzoMWhhlWQIJFCYnOH0uAAMrHCRXBSMeBA=="
    ),
}


def _obf_decode(blob: str) -> str:
    """XOR+base64 解码（§5 公共凭据混淆的逆操作）。"""
    import base64
    data = base64.urlsafe_b64decode(blob.strip())
    key = _OBFUSCATION_KEY
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data)).decode("utf-8")


def get_endpoint_token() -> str:
    """取 bugreport 端点访问 token（内嵌混淆 blob 解码；解析失败回退空串）。"""
    blob = _EMBEDDED_SECRETS.get("ct_bugreport_coze")
    if blob:
        try:
            return _obf_decode(blob)
        except Exception:  # pragma: no cover
            return ""
    return ""

# ── 内置双语文案（一次性提示走 i18n 精神：中英各一版，供 agent 原样复述）──
_MSGS = {
    "propose_zh": "检测到可能属于技能缺陷的错误（{error_type}，{test} 检验）。"
                  "是否生成一份【脱敏】错误报告发送给作者？报告仅含技能名/版本/错误类型，"
                  "以及您确认的问题描述（不含您的原始数据）。",
    "propose_en": "A likely skill defect was detected ({error_type}, test {test}). "
                  "Send a sanitized bug report to the author? The report contains only "
                  "skill name/version/error type plus a problem description you approve "
                  "— never your raw input data.",
    "show_zh": "以下为将发送的报告内容（已脱敏，不含原始数据），请确认：",
    "show_en": "The report to be sent (sanitized, no raw data) — please confirm:",
    "desc_hint_zh": "请补充问题描述（可选，但强烈建议）：发生了什么、期望 vs 实际、如何复现？"
                    "请写明所用算法或函数（如 Schoenfeld 公式），必要时可含数值与研究设计"
                    "（如 HR、power、分配比）；仅请勿包含可识别个人/机构/受试者的身份信息。"
                    "内容将在发送前展示给您最终确认。",
    "desc_hint_en": "Describe the problem (optional but strongly recommended): what happened, "
                    "expected vs actual, how to reproduce? Name the algorithm/function used "
                    "(e.g. Schoenfeld formula); values and study design (HR, power, allocation "
                    "ratio) are OK if needed. Just avoid identifiable person/institution/subject "
                    "info — you will review the final content before sending.",
    "local_zh": "本次会话无云端调用，已生成本地报告文件：{path}\n"
                "如您愿意协助改进，请将文件内容粘贴到邮件发送至：{email}",
    "local_en": "No cloud call in this session; local report saved: {path}\n"
                "If you'd like to help improve the skill, please email the content to: {email}",
    # ── 历史回执（§20.3 历史回执，用户 2026-08-22）──
    "thank_zh": "感谢您提交错误报告，我们已经收到，会尽快核查。",
    "thank_en": "Thank you for submitting the bug report — we have received it and will review it shortly.",
    "done_zh": "另外很高兴通知您，您上一次提交的技能 bug 已成功修复，详情为：{memo}",
    "done_en": "Also, good news: the bug you reported last time has been fixed. Details: {memo}",
    "pending_zh": "另外还需要通知您，您上一次提交的技能 bug 目前尚未完成修复，我们会尽快解决此问题。",
    "pending_en": "Also, a note: the bug you reported last time is not yet fixed — we will resolve it as soon as possible.",
}


def _current_locale():
    """会话语言：CTSS_LOCALE / 系统语言探测（与 ct- 技能惯例一致）。"""
    env = os.environ.get("CTSS_LOCALE") or os.environ.get("CTSS_LANG")
    if env:
        return env.strip().lower().startswith("zh") and "zh" or "en"
    try:
        import locale
        return "zh" if locale.getdefaultlocale()[0].lower().startswith("zh") else "en"
    except Exception:  # pragma: no cover
        return "en"


def query_origin() -> str:
    """§8.6 调用来源标识：硬件绑定的 sha256（SMBIOS UUID / MachineGuid / machine-id），
    跨 Windows 账号 / 改主机名 / 重装系统稳定；取不到时回退主机名。"""
    if _hardware_id is not None:
        return _hardware_id()
    try:
        host = socket.gethostname()
    except Exception:  # pragma: no cover
        host = "unknown-host"
    return "sha256:" + hashlib.sha256(host.encode("utf-8", "replace")).hexdigest()


def session_hash() -> str:
    """会话指纹：硬件标识 + 日期哈希（不含会话内容，仅用于服务端去重/归因）。"""
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base = _hardware_id() if _hardware_id is not None else socket.gethostname()
    return hashlib.sha256((base + "|" + day).encode("utf-8", "replace")).hexdigest()[:16]


def sanitize_report(report: dict) -> dict:
    """硬白名单脱敏：仅保留 REPORT_SCHEMA 中的键；多余键（含用户数据）一律剔除。

    description 为可选字段：空串/None 时省略该键（与旧端点 10 键白名单完全兼容）。
    """
    out = {}
    for k, typ in REPORT_SCHEMA.items():
        v = report.get(k)
        if v is None:
            continue
        if k == "description" and not str(v).strip():
            continue  # 空/纯空白描述不占键位（兼容旧端点；有内容才发送）
        if isinstance(v, typ) or (typ is int and isinstance(v, bool)):
            out[k] = v
    out["query_origin"] = report.get("query_origin") or query_origin()
    if "session_hash" not in out:
        out["session_hash"] = session_hash()
    return out


def build_report(skill: str, skill_version: str, test: str,
                 error_type: str, error_code: str = "", engine_status: str = "",
                 description: str = "", locale: str = None, attempts: int = 1) -> dict:
    """组装脱敏报告。

    description：用户把关制问题描述（可选，推荐填写以协助作者 debug）。
      写「现象 / 复现步骤 / 期望 vs 实际 / 所用算法或函数 / 错误消息原文」，
      必要时可含数值与研究设计（如 HR=0.75、power=0.85、1:1 分配比）——以能复现为准；
      唯一硬边界：不写可识别个人/机构/受试者的身份信息；由用户在两阶段确认①检视把关。"""
    return sanitize_report({
        "skill": skill, "skill_version": skill_version, "test": test or "unknown",
        "error_type": error_type, "error_code": error_code or "",
        "engine_status": engine_status or "", "description": description or "",
        "locale": locale or _current_locale(),
        "attempts": max(1, int(attempts)),
    })


def render_report_text(report: dict) -> str:
    """渲染为可读文本（供用户确认；中英按 locale）。description 独立段落、保留换行。"""
    r = sanitize_report(report)
    loc = (r.get("locale") or _current_locale())
    head = _MSGS["show_zh"] if loc == "zh" else _MSGS["show_en"]
    lines = [head, ""]
    for k in REPORT_SCHEMA:
        if k == "description":
            continue
        if k in r and r[k] not in (None, ""):
            lines.append("  %s: %s" % (k, r[k]))
    desc = r.get("description") or ""
    if desc:
        lines.append("")
        lines.append("  description:")
        for ln in desc.splitlines() or [desc]:
            lines.append("    %s" % ln)
    lines.append("")
    return "\n".join(lines).rstrip("\n")


def confirm_prompt(error_type: str = "error", test: str = "unknown", locale: str = None) -> str:
    """双语一次性提议文案（agent 原样复述给用户，i18n 提示）。"""
    loc = locale or _current_locale()
    base = _MSGS["propose_zh" if loc == "zh" else "propose_en"].format(
        error_type=error_type, test=test)
    hint = _MSGS["desc_hint_zh" if loc == "zh" else "desc_hint_en"]
    return base + "\n" + hint


def confirm_thanks(locale: str = None) -> str:
    """2.1 发送成功后固定感谢文案（技能端组织回复时先说这一句）。"""
    loc = locale or _current_locale()
    return _MSGS["thank_zh" if loc == "zh" else "thank_en"]


def parse_history(history_str) -> dict:
    """coze 返回 history 字段（JSON 字符串或 ""）→ dict；空/异常 → {}。"""
    if not history_str:
        return {}
    if isinstance(history_str, dict):
        return history_str
    try:
        d = json.loads(history_str)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def build_followup(history: dict, locale: str = None) -> str:
    """2.2/2.3 追加文案：根据历史记录 resultstr 生成修复状态通知。

    history 为空（无上一次提交）→ 返回 ""（2.1 感谢后即结束）；
    resultstr == "done" → 2.2 已修复通知（带 memo 详情）；
    resultstr != "done" → 2.3 未修复通知。
    """
    if not history:
        return ""
    loc = locale or _current_locale()
    resultstr = (history.get("resultstr") or "").strip()
    memo = (history.get("memo") or "").strip()
    if resultstr == "done":
        if loc == "zh":
            return _MSGS["done_zh"].format(memo=memo if memo else "（暂无备注）")
        return _MSGS["done_en"].format(memo=memo if memo else "(no details provided)")
    if loc == "zh":
        return _MSGS["pending_zh"]
    return _MSGS["pending_en"]


def detect_error_signal(test: str, attempts: int, cli_error: bool = False,
                        engine_error: bool = False, user_questioning: bool = False) -> bool:
    """错误信号判定（§20.3.1）：强信号 + 重试次数。
    强信号 = CLI 非 0 退出 / R 引擎错误 / 用户明确质疑结果；
    弱信号 = 仅同检验多次重试（用户正常调参，不触发）。
    """
    strong = cli_error or engine_error or user_questioning
    return strong and attempts >= 1


def send_to_endpoint(report: dict, endpoint: str = None, token: str = None,
                     timeout: float = 15.0) -> dict:
    """POST 到统一 bug-report 端点（action=report，唯一动作；治理动作不在此实现）。返回 {status, note}。

    - 调用方必须先经技能既有出站授权闸门（§5）确认；
    - token 默认取内嵌公共凭据（§5 XOR+base64），可由调用方显式覆盖（见 ct-samplesize 实装）；
    - 协议（2026-08-21 线上实测）：① 网关入口校验 `Authorization: Bearer <token>` 头（缺头 401）；
      ② 应用层 payload 也带 `token` 字段（服务端配置后校验）。两端必须一致携带。
    """
    r = sanitize_report(report)
    url = endpoint or DEFAULT_ENDPOINT
    token = token if token is not None else get_endpoint_token()
    payload = json.dumps({
        "action": "report",
        "report": r,
        "query_origin": r.get("query_origin"),
        "token": token,
        "ts": datetime.now(timezone.utc).isoformat(),
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST", headers={
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "ct-bug-report/1.0",
        "Authorization": "Bearer %s" % (token or ""),
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
            try:
                data = json.loads(body)
            except Exception:  # pragma: no cover
                return {"status": "ok" if resp.status < 400 else "error",
                        "note": body[:200], "history": ""}
            if not isinstance(data, dict):
                return {"status": "ok" if resp.status < 400 else "error",
                        "note": str(body)[:200], "history": ""}
            data.setdefault("history", "")
            return data
    except (urllib.error.URLError, OSError) as e:
        return {"status": "error", "note": "endpoint unreachable: %s" % e, "history": ""}


def save_local_report(report: dict, outdir: str = ".") -> str:
    """本地兜底（§20.3.4）：无 coze 调用时写脱敏报告 md，提示作者邮箱。"""
    r = sanitize_report(report)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "ct_bug_report_%s.md" % datetime.now().strftime("%Y%m%d_%H%M%S"))
    loc = (r.get("locale") or _current_locale())
    lines = ["# ct- 技能错误报告（脱敏）", ""]
    for k in REPORT_SCHEMA:
        if k == "description":
            continue
        if k in r and r[k] not in (None, ""):
            lines.append("- %s: %s" % (k, r[k]))
    desc = r.get("description") or ""
    if desc:
        lines.append("")
        lines.append("## 问题描述（自由文本）")
        lines.append(desc)
    lines += ["",
              "> 本报告不含您的原始输入数据；description 为经您确认的问题描述。",
              "> 如需协助改进，请粘贴此内容发送至：",
              "> %s" % AUTHOR_EMAIL,
              "> 注意：若经对话确认后由技能发送，此本地文件仅为备份。"]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    msg = _MSGS["local_zh" if loc == "zh" else "local_en"].format(path=path, email=AUTHOR_EMAIL)
    return path + "\n" + msg


if __name__ == "__main__":
    # 模板自检：生成带问题描述的示例报告并本地落盘（不发网络）
    demo = build_report(skill="ct-samplesize", skill_version="5.0.1",
                        test="survival", error_type="engine_error",
                        error_code="R_ENGINE_ERROR", engine_status="coze r engine error",
                        description="survival 检验（ss_survival_logrank，Schoenfeld 公式）"
                                    "输入 HR=0.75、power=0.85、1:1 分配，返回事件数 109；"
                                    "手工复核应为 434（疑似缺 (1+r)²/r=4 因子）。"
                                    "期望与 rpact 一致，实际偏小 4 倍。")
    print(render_report_text(demo))
    print("---")
    print(save_local_report(demo, outdir="."))
