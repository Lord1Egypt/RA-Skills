"""
抖音创作者中心 - 评论抓取模块
通过 Playwright 自动化抓取作品列表和未回复评论。
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
    DOUYIN_CREATOR_URL, DOUYIN_CONTENT_URL, DOUYIN_COMMENT_URL,
    load_config, ensure_dirs
)


def launch_browser_context(playwright, config):
    """启动持久化浏览器上下文"""
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=config.get("headless", False),
        viewport=config["viewport"],
        locale=config["locale"],
        timezone_id=config["timezone_id"],
        slow_mo=config.get("slow_mo", 50),
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    )
    return context


def check_login(page):
    """检查是否登录成功"""
    current_url = page.url
    if "login" in current_url.lower() or "passport" in current_url.lower():
        print("[ERROR] 未登录或登录态已过期，请先运行: python scripts/auth.py")
        return False
    return True


def wait_for_content_loaded(page, timeout=15000):
    """等待页面内容加载完成"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except:
        pass
    time.sleep(2)


def fetch_works(page, config):
    """
    获取作品列表。
    导航到创作者中心内容管理页面，抓取所有作品信息。
    """
    print("[STEP] 正在获取作品列表...")
    
    page.goto(DOUYIN_CONTENT_URL, wait_until="domcontentloaded", timeout=30000)
    wait_for_content_loaded(page)
    
    if not check_login(page):
        return []
    
    works = []
    max_scroll = 50  # 最大滚动次数防止无限循环
    prev_count = -1
    
    for i in range(max_scroll):
        # 尝试提取作品数据
        try:
            # 抖音创作者中心页面结构可能变化，使用多种选择器尝试
            items = page.locator('[class*="video"], [class*="item"], [class*="card"], [data-e2e*="work"]').all()
            
            for item in items:
                try:
                    text = item.inner_text()
                    if len(text) > 10:  # 过滤空元素
                        # 尝试提取结构化数据
                        title = ""
                        video_id = ""
                        stats = ""
                        
                        # 尝试找标题
                        title_el = item.locator('[class*="title"], [class*="name"], [class*="desc"]').first
                        try:
                            title = title_el.inner_text().strip()
                        except:
                            title = text.split("\n")[0][:50]
                        
                        # 尝试找统计
                        try:
                            stats = item.locator('[class*="stat"], [class*="num"], [class*="count"]').all()
                            stats = " | ".join([s.inner_text().strip() for s in stats[:3]])
                        except:
                            stats = ""
                        
                        work_entry = {
                            "title": title,
                            "video_id": video_id,
                            "stats": stats,
                            "raw_text": text[:200],
                        }
                        
                        # 去重
                        if not any(w.get("title") == title for w in works):
                            works.append(work_entry)
                except:
                    continue
            
            if len(works) == prev_count:
                break
            prev_count = len(works)
            
            # 滚动加载更多
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(1.5, 3))
            print(f"  [PROGRESS] 已发现 {len(works)} 个作品...")
            
        except Exception as e:
            print(f"  [WARN] 抓取作品时出错: {e}")
            break
    
    print(f"[DONE] 共发现 {len(works)} 个作品")
    
    # 保存作品列表
    output_file = OUTPUT_DIR / "works.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(works, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] 作品列表已保存到 {output_file}")
    
    return works


