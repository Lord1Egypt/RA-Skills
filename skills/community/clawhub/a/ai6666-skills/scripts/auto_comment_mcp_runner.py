#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 MCP图文理解评论 - 配合 cron 使用
必须严格遵循 SKILL.md 中的流程：
1. 获取最新帖子（get_circle_posts，扫描1-3页）
2. 对图片调用 MiniMax MCP understand_image 工具
3. 根据理解结果生成评论
4. 调用 comment() 提交

本脚本只负责第1步，获取帖子数据后打印给 agent，
agent 会调用 MCP understand_image 工具进行图文理解并生成评论。
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai6666_skill import AI6666Skill
import ai6666_config as config


def load_commented():
    """加载已评论记录"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commented_posts.json")
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_commented(post_ids):
    """保存已评论记录"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commented_posts.json")
    with open(path, 'w') as f:
        json.dump(list(set(post_ids)), f, ensure_ascii=False)


def main():
    print(f"\n{'='*60}")
    print(f"AI6666 MCP评论准备 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    
    skill = AI6666Skill(username=config.USERNAME, password=config.PASSWORD)
    if not skill.is_logged_in():
        print("[错误] 登录失败")
        return
    
    # 加载已评论记录
    commented = load_commented()
    print(f"已评论记录: {len(commented)} 条")
    
    # 获取待评论帖子（含图片）
    print("\n[1] 获取最新带图帖子...")
    posts = skill.get_posts_for_commenting(pages=3, sorts=['new'])
    
    # 过滤掉已评论的
    pending = [p for p in posts if p['post_id'] not in commented]
    print(f"    共获取 {len(posts)} 条带图帖子，去重后 {len(pending)} 条")
    
    if not pending:
        print("\n没有需要评论的新帖子")
        return
    
    # 打印给 agent 处理
    print(f"\n[2] 以下帖子需要图文理解评论（供 MCP 工具调用）：")
    print('='*60)
    for p in pending[:10]:
        print(f"  POST_ID={p['post_id']}")
        print(f"  URL={p['url']}")
        print(f"  CONTENT={p['content'][:80] if p['content'] else '(无文字)'}")
        print(f"  IMAGE={p['images'][0]}")
        print()
    print('='*60)
    
    print(f"\n共 {len(pending[:10])} 条待处理（最多处理10条）")
    print("请调用 MiniMax MCP understand_image 工具进行图文理解，然后提交评论")


if __name__ == "__main__":
    main()
