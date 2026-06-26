"""
阶段1：解析微信导出文件
======================
输入：data/raw/ 下的导出文件（CSV / TXT / JSON）
输出：data/parsed/messages.jsonl
      每行格式：{"id": int, "timestamp": "ISO", "sender": str, "role": str, "content": str}
"""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# 将 pipeline/ 加入路径
sys.path.insert(0, str(Path(__file__).parent))
import chardet
from config import (
    BATCH_SIZE, CSV_COLUMNS, DATA_DIR, EXPORT_FORMAT,
    MIN_MSG_LENGTH, SKIP_MSG_TYPES, SPEAKERS,
)
from utils import normalize_timestamp, print_step, resolve_role, save_jsonl


def detect_encoding(path: Path) -> str:
    with open(path, "rb") as f:
        raw = f.read(65536)
    result = chardet.detect(raw)
    return result.get("encoding") or "utf-8"


# ── 格式1：WeChatMsg CSV ───────────────────────────────────────────────────────
def parse_wechatmsg_csv(files: list[Path]) -> list[dict]:
    messages = []
    ts_col = CSV_COLUMNS["timestamp"]
    sender_col = CSV_COLUMNS["sender"]
    content_col = CSV_COLUMNS["content"]
    type_col = CSV_COLUMNS["type"]

    for path in files:
        enc = detect_encoding(path)
        with open(path, encoding=enc, errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg_type = row.get(type_col, "Text")
                if msg_type in SKIP_MSG_TYPES:
                    continue
                content = (row.get(content_col) or "").strip()
                if not content or len(content) < MIN_MSG_LENGTH:
                    continue
                sender = (row.get(sender_col) or "").strip()
                ts_raw = row.get(ts_col, "")
                messages.append({
                    "timestamp": normalize_timestamp(ts_raw),
                    "sender": sender,
                    "content": content,
                })

    return messages


# ── 格式2：TXT 标准格式 ────────────────────────────────────────────────────────
# 每条消息以 "YYYY-MM-DD HH:MM:SS 发送者:" 开头，内容在下一行
_TXT_HEADER = re.compile(
    r"^(\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)[\s:：]+$"
)

def parse_txt_standard(files: list[Path]) -> list[dict]:
    messages = []
    for path in files:
        enc = detect_encoding(path)
        lines = path.read_text(encoding=enc, errors="replace").splitlines()

        current_ts = None
        current_sender = None
        content_lines: list[str] = []

        def flush():
            if current_sender and content_lines:
                content = "\n".join(content_lines).strip()
                if len(content) >= MIN_MSG_LENGTH:
                    messages.append({
                        "timestamp": normalize_timestamp(current_ts),
                        "sender": current_sender,
                        "content": content,
                    })

        for line in lines:
            m = _TXT_HEADER.match(line)
            if m:
                flush()
                current_ts = m.group(1)
                current_sender = m.group(2).strip()
                content_lines = []
            else:
                stripped = line.strip()
                # 跳过媒体占位符
                if any(t in stripped for t in SKIP_MSG_TYPES):
                    continue
                if stripped:
                    content_lines.append(stripped)

        flush()  # 最后一条

    return messages


# ── 格式3：自定义 JSON ─────────────────────────────────────────────────────────
def parse_json(files: list[Path]) -> list[dict]:
    messages = []
    for path in files:
        enc = detect_encoding(path)
        data = json.loads(path.read_text(encoding=enc))
        if isinstance(data, dict):
            data = data.get("messages", [])
        for item in data:
            content = str(item.get("content", item.get("msg", ""))).strip()
            if len(content) < MIN_MSG_LENGTH:
                continue
            messages.append({
                "timestamp": normalize_timestamp(
                    item.get("timestamp", item.get("CreateTime", ""))
                ),
                "sender": str(item.get("sender", item.get("talker", ""))).strip(),
                "content": content,
            })
    return messages


# ── 格式4：WeFlow JSON ─────────────────────────────────────────────────────────
# WeFlow 是 Mac/iOS 微信导出工具，输出结构化 JSON
def parse_weflow(files: list[Path]) -> list[dict]:
    messages = []
    for path in files:
        # WeFlow 导出始终为 UTF-8（含 BOM）
        raw_bytes = path.read_bytes()
        text = raw_bytes.decode("utf-8-sig")
        data = json.loads(text)
        raw = data.get("messages", []) if isinstance(data, dict) else data
        for item in raw:
            msg_type = item.get("type", "")
            if msg_type in SKIP_MSG_TYPES:
                continue
            # 引用消息：合并回复内容和被引用内容
            if msg_type == "引用消息":
                reply = (item.get("content") or "").strip()
                quoted = (item.get("quotedContent") or "").strip()
                content = reply
                if quoted:
                    content = f"{reply}（引用：{quoted}）"
            else:
                content = (item.get("content") or "").strip()

            if len(content) < MIN_MSG_LENGTH:
                continue
            sender = (item.get("senderUsername") or "").strip()
            ts = item.get("formattedTime") or item.get("createTime") or ""
            messages.append({
                "timestamp": normalize_timestamp(ts),
                "sender": sender,
                "content": content,
            })
    return messages


# ── 主函数 ─────────────────────────────────────────────────────────────────────
PARSERS = {
    "wechatmsg_csv":  (parse_wechatmsg_csv,  [".csv"]),
    "txt_standard":   (parse_txt_standard,   [".txt"]),
    "json":           (parse_json,           [".json"]),
    "weflow":         (parse_weflow,         [".json"]),
}

def main():
    print_step(1, "解析微信导出文件")
    raw_dir = DATA_DIR / "raw"
    if not raw_dir.exists() or not any(raw_dir.iterdir()):
        print(f"\n⚠  请将微信导出文件放入：{raw_dir}")
        print("   然后在 pipeline/config.py 中设置正确的 EXPORT_FORMAT 和 SPEAKERS")
        sys.exit(1)

    if EXPORT_FORMAT not in PARSERS:
        print(f"✗ 未知格式：{EXPORT_FORMAT}")
        sys.exit(1)

    parser_fn, exts = PARSERS[EXPORT_FORMAT]
    files = [f for f in raw_dir.rglob("*") if f.suffix.lower() in exts]
    if not files:
        print(f"✗ 在 {raw_dir} 中未找到 {exts} 文件")
        sys.exit(1)

    print(f"  找到 {len(files)} 个文件，格式：{EXPORT_FORMAT}")
    messages = parser_fn(files)
    print(f"  解析出 {len(messages)} 条文本消息")

    # 附加 role 和 id
    for i, msg in enumerate(messages):
        msg["id"] = i
        msg["role"] = resolve_role(msg["sender"], SPEAKERS)

    # 按时间排序
    messages.sort(key=lambda m: m["timestamp"])

    # 统计
    from collections import Counter
    role_counts = Counter(m["role"] for m in messages)
    for role, count in sorted(role_counts.items()):
        sender_examples = set(
            m["sender"] for m in messages if m["role"] == role
        )
        print(f"  {role:10s}  {count:6,} 条  [{', '.join(sorted(sender_examples)[:3])}]")

    save_jsonl(messages, DATA_DIR / "parsed" / "messages.jsonl")


if __name__ == "__main__":
    main()
