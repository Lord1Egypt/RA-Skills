"""
抖音创作者中心 - 批量回复模块
按模板策略批量回复未回复评论。
"""

import sys
import json
import time
import random
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    PROJECT_DIR, OUTPUT_DIR, PROFILE_DIR,
    DOUYIN_COMMENT_URL,
    load_config, load_reply_templates,
    match_template, contains_blocked_content, ensure_dirs
)


def generate_reply(content, strategy, templates=None, ai_prompt=None):
    """
    根据策略生成回复文本。
    
    策略:
    - template: 关键词匹配模板
    - random: 从模板中随机选择
    - ai: 使用 AI 生成（预留接口）
    """
    if strategy == "template" and templates:
        reply = match_template(content, templates)
        return reply
    
    elif strategy == "random" and templates:
        template_list = templates.get("templates", [])
        if template_list:
            return random.choice(template_list)["reply"]
        return templates.get("default_reply", "感谢评论！💕")
    
    elif strategy == "ai":
        # AI 生成回复的预留接口
        # 此处可由上层 Skill 编排注入 AI 回复
        print(f"  [AI] AI 生成回复（当前为占位模式）")
        return f"感谢你的评论！关于「{content[:30]}」，我们会认真考虑的。"
    
    return "感谢评论！💕"


def batch_reply_dry_run(comments, strategy, templates=None, ai_prompt=None):
    """
    预览模式：不实际执行回复，只展示回复计划。
    """
    print("\n" + "=" * 60)
    print("  📋 批量回复预览 (DRY RUN)")
    print("=" * 60)
    print(f"  策略: {strategy}")
    print(f"  待回复: {len(comments)} 条")
    print(f"  默认回复: {templates.get('default_reply', 'N/A') if templates else 'N/A'}")
    print()
    
    for i, c in enumerate(comments):
        content = c.get("content", "")
        author = c.get("author_name", "未知")
        reply = generate_reply(content, strategy, templates, ai_prompt)
        
        print(f"  [{i+1}/{len(comments)}] @{author}: {content[:60]}...")
        print(f"       → 回复: {reply}")
        print()
    
    print(f"[INFO] 预览完成。确认无误后去掉 --dry-run 执行实际回复。")
    
    return {
        "strategy": strategy,
        "total": len(comments),
        "plan": [
            {
                "index": i + 1,
                "author": c.get("author_name", ""),
                "comment": c.get("content", ""),
                "reply": generate_reply(c.get("content", ""), strategy, templates, ai_prompt),
            }
            for i, c in enumerate(comments)
        ],
        "dry_run": True,
    }


