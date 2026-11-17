#!/usr/bin/env python3
"""audit_constraints.py — 约束丢失审计(Governance Decay 确定性初筛)

背景:治理衰减研究(arXiv:2606.22528, 2026)表明——上下文压缩是否导致 Agent 违规,
几乎完全由"约束是否活过摘要"决定:约束存活违规率 0%,被丢则 38%;软组织策略的
衰减是硬安全规范的 8.3 倍。本脚本做确定性初筛:找出会话里的约束语句,标注每条
约束的位置与可见性,判断它在压缩中是已丢失、面临丢失还是当前可见。

判定规则(透明可解释,非黑盒):
  - 系统角色约束 → 低危(多数 Harness 压缩时保留 system 消息;
    但注意:仅当约束确实经由 system 通道注入时成立)
  - 有 usage 骤降点时(Claude Code 会话):
      最后一次出现在首个骤降点之前且之后再未出现:
        → 先对照压缩摘要行(isCompactSummary / type=summary):
          摘要中再现(实体全命中或中文 4-gram 覆盖 ≥60%) → 低危:大概率存活,
            但已经摘要改写,建议抽查保真
          摘要中无再现(或无摘要行可对照) → 高危:已随压缩丢失
      出现在骤降点之后但不在最近区 → 中危:面临下一次压缩
      最近区(消息末 15%)内有出现 → 低危:当前可见
  - 无 usage 时(OpenClaw/通用 JSONL,仅位置分析):
      单次出现且不在最近区 → 高危:单一副本,位置靠前
      多次出现但全部不在最近区(长会话) → 中危:全部副本已被"晾旧"
      最近区有出现 → 低危
  - 摘要行本身只作对照材料:不作约束来源、不参与位置统计,
    避免摘要复述被误当作「约束仍在对话中」

统计口径:
  - 只扫描 system/user/assistant 的文本段(约束是治理内容,不来自工具输出);
    assistant 的复述算"再可见"——最近被复述的约束仍在上下文前沿
  - 消息位置 = 该文本段在全部 user/assistant 文本段中的序号占比

输出:Markdown 审计报告(或 --json)。所有 Token 为估算值。
本脚本只做位置与可见性判断;约束的语义重要性、是否仍然有效,由 SKILL.md 流程人工复核。

用法:
  python3 audit_constraints.py session.jsonl [--json]
适用格式:与 analyze_session.py 相同(OpenClaw / 通用 JSONL / Claude Code)。
Claude Code 会话额外利用 message.usage 骤降点做压缩关联;其他格式自动降级为位置分析。
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 约束语句特征(与 analyze_session.py 同族,中英)
CONSTRAINT_PATTERNS = [
    r"不要|禁止|不能|不许|别动|避免|必须|务必|只能|一律|严禁",
    r"\bdon't\b|\bdo not\b|\bmust\b|\bnever\b|\bcannot\b|\bforbidden\b|\bavoid\b|\brestrict\b|\bonly use\b",
    r"安全边界|红线|约束|policy|constraint|boundary",
]
# 引用价值低的整段(纯模式匹配会误伤:比如教程里引用的"不要")——长度上限过滤
MAX_QUOTE_LEN = 600
MIN_CONSTRAINT_LEN = 4
RECENT_ZONE = 0.15   # 消息末 15% 视为"最近区"


_PUNCT_RE = re.compile(r"[\s,.;:!?、。,;:!?·…—\"'`()<>《》\[\]{}|]+")
_ENTITY_RE = re.compile(r"[A-Za-z0-9_./\\-]{3,}")


def _norm_text(s: str) -> str:
    """去空白与常见标点、小写化,用于摘要再现的 n-gram 对照。"""
    return _PUNCT_RE.sub("", s).lower()


def _constraint_in_summary(quote: str, summary_raw: str, summary_norm: str):
    """判断约束语句是否在压缩摘要中再现。返回 (kept, 判定依据说明)。
    有英文/路径/数字实体(≥3 字符)时以实体命中为准(全命中=再现);
    纯中文语句用 4-gram 覆盖率 ≥60% 判定。确定性规则,不做语义理解。"""
    ents = _ENTITY_RE.findall(quote)
    if ents:
        low = summary_raw.lower()
        missing = [e for e in ents if e.lower() not in low]
        if not missing:
            shown = ", ".join(ents[:3]) + ("等" if len(ents) > 3 else "")
            return True, f"实体命中:{shown}"
        if len(missing) < len(ents):
            return False, f"实体部分命中(缺:{', '.join(missing[:3])})"
        return False, None
    nq = _norm_text(quote)
    if len(nq) < 8:
        return False, None
    grams = [nq[i:i + 4] for i in range(len(nq) - 3)]
    if not grams:
        return False, None
    hit = sum(1 for g in grams if g in summary_norm)
    if hit / len(grams) >= 0.6:
        return True, f"n-gram 覆盖 {hit}/{len(grams)}"
    return False, None


def _extract_compact_text(obj: dict):
    """识别压缩摘要行,返回摘要文本或 None。
    已知形态:Claude Code 顶层 isCompactSummary=true 的 user 行(content 为 str 或
    content[].text);CC 老版 type=summary 行(summary 字段)。其他平台返回 None。"""
    if obj.get("isCompactSummary") is True:
        msg = obj.get("message")
        content = msg.get("content") if isinstance(msg, dict) else obj.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [pp.get("text", "") for pp in content
                     if isinstance(pp, dict) and pp.get("type") == "text"]
            if parts:
                return "\n".join(parts)
    if obj.get("type") == "summary" and isinstance(obj.get("summary"), str):
        return obj["summary"]
    return None



def _tok(text: str) -> int:
    """与 estimate_tokens.py 相同的估算规则(内联避免跨文件依赖)"""
    if not text:
        return 0
    cjk = sum(1 for ch in text if (0x4E00 <= ord(ch) <= 0x9FFF or 0x3400 <= ord(ch) <= 0x4DBF
               or 0x3040 <= ord(ch) <= 0x30FF or 0xAC00 <= ord(ch) <= 0xD7AF))
    rest = len(text) - cjk
    tokens = cjk * 1.25
    if rest:
        density = sum(text.count(c) for c in "{};=()[]<>") / max(rest, 1)
        tokens += rest / (3 if density > 0.08 else 4)
    return max(1, round(tokens))


def _iter_texts(content):
    """把 message.content 归一为 (kind, text);kind: text|thinking|toolCall|toolResult"""
    if content is None:
        return
    if isinstance(content, str):
        yield "text", content
        return
    if isinstance(content, list):
        for part in content:
            if not isinstance(part, dict):
                continue
            t = part.get("type")
            if t == "text":
                yield "text", part.get("text", "")
            elif t == "thinking":
                yield "thinking", part.get("thinking", "") or part.get("text", "")
            elif t in ("toolCall", "tool_call", "toolUse"):
                yield "toolCall", json.dumps(part.get("arguments", part.get("input", {})), ensure_ascii=False)
            elif t in ("toolResult", "tool_result"):
                c = part.get("content", part.get("text", ""))
                if isinstance(c, list):
                    c = "\n".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)
                yield "toolResult", str(c)


def _split_constraint_sentences(text: str):
    """把段落按句切分,返回含约束特征的句子。
    切分后把过短碎片(如「红线:」)并回前句,避免标题词被单独当作约束。
    换行本身视为句子边界(不往行尾补句号,避免引用出现「。。」瑕疵)。"""
    out = []
    for line_txt in (text.splitlines() or [text]):
        for sent in re.split(r"(?<=[。!?;.!?])", line_txt):
            s = sent.strip()
            if not s:
                continue
            if len(s) < MIN_CONSTRAINT_LEN and out:
                out[-1] = out[-1] + s     # 碎片并回前句,保持原文完整
                continue
            out.append(s)
    return [s for s in out
            if MIN_CONSTRAINT_LEN <= len(s.rstrip("。.::、,，;；!！?？ \n")) <= MAX_QUOTE_LEN
            and any(re.search(p, s) for p in CONSTRAINT_PATTERNS)]


def _extract_usage_total(obj: dict):
    if obj.get("type") != "assistant":
        return None
    msg = obj.get("message")
    if not isinstance(msg, dict):
        return None
    u = msg.get("usage")
    if not isinstance(u, dict) or "input_tokens" not in u:
        return None
    return (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
            + u.get("cache_creation_input_tokens", 0))


def analyze(path: Path):
    hits = []
    n_text_msgs = 0
    unparsed = 0
    roles_seen = set()
    usage_trace = []      # (lineno, total_in)
    summaries = []        # 压缩摘要行:[{line, chars, text}]

    with open(path, encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                unparsed += 1
                continue
            u = _extract_usage_total(obj)
            if u is not None:
                if not usage_trace or usage_trace[-1][1] != u:
                    usage_trace.append((lineno, u))
            ct = _extract_compact_text(obj)
            if ct:
                summaries.append({"line": lineno, "chars": len(ct), "text": ct})
                continue   # 摘要行是压缩对照材料,不作为约束来源参与判级
            msg = obj.get("message") if isinstance(obj.get("message"), dict) else obj
            role = msg.get("role") or obj.get("role") or ""
            if obj.get("type") == "toolResult" or role in ("tool", "toolResult"):
                continue   # 工具输出不产生合法约束
            content = msg.get("content", obj.get("content"))
            for kind, text in _iter_texts(content):
                if kind != "text" or role not in ("system", "user", "assistant"):
                    continue
                if role not in roles_seen:
                    roles_seen.add(role)
                n_text_msgs += 1
                for sent in _split_constraint_sentences(text):
                    hits.append({"quote": sent, "role": role, "line": lineno,
                                 "msg_idx": n_text_msgs - 1})

    if not hits and n_text_msgs == 0 and unparsed > 0:
        return {"file": str(path), "error": "文件无法解析为会话记录(无有效消息行)。", "unparsed_lines": unparsed}

    # 同源行聚合:同一条消息里 ≥4 句约束 → 视为一个「策略文档块」而非零散约束。
    # 治理语义不同:零散单句约束是治理衰减的高危对象;整块策略文档已有结构,
    # 风险在于整块被摘要压缩,处置也不同(整块提升而非逐句钉扎)。
    by_line = {}
    for h in hits:
        by_line.setdefault(h["line"], []).append(h)
    grouped_hits = []
    for line_no, hs in by_line.items():
        if len(hs) >= 4:
            grouped_hits.append({"quote": hs[0]["quote"], "role": hs[0]["role"], "line": line_no,
                                 "msg_idx": hs[0]["msg_idx"], "block": True,
                                 "block_sentences": len(hs),
                                 "block_tokens": sum(_tok(x["quote"]) for x in hs)})
        else:
            grouped_hits.extend(hs)

    # 聚合:相同句子合并为一条约束,保留全部出现位置
    constraints = []
    for h in grouped_hits:
        for c in constraints:
            if h["quote"] == c["occurrences"][0]["quote"]:
                c["occurrences"].append(h)
                break
        else:
            constraints.append({"occurrences": [h]})

    # usage 骤降点(与 analyze_usage.py 同阈值:较前值下降 ≥20%)
    drops = []
    for k in range(1, len(usage_trace)):
        prev_v, cur_v = usage_trace[k - 1][1], usage_trace[k][1]
        if prev_v > 0 and cur_v < prev_v * 0.8:
            drops.append({"line": usage_trace[k][0], "from_tokens": prev_v,
                          "to_tokens": cur_v, "drop_pct": round((prev_v - cur_v) / prev_v * 100, 1)})
    has_usage = len(usage_trace) > 0
    first_drop_line = drops[0]["line"] if drops else None

    # 逐条判级
    recent_cut = max(0, int(n_text_msgs * (1 - RECENT_ZONE)))
    for c in constraints:
        occ = c["occurrences"]
        idxs = [o["msg_idx"] for o in occ]
        last = max(idxs)
        c["count"] = len(occ)
        c["first_line"] = min(o["line"] for o in occ)
        c["last_line"] = max(o["line"] for o in occ)
        c["last_pos_pct"] = round(last / n_text_msgs * 100, 1) if n_text_msgs else None
        if occ[0].get("block"):
            c["block"] = True
            c["block_sentences"] = occ[0]["block_sentences"]
            c["est_tokens"] = occ[0]["block_tokens"]
        else:
            c["est_tokens"] = sum(_tok(o["quote"]) for o in occ)
        c["roles"] = sorted({o["role"] for o in occ})
        in_recent = last >= recent_cut and n_text_msgs >= 8

        if c["roles"] == ["system"]:
            c["verdict"] = "low"
            c["reason"] = "系统通道注入(压缩通常豁免 system 消息);若实际经对话注入请人工改判"
            continue

        if has_usage and first_drop_line:
            if c["last_line"] < first_drop_line:
                prior = [s for s in summaries if s["line"] < first_drop_line]
                kept, how = (False, None)
                s_line = s_chars = None
                if prior:
                    s_line, s_chars = prior[-1]["line"], prior[-1]["chars"]
                    kept, how = _constraint_in_summary(
                        c["occurrences"][0]["quote"], prior[-1]["text"], _norm_text(prior[-1]["text"]))
                if kept:
                    c["verdict"] = "low"
                    c["saved_by_summary"] = {"line": s_line, "how": how}
                    c["reason"] = (f"原文出现在压缩前(第 {c['last_line']} 行),但压缩摘要"
                                   f"(第 {s_line} 行,{s_chars} 字)中再现({how})→ 大概率存活;"
                                   f"已经摘要改写,建议抽查保真")
                else:
                    c["verdict"] = "high"
                    where = (f";压缩摘要(第 {s_line} 行,{s_chars} 字)中无再现" if prior
                             else ";会话中未找到压缩摘要行,无法对照")
                    c["reason"] = (f"最后一次出现(第 {c['last_line']} 行)早于首个压缩骤降点"
                                   f"(第 {first_drop_line} 行),且之后再未出现{where} → 已随摘要重写丢失")
            elif not in_recent:
                c["verdict"] = "mid"
                c["reason"] = f"骤降后出现过,但已退出最近区(最后位置 {c['last_pos_pct']}%)→ 面临下一次压缩"
            else:
                c["verdict"] = "low"
                c["reason"] = f"最近区仍可见(最后位置 {c['last_pos_pct']}%)"
        else:
            if c["count"] == 1 and not in_recent:
                c["verdict"] = "high"
                c["reason"] = f"单一副本,最后位置 {c['last_pos_pct']}% → 摘要重写时极易被当作低显著度内容丢弃"
            elif not in_recent and n_text_msgs >= 8:
                c["verdict"] = "mid"
                c["reason"] = f"{c['count']} 个副本但全部不在最近区(最后位置 {c['last_pos_pct']}%)→ '晾旧'后显著性衰减"
            else:
                c["verdict"] = "low"
                c["reason"] = f"最近区可见(最后位置 {c['last_pos_pct']}%)"

    order = {"high": 0, "mid": 1, "low": 2}
    constraints.sort(key=lambda c: (order[c["verdict"]], -c["est_tokens"]))
    return {
        "file": str(path),
        "mode": "usage-correlated" if (has_usage and first_drop_line) else ("usage-no-drop" if has_usage else "position-only"),
        "text_messages": n_text_msgs,
        "usage_drops": drops,
        "compact_summaries": [{"line": s["line"], "chars": s["chars"],
                               "preview": s["text"][:80].replace("\n", " ")} for s in summaries],
        "constraints": constraints,
        "summary": {
            "total": len(constraints),
            "high": sum(1 for c in constraints if c["verdict"] == "high"),
            "mid": sum(1 for c in constraints if c["verdict"] == "mid"),
            "low": sum(1 for c in constraints if c["verdict"] == "low"),
        },
        "unparsed_lines": unparsed,
    }


_VERDICT_LABEL = {"high": "[高] 高危", "mid": "[中] 中危", "low": "[低] 低危"}


def to_markdown(r: dict) -> str:
    if r.get("error"):
        return "# 约束丢失审计(失败)\n\n- 文件:`" + r["file"] + "`\n- " + r["error"]
    s = r["summary"]
    mode_note = {
        "usage-correlated": "已关联 usage 骤降点(Claude Code 真实压缩边界)",
        "usage-no-drop": "含 usage 数据但未检出骤降点,按位置分析判级",
        "position-only": "无 usage 数据,按消息位置分析(OpenClaw/通用格式)",
    }[r["mode"]]
    lines = ["# 约束丢失审计(Governance Decay 初筛)", "",
             "- 文件:`" + r["file"] + "`",
             "- 分析模式:" + mode_note,
             "- 文本消息 " + str(r["text_messages"]) + " 条;检出约束 " + str(s["total"]) + " 条:"
             "高危 " + str(s["high"]) + " / 中危 " + str(s["mid"]) + " / 低危 " + str(s["low"]), ""]
    if not r["constraints"]:
        lines.append("未检出约束语句。若你确认会话中存在约束(如「不要动 X」),"
                     "脚本可能因句式变体漏检——请按 SKILL.md 人工流程补充审读,不要直接下结论「无约束」。")
    shown = r["constraints"][:12]
    for i, c in enumerate(shown, 1):
        lines.append("### C" + str(i) + " " + _VERDICT_LABEL[c["verdict"]])
        q = c["occurrences"][0]["quote"]
        show = q if len(q) <= 80 else q[:77] + "..."
        if c.get("block"):
            lines.append("- 策略文档块(第 " + str(c["first_line"]) + " 行,含 " + str(c["block_sentences"])
                         + " 句规则):首句「" + show + "」")
        else:
            lines.append("- 原文(首现):「" + show + "」")
        lines.append("- 角色:" + "/".join(c["roles"]) + ";出现 " + str(c["count"]) + " 次"
                     "(第 " + str(c["first_line"]) + "-" + str(c["last_line"]) + " 行,最后位于消息流 "
                     + str(c["last_pos_pct"]) + "% 处);≈" + str(c["est_tokens"]) + " tokens")
        lines.append("- 判定:" + c["reason"])
        if c["verdict"] == "high":
            if c.get("block"):
                lines.append("- 处置:整块钉扎——该策略块提升到 system 通道或压缩豁免的固定区块,"
                             "避免被摘要整段重写;逐句拆钉通常不必要")
            else:
                lines.append("- 处置:钉扎——原文提升到 system 通道或压缩豁免的固定区块;"
                             "若在 Claude Code 中用 CLAUDE.md 承载,确认其进入每轮注入")
        elif c["verdict"] == "mid":
            lines.append("- 处置:在最近一轮复述一次关键约束,或纳入压缩摘要的必含清单")
    if len(r["constraints"]) > 12:
        lines.append("")
        lines.append("(报告仅展开前 12 条;其余 " + str(len(r["constraints"]) - 12)
                     + " 条见 --json 输出,多为低危或同源重复。)")
    lines.append("")
    lines.append("> 判定基于位置与可见性启发式 +(如有)usage 骤降点关联;约束是否仍有效、语义权重如何,"
                 "请结合 SKILL.md 人工复核。Token 为估算值。规则与依据见脚本 docstring(arXiv:2606.22528)。")
    lines.append(_render_summary_section(r))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="约束丢失审计:治理衰减确定性初筛")
    ap.add_argument("file", help="会话记录路径(JSONL,支持 Claude Code / OpenClaw / 通用格式)")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    args = ap.parse_args()
    path = Path(args.file)
    if not path.exists():
        print("错误:文件不存在:" + str(path), file=sys.stderr)
        sys.exit(1)
    result = analyze(path)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else to_markdown(result))




def _render_summary_section(r: dict) -> str:
    """「压缩摘要对照」小节:直答这轮压缩丢掉了什么、保住了什么。"""
    ss = r.get("compact_summaries") or []
    if not ss:
        return ""
    lines = ["", "## 压缩摘要对照", "",
             f"会话含 {len(ss)} 处压缩摘要行:" +
             ", ".join(f"第 {s['line']} 行({s['chars']} 字)" for s in ss) + "。"]
    saved = [c for c in r.get("constraints", []) if c.get("saved_by_summary")]
    lost = [c for c in r.get("constraints", []) if c["verdict"] == "high"]
    if saved:
        lines.append("")
        lines.append("**摘要中再现(大概率存活)**:")
        for c in saved:
            how = c["saved_by_summary"]["how"]
            lines.append(f"- 「{c['occurrences'][0]['quote'][:60]}」({how})")
    if lost:
        lines.append("")
        lines.append("**摘要中无再现(确认丢失,需重新注入)**:")
        for c in lost:
            lines.append(f"- 「{c['occurrences'][0]['quote'][:60]}」")
    lines.append("")
    lines.append("> 摘要再现判定是确定性对照(实体命中或 4-gram 覆盖 ≥60%),不等于语义保真;"
                 "被改写的约束建议抽查原文完整性。")
    return "\n".join(lines)
if __name__ == "__main__":
    main()
