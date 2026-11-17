"""Build conversation inventory tables (no deep analysis)."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core import redact_path
from load_export import Conversation, filter_messages


def _fmt_ts(ts: Optional[int]) -> str:
    if ts is None:
        return ""
    # support sec and ms
    if ts > 10_000_000_000:
        ts = ts // 1000
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return str(ts)


def inventory_conversations(convs: List[Conversation], cfg: dict) -> Dict[str, Any]:
    top_n = int((cfg.get("limits") or {}).get("inventory_top_senders", 12))
    drop_system = bool((cfg.get("filters") or {}).get("drop_system", True))
    rows = []
    for idx, c in enumerate(convs, 1):
        msgs = filter_messages(c.messages, drop_system=drop_system)
        senders = Counter(m.sender_name for m in msgs if m.sender_name)
        ts_list = [m.ts for m in msgs if m.ts]
        share_n = sum(1 for m in msgs if m.is_share_like)
        prose_n = sum(1 for m in msgs if not m.is_share_like and (m.content or "").strip())
        top_senders = [
            {"name": n, "count": cnt}
            for n, cnt in senders.most_common(top_n)
        ]
        rows.append(
            {
                "index": idx,
                "conversation_id": c.conversation_id,
                "name": c.name,
                "type": c.conv_type,
                "platform": c.platform,
                "source_path": redact_path(c.source_path),
                "members_listed": len(c.members),
                "messages_raw": len(c.messages),
                "messages_kept": len(msgs),
                "prose_messages": prose_n,
                "share_like_messages": share_n,
                "unique_senders": len(senders),
                "top_senders": top_senders,
                "date_start": _fmt_ts(min(ts_list) if ts_list else None),
                "date_end": _fmt_ts(max(ts_list) if ts_list else None),
            }
        )
    return {
        "status": "inventory",
        "conversation_count": len(rows),
        "conversations": rows,
        "next_step": (
            "请指定分析对象后再深挖。回复：会话#编号 / 会话名 / 人物名 / "
            "`会话#1 + 只看@某人`。或 CLI: --conv 1 --person 名称"
            if len(rows) >= 1
            else "未解析到会话"
        ),
        "gate": "deep_analyze_blocked_until_target" if len(rows) != 1 else "single_conversation_still_requires_explicit_deep",
    }


def format_inventory_text(inv: Dict[str, Any]) -> str:
    lines = [
        "## 会话概况（Inventory）",
        f"会话数: {inv.get('conversation_count', 0)}",
        "",
        "| # | 名称 | 类型 | 消息(有效) | 发言人 | 时段 | 分享/卡片 |",
        "|---|------|------|------------|--------|------|-----------|",
    ]
    rows = inv.get("conversations") or []
    for r in rows:
        lines.append(
            f"| {r['index']} | {r['name'][:24]} | {r['type']} | {r['messages_kept']} | "
            f"{r['unique_senders']} | {r.get('date_start','') or '-'}→{r.get('date_end','') or '-'} | {r['share_like_messages']} |"
        )
    lines.append("")
    lines.append("### Top 发言人（按会话）")
    for r in rows:
        tops = ", ".join(f"{t['name']}({t['count']})" for t in (r.get("top_senders") or [])[:6])
        lines.append(f"- #{r['index']} {r['name']}: {tops or '—'}")
    lines.append("")
    lines.append(f"**下一步:** {inv.get('next_step')}")
    if rows:
        n = rows[0]["index"]
        lines.append(f"CLI 示例: python3 scripts/run.py -i <导出路径> --conv {n}")
        lines.append(f"只看某人: python3 scripts/run.py -i <导出路径> --conv {n} --person <昵称>")
        lines.append("群主别名（需求墙降权）: 加 --owner-alias '群主昵称'")
    lines.append("无导出文件? 见 references/how-to-get-exports.md（可选第三方，非本 skill 依赖）")
    share_total = sum(int(r.get("share_like_messages") or 0) for r in rows)
    if share_total > 0:
        lines.append(
            f"提示: 概况含分享/卡片类消息约 {share_total} 条。文字分析不需要百炼；"
            "若要对其中抖音链接做转写，见 references/optional-douyin-link-asr.md（可选端口，不强制）。"
        )
    return "\n".join(lines) + "\n"


def resolve_target(
    convs: List[Conversation],
    *,
    conv: Optional[str] = None,
    person: Optional[str] = None,
) -> Conversation:
    if not convs:
        raise ValueError("没有会话可解析")
    if conv is None or str(conv).strip() == "":
        raise ValueError(
            "未指定会话。请先看 inventory，再用 --conv <编号或名称>。"
            "禁止默认深挖最大群。"
        )
    key = str(conv).strip()
    # numeric index
    if key.isdigit():
        idx = int(key)
        if idx < 1 or idx > len(convs):
            raise ValueError(f"会话编号越界: {idx}（共 {len(convs)}）")
        return convs[idx - 1]
    # #1 style
    if key.startswith("#") and key[1:].isdigit():
        return resolve_target(convs, conv=key[1:], person=person)
    # name / id fuzzy
    key_l = key.lower()
    hits = []
    for c in convs:
        if key_l == c.conversation_id.lower() or key_l == c.name.lower():
            hits.append(c)
        elif key_l in c.name.lower() or key_l in c.conversation_id.lower():
            hits.append(c)
    if len(hits) == 1:
        return hits[0]
    if not hits:
        names = ", ".join(f"#{i+1}:{c.name}" for i, c in enumerate(convs)[:20])
        raise ValueError(f"找不到会话匹配 “{conv}”。候选: {names}")
    names = ", ".join(f"{c.name}" for c in hits[:10])
    raise ValueError(f"会话 “{conv}” 有 {len(hits)} 个匹配，请用编号: {names}")
