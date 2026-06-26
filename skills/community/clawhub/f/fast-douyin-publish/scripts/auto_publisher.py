#!/usr/bin/env python3
"""
🦞 抖音视频发布助手
一键上传视频到抖音

Usage: python auto_publisher.py --video "path/to/video.mp4"
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 避免 asyncio 冲突 - 在导入 playwright 前设置
os.environ['PLAYWRIGHT_ASYNC'] = '0'

# 尝试导入 playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright 未安装，运行：pip install playwright")
    print("⚠️  然后运行：playwright install")

class VideoPublisher:
    """抖音视频发布器"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or "config/accounts.json"
        self.accounts = self.load_accounts()
        self.results = {}
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.cookies_dir = Path("config/cookies")
        self.cookies_dir.mkdir(parents=True, exist_ok=True)

    def get_cookies_path(self, platform: str) -> Path:
        """获取指定平台的 cookies 文件路径"""
        return self.cookies_dir / f"{platform}.json"

    def load_cookies(self, platform: str) -> Optional[dict]:
        """加载指定平台的 cookies，并修复 SameSite 兼容性问题"""
        cookies_path = self.get_cookies_path(platform)
        if cookies_path.exists():
            return cookies_path
        return None

    def save_cookies(self, platform: str):
        """保存当前会话的 cookies"""
        if self.context:
            cookies_path = self.get_cookies_path(platform)
            self.context.storage_state(path=str(cookies_path))
            print(f"✅ 已保存 {platform} 登录状态")

    def load_accounts(self) -> Dict:
        """加载账号配置"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建默认配置（仅抖音）
            default_config = {
                "douyin": {
                    "enabled": True,
                    "username": "",
                    "password": "",
                    "qr_login": True  # 使用二维码登录
                }
            }

            # 保存默认配置
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)

            print(f"📝 已创建默认配置文件：{config_file}")
            print("⚠️  请编辑配置文件，填写账号信息后重新运行")

            return default_config

    def save_accounts(self):
        """保存账号配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, indent=2, ensure_ascii=False)

    def start_browser(self, headless: bool = False, platform: str = None):
        """启动浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright 未安装")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)

        # 构建 context 参数
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # 如果指定了平台，尝试加载已保存的 cookies
        if platform:
            cookies_path = self.load_cookies(platform)
            if cookies_path:
                with open(cookies_path, 'r', encoding='utf-8') as f:
                    storage_data = json.load(f)

                # 遍历并修正 sameSite 属性
                if "cookies" in storage_data:
                    for cookie in storage_data["cookies"]:
                        if cookie.get("sameSite") not in ["Strict", "Lax", "None"]:
                            # 如果不合法，统一修正为 'Lax' (浏览器默认行为)
                            cookie["sameSite"] = "Lax"

                # 将修正后的数据存回或直接传入 (Playwright 支持直接传 dict)
                context_options["storage_state"] = storage_data
                print(f"📂 已加载并清洗 {platform} 登录状态")

        self.context = self.browser.new_context(**context_options)
        # 设置默认超时
        self.context.set_default_timeout(30000)
        self.page = self.context.new_page()

    def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def login_douyin(self) -> bool:
        """登录抖音"""
        print("📱 正在检查登录状态...")
        
        try:
            self.page.goto("https://creator.douyin.com/", wait_until="domcontentloaded")
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            # 检测是否已登录（多种方式检测）
            page_content = self.page.content()
            
            # 检查是否有登录相关内容
            is_logged_in = True
            if "登录" in page_content and "扫码" in page_content:
                is_logged_in = False
            
            # 或者检查是否有发布/上传相关内容
            if "发布" not in page_content and "上传" not in page_content:
                # 尝试检查特定元素
                try:
                    self.page.wait_for_selector('.upload-area, .publish-entry, [class*="upload"]', timeout=3000)
                except:
                    is_logged_in = False
            
            if is_logged_in:
                print("✅ 抖音已登录（使用保存的 cookies）")
                return True
            
            # 需要扫码登录
            print("📱 请使用抖音 APP 扫描二维码登录")
            print("⏳ 等待扫码...（60 秒超时）")

            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_function(
                '() => document.querySelector(".login-container") === null',
                timeout=60000
            )
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)

            print("✅ 抖音登录成功")
            return True

        except PlaywrightTimeout:
            print("❌ 抖音登录超时")
            return False
        except Exception as e:
            print(f"❌ 抖音登录失败：{e}")
            return False

    def publish_douyin(self, video_path: str, title: str, tags: List[str], description: str = "") -> bool:
        """发布到抖音

        Args:
            video_path: 视频文件路径
            title: 标题
            tags: 标签列表
            description: 作品简介（可选）
        """
        print("📱 正在发布到抖音...")

        try:
            # 进入发布页面
            self.page.goto("https://creator.douyin.com/creator-micro/content/upload", wait_until="domcontentloaded")
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)

            # 等待上传按钮
            self.page.wait_for_selector('input[type="file"]', timeout=10000)

            # 上传视频
            file_input = self.page.query_selector('input[type="file"]')
            if file_input:
                file_input.set_input_files(video_path)
                print("📹 视频上传中...")

                # 等待标题输入框出现
                title_input = self.page.get_by_placeholder("填写作品标题")
                title_input.wait_for(state="visible", timeout=60000)
                time.sleep(2)

                # 填写标题（使用 keyboard.type 模拟真实输入）
                full_title = f"{title} {' '.join(['#' + t for t in tags[:5]])}"
                title_input.click()
                self.page.keyboard.type(full_title[:100])
                print(f"📝 标题已填写: {full_title[:20]}...")

                # 填写作品简介（如果有）
                if description:
                    try:
                        print("📄 正在填写作品简介...")
                        desc_input = self.page.get_by_placeholder("添加作品简介，让更多人看到你的作品")
                        desc_input.wait_for(state="visible", timeout=5000)
                        desc_input.click()
                        self.page.keyboard.type(description[:500])
                        print(f"✅ 简介已填写: {description[:30]}...")
                    except Exception as e:
                        print(f"⚠️ 简介填写跳过: {e}")

                # 设置封面（必须）
                print("🖼️ 正在设置封面...")
                try:
                    # 点击"选择封面", 等待弹窗容器出现
                    cover_btn = self.page.get_by_text("选择封面").first
                    cover_btn.wait_for(state="visible", timeout=10000)
                    cover_btn.click()
                    print("🖼️ 正在打开封面选择弹窗...")
                    
                    v_cover_btn = self.page.get_by_role("button", name=re.compile(r"设置[竖横]封面"))
                    v_cover_btn.wait_for(state="visible", timeout=15000)  # 给 15 秒，因为视频解析封面可能慢
                    
                    v_cover_btn.click()
                    print("📏 已选择竖/横封面")
                    
                    # 等待"完成"按钮, 强制等待一会儿，确保抖音的前端逻辑已经绑定好点击事件
                    done_btn = self.page.get_by_role("button", name="完成", exact=True).last
                    done_btn.wait_for(state="visible", timeout=10000)
                    
                    self.page.wait_for_timeout(1000)
                    done_btn.click()
                    
                    # 等待弹窗完全消失
                    v_cover_btn.wait_for(state="hidden", timeout=10000)
                    print("✨ 封面设置成功，弹窗已关闭")
                    
                except Exception as e:
                    print(f"⚠️ 封面设置跳过: {e}")
                    # 封面设置失败则继续发布，使用默认封面
                    pass

                # 等待发布按钮
                print("⏳ 等待视频处理完毕...")
                publish_btn = self.page.get_by_role("button", name="发布", exact=True)
                publish_btn.wait_for(state="visible", timeout=300000)

                # 点击发布
                if publish_btn.is_enabled():
                    publish_btn.click()
                    print("🚀 点击发布按钮")
                else:
                    publish_btn.click(force=True)
                    print("🚀 强制触发发布")

                time.sleep(2)

                # 检测验证码弹窗
                try:
                    popup = page.locator('.cancel-btn-zy_rHA, button:has-text("暂存离开")')
                    popup.wait_for(state="visible", timeout=5000)

                    popup.click()
                    print("VERIFY_BLOCKED: 已暂存为草稿")
                    return False
                except:
                    pass

                # 等待发布完成
                time.sleep(3)
                print("✅ 抖音视频已发布")
                return True

            print("❌ 抖音发布失败：未找到上传按钮")
            return False

        except Exception as e:
            print(f"❌ 抖音发布失败：{e}")
            # 截图留证
            self.page.screenshot(path="error_debug.png")
            return False

    def publish(self, video_path: str, title: str, tags: List[str],
                headless: bool = False, description: str = "") -> Dict:
        """发布视频到抖音

        Args:
            video_path: 视频文件路径
            title: 标题
            tags: 标签列表
            headless: 是否无头模式
            description: 作品简介
        """

        video_path = Path(video_path)
        if not video_path.exists():
            print(f"❌ 视频文件不存在：{video_path}")
            return {"success": False, "error": "File not found"}

        print(f"\n🦞 抖音发布助手")
        print(f"=" * 60)
        print(f"视频：{video_path.name}")
        print(f"标题：{title}")
        print(f"=" * 60)

        try:
            # 登录抖音
            print(f"\n📱 登录抖音...")
            self.start_browser(headless=headless, platform="douyin")
            if not self.login_douyin():
                self.results["douyin"] = False
            else:
                # 登录成功后保存 cookies
                self.save_cookies("douyin")

                # 发布视频
                success = self.publish_douyin(str(video_path), title, tags, description)
                self.results["douyin"] = success

            # 总结
            print(f"\n{'='*60}")
            print(f"📊 发布结果")
            print(f"{'='*60}")
            for platform, success in self.results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {platform}")

            return {
                "success": all(self.results.values()),
                "results": self.results,
                "timestamp": datetime.now().isoformat()
            }

        finally:
            self.close_browser()

def main():
    parser = argparse.ArgumentParser(description='🦞 抖音视频发布助手')
    parser.add_argument('video', help='视频文件路径')
    parser.add_argument('--title', required=True, help='视频标题（必填）')
    parser.add_argument('--tags', required=True, help='标签（逗号分隔，必填）')
    parser.add_argument('--description', '-d', default='', help='作品简介（可选）')
    parser.add_argument('--headless', action='store_true',
                       help='无头模式（不显示浏览器）')
    parser.add_argument('--config', default='config/accounts.json',
                       help='账号配置文件路径')

    args = parser.parse_args()

    # title 和 tags 是必填参数
    if not args.title or not args.tags:
        print("❌ 错误：--title 和 --tags 是必填参数")
        print("   示例：python scripts/auto_publisher.py video.mp4 --title '我的视频' --tags 'AI,科技'")
        sys.exit(1)

    tags = [tag.strip() for tag in args.tags.split(',')]

    # 简介默认为空
    description = args.description or ""

    # 创建发布器
    publisher = VideoPublisher(config_path=args.config)

    # 发布
    result = publisher.publish(
        video_path=args.video,
        title=args.title,
        tags=tags,
        headless=args.headless,
        description=description
    )

    # 保存发布记录
    log_file = Path('config/publish_log.json')
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logs = []
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)

    logs.append({
        'video': str(args.video),
        'title': args.title,
        'tags': tags,
        'result': result
    })

    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"\n📝 发布记录已保存：{log_file}")

    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
