#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频发布脚本
支持上传视频、设置标题话题、定时发布等功能
"""

import argparse
import asyncio
import faulthandler
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional
from platform_client import PlatformClientError, request_json

try:
    from playwright.async_api import async_playwright, Page, BrowserContext
except ImportError:
    print("错误：未安装 playwright")
    print("请运行：pip install playwright && playwright install chromium")
    sys.exit(1)


# Cookie 存储路径
COOKIE_DIR = Path(__file__).resolve().parent.parent / "cookies"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
DEFAULT_COOKIE_FILE = COOKIE_DIR / "douyin.json"
INVALID_COOKIE_NAME_CHARS = set('<>:"/\\|?*')
_LOG_FILE_HANDLE = None


class TeeStream:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()
        return len(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def isatty(self):
        return any(getattr(stream, "isatty", lambda: False)() for stream in self.streams)

    @property
    def encoding(self):
        for stream in self.streams:
            encoding = getattr(stream, "encoding", None)
            if encoding:
                return encoding
        return "utf-8"


def setup_runtime_logging() -> Path:
    global _LOG_FILE_HANDLE

    if _LOG_FILE_HANDLE is not None:
        return Path(_LOG_FILE_HANDLE.name)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"publish-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    _LOG_FILE_HANDLE = log_path.open("a", encoding="utf-8", buffering=1)

    sys.stdout = TeeStream(sys.__stdout__, _LOG_FILE_HANDLE)
    sys.stderr = TeeStream(sys.__stderr__, _LOG_FILE_HANDLE)

    try:
        faulthandler.enable(_LOG_FILE_HANDLE, all_threads=True)
    except Exception:
        pass

    def _log_uncaught_exception(exc_type, exc_value, exc_traceback):
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

    sys.excepthook = _log_uncaught_exception
    print(f"[log] publish log file: {log_path}")
    return log_path


def resolve_cookie_file(cookie_name: str = "") -> Path:
    raw_name = (cookie_name or "").strip()
    if not raw_name:
        return DEFAULT_COOKIE_FILE

    safe_name = "".join(
        "_" if char in INVALID_COOKIE_NAME_CHARS or ord(char) < 32 else char
        for char in raw_name
    ).rstrip(" .")
    if not safe_name:
        raise ValueError("Cookie 名称不能为空，且不能只包含非法文件名字符。")

    return COOKIE_DIR / f"douyin-{safe_name}.json"


def authorize_publish(
    *,
    title: str,
    video_path: str,
    cover_path: str | None,
    tags: list[str],
    schedule_time: str | None,
) -> str:
    payload = {
        "title": title,
        "video_file_name": Path(video_path).name,
        "cover_file_name": Path(cover_path).name if cover_path else None,
        "tags": tags,
        "schedule_time": schedule_time,
    }
    response = request_json("POST", "/skills/auto-douyin/publish/authorize", payload)
    grant_id = (response or {}).get("grant_id")
    if not grant_id:
        raise RuntimeError("Douyin publish authorization did not return grant_id.")
    return str(grant_id)


def report_publish_result(
    grant_id: str,
    status: str,
    detail: str | None = None,
    result_payload: dict | None = None,
) -> None:
    payload = {
        "grant_id": grant_id,
        "status": status,
        "detail": detail,
        "result_payload": result_payload or {},
    }
    try:
        request_json("POST", "/skills/auto-douyin/publish/report", payload)
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: failed to report publish result: {exc}", file=sys.stderr)


class DouyinUploader:
    """抖音视频上传器"""
    
    def __init__(
        self,
        video_path: str,
        title: str,
        tags: List[str] = None,
        cover_path: str = None,
        schedule_time: datetime = None,
        cookie_file: Path = DEFAULT_COOKIE_FILE,
        headless: bool = False
    ):
        self.video_path = Path(video_path)
        self.title = title[:30]  # 抖音标题最多30字
        self.tags = tags or []
        self.cover_path = Path(cover_path) if cover_path else None
        self.schedule_time = schedule_time
        self.cookie_file = Path(cookie_file)
        self.headless = headless
        
        # 验证文件
        if not self.video_path.exists():
            raise FileNotFoundError(f"视频文件不存在: {self.video_path}")
        if self.cover_path and not self.cover_path.exists():
            raise FileNotFoundError(f"封面文件不存在: {self.cover_path}")
    
    async def upload(self) -> bool:
        """执行上传"""
        
        print("=" * 60)
        print("抖音视频发布")
        print("=" * 60)
        print()
        print(f"视频文件: {self.video_path}")
        print(f"标题: {self.title}")
        print(f"话题: {', '.join(self.tags) if self.tags else '无'}")
        print(f"封面: {self.cover_path if self.cover_path else '自动选择'}")
        print(f"发布时间: {self.schedule_time.strftime('%Y-%m-%d %H:%M') if self.schedule_time else '立即发布'}")
        print()
        
        # 检查 Cookie
        if not self.cookie_file.exists():
            print("❌ Cookie 文件不存在，请先运行 get_cookie.py 获取登录凭证")
            return False
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            
            try:
                # 加载 Cookie
                context = await browser.new_context(storage_state=str(self.cookie_file))
                page = await context.new_page()
                
                # 进入上传页面
                print("[1/6] 打开抖音创作者中心...")
                await page.goto("https://creator.douyin.com/creator-micro/content/upload", timeout=120000)
                
                # 等待页面加载
                try:
                    await page.wait_for_url(
                        "https://creator.douyin.com/creator-micro/content/upload",
                        timeout=10000
                    )
                except:
                    pass
                
                # 检查登录状态
                if await page.get_by_text('手机号登录').count() > 0 or await page.get_by_text('扫码登录').count() > 0:
                    print("❌ Cookie 已失效，请重新运行 get_cookie.py 获取登录凭证")
                    await browser.close()
                    return False
                
                # 上传视频
                print("[2/6] 上传视频文件...")
                await self._set_initial_video_file(page)
                
                # 等待跳转到发布页面
                print("[3/6] 等待视频处理...")
                await self._wait_for_publish_page(page)
                
                # 等待视频上传完成
                await self._wait_for_upload_complete(page)
                
                # 设置封面（如果指定）
                if self.cover_path:
                    print("[4/6] 设置视频封面...")
                    await self._set_cover(page)
                else:
                    print("[4/6] 主动选择自动推荐封面...")
                    await self._set_recommended_cover(page)

                # 填写标题和话题
                print("[5/6] 填写标题和话题...")
                await self._fill_title_and_tags(page)
                
                # 设置定时发布（如果指定）
                if self.schedule_time:
                    print(f"[6/6] 设置定时发布: {self.schedule_time.strftime('%Y-%m-%d %H:%M')}...")
                    await self._set_schedule_time(page)
                else:
                    print("[6/6] 准备立即发布...")
                
                # 点击发布
                await self._publish(page)
                
                # 保存更新的 Cookie
                await context.storage_state(path=str(self.cookie_file))
                
                print()
                print("=" * 60)
                print("✅ 视频发布成功！")
                print("=" * 60)
                
                await asyncio.sleep(2)
                await browser.close()
                return True
                
            except Exception as e:
                print(f"❌ 发布失败: {e}")
                import traceback
                traceback.print_exc()
                await browser.close()
                return False

    async def _set_initial_video_file(self, page: Page) -> None:
        """只命中首次上传入口，避免落到“重新上传”区域。"""
        upload_input = await self._locate_initial_video_input(page)
        if upload_input is None:
            raise RuntimeError("Could not find the initial Douyin video upload input.")
        await upload_input.set_input_files(str(self.video_path))

    async def _locate_initial_video_input(self, page: Page):
        selectors = [
            "input[type='file']",
            "div[class^='container'] input",
        ]
        for selector in selectors:
            locator = page.locator(selector)
            count = await locator.count()
            for index in range(count):
                candidate = locator.nth(index)
                try:
                    is_initial = await candidate.evaluate(
                        """node => {
                            if (!(node instanceof HTMLInputElement)) return false;
                            const type = (node.getAttribute('type') || '').toLowerCase();
                            if (type && type !== 'file') return false;
                            const accept = (node.getAttribute('accept') || '').toLowerCase();
                            if (accept && !accept.includes('video')) return false;

                            let current = node;
                            while (current) {
                                const text = (current.textContent || '').replace(/\\s+/g, '');
                                if (text.includes('重新上传')) return false;
                                if (text.includes('上传失败')) return false;
                                current = current.parentElement;
                            }
                            return true;
                        }"""
                    )
                except Exception:
                    continue
                if is_initial:
                    return candidate
        return None
    
    async def _wait_for_publish_page(self, page: Page):
        """等待进入发布页面"""
        max_attempts = 60
        for _ in range(max_attempts):
            try:
                await page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page",
                    timeout=2000
                )
                return
            except:
                pass
            
            try:
                await page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/post/video?enter_from=publish_page",
                    timeout=2000
                )
                return
            except:
                pass
            
            await asyncio.sleep(0.5)
        
        raise TimeoutError("等待发布页面超时")
    
    async def _wait_for_upload_complete(self, page: Page):
        """等待视频上传完成"""
        max_attempts = 120  # 最多等待2分钟
        for i in range(max_attempts):
            # 检查是否出现"重新上传"按钮（表示上传完成）
            if await page.locator('[class^="long-card"] div:has-text("重新上传")').count() > 0:
                print("   视频上传完成")
                return
            
            # 检查上传失败
            if await page.locator('div.progress-div > div:has-text("上传失败")').count() > 0:
                raise Exception("视频上传失败，请检查文件格式")
            
            if i % 10 == 0:
                print(f"   正在上传... ({i}s)")
            await asyncio.sleep(1)
        
        raise TimeoutError("视频上传超时")
    
    async def _fill_title_and_tags(self, page: Page):
        """填写标题和话题"""
        await asyncio.sleep(1)
        
        # 尝试填写标题
        title_input = page.get_by_text('作品标题').locator("..").locator("xpath=following-sibling::div[1]").locator("input")
        if await title_input.count() > 0:
            await title_input.fill(self.title)
        else:
            # 备用方案：直接在编辑区域输入
            title_area = page.locator(".notranslate")
            await title_area.click()
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(self.title)
            await page.keyboard.press("Enter")
        
        # 填写话题标签
        if self.tags:
            css_selector = ".zone-container"
            for tag in self.tags:
                await page.type(css_selector, "#" + tag)
                await page.press(css_selector, "Space")
                await asyncio.sleep(0.3)
            print(f"   已添加 {len(self.tags)} 个话题")
    
    async def _set_cover(self, page: Page):
        """设置视频封面。"""
        try:
            await self._refresh_before_cover_setup(page)
            await self._click_cover_mode_with_retry(page, button_text="设置横封面")

            await page.locator(
                "div[class^='semi-upload upload'] >> input.semi-upload-hidden-input"
            ).set_input_files(str(self.cover_path))
            await asyncio.sleep(2)

            done_clicked = False
            for _ in range(3):
                done_button = page.get_by_role("button", name="完成")
                if await done_button.count() > 0:
                    await done_button.first.click(force=True)
                    done_clicked = True
                else:
                    legacy_done = page.locator("div#tooltip-container button:visible:has-text('完成')")
                    if await legacy_done.count() > 0:
                        await legacy_done.first.click(force=True)
                        done_clicked = True

                if done_clicked:
                    print("   封面设置完成")
                    break

                confirm_button = page.get_by_role("button", name="确定")
                if await confirm_button.count() > 0:
                    await confirm_button.first.click(force=True)
                    done_clicked = True
                    print("   封面设置完成（确定）")
                    break

                await asyncio.sleep(1)

            if not done_clicked:
                raise RuntimeError("未找到可点击的“完成”或“确定”按钮，无法确认封面设置")

            await self._wait_for_cover_dialog_closed(page)
            await page.wait_for_selector("div.extractFooter", state="detached", timeout=5000)
        except Exception as e:
            print(f"   封面设置失败: {e}，将使用自动推荐封面")
            await self._set_recommended_cover(page)

    async def _open_cover_dialog(self, page: Page) -> None:
        cover_btn = page.get_by_text("选择封面")
        if await cover_btn.count() == 0:
            raise RuntimeError("未找到“选择封面”按钮")
        await cover_btn.first.click()
        await page.wait_for_selector("div.dy-creator-content-modal", timeout=10000)

    async def _refresh_before_cover_setup(self, page: Page) -> None:
        print("   设置封面前刷新页面，等待封面按钮状态稳定...")
        await page.reload(timeout=120000, wait_until="domcontentloaded")
        await self._wait_for_publish_page(page)
        await self._wait_for_upload_complete(page)

    async def _wait_for_cover_mode_button(
        self,
        page: Page,
        button_text: str,
        timeout_ms: int = 10000,
    ):
        button = page.get_by_text(button_text).first
        deadline = asyncio.get_running_loop().time() + (timeout_ms / 1000)
        last_state = "not_found"

        while asyncio.get_running_loop().time() < deadline:
            if await button.count() > 0:
                try:
                    visible = await button.is_visible()
                except Exception:
                    visible = False

                if visible:
                    try:
                        clickable = await button.evaluate(
                            """node => {
                                const disabled = typeof node.matches === 'function' && node.matches(':disabled');
                                const attrDisabled = node.getAttribute('disabled') !== null;
                                const ariaDisabled = node.getAttribute('aria-disabled') === 'true';
                                const className = typeof node.className === 'string' ? node.className : '';
                                const hasDisabledClass = /(^|\\s)(disabled|disable)(\\s|$)/i.test(className);
                                return !(disabled || attrDisabled || ariaDisabled || hasDisabledClass);
                            }"""
                        )
                    except Exception:
                        try:
                            clickable = await button.is_enabled()
                        except Exception:
                            clickable = False

                    if clickable:
                        return button
                    last_state = "disabled"
                else:
                    last_state = "hidden"

            await asyncio.sleep(0.5)

        raise TimeoutError(f"{button_text} 按钮长时间不可点击，当前状态: {last_state}")

    async def _click_cover_mode_with_retry(
        self,
        page: Page,
        button_text: str,
        wait_timeout_ms: int = 10000,
        refresh_retries: int = 2,
    ) -> None:
        last_error: Exception | None = None

        for attempt in range(refresh_retries + 1):
            try:
                await self._open_cover_dialog(page)
                button = await self._wait_for_cover_mode_button(
                    page,
                    button_text,
                    timeout_ms=wait_timeout_ms,
                )
                await button.click()
                await asyncio.sleep(1)
                return
            except Exception as exc:
                last_error = exc
                if attempt >= refresh_retries:
                    break

                print(
                    f"   {button_text} 暂时不可点击，刷新页面后重试 "
                    f"({attempt + 1}/{refresh_retries})..."
                )
                await page.reload(timeout=120000, wait_until="domcontentloaded")
                await self._wait_for_publish_page(page)
                await self._wait_for_upload_complete(page)

        raise RuntimeError(f"无法点击{button_text}: {last_error}")

    async def _locator_is_visible(self, locator) -> bool:
        try:
            if await locator.count() == 0:
                return False
            return await locator.first.is_visible()
        except Exception:
            return False

    async def _click_cover_dialog_confirm(self, page: Page) -> bool:
        done_button = page.get_by_role("button", name="完成")
        if await self._locator_is_visible(done_button):
            await done_button.first.click(force=True)
            return True

        legacy_done = page.locator("div#tooltip-container button:visible:has-text('完成')")
        if await self._locator_is_visible(legacy_done):
            await legacy_done.first.click(force=True)
            return True

        confirm_button = page.get_by_role("button", name="确定")
        if await self._locator_is_visible(confirm_button):
            await confirm_button.first.click(force=True)
            return True

        legacy_confirm = page.locator("div#tooltip-container button:visible:has-text('确定')")
        if await self._locator_is_visible(legacy_confirm):
            await legacy_confirm.first.click(force=True)
            return True

        return False

    async def _wait_for_cover_dialog_closed(self, page: Page, timeout_ms: int = 15000) -> None:
        modal = page.locator("div.dy-creator-content-modal")
        footer = page.locator("div.extractFooter")
        deadline = asyncio.get_running_loop().time() + (timeout_ms / 1000)

        while asyncio.get_running_loop().time() < deadline:
            modal_visible = await self._locator_is_visible(modal)
            footer_visible = await self._locator_is_visible(footer)

            if not modal_visible and not footer_visible:
                print("   已确认封面设置弹窗关闭")
                return

            clicked = await self._click_cover_dialog_confirm(page)
            if clicked:
                await asyncio.sleep(1)
                continue

            await asyncio.sleep(0.5)

        raise TimeoutError("封面设置弹窗未关闭，封面设置未确认完成")

    async def _wait_for_recommended_cover_item(self, page: Page, timeout_ms: int = 10000):
        items = page.locator('[class^="recommendCover-"]')
        deadline = asyncio.get_running_loop().time() + (timeout_ms / 1000)

        while asyncio.get_running_loop().time() < deadline:
            if await items.count() > 0:
                first_item = items.first
                try:
                    if await first_item.is_visible():
                        return first_item
                except Exception:
                    pass
            await asyncio.sleep(0.5)

        raise TimeoutError("等待推荐封面项超时")

    async def _dismiss_cover_dialog(self, page: Page) -> bool:
        candidates = [
            page.get_by_role("button", name="取消"),
            page.get_by_role("button", name="关闭"),
            page.locator("div.dy-creator-content-modal [aria-label='关闭']"),
            page.locator("div.dy-creator-content-modal .semi-modal-close"),
            page.locator("div.dy-creator-content-modal [class*='close']").first,
        ]

        for candidate in candidates:
            try:
                if await self._locator_is_visible(candidate):
                    await candidate.first.click(force=True)
                    await asyncio.sleep(1)
                    if not await self._locator_is_visible(page.locator("div.dy-creator-content-modal")):
                        print("   已关闭封面设置弹窗")
                        return True
            except Exception:
                continue

        try:
            await page.keyboard.press("Escape")
            await asyncio.sleep(1)
            if not await self._locator_is_visible(page.locator("div.dy-creator-content-modal")):
                print("   已通过 Esc 关闭封面设置弹窗")
                return True
        except Exception:
            pass

        return False
    
    async def _set_schedule_time(self, page: Page):
        """设置定时发布"""
        # 点击定时发布
        label_element = page.locator("[class^='radio']:has-text('定时发布')")
        await label_element.click()
        await asyncio.sleep(1)
        
        # 格式化时间
        time_str = self.schedule_time.strftime("%Y-%m-%d %H:%M")
        
        # 输入时间
        await page.locator('.semi-input[placeholder="日期和时间"]').click()
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.type(time_str)
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)
    
    async def _set_recommended_cover(self, page: Page):
        """主动选择推荐封面。"""
        last_error: Exception | None = None

        for attempt in range(3):
            try:
                await self._refresh_before_cover_setup(page)
                try:
                    await self._click_cover_mode_with_retry(page, button_text="设置横封面")
                except Exception as horizontal_error:
                    print(f"   设置横封面失败，尝试设置竖封面: {horizontal_error}")
                    await self._click_cover_mode_with_retry(
                        page,
                        button_text="设置竖封面",
                        wait_timeout_ms=8000,
                        refresh_retries=1,
                    )

                recommend_item = await self._wait_for_recommended_cover_item(page, timeout_ms=12000)
                await recommend_item.click(force=True)
                await asyncio.sleep(1)

                confirmed = False
                done_btn = page.get_by_role("button", name="完成")
                if await done_btn.count() > 0:
                    await done_btn.first.click(force=True)
                    print("   已自动选择推荐封面并点击“完成”")
                    await asyncio.sleep(2)
                    confirmed = True
                else:
                    confirm_btn = page.get_by_role("button", name="确定")
                    if await confirm_btn.count() > 0:
                        await confirm_btn.first.click(force=True)
                        print("   已自动选择推荐封面并点击“确定”")
                        await asyncio.sleep(2)
                        confirmed = True

                if not confirmed:
                    raise RuntimeError("推荐封面已选中，但未找到可点击的确认按钮")

                await self._wait_for_cover_dialog_closed(page)
                return
            except Exception as e:
                last_error = e
                print(f"   主动设置封面失败，准备重试: {e}")
                await self._dismiss_cover_dialog(page)

        print(f"   主动设置封面失败，跳过封面预设置，后续由发布阶段兜底: {last_error}")

    async def _publish(self, page: Page):
        """点击发布按钮"""
        max_attempts = 30
        for _ in range(max_attempts):
            try:
                publish_button = page.get_by_role('button', name="发布", exact=True)
                if await publish_button.count() > 0:
                    await publish_button.click()
                
                # 等待跳转到管理页面（表示发布成功）
                await page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/manage**",
                    timeout=5000
                )
                return
            except:
                # 处理封面提示
                await self._handle_cover_prompt(page)
                await asyncio.sleep(1)
        
        raise TimeoutError("发布超时")
    
    async def _handle_cover_prompt(self, page: Page):
        """处理封面设置提示"""
        try:
            if page.is_closed():
                return
            
            cover_warning = page.get_by_text("请设置封面后再发布").first
            if await cover_warning.count() > 0 and await cover_warning.is_visible():
                print("   检测到需要设置封面，正在选择推荐封面...")
                recommend_cover = page.locator('[class^="recommendCover-"]').first
                if await recommend_cover.count() > 0:
                    await recommend_cover.click()
                    await asyncio.sleep(1)
                    
                    # 处理确认弹窗
                    confirm_btn = page.get_by_role("button", name="确定")
                    if await confirm_btn.count() > 0 and await confirm_btn.is_visible():
                        await confirm_btn.click()
                        await asyncio.sleep(1)
        except Exception as e:
            print(f"   处理封面提示时发生非致命错误: {e}")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="抖音视频自动发布")
    
    parser.add_argument(
        "-v", "--video",
        required=True,
        help="视频文件路径"
    )
    parser.add_argument(
        "-t", "--title",
        required=True,
        help="视频标题（最多30字）"
    )
    parser.add_argument(
        "-g", "--tags",
        default="",
        help="话题标签，逗号分隔（如：干货分享,效率提升）"
    )
    parser.add_argument(
        "-c", "--cover",
        default=None,
        help="封面图片路径（可选，不指定则自动选择）"
    )
    parser.add_argument(
        "-s", "--schedule",
        default=None,
        help="定时发布时间，格式：YYYY-MM-DD HH:MM（可选，不指定则立即发布）"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="无头模式运行（不显示浏览器窗口）"
    )
    
    parser.add_argument(
        "--guarded-grant-id",
        default="",
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--cookie-name",
        default="",
        help="可选 Cookie 档案名；不传时使用默认 douyin.json"
    )

    return parser.parse_args()


def main():
    log_path = setup_runtime_logging()
    print(f"[log] publish started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    args = parse_args()
    
    try:
        cookie_file = resolve_cookie_file(args.cookie_name)
    except ValueError as exc:
        print(f"错误：{exc}")
        sys.exit(1)
    
    # 解析话题
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    
    # 解析定时发布时间
    schedule_time = None
    if args.schedule:
        try:
            schedule_time = datetime.strptime(args.schedule, "%Y-%m-%d %H:%M")
        except ValueError:
            print(f"❌ 时间格式错误，应为 YYYY-MM-DD HH:MM，例如：2025-02-01 18:00")
            sys.exit(1)
    
    grant_id = str(args.guarded_grant_id or "").strip()
    if not grant_id:
        try:
            grant_id = authorize_publish(
                title=args.title,
                video_path=args.video,
                cover_path=args.cover,
                tags=tags,
                schedule_time=args.schedule,
            )
        except PlatformClientError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"Failed to authorize Douyin publish: {exc}", file=sys.stderr)
            sys.exit(1)

    try:
        uploader = DouyinUploader(
            video_path=args.video,
            title=args.title,
            tags=tags,
            cover_path=args.cover,
            schedule_time=schedule_time,
            cookie_file=cookie_file,
            headless=args.headless
        )
        
        success = asyncio.run(uploader.upload())
        print(f"[log] publish finished with success={success}")
        if success:
            report_publish_result(
                grant_id,
                "success",
                result_payload={"video_file_name": Path(args.video).name},
            )
            sys.exit(0)
        report_publish_result(
            grant_id,
            "failed",
            detail="Local publish returned unsuccessful status.",
            result_payload={"video_file_name": Path(args.video).name},
        )
        sys.exit(1)
        
    except FileNotFoundError as e:
        if grant_id:
            report_publish_result(
                grant_id,
                "failed",
                detail=str(e),
                result_payload={"stage": "validation"},
            )
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        if grant_id:
            report_publish_result(
                grant_id,
                "failed",
                detail=str(e),
                result_payload={"stage": "publish"},
            )
        print(f"❌ 发生错误: {e}")
        print(f"[log] exception log file: {log_path}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
