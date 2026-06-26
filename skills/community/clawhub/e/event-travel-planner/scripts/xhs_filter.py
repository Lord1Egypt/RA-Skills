#!/usr/bin/env python3
"""
xhs_filter.py — 精简 xhs-cli JSON 输出，只保留 AI 决策所需的关键字段。

用法（通过管道接收 xhs-cli 的 --json 输出）：
    xhs search "关键词" --json | python3 xhs_filter.py search
    xhs read 1 --json | python3 xhs_filter.py read
    xhs comments 1 --json | python3 xhs_filter.py comments

输出为精简的纯文本，方便 AI 直接阅读和判断。
"""

import json
import sys
from datetime import datetime


def ms_to_date(ms):
    """Unix 毫秒时间戳 → YYYY-MM-DD"""
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(int(ms) / 1000).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return None


def filter_search(data):
    """精简搜索结果：只保留索引、标题、发布时间、互动数据"""
    items = data.get("items", [])
    if not items:
        print("无搜索结果")
        return

    print(f"共 {len(items)} 条结果：")
    print()
    for i, item in enumerate(items, 1):
        card = item.get("note_card", {})
        interact = card.get("interact_info", {})

        # 提取发布时间
        publish_time = ""
        for tag in card.get("corner_tag_info", []):
            if tag.get("type") == "publish_time":
                publish_time = tag.get("text", "")
                break

        title = card.get("display_title", "无标题")
        note_type = "图文" if card.get("type") == "normal" else "视频"
        collected = interact.get("collected_count", "0")
        liked = interact.get("liked_count", "0")
        comments = interact.get("comment_count", "0")

        print(f"[{i}] {title}")
        print(f"    发布: {publish_time} | 类型: {note_type} | 收藏: {collected} | 点赞: {liked} | 评论: {comments}")
        print()


def filter_read(data):
    """精简笔记详情：只保留标题、发布时间、正文字数和正文内容"""
    # read 的 JSON 结构：data.items[0].note_card 包含笔记字段
    note = data
    items = data.get("items", [])
    if items:
        note = items[0].get("note_card", items[0])

    title = note.get("title", "无标题")
    desc = note.get("desc", "")
    time_str = ms_to_date(note.get("time"))
    update_str = ms_to_date(note.get("last_update_time"))

    print(f"标题: {title}")
    if time_str:
        print(f"发布: {time_str}", end="")
        if update_str and update_str != time_str:
            print(f" | 更新: {update_str}", end="")
        print()
    print(f"正文字数: {len(desc)}")
    print()
    if desc:
        print(desc)
    else:
        print("（正文为空，内容可能在图片中）")


def filter_comments(data):
    """精简评论：只保留评论内容和点赞数"""
    comments = data.get("comments", [])
    if not comments:
        print("无评论")
        return

    total = data.get("total_fetched", len(comments))
    print(f"共 {total} 条评论：")
    print()
    for c in comments:
        nickname = c.get("user_info", {}).get("nickname", "匿名")
        content = c.get("content", "").strip()
        like_count = c.get("like_count", "0")
        if content:
            print(f"[赞 {like_count}] {nickname}: {content}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("用法: xhs <command> --json | python3 xhs_filter.py <search|read|comments>")
        print("精简 xhs-cli 输出，只保留 AI 决策所需的关键字段。")
        sys.exit(0)

    mode = sys.argv[1]
    if mode not in ("search", "read", "comments"):
        print(f"未知模式: {mode}（支持 search / read / comments）", file=sys.stderr)
        sys.exit(1)

    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 检查 xhs-cli 是否返回错误
    if raw.get("ok") is False:
        error = raw.get("error", {})
        print(f"错误: [{error.get('code', 'unknown')}] {error.get('message', '')}", file=sys.stderr)
        sys.exit(1)

    data = raw.get("data", raw)

    filters = {"search": filter_search, "read": filter_read, "comments": filter_comments}
    filters[mode](data)


if __name__ == "__main__":
    main()
