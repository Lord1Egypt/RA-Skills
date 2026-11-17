"""
browser-smart-click: 智能点击封装层
解决 Playwright 点击被遮挡元素时的失败问题。

功能：
- 遮挡检测：使用 elementFromPoint 检测遮挡元素
- 智能点击：自动检测遮挡并报告
- 自动重试：尝试关闭遮挡元素后重试
- 等待策略：智能等待元素可交互
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class BlockerInfo:
    """遮挡元素信息"""
    tag: str = ""
    class_name: str = ""
    text: str = ""
    bounding_box: Optional[dict] = None
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def summary(self) -> str:
        """返回人类可读的遮挡描述"""
        parts = [f"<{self.tag}"]
        if self.class_name:
            parts[0] += f' class="{self.class_name}"'
        parts[0] += ">"
        if self.text:
            parts.append(f' text="{self.text[:50]}"')
        return "".join(parts)


@dataclass
class ClickResult:
    """点击操作结果"""
    success: bool = False
    target: dict = field(default_factory=dict)  # {"selector": "...", "text": "..."}
    blocked: bool = False
    blocker: Optional[dict] = None  # BlockerInfo.to_dict() or None
    retry_count: int = 0
    message: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ---------------------------------------------------------------------------
# JS snippets injected into the page
# ---------------------------------------------------------------------------

_JS_DETECT_BLOCKER = """
(x, y) => {
    const topEl = document.elementFromPoint(x, y);
    if (!topEl) return null;
    const rect = topEl.getBoundingClientRect();
    return {
        tag: topEl.tagName.toLowerCase(),
        className: topEl.className || '',
        text: (topEl.innerText || topEl.textContent || '').trim().substring(0, 200),
        boundingBox: {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height
        },
        attributes: Object.fromEntries(
            Array.from(topEl.attributes).map(a => [a.name, a.value])
        )
    };
}
"""

_JS_IS_VISIBLE = """
(selector) => {
    const el = document.querySelector(selector);
    if (!el) return false;
    const style = window.getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0')
        return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
}
"""

_JS_FIND_CLOSE_BUTTON = """
(containerSelector) => {
    const container = document.querySelector(containerSelector);
    if (!container) return null;
    // 常见关闭按钮选择器
    const closeSelectors = [
        'button[aria-label*="close" i]',
        'button[aria-label*="Close" i]',
        'button[aria-label*="关闭"]',
        '[class*="close" i]',
        '[class*="dismiss" i]',
        'button × ',
        'button .close-icon',
        '.modal-close',
        '.dialog-close',
    ];
    for (const sel of closeSelectors) {
        const btn = container.querySelector(sel);
        if (btn) return sel;
    }
    // 查找包含 × 或 Close 文字的按钮
    const buttons = container.querySelectorAll('button, [role="button"], a');
    for (const btn of buttons) {
        const text = (btn.textContent || '').trim();
        if (text === '×' || text === 'x' || text === 'X' || text === '✕' ||
            text.toLowerCase() === 'close' || text === '关闭') {
            return null; // 返回 null 但标记找到文字匹配
        }
    }
    return null;
}
"""

_JS_FIND_ACCEPT_BUTTON = """
(containerSelector) => {
    const container = document.querySelector(containerSelector);
    if (!container) return null;
    const acceptTexts = ['accept', 'agree', 'allow', 'got it', 'ok', 'i agree',
                         '同意', '接受', '允许', '我知道了', '确定'];
    const buttons = container.querySelectorAll('button, [role="button"], a');
    for (const btn of buttons) {
        const text = (btn.textContent || '').trim().toLowerCase();
        for (const accept of acceptTexts) {
            if (text.includes(accept.toLowerCase())) {
                return true;
            }
        }
    }
    return null;
}
"""


# ---------------------------------------------------------------------------
# SmartClick class
# ---------------------------------------------------------------------------

class SmartClick:
    """
    智能点击管理器。

    用法：
        from smart_click import SmartClick
        sc = SmartClick()
        result = await sc.click(page, '#submit-btn')
        print(result.to_json())
    """

    # 常见遮挡元素的 CSS 选择器模式
    COOKIE_BANNER_SELECTORS = [
        '[class*="cookie" i]',
        '[id*="cookie" i]',
        '[class*="consent" i]',
        '[id*="consent" i]',
        '[class*="gdpr" i]',
        '[data-testid*="cookie" i]',
        '[role="dialog"][class*="banner" i]',
    ]

    MODAL_SELECTORS = [
        '[role="dialog"]',
        '[class*="modal" i]',
        '[class*="overlay" i]',
        '[class*="popup" i]',
        '[class*="dialog" i]',
        '.mfp-wrap',
        '.lightbox',
    ]

    def __init__(self, auto_dismiss: bool = True, max_retries: int = 3,
                 retry_delay_ms: int = 500):
        self.auto_dismiss = auto_dismiss
        self.max_retries = max_retries
        self.retry_delay_ms = retry_delay_ms

    async def click(self, page, selector: str, **options) -> ClickResult:
        """
        智能点击入口。

        Args:
            page: Playwright Page 对象
            selector: CSS 选择器
            **options:
                timeout (int): 等待超时 ms，默认 10000
                force (bool): 强制点击（跳过遮挡检测），默认 False
                position (dict): 点击位置 {"x": ..., "y": ...}
                auto_dismiss (bool): 是否自动关闭遮挡元素，默认 True

        Returns:
            ClickResult
        """
        timeout = options.get("timeout", 10000)
        force = options.get("force", False)
        position = options.get("position")
        auto_dismiss = options.get("auto_dismiss", self.auto_dismiss)

        result = ClickResult(target={"selector": selector, "text": ""})

        try:
            # 等待元素存在
            await page.wait_for_selector(selector, timeout=timeout, state="attached")

            # 获取元素信息
            element = await page.query_selector(selector)
            if not element:
                result.message = f"Element not found: {selector}"
                return result

            text = await element.text_content() or ""
            result.target["text"] = text.strip()[:100]

            # 等待元素可见
            try:
                await element.wait_for_element_state("visible", timeout=timeout)
            except Exception:
                result.message = f"Element not visible: {selector}"
                return result

            # 获取元素位置
            box = await element.bounding_box()
            if not box:
                result.message = f"Element has no bounding box: {selector}"
                return result

            # 计算点击坐标
            if position:
                click_x = box["x"] + position.get("x", box["width"] / 2)
                click_y = box["y"] + position.get("y", box["height"] / 2)
            else:
                click_x = box["x"] + box["width"] / 2
                click_y = box["y"] + box["height"] / 2

            # 遮挡检测
            blocker_info = await self._detect_blocker(page, click_x, click_y, selector)

            if blocker_info and not force:
                result.blocked = True
                result.blocker = blocker_info.to_dict()
                result.message = f"Element blocked by: {blocker_info.summary()}"

                # 尝试自动关闭遮挡元素
                if auto_dismiss:
                    for attempt in range(self.max_retries):
                        result.retry_count = attempt + 1
                        dismissed = await self._auto_dismiss_blocker(page, blocker_info)

                        if dismissed:
                            logger.info(f"Blocker dismissed on attempt {attempt + 1}")
                            await asyncio.sleep(self.retry_delay_ms / 1000)

                            # 重新检测遮挡
                            new_blocker = await self._detect_blocker(
                                page, click_x, click_y, selector
                            )
                            if not new_blocker:
                                # 遮挡已清除，执行点击
                                await self._do_click(page, selector, click_x, click_y)
                                result.success = True
                                result.blocked = False
                                result.blocker = None
                                result.message = (
                                    f"Clicked successfully after dismissing blocker "
                                    f"(retry #{attempt + 1})"
                                )
                                return result
                            else:
                                blocker_info = new_blocker
                                result.blocker = new_blocker.to_dict()
                                result.message = (
                                    f"Still blocked after dismiss attempt "
                                    f"#{attempt + 1}: {new_blocker.summary()}"
                                )
                        else:
                            result.message = (
                                f"Failed to dismiss blocker on attempt "
                                f"#{attempt + 1}: {blocker_info.summary()}"
                            )

                return result
            else:
                # 无遮挡或强制点击
                await self._do_click(page, selector, click_x, click_y)
                result.success = True
                result.message = "Clicked successfully"
                return result

        except Exception as e:
            result.message = f"Click failed: {str(e)}"
            return result

    async def wait_for_clickable(self, page, selector: str,
                                 timeout: int = 10000) -> bool:
        """
        等待元素可见且不被遮挡。

        Args:
            page: Playwright Page 对象
            selector: CSS 选择器
            timeout: 超时 ms

        Returns:
            True 如果元素在超时前变为可点击
        """
        deadline = asyncio.get_event_loop().time() + timeout / 1000

        while asyncio.get_event_loop().time() < deadline:
            try:
                element = await page.query_selector(selector)
                if not element:
                    await asyncio.sleep(0.2)
                    continue

                # 检查可见性
                is_visible = await page.evaluate(_JS_IS_VISIBLE, selector)
                if not is_visible:
                    await asyncio.sleep(0.2)
                    continue

                # 检查遮挡
                box = await element.bounding_box()
                if not box:
                    await asyncio.sleep(0.2)
                    continue

                cx = box["x"] + box["width"] / 2
                cy = box["y"] + box["height"] / 2
                blocker = await self._detect_blocker(page, cx, cy, selector)
                if not blocker:
                    return True

            except Exception:
                pass

            await asyncio.sleep(0.3)

        return False

    async def click_with_retry(self, page, selector: str,
                               max_retries: int = 3, **options) -> ClickResult:
        """
        带重试的点击。每次重试前尝试不同的策略。

        策略顺序：
        1. 正常点击
        2. 滚动到元素后点击
        3. 使用 JavaScript 点击（最后手段）

        Args:
            page: Playwright Page 对象
            selector: CSS 选择器
            max_retries: 最大重试次数
            **options: 传递给 click() 的选项

        Returns:
            ClickResult
        """
        options["auto_dismiss"] = options.get("auto_dismiss", self.auto_dismiss)
        last_result = None

        for attempt in range(max_retries + 1):
            result = await self.click(page, selector, **options)
            last_result = result

            if result.success:
                return result

            if attempt == 0 and result.blocked:
                # 第一次失败且有遮挡 → click() 内部已尝试 auto_dismiss
                # 继续到滚动策略
                pass

            if attempt == 1:
                # 策略2：滚动到元素
                try:
                    await page.evaluate(
                        """(sel) => {
                            const el = document.querySelector(sel);
                            if (el) el.scrollIntoView({behavior: 'smooth', block: 'center'});
                        }""",
                        selector
                    )
                    await asyncio.sleep(0.5)
                except Exception:
                    pass
                continue

            if attempt == 2:
                # 策略3：JavaScript 点击
                try:
                    await page.evaluate(
                        """(sel) => {
                            const el = document.querySelector(sel);
                            if (el) el.click();
                        }""",
                        selector
                    )
                    await asyncio.sleep(0.3)
                    # 验证点击是否生效（简单检查：元素是否还存在且可见）
                    is_visible = await page.evaluate(_JS_IS_VISIBLE, selector)
                    if not is_visible:
                        result.success = True
                        result.message = "Clicked via JavaScript (element no longer visible)"
                        return result
                except Exception as e:
                    result.message = f"JavaScript click failed: {str(e)}"

            await asyncio.sleep(self.retry_delay_ms / 1000)

        return last_result or ClickResult(
            target={"selector": selector, "text": ""},
            message="All retry attempts exhausted"
        )

    # -----------------------------------------------------------------------
    # Internal methods
    # -----------------------------------------------------------------------

    async def _detect_blocker(self, page, x: float, y: float,
                              target_selector: str) -> Optional[BlockerInfo]:
        """
        检测指定坐标是否有遮挡元素。

        如果 elementFromPoint 返回的元素是目标元素本身或其子元素，
        则不算遮挡。
        """
        try:
            blocker_data = await page.evaluate(_JS_DETECT_BLOCKER, x, y)
            if not blocker_data:
                return None

            # 检查是否是目标元素本身或其子元素
            is_target = await page.evaluate(
                """([x, y, sel]) => {
                    const topEl = document.elementFromPoint(x, y);
                    const targetEl = document.querySelector(sel);
                    if (!topEl || !targetEl) return false;
                    return targetEl === topEl || targetEl.contains(topEl);
                }""",
                [x, y, target_selector]
            )

            if is_target:
                return None

            # 构建 BlockerInfo
            blocker = BlockerInfo(
                tag=blocker_data.get("tag", ""),
                class_name=blocker_data.get("className", ""),
                text=blocker_data.get("text", ""),
                bounding_box=blocker_data.get("boundingBox"),
                attributes=blocker_data.get("attributes", {}),
            )
            return blocker

        except Exception as e:
            logger.debug(f"Blocker detection failed: {e}")
            return None

    async def _auto_dismiss_blocker(self, page,
                                    blocker: BlockerInfo) -> bool:
        """
        尝试自动关闭遮挡元素。

        策略：
        1. 检测是否为 cookie banner → 点击 Accept
        2. 检测是否为 modal → 点击关闭按钮
        3. 检测是否为 fixed header → 滚动页面
        4. 通用：尝试按 Escape
        """
        # 策略1：Cookie banner
        if self._is_cookie_banner(blocker):
            return await self._dismiss_cookie_banner(page, blocker)

        # 策略2：Modal / Dialog
        if self._is_modal(blocker):
            return await self._dismiss_modal(page, blocker)

        # 策略3：Fixed header / sticky element
        if self._is_fixed_element(blocker):
            return await self._dismiss_fixed_element(page, blocker)

        # 策略4：通用 - 尝试 Escape
        try:
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.3)
            return True  # 假设成功，由调用方重新检测
        except Exception:
            return False

    async def _dismiss_cookie_banner(self, page,
                                     blocker: BlockerInfo) -> bool:
        """关闭 cookie banner"""
        # 查找包含 cookie/consent 的容器
        for sel in self.COOKIE_BANNER_SELECTORS:
            try:
                has_accept = await page.evaluate(_JS_FIND_ACCEPT_BUTTON, sel)
                if has_accept:
                    # 找到 accept 按钮，点击它
                    await page.evaluate(
                        """(sel) => {
                            const container = document.querySelector(sel);
                            if (!container) return;
                            const acceptTexts = ['accept', 'agree', 'allow', 'got it',
                                                 'ok', 'i agree', '同意', '接受', '允许',
                                                 '我知道了', '确定'];
                            const buttons = container.querySelectorAll('button, [role="button"], a');
                            for (const btn of buttons) {
                                const text = (btn.textContent || '').trim().toLowerCase();
                                for (const accept of acceptTexts) {
                                    if (text.includes(accept.toLowerCase())) {
                                        btn.click();
                                        return;
                                    }
                                }
                            }
                        }""",
                        sel
                    )
                    await asyncio.sleep(0.3)
                    return True
            except Exception:
                continue

        # 如果找不到特定容器，在整个页面搜索
        try:
            await page.evaluate("""
                () => {
                    const acceptTexts = ['accept', 'agree', 'allow', 'got it',
                                         'ok', 'i agree', '同意', '接受', '允许'];
                    const buttons = document.querySelectorAll('button, [role="button"], a');
                    for (const btn of buttons) {
                        const text = (btn.textContent || '').trim().toLowerCase();
                        for (const accept of acceptTexts) {
                            if (text.includes(accept.toLowerCase())) {
                                // 检查按钮是否在 cookie 相关容器内
                                const parent = btn.closest('[class*="cookie" i], [id*="cookie" i], [class*="consent" i]');
                                if (parent) {
                                    btn.click();
                                    return;
                                }
                            }
                        }
                    }
                }
            """)
            await asyncio.sleep(0.3)
            return True
        except Exception:
            return False

    async def _dismiss_modal(self, page, blocker: BlockerInfo) -> bool:
        """关闭 modal"""
        for sel in self.MODAL_SELECTORS:
            try:
                # 查找关闭按钮
                close_btn_sel = await page.evaluate(_JS_FIND_CLOSE_BUTTON, sel)
                if close_btn_sel:
                    await page.click(f"{sel} {close_btn_sel}", timeout=2000)
                    await asyncio.sleep(0.3)
                    return True

                # 尝试通过文字匹配点击关闭按钮
                clicked = await page.evaluate(
                    """(sel) => {
                        const container = document.querySelector(sel);
                        if (!container) return false;
                        const buttons = container.querySelectorAll('button, [role="button"], a');
                        for (const btn of buttons) {
                            const text = (btn.textContent || '').trim();
                            if (text === '×' || text === 'x' || text === 'X' ||
                                text === '✕' || text.toLowerCase() === 'close' ||
                                text === '关闭') {
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    }""",
                    sel
                )
                if clicked:
                    await asyncio.sleep(0.3)
                    return True
            except Exception:
                continue

        # 通用：按 Escape
        try:
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.3)
            return True
        except Exception:
            return False

    async def _dismiss_fixed_element(self, page,
                                     blocker: BlockerInfo) -> bool:
        """处理 fixed header 等固定元素"""
        try:
            # 向下滚动一段距离，让目标元素移出 fixed header 范围
            await page.evaluate("""
                () => {
                    window.scrollBy({top: 100, behavior: 'smooth'});
                }
            """)
            await asyncio.sleep(0.5)
            return True
        except Exception:
            return False

    async def _do_click(self, page, selector: str, x: float, y: float):
        """执行实际点击"""
        element = await page.query_selector(selector)
        box = await element.bounding_box()
        rel_x = x - box["x"]
        rel_y = y - box["y"]
        await page.click(selector, position={"x": rel_x, "y": rel_y}, timeout=5000)

    # -----------------------------------------------------------------------
    # Classification helpers
    # -----------------------------------------------------------------------

    def _is_cookie_banner(self, blocker: BlockerInfo) -> bool:
        cls = blocker.class_name.lower()
        tag = blocker.tag.lower()
        attrs = " ".join(f"{k}={v}" for k, v in blocker.attributes.items()).lower()
        text = blocker.text.lower()

        keywords = ["cookie", "consent", "gdpr", "privacy-banner", "cc-banner"]
        return any(kw in cls or kw in attrs for kw in keywords) or \
               (any(kw in text for kw in ["cookie", "consent"]) and
                tag in ("div", "section", "aside", "footer"))

    def _is_modal(self, blocker: BlockerInfo) -> bool:
        cls = blocker.class_name.lower()
        attrs = " ".join(f"{k}={v}" for k, v in blocker.attributes.items()).lower()
        role = blocker.attributes.get("role", "").lower()

        if role == "dialog":
            return True
        keywords = ["modal", "dialog", "popup", "overlay", "lightbox",
                     "mfp", "fancybox"]
        return any(kw in cls or kw in attrs for kw in keywords)

    def _is_fixed_element(self, blocker: BlockerInfo) -> bool:
        attrs = blocker.attributes
        # 检查 style 中是否有 position: fixed/sticky
        style = attrs.get("style", "").lower().replace(" ", "")
        cls = blocker.class_name.lower()

        if "position:fixed" in style or "position:sticky" in style:
            return True
        fixed_keywords = ["fixed-header", "sticky-header", "fixed-nav",
                          "sticky-nav", "navbar-fixed"]
        return any(kw in cls for kw in fixed_keywords)


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

async def smart_click(page, selector: str, **options) -> ClickResult:
    """
    便捷函数：一行调用智能点击。

    用法：
        result = await smart_click(page, '#submit-btn')
        if result.success:
            print("Clicked!")
        else:
            print(f"Failed: {result.message}")
    """
    sc = SmartClick()
    return await sc.click(page, selector, **options)


async def wait_for_clickable(page, selector: str, timeout: int = 10000) -> bool:
    """便捷函数：等待元素可点击。"""
    sc = SmartClick()
    return await sc.wait_for_clickable(page, selector, timeout)


# ---------------------------------------------------------------------------
# CLI entry point (for standalone usage)
# ---------------------------------------------------------------------------

def main():
    """命令行入口（演示用途）"""
    import sys

    print("browser-smart-click - 智能点击工具")
    print("=" * 40)
    print()
    print("用法（在 Python 中导入）：")
    print("  from smart_click import SmartClick, smart_click, wait_for_clickable")
    print()
    print("  # 异步使用")
    print("  result = await smart_click(page, '#button')")
    print("  print(result.to_json())")
    print()
    print("  # 等待可点击")
    print("  clickable = await wait_for_clickable(page, '#button', timeout=5000)")
    print()

    if "--demo" in sys.argv:
        print("Demo mode requires a running browser. Use programmatically.")


if __name__ == "__main__":
    main()
