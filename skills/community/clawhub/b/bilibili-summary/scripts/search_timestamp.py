"""
search_timestamp.py — 在 SRT 字幕文件中搜索关键词并返回时间戳

用法：
    python search_timestamp.py <srt文件路径> <关键词> [--context <前后行数>]

示例：
    python search_timestamp.py subtitles_output/BV1ZL411o7LZ/BV1ZL411o7LZ.srt "机器学习" --context 2

输出格式（逐匹配块打印）：
    [00:01:23,456 --> 00:01:26,789]
    机器学习是人工智能的重要分支...
    （上下文行）
"""

import argparse
import re
import sys


def parse_srt(filepath: str):
    """解析 SRT 文件，返回字幕块列表。

    每个字幕块包含：
        index   : 序号
        start   : 开始时间字符串（如 "00:01:23,456"）
        end     : 结束时间字符串
        text    : 字幕文本
    """
    blocks = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 按空行分割成字幕块
    raw_blocks = re.split(r"\n\s*\n", content.strip())
    for raw in raw_blocks:
        lines = raw.strip().splitlines()
        if len(lines) < 3:
            continue
        try:
            idx = int(lines[0].strip())
        except ValueError:
            continue

        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})",
            lines[1],
        )
        if not time_match:
            continue

        start, end = time_match.group(1), time_match.group(2)
        text = " ".join(lines[2:])
        blocks.append({"index": idx, "start": start, "end": end, "text": text})

    return blocks


def timestamp_to_seconds(ts: str) -> float:
    """将 SRT 时间戳（HH:MM:SS,mmm）转换为秒数。"""
    ts = ts.replace(",", ".")
    h, m, rest = ts.split(":")
    s, ms = rest.split(".")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def search(filepath: str, keyword: str, context: int = 2):
    """搜索关键词，返回匹配的字幕块（含上下文）。"""
    blocks = parse_srt(filepath)
    results = []
    matched_indices = set()

    for i, block in enumerate(blocks):
        if keyword.lower() in block["text"].lower():
            # 收集上下文范围
            start_i = max(0, i - context)
            end_i = min(len(blocks) - 1, i + context)
            for j in range(start_i, end_i + 1):
                if j not in matched_indices:
                    matched_indices.add(j)
                    results.append(
                        {
                            "is_match": j == i,
                            "index": blocks[j]["index"],
                            "start": blocks[j]["start"],
                            "end": blocks[j]["end"],
                            "text": blocks[j]["text"],
                            "start_seconds": timestamp_to_seconds(blocks[j]["start"]),
                        }
                    )

    # 按时间顺序排序
    results.sort(key=lambda x: x["start_seconds"])
    return results


def main():
    parser = argparse.ArgumentParser(description="在 SRT 文件中搜索关键词并返回时间戳")
    parser.add_argument("srt_file", help="SRT 字幕文件路径")
    parser.add_argument("keyword", help="要搜索的关键词")
    parser.add_argument("--context", type=int, default=2, help="匹配行前后显示的字幕条数（默认 2）")
    args = parser.parse_args()

    try:
        results = search(args.srt_file, args.keyword, args.context)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {args.srt_file}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print(f"未找到与「{args.keyword}」相关的字幕片段。")
        sys.exit(0)

    print(f"找到与「{args.keyword}」相关的片段，共 {sum(1 for r in results if r['is_match'])} 处匹配：\n")

    prev_end_sec = None
    for r in results:
        # 片段间插入分隔线
        if prev_end_sec is not None and r["start_seconds"] - prev_end_sec > 10:
            print("  ──────────────────────")
        marker = "► " if r["is_match"] else "  "
        print(f"{marker}[{r['start']} --> {r['end']}]  {r['text']}")
        prev_end_sec = r["start_seconds"]


if __name__ == "__main__":
    main()
