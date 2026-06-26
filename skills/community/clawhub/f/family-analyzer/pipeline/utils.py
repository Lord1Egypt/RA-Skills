"""共享工具函数"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def save_jsonl(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  ✓ 写入 {len(records)} 条 → {path}")


def save_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  ✓ 写入 → {path}")


def iter_chunks(lst: list, size: int) -> Iterator[list]:
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def normalize_timestamp(ts: Any) -> str:
    """将各种时间格式统一为 ISO8601 字符串"""
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts).isoformat(sep=" ")
    if isinstance(ts, str):
        # 尝试常见格式
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ):
            try:
                return datetime.strptime(ts.strip(), fmt).isoformat(sep=" ")
            except ValueError:
                pass
        return ts  # 保留原始字符串
    return str(ts)


def resolve_role(sender: str, speakers: dict) -> str:
    """将发送者名字映射到 dad/mom/son/unknown"""
    # 精确匹配
    if sender in speakers:
        return speakers[sender]["role"]
    # 包含匹配（处理微信在名字后加群昵称的情况）
    for name, info in speakers.items():
        if name in sender or sender in name:
            return info["role"]
    return "unknown"


def print_step(n: int, title: str) -> None:
    bar = "─" * 60
    print(f"\n{bar}")
    print(f"  阶段 {n}：{title}")
    print(bar)
