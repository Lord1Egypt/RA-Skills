#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 自动评论脚本
Python 管"手脚"：接收 post_id + 评论内容，执行提交
agent 管"大脑"：图文理解 + 评论内容生成由 agent 通过 MCP 完成

⚠️ MCP 图文理解超时处理：
    MiniMax MCP understand_image 偶尔会超时（32001 错误），遇到时建议重试 1-2 次，
    通常第二次会成功。同一张图的多次调用结果稳定，不影响评论质量。

    **ai6666.com URL 访问失败**：MCP 工具访问 ai6666.com 图片 URL 时可能报 "Not connected" 或
    "Connection closed"，这是因为 ai6666.com 不允许外部图片抓取（防盗链）。
    **解法**：使用 `--download <post_id>` 先把图片下载到本地，再用 `image` 工具分析本地文件。

使用方法:
    # 评论（agent 生成内容后调用）
    python3 auto_comment_runner.py --comment "12345" "评论内容..."

    # 获取待评论帖子列表（供 agent 理解图片用）
    python3 auto_comment_runner.py --fetch 3

    # 检查帖子详情
    python3 auto_comment_runner.py --info "12345"

    # 下载帖子图片到本地（当 MCP URL 访问失败时使用）
    python3 auto_comment_runner.py --download "12345"
"""

import sys
import os
import json
import shutil
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai6666_skill import AI6666Skill
import ai6666_config as config


def load_commented():
    """加载已评论记录，支持列表格式和字典格式。"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commented_posts.json")
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            # 兼容旧版列表格式，转换为字典
            if isinstance(data, list):
                return {pid: {"time": "", "comment": ""} for pid in data}
            return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}


def save_commented(commented_dict):
    """保存已评论记录（字典格式）。"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commented_posts.json")
    with open(path, 'w') as f:
        json.dump(commented_dict, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='AI6666 评论脚本（Python 管手脚，agent 管大脑）')
    parser.add_argument('--comment', nargs='+', help='评论：post_id 评论内容')
    parser.add_argument('--fetch', type=int, nargs='?', const=3, default=0, help='获取待评论帖子列表（默认3页）')
    parser.add_argument('--info', type=str, help='查看帖子详情')
    parser.add_argument('--list-commented', action='store_true', help='查看已评论列表')
    parser.add_argument('--download', type=str, help='下载指定帖子的图片到本地（当 MCP URL 访问失败时使用）')

    args = parser.parse_args()
    skill = AI6666Skill(username=config.USERNAME, password=config.PASSWORD)

    if not skill.is_logged_in():
        print("[提示] 未登录，自动尝试登录...")
        if skill.login(config.USERNAME, config.PASSWORD):
            print("[成功] 登录成功！")
        else:
            print("[错误] 登录失败")
            sys.exit(1)

    # -------- 评论 --------
    if args.comment:
        post_id = args.comment[0]
        comment = ' '.join(args.comment[1:])
        if not comment:
            print("[错误] 评论内容不能为空")
            sys.exit(1)

        print(f"评论帖子 {post_id}: {comment[:50]}{'...' if len(comment) > 50 else ''}")
        result = skill.comment(post_id, comment)

        # 评论 403 时自动重登录重试
        if not result.get('success') and '403' in str(result.get('message', '')):
            print("[提示] 评论 403（session 可能过期），自动重新登录...")
            if skill.login(config.USERNAME, config.PASSWORD):
                result = skill.comment(post_id, comment)

        if result.get('success'):
            commented = load_commented()
            commented[post_id] = {"time": "", "comment": comment[:50]}
            save_commented(commented)
            print(f"✓ 评论成功!")
        else:
            print(f"✗ 失败: {result.get('message')}")
            sys.exit(1)
        sys.exit(0)

    # -------- 下载帖子图片（当 MCP URL 访问失败时使用）--------
    if args.download:
        import requests
        pid = args.download
        # 优先从 get_posts_for_commenting 拿（已去重），没有则查详情
        posts = skill.get_posts_for_commenting(pages=1)
        target = next((p for p in posts if str(p['post_id']) == str(pid)), None)
        if not target:
            target = skill.get_post_details(pid)
        if not target:
            print(f"[错误] 帖子 {pid} 不存在")
            sys.exit(1)
        images = target.get('images') or []
        if not images:
            print(f"帖子 {pid} 无图片")
            sys.exit(0)
        saved = []
        for i, url in enumerate(images):
            try:
                r = requests.get(url, timeout=15)
                local_path = f"/tmp/ai6666_img_{pid}_{i}.jpg"
                with open(local_path, 'wb') as f:
                    f.write(r.content)
                # image 工具要求文件在 workspace 目录
                ws_dir = os.path.expanduser("~/.openclaw/workspace/tmp")
                os.makedirs(ws_dir, exist_ok=True)
                ws_path = os.path.join(ws_dir, f"img_{pid}_{i}.jpg")
                shutil.copy(local_path, ws_path)
                saved.append((local_path, ws_path))
                print(f"✓ [{i+1}] {ws_path} ({len(r.content)//1024}KB)")
            except Exception as e:
                print(f"✗ [{i+1}] 下载失败: {e}")
        if saved:
            print(f"\n本地路径（供 image 工具分析）:")
            for _, ws in saved:
                print(f"  {ws}")
        sys.exit(0)

    # -------- 获取待评论帖子 --------
    if args.fetch > 0:
        print(f"\n{'='*60}")
        print(f"获取待评论帖子 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print('='*60)
        posts = skill.get_posts_for_commenting(pages=args.fetch)
        commented = load_commented()
        pending = [p for p in posts if str(p['post_id']) not in [str(x) for x in commented]]
        print(f"总帖子: {len(posts)} 条，已评论: {len(commented)} 条，待评论: {len(pending)} 条\n")
        for p in pending[:10]:
            pid = p['post_id']
            content = p.get('content', '') or ''
            images = p.get('images', []) or []
            print(f"  [{pid}] {content[:40]}{'...' if len(content) > 40 else ''}")
            print(f"    图片数量: {len(images)}")
            for i, img_url in enumerate(images):
                print(f"    [{i+1}] {img_url}")
            print()
        print(f"可评论: {len(pending)} 条")
        sys.exit(0)

    # -------- 查看帖子详情 --------
    if args.info:
        details = skill.get_post_details(args.info)
        if details:
            print(f"\n帖子 {args.info}:")
            print(f"  内容: {details.get('content', '')}")
            print(f"  图片: {details.get('images', [])}")
        else:
            print(f"✗ 帖子不存在或获取失败")
            sys.exit(1)
        sys.exit(0)

    # -------- 已评论列表 --------
    if args.list_commented:
        commented = load_commented()
        print(f"已评论: {len(commented)} 条")
        for pid in commented[-20:]:
            print(f"  - {pid}")
        sys.exit(0)

    # 无参数
    parser.print_help()
    print("\n示例:")
    print("  python3 auto_comment_runner.py --comment \"12345\" \"好美啊...忍不住多看两眼💕\"")
    print("  python3 auto_comment_runner.py --fetch 3")
    print("  python3 auto_comment_runner.py --info \"12345\"")
    print("  python3 auto_comment_runner.py --download \"12345\"")


if __name__ == "__main__":
    main()
