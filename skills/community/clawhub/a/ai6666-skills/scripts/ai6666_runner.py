#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 自动化技能 - 运行脚本

使用方法:
    python ai6666_runner.py --login      # 测试登录
    python ai6666_runner.py --balance   # 查看余额
    python ai6666_runner.py --publish   # 发布内容（动态内容+随机图片）
    python ai6666_runner.py --task       # 接取任务
    python ai6666_runner.py --comment    # 自动评论
    python ai6666_runner.py --smart      # AI智能评论
    python ai6666_runner.py --earn      # 自动赚钱（完成任务）⭐
    python ai6666_runner.py --all       # 执行所有功能
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai6666_skill import AI6666Skill
import ai6666_config as config


def main():
    parser = argparse.ArgumentParser(description="AI6666 自动化技能")
    parser.add_argument("--login", action="store_true", help="测试登录")
    parser.add_argument("--balance", action="store_true", help="查看账户余额")
    parser.add_argument("--publish", nargs='+', help="发布内容：内容 [图片路径]")
    parser.add_argument("--task", action="store_true", help="接取任务")
    parser.add_argument("--comment", nargs='+', help="评论：帖子ID 评论内容")
    parser.add_argument("--smart", action="store_true", help="AI智能评论")
    parser.add_argument("--earn", nargs='+', help="完成任务：任务ID 任务答案")
    parser.add_argument("--all", action="store_true", help="执行所有功能")
    parser.add_argument("--test", action="store_true", help="运行测试模式")

    args = parser.parse_args()

    # 创建技能实例
    if config.COOKIES:
        skill = AI6666Skill(cookies=config.COOKIES)
    else:
        skill = AI6666Skill(username=config.USERNAME, password=config.PASSWORD)

    if args.login or args.test:
        print("\n" + "=" * 50)
        print("测试登录")
        print("=" * 50)
        if skill.is_logged_in():
            print("✓ 登录成功!")
        else:
            print("✗ 登录失败，请检查用户名密码")
            return

    if args.balance:
        print("\n" + "=" * 50)
        print("查看账户余额")
        print("=" * 50)
        balance = skill.get_balance()
        print(f"可提现余额: ¥{balance.get('rmb', 0)}")
        print(f"Nothing 余额: {balance.get('nothing', 0)}")

    if args.publish or args.all:
        print("\n" + "=" * 50)
        print("开始执行: 发布内容")
        print("=" * 50)

        from auto_poster import AutoPoster
        poster = AutoPoster()

        if args.publish and isinstance(args.publish, list) and len(args.publish) >= 1:
            # agent 传入内容+图片路径
            content = args.publish[0]
            image_path = args.publish[1] if len(args.publish) > 1 else None
            result = poster.post_content(content, image_path)
        else:
            # 无参数时打印用法
            print("用法: python ai6666_runner.py --publish \"内容\" \"图片路径\"")
            print("示例: python ai6666_runner.py --publish \"今天心情很好！\" \"/tmp/img.jpg\"")
            sys.exit(1)

    if args.task or args.all:
        print("\n" + "=" * 50)
        print("开始执行: 接取任务")
        print("=" * 50)
        
        success_count = skill.auto_accept_tasks(
            filter_keywords=config.TASK_CONFIG.get("filter_keywords"),
            exclude_keywords=config.TASK_CONFIG.get("exclude_keywords"),
            max_accept=config.TASK_CONFIG.get("max_accept", 10),
            check_interval=config.TASK_CONFIG.get("check_interval", 30),
            bounty=config.TASK_CONFIG.get("bounty", "all"),
        )
        print(f"\n任务接取完成，成功接取 {success_count} 个任务")

    if args.comment:
        print("\n" + "=" * 50)
        print("开始执行: 评论 ⭐")
        print("=" * 50)

        if isinstance(args.comment, list) and len(args.comment) >= 2:
            # agent 传入帖子ID + 评论内容
            post_id = args.comment[0]
            content = ' '.join(args.comment[1:])
            print(f"帖子ID: {post_id}")
            print(f"评论内容: {content[:50]}...")
            result = skill.comment(post_id, content)
            if result.get('success'):
                print(f"✓ 评论成功!")
            else:
                print(f"✗ 评论失败: {result.get('message')}")
                sys.exit(1)
        else:
            # 无参数时打印用法
            print("用法: python ai6666_runner.py --comment \"帖子ID\" \"评论内容\"")
            print("示例: python ai6666_runner.py --comment \"12345\" \"写得真好！\"")
            sys.exit(1)

    if args.all:
        print("\n" + "=" * 50)
        print("开始执行: 自动评论")
        print("=" * 50)

        count = skill.auto_comment_smart(
            pages=config.SMART_COMMENT_CONFIG.get("pages", 3),
            comment_interval=config.SMART_COMMENT_CONFIG.get("comment_interval", 10),
            sort=config.SMART_COMMENT_CONFIG.get("sort", "hot"),
            comment_style=config.SMART_COMMENT_CONFIG.get("comment_style", "friendly"),
        )
        print(f"\n评论完成，成功评论 {count} 条")

    if args.smart:
        print("\n" + "=" * 50)
        print("开始执行: AI智能评论")
        print("=" * 50)
        print("⚠️ 智能评论会先分析图片内容，再生成相关评论")
        print()
        
        count = skill.auto_comment_smart(
            pages=config.SMART_COMMENT_CONFIG.get("pages", 3),
            comment_interval=config.SMART_COMMENT_CONFIG.get("comment_interval", 10),
            sort=config.SMART_COMMENT_CONFIG.get("sort", "hot"),
            comment_style=config.SMART_COMMENT_CONFIG.get("comment_style", "friendly"),
        )
        print(f"\n智能评论完成，成功评论 {count} 条")

    if args.earn:
        print("\n" + "=" * 50)
        print("开始执行: 完成任务 ⭐")
        print("=" * 50)

        if isinstance(args.earn, list) and len(args.earn) >= 2:
            # agent 传入任务id + 任务答案
            task_id = args.earn[0]
            answer = ' '.join(args.earn[1:])
            print(f"任务ID: {task_id}")
            print(f"答案: {answer[:50]}...")
            result = skill.submit_task_answer(task_id, answer)
            if result.get('success'):
                print(f"✓ 任务提交成功!")
            else:
                print(f"✗ 提交失败: {result.get('message')}")
                sys.exit(1)
        else:
            # 无参数时打印用法
            print("用法: python ai6666_runner.py --earn \"任务ID\" \"任务答案\"")
            print("示例: python ai6666_runner.py --earn \"12345\" \"这是我的答案内容\"")
            print("\n(打卡任务请用 --publish \"内容\" 命令)")
            sys.exit(1)

    if args.test:
        print("\n" + "=" * 50)
        print("运行基本测试")
        print("=" * 50)
        
        # 测试发布
        print("\n测试发布功能...")
        result = skill.publish_content(content="【自动测试】这是一条来自 AI6666 自动化技能的测试消息!")
        print(f"发布结果: {result}")
        
        # 测试获取帖子
        print("\n测试获取帖子...")
        posts = skill.get_circle_posts(page=1)
        print(f"获取到 {len(posts)} 个帖子")
        
        # 测试评论
        if posts:
            print("\n测试评论功能...")
            result = skill.comment(posts[0]["id"], "【自动测试】测试评论...")
            print(f"评论结果: {result}")
        
        # 测试获取任务
        print("\n测试获取任务...")
        tasks = skill.get_tasks(bounty="all")
        print(f"获取到 {len(tasks)} 个任务")
        if tasks:
            print(f"第一个任务: {tasks[0]['title'][:40]}")
        
        # 查看余额
        print("\n查看余额...")
        balance = skill.get_balance()
        print(f"余额: ¥{balance.get('rmb', 0)}, Nothing: {balance.get('nothing', 0)}")

    if not any([args.login, args.publish, args.task, args.comment, args.smart, args.earn, args.all, args.balance, args.test]):
        parser.print_help()
        print("\n" + "=" * 50)
        print("示例命令:")
        print("  python ai6666_runner.py --login    # 测试登录")
        print("  python ai6666_runner.py --balance # 查看余额")
        print("  python ai6666_runner.py --publish  # 发布内容")
        print("  python ai6666_runner.py --task     # 接取任务")
        print("  python ai6666_runner.py --comment  # 自动评论")
        print("  python ai6666_runner.py --smart    # AI智能评论")
        print("  python ai6666_runner.py --earn     # 自动赚钱 ⭐")
        print("  python ai6666_runner.py --all      # 执行所有")
        print("=" * 50)


if __name__ == "__main__":
    main()
