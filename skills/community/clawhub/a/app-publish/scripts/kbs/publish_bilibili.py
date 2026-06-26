"""哔哩哔哩创作中心：上传视频、封面，填写标题与标签，可选投稿。"""

from __future__ import annotations

import logging
import time

from kbs.cdp import Page, wait_until_upload_hints
from kbs.selectors_bili import (
    TAG_INPUT_CANDIDATES,
    TEXT_UPLOAD_FAIL_HINTS,
    TEXT_VIDEO_READY_HINTS,
    TITLE_INPUT_CANDIDATES,
    UPLOAD_URL,
)
from kbs.types import PublishResult, VideoPublishConfig

logger = logging.getLogger(__name__)


def _first_selector(page: Page, candidates: tuple[str, ...]) -> str | None:
    for sel in candidates:
        if page.has_element(sel):
            return sel
    return None


def _fill_title(page: Page, title: str) -> None:
    sel = _first_selector(page, TITLE_INPUT_CANDIDATES)
    if not sel:
        logger.warning("未找到 B 站标题输入框")
        return
    page.scroll_element_into_view(sel)
    page.input_text(sel, title)


def _fill_tags(page: Page, keywords: list[str]) -> None:
    if not keywords:
        return
    sel = _first_selector(page, TAG_INPUT_CANDIDATES)
    if not sel:
        logger.warning("未找到标签输入框")
        return
    for kw in keywords:
        page.input_text(sel, kw)
        time.sleep(0.15)
        page.press_key("Enter")
        time.sleep(0.2)


def _upload_cover(page: Page, cover_path: str) -> None:
    try:
        page.set_file_input_by_accept_hint("image", [cover_path])
        return
    except Exception:
        logger.debug("accept=image 未匹配，尝试第二个 file input")
    try:
        page.set_file_input_by_index(1, [cover_path])
    except Exception as e:
        logger.warning("封面上传跳过: %s", e)


def publish_bilibili(
    page: Page,
    config: VideoPublishConfig,
    *,
    wait_timeout: float = 300.0,
    do_publish: bool = True,
) -> PublishResult:
    """打开 B 站上传页，上传素材并填写稿件信息。"""
    config.validate()

    page.navigate(UPLOAD_URL)
    page.wait_for_load()
    time.sleep(2.0)

    try:
        page.set_file_input_by_index(0, [config.video_path])
    except Exception as e:
        return PublishResult(
            success=False,
            platform="bilibili",
            message="无法设置视频文件",
            detail=str(e),
        )

    phase = wait_until_upload_hints(
        page,
        TEXT_VIDEO_READY_HINTS,
        TEXT_UPLOAD_FAIL_HINTS,
        timeout=wait_timeout,
    )
    if phase == "fail":
        return PublishResult(
            success=False,
            platform="bilibili",
            message="上传失败（页面提示）",
            upload_phase="video_failed",
        )
    if phase == "timeout":
        return PublishResult(
            success=False,
            platform="bilibili",
            message=f"等待上传/处理超时（{wait_timeout}s）",
            upload_phase="video_timeout",
        )

    time.sleep(1.0)
    if config.cover_path:
        _upload_cover(page, config.cover_path)
        time.sleep(1.5)

    _fill_title(page, config.title)
    time.sleep(0.5)
    _fill_tags(page, config.keywords)

    if not do_publish:
        return PublishResult(
            success=True,
            platform="bilibili",
            message="表单已填写，未提交投稿",
            upload_phase="form_filled",
        )

    clicked = (
        page.click_by_inner_text_then_center("立即投稿")
        or page.click_by_inner_text_then_center("提交投稿")
        or page.click_by_inner_text_then_center("投稿")
    )
    if not clicked:
        logger.warning("未找到投稿按钮，请手动点击")
        return PublishResult(
            success=True,
            platform="bilibili",
            message="表单已填写，未自动点击投稿",
            upload_phase="form_filled",
        )

    time.sleep(2.0)
    return PublishResult(
        success=True,
        platform="bilibili",
        message="已点击投稿",
        upload_phase="published",
    )
