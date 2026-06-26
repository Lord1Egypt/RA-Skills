#!/usr/bin/env python3
"""
抖音视频发布脚本
使用 Playwright 浏览器自动化发布视频到抖音创作者平台
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("[ERROR] Playwright 未安装，请运行:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)

# 抖音创作者平台 URL
DOUYIN_CREATOR_URL = "https://creator.douyin.com/"
DOUYIN_UPLOAD_URL = "https://creator.douyin.com/creator-micro/content/upload"

# 浏览器用户数据目录（保存登录状态）
USER_DATA_DIR = os.path.expanduser("~/.openclaw/browser/douyin-publisher")


def parse_args():
    parser = argparse.ArgumentParser(description="发布视频到抖音")
    parser.add_argument("--video", required=True, help="视频文件路径或URL")
    parser.add_argument("--title", required=True, help="视频标题")
    parser.add_argument("--desc", default="", help="视频描述/文案")
    parser.add_argument("--tags", default="", help="话题标签，空格分隔")
    parser.add_argument("--cover", default="", help="封面图片路径")
    parser.add_argument("--test", action="store_true", help="仅启动浏览器测试，不发布")
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    return parser.parse_args()


def check_login_status(page):
    """检查是否已登录"""
    try:
        # 检查是否有登录按钮或用户头像
        login_btn = page.query_selector('text=登录')
        if login_btn:
            return False
        # 检查是否有用户头像（已登录状态）
        avatar = page.query_selector('[class*="avatar"]')
        return avatar is not None
    except:
        return False


def wait_for_login(page, timeout=120):
    """等待用户扫码登录"""
    print("[INFO] 请在浏览器中扫码登录抖音账号...")
    print(f"[INFO] 等待登录（最多 {timeout} 秒）...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_login_status(page):
            print("[SUCCESS] 登录成功！")
            return True
        time.sleep(2)
    
    print("[ERROR] 登录超时")
    return False


def upload_video(page, video_path):
    """上传视频文件"""
    print(f"[INFO] 正在上传视频: {video_path}")
    
    # 检查文件是否存在
    if not os.path.exists(video_path):
        # 可能是 URL，需要先下载
        if video_path.startswith("http"):
            print(f"[INFO] 视频是 URL，正在下载...")
            video_path = download_video(video_path)
            if not video_path:
                return False
        else:
            print(f"[ERROR] 视频文件不存在: {video_path}")
            return False
    
    # 找到上传按钮/区域
    try:
        # 点击上传按钮
        upload_btn = page.query_selector('input[type="file"]')
        if upload_btn:
            upload_btn.set_input_files(video_path)
            print("[INFO] 视频上传中...")
            return True
        else:
            print("[ERROR] 未找到上传按钮")
            return False
    except Exception as e:
        print(f"[ERROR] 上传失败: {e}")
        return False


def fill_content(page, title, desc="", tags=""):
    """填写视频内容（标题、描述、话题）"""
    print("[INFO] 正在填写视频信息...")
    
    try:
        # 等待视频上传完成（页面加载）
        time.sleep(3)
        
        # 填写标题/描述（抖音使用同一个输入框）
        # 组合标题和描述
        full_text = title
        if desc:
            full_text += f"\n{desc}"
        if tags:
            full_text += f"\n{tags}"
        
        # 找到文本输入框
        textarea = page.query_selector('textarea[placeholder*="描述"]') or \
                   page.query_selector('textarea[placeholder*="标题"]') or \
                   page.query_selector('textarea')
        
        if textarea:
            textarea.fill(full_text)
            print(f"[INFO] 已填写内容: {full_text[:50]}...")
        else:
            print("[WARN] 未找到文本输入框，请手动填写")
        
        return True
    except Exception as e:
        print(f"[ERROR] 填写内容失败: {e}")
        return False


def publish_video(page):
    """点击发布按钮"""
    print("[INFO] 正在发布视频...")
    
    try:
        # 找到发布按钮
        publish_btn = page.query_selector('button:has-text("发布")')
        if not publish_btn:
            publish_btn = page.query_selector('button:has-text("发表")')
        
        if publish_btn:
            publish_btn.click()
            print("[INFO] 已点击发布按钮")
            
            # 等待发布完成
            time.sleep(3)
            
            # 检查是否发布成功
            success_indicator = page.query_selector('text=发布成功') or \
                               page.query_selector('text=成功')
            
            if success_indicator:
                print("[SUCCESS] 视频发布成功！")
                return True
            else:
                print("[WARN] 发布状态未知，请检查浏览器")
                return True
        else:
            print("[ERROR] 未找到发布按钮")
            return False
    except Exception as e:
        print(f"[ERROR] 发布失败: {e}")
        return False


def download_video(url):
    """下载视频文件"""
    import urllib.request
    
    try:
        temp_dir = os.path.expanduser("~/.openclaw/workspace/temp_videos")
        os.makedirs(temp_dir, exist_ok=True)
        
        video_path = os.path.join(temp_dir, f"video_{int(time.time())}.mp4")
        
        print(f"[INFO] 正在下载视频到: {video_path}")
        urllib.request.urlretrieve(url, video_path)
        
        print(f"[SUCCESS] 视频下载完成")
        return video_path
    except Exception as e:
        print(f"[ERROR] 下载视频失败: {e}")
        return None


def main():
    args = parse_args()
    
    print("=" * 50)
    print("抖音视频发布工具")
    print("=" * 50)
    
    if args.test:
        print("[TEST MODE] 仅启动浏览器，不发布")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=args.headless,
            args=["--start-maximized"],
            viewport={"width": 1280, "height": 800}
        )
        
        page = browser.new_page()
        
        try:
            # 访问抖音创作者平台
            print(f"[INFO] 正在访问抖音创作者平台...")
            page.goto(DOUYIN_CREATOR_URL, wait_until="networkidle")
            
            # 检查登录状态
            if not check_login_status(page):
                print("[WARN] 未检测到登录状态")
                if not wait_for_login(page):
                    print("[ERROR] 请先登录抖音账号")
                    browser.close()
                    sys.exit(1)
            
            if args.test:
                print("[TEST] 浏览器已启动，请手动检查")
                input("按 Enter 关闭浏览器...")
            else:
                # 导航到上传页面
                page.goto(DOUYIN_UPLOAD_URL, wait_until="networkidle")
                time.sleep(2)
                
                # 上传视频
                if not upload_video(page, args.video):
                    browser.close()
                    sys.exit(1)
                
                # 等待视频处理
                print("[INFO] 等待视频处理...")
                time.sleep(10)
                
                # 填写内容
                if not fill_content(page, args.title, args.desc, args.tags):
                    browser.close()
                    sys.exit(1)
                
                # 发布
                if not publish_video(page):
                    browser.close()
                    sys.exit(1)
                
                print("[SUCCESS] 发布流程完成！")
        
        except PlaywrightTimeout as e:
            print(f"[ERROR] 操作超时: {e}")
        except Exception as e:
            print(f"[ERROR] 发生错误: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