def fetch_comments_for_video(page, video_title, config, max_comments=500):
    """
    抓取指定视频的未回复评论。
    尝试通过搜索或直接导航到视频评论页。
    """
    print(f"[STEP] 正在搜索视频: {video_title}")
    
    # 先到内容管理页
    page.goto(DOUYIN_CONTENT_URL, wait_until="domcontentloaded", timeout=30000)
    wait_for_content_loaded(page)
    
    if not check_login(page):
        return []
    
    # 尝试点击搜索到的作品进入评论管理
    comments = []
    found = False
    
    try:
        # 查找匹配的视频条目并点击
        items = page.locator('[class*="video"], [class*="item"], [class*="card"], [class*="work"]').all()
        for item in items:
            try:
                text = item.inner_text()
                if video_title in text:
                    print(f"  [FOUND] 找到匹配视频")
                    item.click()
                    time.sleep(3)
                    found = True
                    break
            except:
                continue
    except Exception as e:
        print(f"  [WARN] 查找视频失败: {e}")

    if not found:
        print(f"  [WARN] 未找到标题含 '{video_title}' 的视频")
        print(f"  [INFO] 将尝试从当前页面抓取评论...")
    
    # 尝试进入评论管理
    try:
        # 查找"评论管理"或类似入口
        comment_links = page.locator('a:has-text("评论"), span:has-text("评论"), [class*="comment"]').all()
        for link in comment_links:
            try:
                link_text = link.inner_text().strip()
                if "评论" in link_text and len(link_text) < 10:
                    print(f"  [CLICK] 进入评论管理: {link_text}")
                    link.click()
                    time.sleep(3)
                    break
            except:
                continue
    except:
        pass
    
    wait_for_content_loaded(page)
    
    # 尝试筛选未回复评论
    try:
        # 查找筛选/过滤按钮
        filter_btns = page.locator('text=未回复, text=待回复, [class*="filter"], [class*="tab"]').all()
        for btn in filter_btns:
            try:
                text = btn.inner_text().strip()
                if "未回复" in text or "待回复" in text:
                    print(f"  [CLICK] 筛选: {text}")
                    btn.click()
                    time.sleep(2)
                    break
            except:
                continue
    except:
        pass
    
    # 抓取评论
    print(f"[STEP] 正在抓取评论（最多 {max_comments} 条）...")
    
    prev_count = -1
    no_change_count = 0
    
    while len(comments) < max_comments:
        try:
            # 尝试提取评论数据
            comment_items = page.locator(
                '[class*="comment"], [class*="reply"], [class*="message"], [class*="item"]'
            ).all()
            
            for item in comment_items:
                try:
                    full_text = item.inner_text()
                    if len(full_text) < 5 or len(full_text) > 5000:
                        continue
                    
                    # 提取评论关键信息
                    lines = full_text.split("\n")
                    
                    comment = {
                        "video_title": video_title,
                        "content": full_text[:500],
                        "author_name": lines[0] if lines else "",
                        "like_count": 0,
                        "reply_count": 0,
                        "create_time": datetime.now().isoformat(),
                        "is_replied": False,
                        "raw_text": full_text,
                    }
                    
                    # 判断是否已回复
                    if "已回复" in full_text or "回复" in "".join(lines[-3:]):
                        comment["is_replied"] = True
                    
                    # 去重
                    if not any(c.get("content") == comment["content"] for c in comments):
                        comments.append(comment)
                except:
                    continue
            
            # 只保留未回复的
            unreplied = [c for c in comments if not c["is_replied"]]
            
            if len(comments) == prev_count:
                no_change_count += 1
                if no_change_count >= 3:
                    break
            else:
                no_change_count = 0
            
            prev_count = len(comments)
            
            # 滚动加载更多
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(1.5, 3))
            print(f"  [PROGRESS] 已抓取 {len(comments)} 条（{len(unreplied)} 条未回复）...")
            
        except Exception as e:
            print(f"  [WARN] 抓取评论出错: {e}")
            break
    
    # 过滤只保留未回复评论
    unreplied = [c for c in comments if not c["is_replied"]]
    
    print(f"[DONE] 抓取完成: {len(comments)} 条评论，{len(unreplied)} 条未回复")
    
    # 添加序号
    for i, c in enumerate(unreplied):
        c["index"] = i + 1
    
    return unreplied


def fetch_all_comments(page, config, max_per_video=500):
    """抓取所有作品的未回复评论"""
    # 先获取作品列表
    works = fetch_works(page, config)
    
    all_comments = []
    
    for i, work in enumerate(works):
        title = work.get("title", f"作品{i+1}")
        if not title:
            continue
        
        print(f"\n{'='*40}")
        print(f"  作品 {i+1}/{len(works)}: {title[:50]}")
        print(f"{'='*40}")
        
        comments = fetch_comments_for_video(page, title, config, max_per_video)
        all_comments.extend(comments)
        
        # 随机延迟
        time.sleep(random.uniform(2, 5))
    
    # 重新编号
    for i, c in enumerate(all_comments):
        c["index"] = i + 1
    
    return all_comments


def main():
    parser = argparse.ArgumentParser(description="抖音评论抓取工具")
    parser.add_argument("--works", action="store_true", help="获取作品列表")
    parser.add_argument("--video-title", type=str, help="指定作品标题")
    parser.add_argument("--video-id", type=str, help="指定作品 ID")
    parser.add_argument("--all", action="store_true", help="拉取所有作品的未回复评论")
    parser.add_argument("--max-per-video", type=int, default=500, help="每个视频最多抓取评论数")
    parser.add_argument("--output", type=str, help="输出 JSON 路径")
    parser.add_argument("--include-replied", action="store_true", help="同时输出已回复评论")
    parser.add_argument("--filter-keyword", type=str, help="只抓取包含关键词的评论")
    parser.add_argument("--sort-by", choices=["time", "likes"], default="time", help="排序方式")
    parser.add_argument("--headless", action="store_true", help="无头模式运行（需要已有登录态）")
    
    args = parser.parse_args()
    
    ensure_dirs()
    config = load_config()
    
    if args.headless:
        config["headless"] = True
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] 请先安装 Playwright: pip install playwright && python -m playwright install chromium")
        sys.exit(1)
    
    with sync_playwright() as p:
        context = launch_browser_context(p, config)
        page = context.new_page()
        
        try:
            if args.works:
                fetch_works(page, config)
            
            elif args.video_title:
                comments = fetch_comments_for_video(
                    page, args.video_title, config, args.max_per_video
                )
                output_file = args.output or str(OUTPUT_DIR / "unreplied_comments.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(comments, f, ensure_ascii=False, indent=2)
                print(f"[SAVED] {len(comments)} 条未回复评论 → {output_file}")
            
            elif args.all:
                comments = fetch_all_comments(page, config, args.max_per_video)
                output_file = args.output or str(OUTPUT_DIR / "unreplied_comments.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(comments, f, ensure_ascii=False, indent=2)
                print(f"\n[SAVED] 共 {len(comments)} 条未回复评论 → {output_file}")
            
            else:
                print("[ERROR] 请指定操作: --works / --video-title / --all")
                parser.print_help()
        
        finally:
            context.close()


if __name__ == "__main__":
    main()
