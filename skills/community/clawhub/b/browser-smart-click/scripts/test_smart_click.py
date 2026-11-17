"""
browser-smart-click 测试用例

使用 pytest + pytest-asyncio + unittest.mock 模拟 Playwright Page 对象。
无需真实浏览器即可验证核心逻辑。

运行方式：
    pytest test_smart_click.py -v
"""

import asyncio
import json
import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import asdict

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from smart_click import (
    SmartClick,
    ClickResult,
    BlockerInfo,
    smart_click,
    wait_for_clickable,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_element():
    """模拟 Playwright ElementHandle"""
    elem = AsyncMock()
    elem.text_content = AsyncMock(return_value="Submit Button")
    elem.wait_for_element_state = AsyncMock()
    elem.bounding_box = AsyncMock(return_value={
        "x": 100, "y": 200, "width": 120, "height": 40
    })
    return elem


@pytest.fixture
def mock_page(mock_element):
    """模拟 Playwright Page 对象"""
    page = AsyncMock()
    page.wait_for_selector = AsyncMock(return_value=mock_element)
    page.query_selector = AsyncMock(return_value=mock_element)
    page.click = AsyncMock()
    page.keyboard = MagicMock()
    page.keyboard.press = AsyncMock()

    # 默认：elementFromPoint 返回目标元素本身（无遮挡）
    page.evaluate = AsyncMock(return_value=None)

    return page


@pytest.fixture
def smart_click_instance():
    return SmartClick(auto_dismiss=True, max_retries=3, retry_delay_ms=10)


# ---------------------------------------------------------------------------
# Test: 正常点击
# ---------------------------------------------------------------------------

class TestNormalClick:
    """测试正常点击场景"""

    @pytest.mark.asyncio
    async def test_click_success_no_blocker(self, mock_page, mock_element,
                                             smart_click_instance):
        """正常点击：无遮挡时直接成功"""
        # elementFromPoint 返回 null（无遮挡）
        mock_page.evaluate = AsyncMock(side_effect=self._evaluate_no_blocker)

        result = await smart_click_instance.click(mock_page, "#submit-btn")

        assert result.success is True
        assert result.blocked is False
        assert result.blocker is None
        assert result.retry_count == 0
        assert "Clicked successfully" in result.message
        assert result.target["selector"] == "#submit-btn"

    @pytest.mark.asyncio
    async def test_click_success_returns_text(self, mock_page, mock_element,
                                               smart_click_instance):
        """正常点击：返回元素文本"""
        mock_element.text_content = AsyncMock(return_value="  Submit Form  ")
        mock_page.evaluate = AsyncMock(side_effect=self._evaluate_no_blocker)

        result = await smart_click_instance.click(mock_page, "#submit-btn")

        assert result.success is True
        assert result.target["text"] == "Submit Form"

    @pytest.mark.asyncio
    async def test_click_force_ignores_blocker(self, mock_page, mock_element,
                                                smart_click_instance):
        """强制点击：忽略遮挡直接点击"""
        # 模拟有遮挡
        mock_page.evaluate = AsyncMock(side_effect=self._evaluate_with_blocker)

        result = await smart_click_instance.click(
            mock_page, "#submit-btn", force=True
        )

        assert result.success is True
        assert result.blocked is False

    @staticmethod
    async def _evaluate_no_blocker(js, *args):
        """模拟：elementFromPoint 返回 null（无遮挡）"""
        # is_target check (contains querySelector + targetEl)
        if "querySelector" in js and "targetEl" in js:
            return True  # is the target itself
        # detect blocker (elementFromPoint without targetEl)
        if "elementFromPoint" in js and "targetEl" not in js:
            return None  # no blocker
        return None

    @staticmethod
    async def _evaluate_with_blocker(js, *args):
        """模拟：elementFromPoint 返回遮挡元素"""
        # is_target check
        if "querySelector" in js and "targetEl" in js:
            return False  # not the target
        # detect blocker
        if "elementFromPoint" in js and "targetEl" not in js:
            return {
                "tag": "div",
                "className": "cookie-banner",
                "text": "We use cookies",
                "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 100},
                "attributes": {"class": "cookie-banner", "id": "cookie-consent"}
            }
        return None


# ---------------------------------------------------------------------------
# Test: 遮挡检测
# ---------------------------------------------------------------------------

class TestBlockerDetection:
    """测试遮挡检测逻辑"""

    @pytest.mark.asyncio
    async def test_detect_cookie_banner(self, mock_page, smart_click_instance):
        """遮挡检测：识别 cookie banner"""
        mock_page.evaluate = AsyncMock(side_effect=self._evaluate_cookie_banner)

        blocker = await smart_click_instance._detect_blocker(
            mock_page, 160, 220, "#submit-btn"
        )

        assert blocker is not None
        assert blocker.tag == "div"
        assert "cookie" in blocker.class_name.lower()
        assert blocker.text == "We use cookies to improve your experience"

    @pytest.mark.asyncio
    async def test_detect_modal_overlay(self, mock_page, smart_click_instance):
        """遮挡检测：识别 modal overlay"""
        mock_page.evaluate = AsyncMock(side_effect=self._evaluate_modal)

        blocker = await smart_click_instance._detect_blocker(
            mock_page, 400, 300, "#content"
        )

        assert blocker is not None
        assert blocker.tag == "div"
        assert blocker.attributes.get("role") == "dialog"

    @pytest.mark.asyncio
    async def test_no_blocker_when_target_itself(self, mock_page,
                                                  smart_click_instance):
        """遮挡检测：elementFromPoint 返回目标本身不算遮挡"""
        mock_page.evaluate = AsyncMock(side_effect=self._evaluate_target_self)

        blocker = await smart_click_instance._detect_blocker(
            mock_page, 160, 220, "#submit-btn"
        )

        assert blocker is None

    @pytest.mark.asyncio
    async def test_blocker_info_summary(self):
        """BlockerInfo 摘要格式"""
        info = BlockerInfo(
            tag="div",
            class_name="cookie-banner",
            text="Accept cookies",
            bounding_box={"x": 0, "y": 0, "width": 800, "height": 100}
        )
        summary = info.summary()
        assert "<div" in summary
        assert "cookie-banner" in summary
        assert "Accept cookies" in summary

    @staticmethod
    async def _evaluate_cookie_banner(js, *args):
        # is_target check (contains querySelector + targetEl)
        if "querySelector" in js and "targetEl" in js:
            return False
        # detect blocker
        if "elementFromPoint" in js and "targetEl" not in js:
            return {
                "tag": "div",
                "className": "cookie-banner",
                "text": "We use cookies to improve your experience",
                "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 100},
                "attributes": {"class": "cookie-banner"}
            }
        return None

    @staticmethod
    async def _evaluate_modal(js, *args):
        # is_target check
        if "querySelector" in js and "targetEl" in js:
            return False
        # detect blocker
        if "elementFromPoint" in js and "targetEl" not in js:
            return {
                "tag": "div",
                "className": "modal-overlay",
                "text": "Sign up for our newsletter",
                "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 600},
                "attributes": {"class": "modal-overlay", "role": "dialog"}
            }
        return None

    @staticmethod
    async def _evaluate_target_self(js, *args):
        # is_target check
        if "querySelector" in js and "targetEl" in js:
            return True  # is the target itself
        # detect blocker
        if "elementFromPoint" in js and "targetEl" not in js:
            return {
                "tag": "button",
                "className": "submit-btn",
                "text": "Submit",
                "boundingBox": {"x": 100, "y": 200, "width": 120, "height": 40},
                "attributes": {}
            }
        return None


# ---------------------------------------------------------------------------
# Test: Cookie Banner 自动关闭
# ---------------------------------------------------------------------------

class TestCookieBannerDismiss:
    """测试 cookie banner 自动关闭"""

    @pytest.mark.asyncio
    async def test_dismiss_cookie_banner_by_class(self, mock_page,
                                                   smart_click_instance):
        """自动关闭：通过 class 名找到 cookie banner 并点击 Accept"""
        dismiss_calls = []

        async def track_evaluate(js, *args):
            if "elementFromPoint" in js and "targetEl" not in js:
                return {
                    "tag": "div",
                    "className": "cookie-consent-banner",
                    "text": "Accept cookies?",
                    "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 80},
                    "attributes": {"class": "cookie-consent-banner"}
                }
            if "targetEl" in js:
                return False
            if "acceptTexts" in js or "findAccept" in js.lower() or "Accept" in js:
                return True  # 找到 accept 按钮
            if "btn.click" in js:
                dismiss_calls.append("clicked")
                return None
            return None

        mock_page.evaluate = AsyncMock(side_effect=track_evaluate)

        blocker = BlockerInfo(
            tag="div",
            class_name="cookie-consent-banner",
            text="Accept cookies?",
            attributes={"class": "cookie-consent-banner"}
        )

        result = await smart_click_instance._dismiss_cookie_banner(
            mock_page, blocker
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_is_cookie_banner_classification(self, smart_click_instance):
        """分类判断：正确识别 cookie banner"""
        # 是 cookie banner
        blocker1 = BlockerInfo(
            tag="div",
            class_name="cc-cookie-banner",
            text="We use cookies",
            attributes={"class": "cc-cookie-banner"}
        )
        assert smart_click_instance._is_cookie_banner(blocker1) is True

        # 不是 cookie banner
        blocker2 = BlockerInfo(
            tag="button",
            class_name="submit-btn",
            text="Submit",
            attributes={}
        )
        assert smart_click_instance._is_cookie_banner(blocker2) is False


# ---------------------------------------------------------------------------
# Test: Modal 自动关闭
# ---------------------------------------------------------------------------

class TestModalDismiss:
    """测试 modal 自动关闭"""

    @pytest.mark.asyncio
    async def test_dismiss_modal_via_close_button(self, mock_page,
                                                   smart_click_instance):
        """自动关闭：通过关闭按钮关闭 modal"""
        mock_page.evaluate = AsyncMock(side_effect=self._modal_with_close_btn)
        mock_page.click = AsyncMock()

        blocker = BlockerInfo(
            tag="div",
            class_name="modal-dialog",
            text="Welcome!",
            attributes={"class": "modal-dialog", "role": "dialog"}
        )

        result = await smart_click_instance._dismiss_modal(mock_page, blocker)
        assert result is True

    @pytest.mark.asyncio
    async def test_dismiss_modal_via_escape(self, mock_page,
                                             smart_click_instance):
        """自动关闭：无关闭按钮时按 Escape"""
        # evaluate 找不到关闭按钮
        mock_page.evaluate = AsyncMock(return_value=None)

        blocker = BlockerInfo(
            tag="div",
            class_name="some-popup",
            text="Hello",
            attributes={"class": "some-popup"}
        )

        result = await smart_click_instance._dismiss_modal(mock_page, blocker)
        assert result is True
        mock_page.keyboard.press.assert_called_with("Escape")

    @pytest.mark.asyncio
    async def test_is_modal_classification(self, smart_click_instance):
        """分类判断：正确识别 modal"""
        # role=dialog → 是 modal
        blocker1 = BlockerInfo(
            tag="div",
            class_name="",
            attributes={"role": "dialog"}
        )
        assert smart_click_instance._is_modal(blocker1) is True

        # class 包含 modal → 是 modal
        blocker2 = BlockerInfo(
            tag="div",
            class_name="my-modal-overlay",
            attributes={}
        )
        assert smart_click_instance._is_modal(blocker2) is True

        # 普通 div → 不是 modal
        blocker3 = BlockerInfo(
            tag="div",
            class_name="content-wrapper",
            attributes={}
        )
        assert smart_click_instance._is_modal(blocker3) is False

    @staticmethod
    async def _modal_with_close_btn(js, *args):
        if "close" in js.lower() or "×" in js:
            return 'button.close-btn'
        return None


# ---------------------------------------------------------------------------
# Test: 等待可点击状态
# ---------------------------------------------------------------------------

class TestWaitForClickable:
    """测试等待元素可点击"""

    @pytest.mark.asyncio
    async def test_wait_clickable_immediately(self, mock_page, mock_element,
                                               smart_click_instance):
        """等待：元素立即可点击"""
        call_count = 0

        async def evaluate_side_effect(js, *args):
            nonlocal call_count
            if "elementFromPoint" in js and "targetEl" not in js:
                return None  # 无遮挡
            if "getComputedStyle" in js:
                return True  # 可见
            return None

        mock_page.evaluate = AsyncMock(side_effect=evaluate_side_effect)

        result = await smart_click_instance.wait_for_clickable(
            mock_page, "#btn", timeout=2000
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_wait_clickable_timeout(self, mock_page, mock_element,
                                           smart_click_instance):
        """等待：超时后返回 False"""
        async def evaluate_blocked(js, *args):
            if "elementFromPoint" in js and "targetEl" not in js:
                return {
                    "tag": "div",
                    "className": "overlay",
                    "text": "Loading...",
                    "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 600},
                    "attributes": {}
                }
            if "targetEl" in js:
                return False
            if "getComputedStyle" in js:
                return True
            return None

        mock_page.evaluate = AsyncMock(side_effect=evaluate_blocked)

        result = await smart_click_instance.wait_for_clickable(
            mock_page, "#btn", timeout=500  # 短超时
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_wait_clickable_element_not_found(self, mock_page,
                                                     smart_click_instance):
        """等待：元素不存在时返回 False"""
        mock_page.query_selector = AsyncMock(return_value=None)

        result = await smart_click_instance.wait_for_clickable(
            mock_page, "#nonexistent", timeout=500
        )

        assert result is False


# ---------------------------------------------------------------------------
# Test: 重试机制
# ---------------------------------------------------------------------------

class TestRetryMechanism:
    """测试重试机制"""

    @pytest.mark.asyncio
    async def test_retry_success_after_dismiss(self, mock_page, mock_element,
                                                smart_click_instance):
        """重试：第一次被遮挡，关闭遮挡后第二次成功"""
        attempt = {"count": 0}

        async def evaluate_retry(js, *args):
            # is_target check
            if "querySelector" in js and "targetEl" in js:
                return attempt["count"] > 1
            # detect blocker
            if "elementFromPoint" in js and "targetEl" not in js:
                attempt["count"] += 1
                if attempt["count"] <= 1:
                    # 第一次：有遮挡
                    return {
                        "tag": "div",
                        "className": "cookie-banner",
                        "text": "Accept cookies",
                        "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 80},
                        "attributes": {"class": "cookie-banner"}
                    }
                else:
                    # 第二次：无遮挡
                    return None
            if "acceptTexts" in js or "Accept" in js:
                return True
            if "getComputedStyle" in js:
                return True
            return None

        mock_page.evaluate = AsyncMock(side_effect=evaluate_retry)

        result = await smart_click_instance.click(
            mock_page, "#submit-btn", auto_dismiss=True
        )

        assert result.success is True
        assert result.retry_count >= 1

    @pytest.mark.asyncio
    async def test_click_with_retry_fallback_to_scroll(self, mock_page,
                                                        mock_element,
                                                        smart_click_instance):
        """重试：回退到滚动策略"""
        attempt = {"count": 0}

        async def evaluate_scroll(js, *args):
            # is_target check
            if "querySelector" in js and "targetEl" in js:
                return attempt["count"] > 2
            # detect blocker
            if "elementFromPoint" in js and "targetEl" not in js:
                attempt["count"] += 1
                if attempt["count"] <= 2:
                    return {
                        "tag": "header",
                        "className": "fixed-header",
                        "text": "Navigation",
                        "boundingBox": {"x": 0, "y": 0, "width": 800, "height": 60},
                        "attributes": {"class": "fixed-header",
                                       "style": "position: fixed"}
                    }
                return None
            if "scrollIntoView" in js or "scrollBy" in js:
                return None
            if "acceptTexts" in js:
                return None
            if "getComputedStyle" in js:
                return True
            return None

        mock_page.evaluate = AsyncMock(side_effect=evaluate_scroll)

        result = await smart_click_instance.click_with_retry(
            mock_page, "#submit-btn", max_retries=3
        )

        # 应该至少尝试了滚动
        assert attempt["count"] >= 2

    @pytest.mark.asyncio
    async def test_element_not_found(self, mock_page, smart_click_instance):
        """错误处理：元素不存在"""
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception("Timeout"))
        mock_page.query_selector = AsyncMock(return_value=None)

        result = await smart_click_instance.click(mock_page, "#nonexistent")

        assert result.success is False
        assert "not found" in result.message.lower() or "failed" in result.message.lower()


# ---------------------------------------------------------------------------
# Test: ClickResult 序列化
# ---------------------------------------------------------------------------

class TestClickResultSerialization:
    """测试 ClickResult 序列化"""

    def test_to_dict(self):
        result = ClickResult(
            success=True,
            target={"selector": "#btn", "text": "Submit"},
            blocked=False,
            blocker=None,
            retry_count=0,
            message="Clicked successfully"
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["target"]["selector"] == "#btn"
        assert d["blocked"] is False

    def test_to_json(self):
        result = ClickResult(
            success=False,
            target={"selector": "#btn", "text": ""},
            blocked=True,
            blocker={"tag": "div", "class_name": "overlay"},
            retry_count=2,
            message="Still blocked"
        )
        j = result.to_json()
        parsed = json.loads(j)
        assert parsed["success"] is False
        assert parsed["blocked"] is True
        assert parsed["retry_count"] == 2

    def test_default_values(self):
        result = ClickResult()
        assert result.success is False
        assert result.blocked is False
        assert result.blocker is None
        assert result.retry_count == 0


# ---------------------------------------------------------------------------
# Test: 分类辅助方法
# ---------------------------------------------------------------------------

class TestClassificationHelpers:
    """测试遮挡元素分类"""

    def test_is_fixed_element_by_style(self, smart_click_instance):
        blocker = BlockerInfo(
            tag="header",
            class_name="main-header",
            attributes={"style": "position: fixed; top: 0;"}
        )
        assert smart_click_instance._is_fixed_element(blocker) is True

    def test_is_fixed_element_by_class(self, smart_click_instance):
        blocker = BlockerInfo(
            tag="nav",
            class_name="navbar-fixed-top",
            attributes={}
        )
        assert smart_click_instance._is_fixed_element(blocker) is True

    def test_not_fixed_element(self, smart_click_instance):
        blocker = BlockerInfo(
            tag="div",
            class_name="content",
            attributes={}
        )
        assert smart_click_instance._is_fixed_element(blocker) is False


# ---------------------------------------------------------------------------
# Test: 便捷函数
# ---------------------------------------------------------------------------

class TestConvenienceFunctions:
    """测试便捷函数接口"""

    @pytest.mark.asyncio
    async def test_smart_click_function(self, mock_page, mock_element):
        """smart_click() 便捷函数"""
        mock_page.evaluate = AsyncMock(return_value=None)

        result = await smart_click(mock_page, "#btn")
        assert isinstance(result, ClickResult)

    @pytest.mark.asyncio
    async def test_wait_for_clickable_function(self, mock_page, mock_element):
        """wait_for_clickable() 便捷函数"""
        mock_page.evaluate = AsyncMock(return_value=None)

        result = await wait_for_clickable(mock_page, "#btn", timeout=1000)
        assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
