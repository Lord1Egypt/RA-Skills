#!/usr/bin/env python3
"""analyze_session.py — 解析 Agent 会话记录,按 SKILL.md 的七类归组统计

支持格式:
  - OpenClaw 会话 JSONL(.openclaw*/agents/*/sessions/*.jsonl)
  - 通用 JSONL: 每行一个 JSON 对象,含 message.role / message.content
  - 纯文本: 整体计入「对话历史」

七类: system(系统指令) / goal(任务目标) / constraint(约束与规则) /
      tool(工具输出) / history(对话历史) / reasoning(中间推理) / state(状态与记忆)

用法:
  python3 analyze_session.py session.jsonl [--window 200000] [--json]
输出: Markdown 预算表(或 --json 机器可读)。所有数字为估算值。
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 约束语句特征(中英):出现在 user/assistant 文本中 → 归入 constraint
CONSTRAINT_PATTERNS = [
    r"不要|禁止|不能|不许|别动|避免|必须|务必|只能",
    r"\bdon't\b|\bdo not\b|\bmust\b|\bnever\b|\bcannot\b|\bforbidden\b|\bavoid\b|\brestrict",
    r"安全边界|约束|红线|权限|边界|policy|constraint|boundary|permission",
]
# 状态/记忆特征:todo/计划文件/清单类内容
STATE_PATTERNS = [
    r"\bTODO\b|待办|任务清单|检查点|checkpoint|state file|memory file|\.md 文件",
    r"- \[ \]|- \[x\]",
]

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
    """把 message.content 归一为 (kind, text) 序列。kind: text|thinking|toolCall|toolResult"""
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
            elif t == "image":
                yield "text", "[image attachment]"

def _classify(role: str, kind: str, text: str, first_user_seen: list) -> str:
    """返回七类之一"""
    if kind == "toolResult":
        return "tool"
    if kind == "thinking":
        return "reasoning"
    if kind == "toolCall":
        return "tool"      # 工具调用参数本质是"将产生工具输出"的请求,与输出合并统计
    # 普通文本
    if role == "system":
        return "system"
    if role == "user":
        if not first_user_seen:
            first_user_seen.append(True)
            return "goal"   # 首条用户消息视为任务目标
        joined = text
        if any(re.search(p, joined) for p in CONSTRAINT_PATTERNS) and len(joined) < 2000:
            return "constraint"
        if any(re.search(p, joined) for p in STATE_PATTERNS) and re.search(r"记录|清单|checkpoint", joined):
            return "state"
        return "history"
    # assistant 文本
    if any(re.search(p, text) for p in CONSTRAINT_PATTERNS) and len(text) < 800:
        return "constraint"
    return "history"

def analyze(path: Path, window: int):
    buckets = {k: {"tokens": 0, "chunks": 0} for k in
               ["system", "goal", "constraint", "tool", "history", "reasoning", "state"]}
    big_tools = []     # (行号, tokens) 单条工具输出超过窗口 5%
    roles_seen = set()
    n_messages = 0
    first_user_seen = []
    unparsed = 0

    with open(path, encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            obj = None
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                unparsed += 1
            if obj is None:
                buckets["history"]["tokens"] += _tok(line)
                buckets["history"]["chunks"] += 1
                continue
            # OpenClaw: type==message 包 message;toolResult 有时是顶层 type
            msg = obj.get("message") if isinstance(obj.get("message"), dict) else obj
            role = msg.get("role") or obj.get("role") or ""
            content = msg.get("content", obj.get("content"))
            kind_override = None
            if obj.get("type") == "toolResult" or role == "toolResult" or role == "tool":
                role, kind_override = "tool", "toolResult"
            texts = list(_iter_texts(content)) if content is not None else []
            if not texts and (role or obj.get("type") == "message"):
                # 无 content 的行跳过
                if not role:
                    continue
            if role:
                roles_seen.add(role)
            for kind, text in texts:
                if kind_override:
                    kind = kind_override
                if kind == "text" and role in ("user", "assistant", "system"):
                    n_messages += 1
                cat = _classify(role, kind, text, first_user_seen)
                tokens = _tok(text)
                buckets[cat]["tokens"] += tokens
                buckets[cat]["chunks"] += 1
                if cat == "tool" and tokens > window * 0.05:
                    big_tools.append((lineno, tokens))

    total = sum(b["tokens"] for b in buckets.values())
    return {
        "file": str(path),
        "window": window,
        "total_tokens": total,
        "window_pct": round(total / window * 100, 1) if window else None,
        "messages": n_messages,
        "roles": sorted(roles_seen),
        "buckets": buckets,
        "big_tool_outputs": big_tools,
        "unparsed_lines": unparsed,
    }

def to_markdown(r: dict) -> str:
    name = {"system": "① 系统指令", "goal": "② 任务目标", "constraint": "③ 约束与规则",
            "tool": "④ 工具输出", "history": "⑤ 对话历史", "reasoning": "⑥ 中间推理",
            "state": "⑦ 状态与记忆"}
    lines = [f"# 会话预算分析(脚本估算)", "",
             f"- 文件:`{r['file']}`",
             f"- 估算总占用:≈{r['total_tokens']:,} tokens(窗口按 {r['window']:,} 估算,占比 ≈{r['window_pct']}%)",
             f"- 消息条数:{r['messages']};角色:{', '.join(r['roles']) or '无'}", ""]
    lines.append("| 类别 | ≈Token | 占比 | 片段数 |")
    lines.append("|---|---|---|---|")
    for k in name:
        b = r["buckets"][k]
        pct = round(b["tokens"] / r["total_tokens"] * 100, 1) if r["total_tokens"] else 0
        lines.append(f"| {name[k]} | ≈{b['tokens']:,} | {pct}% | {b['chunks']} |")
    if r["big_tool_outputs"]:
        lines.append("")
        lines.append("**巨物输出预警**(单条 > 窗口 5%):")
        for lineno, tokens in r["big_tool_outputs"]:
            lines.append(f"- 第 {lineno} 行,≈{tokens:,} tokens")
    lines.append("")
    lines.append("> 数字为脚本估算(规则见 estimate_tokens.py),非精确计量;七类归组基于启发式,最终判定请结合 SKILL.md 的人工分析流程。")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Agent 会话七类归组预算分析(估算)")
    ap.add_argument("file", help="会话记录路径(JSONL/JSON/纯文本)")
    ap.add_argument("--window", type=int, default=200000, help="上下文窗口大小(默认 200000)")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    args = ap.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"错误:文件不存在:{path}", file=sys.stderr)
        sys.exit(1)
    result = analyze(path, args.window)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else to_markdown(result))

if __name__ == "__main__":
    main()
