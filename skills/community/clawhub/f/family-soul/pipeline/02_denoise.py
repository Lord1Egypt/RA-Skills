"""
阶段2：去噪 + 分段
==================
输入：data/parsed/messages.jsonl
输出：data/denoised/chunks.jsonl
      每行是一个对话块：{"chunk_id": int, "messages": [...], "participants": [...]}

策略：
  - 过滤掉过短、重复、纯表情的消息
  - 按时间间隔（CONVERSATION_GAP_MINUTES）分割对话
  - 过滤掉少于 MIN_CHUNK_TURNS 条的块（太短，信息量不够）
  - 如果对话块太长，按 CHUNK_SIZE_TURNS 切分（保证 LLM 上下文安全）
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    CHUNK_SIZE_TURNS, CONVERSATION_GAP_MINUTES,
    DATA_DIR, MIN_MSG_LENGTH,
)
from utils import load_jsonl, print_step, save_jsonl

# 纯表情/符号正则
_EMOJI_RE = re.compile(
    r"^[\U00010000-\U0010ffff\u2600-\u27FF\u2B50\u2B55\uFE00-\uFE0F"
    r"\u200d\u20d0-\u20ff\uff00-\uffef\s\[\]【】「」『』（）！…、。，？！·]+$",
    re.UNICODE,
)

# 常见系统提示词
_SYSTEM_MSGS = {
    "你已退出该群聊", "撤回了一条消息", "邀请加入了群聊", "修改了群名",
    "开启了新的聊天", "[系统消息]", "已成为新群主",
}


def is_noise(content: str) -> bool:
    if len(content) < MIN_MSG_LENGTH:
        return True
    if _EMOJI_RE.match(content):
        return True
    for sys_msg in _SYSTEM_MSGS:
        if sys_msg in content:
            return True
    return False


def parse_ts(ts_str: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(ts_str.strip()[:19], fmt)
        except ValueError:
            pass
    return datetime.min


def split_into_conversations(messages: list[dict]) -> list[list[dict]]:
    """按时间间隔分割对话"""
    if not messages:
        return []
    gap = timedelta(minutes=CONVERSATION_GAP_MINUTES)
    convs: list[list[dict]] = []
    current: list[dict] = [messages[0]]
    prev_dt = parse_ts(messages[0]["timestamp"])

    for msg in messages[1:]:
        dt = parse_ts(msg["timestamp"])
        if dt - prev_dt > gap:
            convs.append(current)
            current = [msg]
        else:
            current.append(msg)
        prev_dt = dt

    if current:
        convs.append(current)
    return convs


def chunk_conversation(conv: list[dict]) -> list[list[dict]]:
    """把单段对话切成不超过 CHUNK_SIZE_TURNS 条的小块"""
    if len(conv) <= CHUNK_SIZE_TURNS:
        return [conv]
    chunks = []
    for i in range(0, len(conv), CHUNK_SIZE_TURNS):
        chunks.append(conv[i : i + CHUNK_SIZE_TURNS])
    return chunks


def format_chunk_text(msgs: list[dict]) -> str:
    """把消息列表格式化成 LLM 可读的纯文本"""
    lines = []
    for m in msgs:
        role = m.get("role", "unknown")
        display_map = {"dad": "爸爸", "mom": "妈妈", "son": "孩子", "child": "孩子", "unknown": m["sender"]}
        speaker = display_map.get(role, m["sender"])
        lines.append(f"[{m['timestamp'][:16]}] {speaker}: {m['content']}")
    return "\n".join(lines)


def main():
    print_step(2, "去噪 + 对话分段")
    messages = load_jsonl(DATA_DIR / "parsed" / "messages.jsonl")
    print(f"  读入 {len(messages):,} 条消息")

    # 过滤噪声
    clean = [m for m in messages if not is_noise(m["content"])]
    print(f"  过滤后剩余 {len(clean):,} 条（去掉 {len(messages)-len(clean):,} 条噪声）")

    # 去重（连续相同内容）
    deduped = [clean[0]] if clean else []
    for m in clean[1:]:
        if m["content"] != deduped[-1]["content"]:
            deduped.append(m)
    print(f"  去重后剩余 {len(deduped):,} 条")

    # 分割对话
    conversations = split_into_conversations(deduped)
    print(f"  分割出 {len(conversations):,} 段对话（间隔 {CONVERSATION_GAP_MINUTES} 分钟）")

    # 切分 + 过滤过短的块
    MIN_CHUNK_TURNS = 6
    chunks = []
    for conv in conversations:
        for chunk in chunk_conversation(conv):
            roles_present = {m.get("role") for m in chunk}
            # 至少要有两个角色参与，才有家庭互动价值
            known_roles = roles_present - {"unknown"}
            if len(known_roles) < 2:
                continue
            if len(chunk) < MIN_CHUNK_TURNS:
                continue
            chunks.append(chunk)

    print(f"  有效对话块：{len(chunks):,} 个")

    # 统计覆盖时间范围
    all_ts = [m["timestamp"] for chunk in chunks for m in chunk]
    if all_ts:
        print(f"  时间范围：{min(all_ts)[:10]}  →  {max(all_ts)[:10]}")

    # 保存
    records = []
    for i, chunk in enumerate(chunks):
        records.append({
            "chunk_id": i,
            "start_time": chunk[0]["timestamp"][:16],
            "end_time": chunk[-1]["timestamp"][:16],
            "turn_count": len(chunk),
            "participants": sorted({m.get("role", "unknown") for m in chunk}),
            "messages": chunk,
            "text": format_chunk_text(chunk),
        })

    save_jsonl(records, DATA_DIR / "denoised" / "chunks.jsonl")


if __name__ == "__main__":
    main()
