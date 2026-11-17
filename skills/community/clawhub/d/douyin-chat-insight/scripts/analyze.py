"""Heuristic deep-analyze → 4-block evidence pack + draft report data."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

from core import redact_path
from load_export import Conversation, Message, filter_messages
from inventory import _fmt_ts

DEMAND_RE = re.compile(
    r"(吗\？|\?|？|怎么|如何|求|有没有|哪[里个]|能不能|可不可以|教程|资料|链接|打不开|失败|报错|不会|求助|想要|需要)"
)
FACT_HINT_RE = re.compile(
    r"(github|gitee|公众号|价格|￥|\$|免费|收费|api|key|docker|skill|clawhub|hermes|openclaw|"
    r"whisper|百炼|模型|token|限时|群公告|置顶|v\d+\.\d+)",
    re.I,
)
URL_RE = re.compile(r"https?://\S+")

# polarity pairs for soft contradiction mining

DOUYIN_LINK_RE = re.compile(
    r"(https?://)?(v\.douyin\.com/\S+|www\.douyin\.com/\S+|www\.iesdouyin\.com/\S+)",
    re.I,
)


def _collect_douyin_links(msgs: List[Message], limit: int = 12) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen = set()
    for m in msgs:
        c = m.content or ""
        for match in DOUYIN_LINK_RE.finditer(c):
            url = match.group(0)
            if not url.startswith("http"):
                url = "https://" + url
            # trim trailing punctuation
            url = url.rstrip(")。,]\}'\"")
            key = url.split("?")[0]
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "url": url[:300],
                    "sender": m.sender_name,
                    "ts": _fmt_ts(m.ts),
                    "msg_ref": f"msg:{m.raw_id}" if m.raw_id else "",
                }
            )
            if len(out) >= limit:
                return out
        if m.is_share_like and ("douyin" in c.lower() or "抖音" in c) and not DOUYIN_LINK_RE.search(c):
            sig = (m.sender_name, (c or "")[:80])
            if sig in seen:
                continue
            seen.add(sig)
            out.append(
                {
                    "url": "",
                    "note": "share_like_without_plain_url",
                    "sender": m.sender_name,
                    "ts": _fmt_ts(m.ts),
                    "snippet": (c or "")[:120],
                    "msg_ref": f"msg:{m.raw_id}" if m.raw_id else "",
                }
            )
            if len(out) >= limit:
                return out
    return out


def _optional_enhancements(msgs: List[Message], share_n: int) -> Dict[str, Any]:
    """Port for optional Douyin-link ASR — guidance only, never calls cloud."""
    import os
    links = _collect_douyin_links(msgs)
    key_present = bool(os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("BAILIAN_API_KEY"))
    relevant = bool(links) or share_n > 0
    return {
        "douyin_links_detected": len(links),
        "share_like_messages": share_n,
        "sample_links": links[:8],
        "cloud_asr_required_for_core": False,
        "dashscope_key_present": key_present,
        "status": (
            "idle_no_links"
            if not relevant
            else ("ready_optional" if key_present else "guidance_available")
        ),
        "user_guidance_zh": (
            "未发现明显抖音链接/分享卡片；文字四块分析无需百炼 Key。"
            if not relevant
            else (
                "检测到分享类消息或抖音链接。核心文字报告不需要阿里百炼；"
                "若你要对链接做语音转写/单条视频分析，见 references/optional-douyin-link-asr.md。"
                + (" 本机已探测到 DASHSCOPE/BAILIAN 环境变量（仅状态，本 run 未调用云 ASR）。" if key_present else " 本机未检测到 DASHSCOPE_API_KEY；无 Key 也可先读文字报告，需要转写时再按该文档配置。")
            )
        ),
        "guide_path": "references/optional-douyin-link-asr.md",
        "routes": {
            "homepage": "douyin-creator-insight",
            "batch_video": "douyin-video-analyst / douyin-workflow",
            "single_link_asr": "optional local Whisper or DASHSCOPE_API_KEY + video skill",
        },
    }


POLAR_PAIRS = [
    (re.compile(r"免费"), re.compile(r"(收费|付费|订阅|买断)")),
    (re.compile(r"(能用|可以|没问题|支持)"), re.compile(r"(不能|无法|不支持|打不开|失败)")),
    (re.compile(r"(本地|开源)"), re.compile(r"(云端|闭源|必须.?key)")),
    (re.compile(r"(简单|一键)"), re.compile(r"(复杂|要配置|手动)")),
]


def analyze_conversation(
    conv: Conversation,
    cfg: dict,
    *,
    person: Optional[str] = None,
) -> Dict[str, Any]:
    filt = cfg.get("filters") or {}
    lim = cfg.get("limits") or {}
    owners = {str(x).lower() for x in (cfg.get("owner_aliases") or []) if x}
    # auto-detect likely owner = top sender if aliases empty
    msgs_all = filter_messages(conv.messages, drop_system=bool(filt.get("drop_system", True)))
    if not msgs_all:
        raise ValueError("过滤后无消息可分析（可能全是系统消息）")
    sender_counts = Counter(m.sender_name for m in msgs_all)
    auto_owner = sender_counts.most_common(1)[0][0].lower() if sender_counts else ""
    if not owners and auto_owner:
        owners.add(auto_owner)

    msgs = filter_messages(msgs_all, drop_system=False, person=person) if person else msgs_all
    if person and not msgs:
        raise ValueError(f"在会话中找不到人物匹配: {person}")

    min_demand = int(filt.get("min_demand_chars", 15))
    demand_wall = _build_demand_wall(msgs, owners, min_demand, int(lim.get("demand_wall", 24)))
    hard_facts = _build_hard_facts(msgs, owners, int(lim.get("hard_fact_candidates", 12)))
    contradictions = _build_contradictions(msgs, int(lim.get("contradiction_pairs", 8)))
    actions = _build_actions(demand_wall, contradictions, hard_facts)

    prose = [m for m in msgs if not m.is_share_like and not m.is_system and (m.content or "").strip()]
    share = [m for m in msgs if m.is_share_like]
    opt = _optional_enhancements(msgs, len(share))

    return {
        "status": "deep_analyze",
        "conversation": {
            "id": conv.conversation_id,
            "name": conv.name,
            "type": conv.conv_type,
            "platform": conv.platform,
            "source_path": redact_path(conv.source_path),
        },
        "scope": {
            "person_filter": person,
            "messages_analyzed": len(msgs),
            "prose_messages": len(prose),
            "share_like_messages": len(share),
            "owner_aliases_used": sorted(owners),
            "unique_senders": len({m.sender_name for m in msgs}),
            "date_start": _fmt_ts(min((m.ts for m in msgs if m.ts), default=None)),
            "date_end": _fmt_ts(max((m.ts for m in msgs if m.ts), default=None)),
        },
        "blocks": {
            "hard_facts": hard_facts,
            "open_contradictions": contradictions,
            "demand_quotes": demand_wall,
            "actions": actions,
        },
        "meta": {
            "generator": "douyin-chat-insight",
            "version": "0.1.1",
            "mode": "heuristic_draft",
            "note": (
                "本报告为可复现启发式草稿 + 证据包。Agent/人工应按 references/report-4block.md "
                "做 chat-first 终审：删分享刷榜、闭合已解决矛盾、动作必须指回原话。"
            ),
        },
        "optional_enhancements": opt,
        "quality_checklist": [
            "是否 chat-first（分享文案未刷高分）",
            "未闭合问题是否标清（无圆场）",
            "需求墙是否以非博主/非群主为主",
            "动作是否条条指回事实/矛盾/原话",
            "是否单页、无重复叙事",
        ],
    }


def _clip(s: str, n: int = 160) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def _build_demand_wall(
    msgs: List[Message],
    owners: set,
    min_chars: int,
    limit: int,
) -> List[Dict[str, Any]]:
    out = []
    for m in msgs:
        if m.is_system or m.is_share_like:
            continue
        c = (m.content or "").strip()
        if len(c) < min_chars:
            continue
        if m.sender_name.lower() in owners or m.sender_id.lower() in owners:
            continue
        if not DEMAND_RE.search(c):
            continue
        # skip pure urls
        if URL_RE.fullmatch(c):
            continue
        out.append(
            {
                "sender": m.sender_name,
                "ts": _fmt_ts(m.ts),
                "quote": _clip(c, 200),
                "msg_id": m.raw_id,
            }
        )
    # prefer unique quotes
    seen = set()
    uniq = []
    for item in out:
        k = item["quote"]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(item)
    return uniq[:limit]


def _build_hard_facts(msgs: List[Message], owners: set, limit: int) -> List[Dict[str, Any]]:
    cands = []
    for m in msgs:
        if m.is_system:
            continue
        c = (m.content or "").strip()
        if len(c) < 10:
            continue
        if m.is_share_like and not FACT_HINT_RE.search(c):
            continue
        score = 0
        if FACT_HINT_RE.search(c):
            score += 3
        if URL_RE.search(c) and len(URL_RE.sub("", c).strip()) >= 8:
            score += 1
        if any(x in c for x in ("注意", "不要", "必须", "默认", "目前", "已经")):
            score += 1
        if m.sender_name.lower() in owners:
            score += 1  # host statements can be facts but not demand
        if score <= 0:
            continue
        # downrank pure promo short
        if len(c) < 20 and m.sender_name.lower() in owners:
            score -= 1
        cands.append((score, m))
    cands.sort(key=lambda x: (-x[0], -(x[1].ts or 0)))
    out = []
    seen = set()
    for score, m in cands:
        q = _clip(m.content, 180)
        if q in seen:
            continue
        seen.add(q)
        out.append(
            {
                "fact": q,
                "sender": m.sender_name,
                "ts": _fmt_ts(m.ts),
                "evidence": q,
                "score": score,
                "msg_id": m.raw_id,
            }
        )
        if len(out) >= limit:
            break
    return out


def _build_contradictions(msgs: List[Message], limit: int) -> List[Dict[str, Any]]:
    buckets: Dict[str, List[Message]] = defaultdict(list)
    for m in msgs:
        if m.is_system or m.is_share_like:
            continue
        c = m.content or ""
        for i, (pos, neg) in enumerate(POLAR_PAIRS):
            if pos.search(c) or neg.search(c):
                buckets[str(i)].append(m)
    out = []
    for i, (pos, neg) in enumerate(POLAR_PAIRS):
        arr = buckets.get(str(i)) or []
        pos_msgs = [m for m in arr if pos.search(m.content or "")]
        neg_msgs = [m for m in arr if neg.search(m.content or "")]
        if not pos_msgs or not neg_msgs:
            continue
        # Prefer different senders (avoid same person "本地可用/云端也行" false positives)
        pair = None
        for a in pos_msgs:
            for b in neg_msgs:
                if a.sender_name != b.sender_name or a is not b:
                    if a.sender_name != b.sender_name:
                        pair = (a, b)
                        break
            if pair:
                break
        if not pair:
            continue  # only same-sender polarity — skip as contradiction
        a, b = pair
        out.append(
            {
                "theme": f"极性对 #{i+1}: {pos.pattern} vs {neg.pattern}",
                "side_a": {"sender": a.sender_name, "quote": _clip(a.content), "ts": _fmt_ts(a.ts), "msg_id": a.raw_id},
                "side_b": {"sender": b.sender_name, "quote": _clip(b.content), "ts": _fmt_ts(b.ts), "msg_id": b.raw_id},
                "status": "unresolved_candidate",
                "note": "启发式候选；终审时若上下文已闭合请删除或标 resolved",
            }
        )
        if len(out) >= limit:
            break
    # also: repeated unanswered questions
    q_counts = Counter()
    q_ex = {}
    for m in msgs:
        if m.is_system or m.is_share_like:
            continue
        c = (m.content or "").strip()
        if "？" in c or "?" in c:
            key = _clip(c, 80)
            q_counts[key] += 1
            q_ex[key] = m
    for key, cnt in q_counts.most_common(5):
        if cnt < 2:
            continue
        m = q_ex[key]
        out.append(
            {
                "theme": "重复提问未收敛",
                "side_a": {"sender": m.sender_name, "quote": key, "ts": _fmt_ts(m.ts)},
                "side_b": {"sender": "—", "quote": f"同义/相同问题出现 {cnt} 次", "ts": ""},
                "status": "unresolved_candidate",
                "note": "需人工确认是否已被群公告/后续回复闭合",
            }
        )
        if len(out) >= limit:
            break
    return out[:limit]


def _build_actions(
    demand: List[dict],
    contradictions: List[dict],
    facts: List[dict],
) -> List[Dict[str, Any]]:
    actions = []
    # From top demands
    for d in demand[:5]:
        mid = d.get("msg_id") or ""
        ref = f"msg:{mid}" if mid else f"demand:{d['sender']}:{d.get('ts','')}"
        actions.append(
            {
                "action": f"针对「{_clip(d['quote'], 40)}」补一份可执行说明或置顶答复",
                "why": "需求墙高频/明确提问",
                "refs": [ref],
                "priority": "P1",
            }
        )
        if len(actions) >= 3:
            break
    for c in contradictions[:3]:
        if len(actions) >= 5:
            break
        sa = (c.get("side_a") or {}).get("msg_id") or ""
        sb = (c.get("side_b") or {}).get("msg_id") or ""
        refs = [x for x in (f"msg:{sa}" if sa else "", f"msg:{sb}" if sb else "") if x]
        if not refs:
            refs = ["contradiction:side_a", "contradiction:side_b"]
        actions.append(
            {
                "action": f"澄清矛盾主题：{c.get('theme','')[:40]}（给出唯一官方口径）",
                "why": "未闭合矛盾会造成反复提问与信任损耗",
                "refs": refs,
                "priority": "P0",
            }
        )
    if not actions and facts:
        mid = facts[0].get("msg_id") or ""
        actions.append(
            {
                "action": "把硬事实区的关键链接/步骤整理成单页 FAQ 置顶",
                "why": "已有事实散落在对话中",
                "refs": [f"msg:{mid}" if mid else f"fact:{facts[0].get('sender')}"],
                "priority": "P2",
            }
        )
    # ensure max 5
    return actions[:5]