def execute_batch_reply(page, comments, strategy, templates=None, 
                         ai_prompt=None, delay_range=(3, 8),
                         max_replies=100, skip_keywords=None):
    """
    实际执行批量回复。
    """
    print("\n" + "=" * 60)
    print("  🚀 开始批量回复")
    print("=" * 60)
    
    total = min(len(comments), max_replies)
    
    # 检查登录状态
    page.goto(DOUYIN_COMMENT_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    
    current_url = page.url
    if "login" in current_url.lower():
        print("[ERROR] 登录态过期，请重新登录: python scripts/auth.py")
        return None
    
    results = []
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for i in range(total):
        comment = comments[i]
        content = comment.get("content", "")
        author = comment.get("author_name", "未知")
        
        progress = f"[{i+1}/{total}]"
        
        # 检查跳过关键词
        if skip_keywords:
            should_skip = False
            for kw in skip_keywords:
                if kw in content:
                    print(f"  {progress} ⏭️ 跳过 @{author}（含屏蔽词: {kw}）")
                    skip_count += 1
                    results.append({
                        "index": i + 1,
                        "author": author,
                        "comment": content[:100],
                        "status": "skipped",
                        "reason": f"含屏蔽词: {kw}",
                    })
                    should_skip = True
                    break
            if should_skip:
                continue
        
        # 生成回复
        reply = generate_reply(content, strategy, templates, ai_prompt)
        
        # 检查回复内容是否合规
        blocked, blocked_kw = contains_blocked_content(reply)
        if blocked:
            print(f"  {progress} ⚠️ 跳过 @{author}（回复含违规词: {blocked_kw}）")
            skip_count += 1
            results.append({
                "index": i + 1,
                "author": author,
                "comment": content[:100],
                "reply": reply,
                "status": "skipped",
                "reason": f"回复含违规词: {blocked_kw}",
            })
            continue
        
        # 执行回复
        try:
            # 定位回复输入框并输入
            # 注意：选择器需根据抖音实际页面结构调整
            reply_input = page.locator(
                '[contenteditable="true"], '
                'textarea, '
                '[class*="reply-input"], '
                '[class*="input"], '
                'input[type="text"]'
            ).first
            
            if await_really_check(reply_input):
                reply_input.click()
                time.sleep(0.5)
                reply_input.fill(reply)
                time.sleep(0.5)
                
                # 查找发送按钮
                send_btn = page.locator(
                    'button:has-text("发送"), '
                    'button:has-text("回复"), '
                    '[class*="send"], '
                    '[class*="submit"]'
                ).first
                
                if await_really_check(send_btn):
                    send_btn.click()
                    time.sleep(1)
                    
                    print(f"  {progress} ✅ @{author} → {reply}")
                    success_count += 1
                    results.append({
                        "index": i + 1,
                        "author": author,
                        "comment": content[:100],
                        "reply": reply,
                        "status": "success",
                        "time": datetime.now().isoformat(),
                    })
                else:
                    print(f"  {progress} ❌ @{author}（找不到发送按钮）")
                    fail_count += 1
                    results.append({
                        "index": i + 1,
                        "author": author,
                        "comment": content[:100],
                        "reply": reply,
                        "status": "failed",
                        "reason": "找不到发送按钮",
                    })
            else:
                print(f"  {progress} ❌ @{author}（找不到输入框）")
                fail_count += 1
                results.append({
                    "index": i + 1,
                    "author": author,
                    "comment": content[:100],
                    "reply": reply,
                    "status": "failed",
                    "reason": "找不到输入框",
                })
        
        except Exception as e:
            print(f"  {progress} ❌ @{author}（异常: {str(e)[:50]}）")
            fail_count += 1
            results.append({
                "index": i + 1,
                "author": author,
                "comment": content[:100],
                "reply": reply,
                "status": "failed",
                "reason": str(e)[:100],
            })
        
        # 随机延迟
        delay = random.uniform(*delay_range)
        time.sleep(delay)
    
    # 汇总
    print(f"\n{'='*60}")
    print(f"  批量回复完成")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ⏭️ 跳过: {skip_count}")
    print(f"  ❌ 失败: {fail_count}")
    print(f"{'='*60}")
    
    return {
        "strategy": strategy,
        "total": total,
        "success": success_count,
        "skipped": skip_count,
        "failed": fail_count,
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }


def await_really_check(element, timeout=3000):
    """检查元素是否存在且可见"""
    try:
        element.wait_for(state="visible", timeout=timeout)
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser(description="抖音批量评论回复工具")
    parser.add_argument("--input", type=str, required=True, help="未回复评论 JSON 文件路径")
    parser.add_argument("--strategy", choices=["template", "random", "ai"], 
                        default="template", help="回复策略")
    parser.add_argument("--template-file", type=str, help="自定义回复模板 JSON")
    parser.add_argument("--ai-system-prompt", type=str, help="AI 回复的系统提示词")
    parser.add_argument("--delay-min", type=float, default=3, help="每条回复最小间隔（秒）")
    parser.add_argument("--delay-max", type=float, default=8, help="每条回复最大间隔（秒）")
    parser.add_argument("--max-replies", type=int, default=100, help="最大回复条数")
    parser.add_argument("--skip-keyword", type=str, nargs="+", help="跳过含此关键词的评论")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际回复")
    parser.add_argument("--output", type=str, help="回复结果 JSON 路径")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    # 加载评论数据
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在: {input_path}")
        sys.exit(1)
    
    with open(input_path, "r", encoding="utf-8") as f:
        comments = json.load(f)
    
    print(f"[INFO] 加载 {len(comments)} 条待回复评论")
    
    # 加载模板
    templates = load_reply_templates(args.template_file)
    
    # 预览模式
    if args.dry_run:
        result = batch_reply_dry_run(
            comments, args.strategy, templates, args.ai_system_prompt
        )
        output_file = args.output or str(OUTPUT_DIR / "reply_preview.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n[SAVED] 预览结果 → {output_file}")
        return
    
    # 实际执行
    config = load_config()
    if args.headless:
        config["headless"] = True
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] 请先安装 Playwright: pip install playwright && python -m playwright install chromium")
        sys.exit(1)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=config.get("headless", False),
            viewport=config["viewport"],
            locale=config["locale"],
            timezone_id=config["timezone_id"],
            slow_mo=config.get("slow_mo", 50),
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        )
        page = context.new_page()
        
        try:
            result = execute_batch_reply(
                page, comments, args.strategy, templates,
                args.ai_system_prompt,
                (args.delay_min, args.delay_max),
                args.max_replies,
                args.skip_keyword,
            )
            
            if result:
                output_file = args.output or str(OUTPUT_DIR / "reply_results.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"\n[SAVED] 回复结果 → {output_file}")
        
        finally:
            context.close()


if __name__ == "__main__":
    main()
