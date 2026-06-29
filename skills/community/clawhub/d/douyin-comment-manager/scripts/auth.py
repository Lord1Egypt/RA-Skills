"""
抖音创作者中心 - 扫码登录模块
使用 Playwright 持久化浏览器上下文，用户扫码登录后保存会话。
"""

import sys
import time
from pathlib import Path

# 添加 scripts 目录到 path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    PROJECT_DIR, PROFILE_DIR, DOUYIN_LOGIN_URL, load_config, ensure_dirs
)


def check_login_state():
    """检查是否存在有效的登录态"""
    state_file = PROFILE_DIR / "state.json"
    if state_file.exists():
        import json
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
            cookies = state.get("cookies", [])
            if cookies:
                print(f"[OK] 发现已有登录态 ({len(cookies)} 个 cookies)")
                return True
    print("[INFO] 未找到有效登录态，需要重新登录")
    return False


def login_with_qr():
    """打开浏览器，让用户扫码登录"""
    ensure_dirs()
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("=" * 60)
        print("[ERROR] 未安装 Playwright！")
        print("请运行以下命令安装：")
        print("  pip install playwright")
        print("  python -m playwright install chromium")
        print("=" * 60)
        sys.exit(1)

    config = load_config()
    
    print("=" * 60)
    print("  抖音创作者中心 - 扫码登录")
    print("=" * 60)
    print()
    print("即将打开浏览器...")
    print("请在浏览器中扫描二维码完成登录")
    print("登录成功后浏览器将自动关闭，会话会被保存")
    print()

    with sync_playwright() as p:
        # 使用持久化上下文，复用已有登录态
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            viewport=config["viewport"],
            locale=config["locale"],
            timezone_id=config["timezone_id"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        page = context.new_page()
        
        # 导航到创作者中心（会自动跳转到登录页）
        print("[STEP] 正在打开创作者中心...")
        page.goto(DOUYIN_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # 检测当前页面状态
        current_url = page.url
        
        if "creator.douyin.com/creator-micro" in current_url:
            print("[OK] 已经处于登录状态！")
            # 保存当前状态
            context.storage_state(path=str(PROFILE_DIR / "state.json"))
            print("[SAVED] 登录态已保存到 .playwright/douyin-profile/")
            context.close()
            return True

        # 等待用户扫码登录
        print("[WAIT] 请在浏览器中扫码登录...")
        print("       (等待最多 5 分钟，登录成功后自动继续)")
        
        try:
            # 等待登录成功（URL 跳转到创作者中心主页）
            page.wait_for_url(
                "**/creator-micro/**",
                timeout=300000  # 5 分钟超时
            )
            print()
            print("[OK] 登录成功！")
            
            # 稍等确保登录态完全写入
            time.sleep(3)
            
            # 保存登录态
            context.storage_state(path=str(PROFILE_DIR / "state.json"))
            print("[SAVED] 登录态已保存到 .playwright/douyin-profile/")
            
            context.close()
            return True
            
        except Exception as e:
            print()
            print(f"[ERROR] 登录超时或失败: {e}")
            print("请重试：python scripts/auth.py")
            
            # 即使超时也尝试保存当前状态
            try:
                context.storage_state(path=str(PROFILE_DIR / "state.json"))
            except:
                pass
            
            context.close()
            return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="抖音创作者中心登录")
    parser.add_argument("--check", action="store_true", help="仅检查登录状态")
    parser.add_argument("--force", action="store_true", help="强制重新登录")
    
    args = parser.parse_args()
    
    if args.check:
        if check_login_state():
            sys.exit(0)
        else:
            sys.exit(1)
    
    if args.force:
        print("[INFO] 强制重新登录模式")
        # 清除旧登录态
        import shutil
        if PROFILE_DIR.exists():
            shutil.rmtree(PROFILE_DIR)
            PROFILE_DIR.mkdir(parents=True)
    
    success = login_with_qr()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
