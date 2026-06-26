"""哔哩哔哩创作中心 — 视频上传页选择器与文案。

上传页: https://member.bilibili.com/platform/upload/video/frame
"""

from __future__ import annotations

UPLOAD_URL = "https://member.bilibili.com/platform/upload/video/frame"

VIDEO_FILE_INPUT = 'input[type="file"]'
COVER_FILE_INPUT = 'input[type="file"]'

# 标题
TITLE_INPUT_CANDIDATES: tuple[str, ...] = (
    'input[class*="title"]',
    "input.video-title",
    'input[placeholder*="标题"]',
    'textarea[placeholder*="标题"]',
)

# 标签 / 话题（分 P 稿件信息区）
TAG_INPUT_CANDIDATES: tuple[str, ...] = (
    'input[placeholder*="标签"]',
    'input[placeholder*="话题"]',
    ".tag-input input",
    'input[type="text"]',
)

# 投稿 / 发布（实际点击在 publish_bilibili 中用文案匹配）
PUBLISH_BUTTON_CANDIDATES: tuple[str, ...] = (
    ".submit-add",
    'button[class*="submit"]',
)

TEXT_VIDEO_READY_HINTS: tuple[str, ...] = (
    "上传完成",
    "填写分P",
    "稿件信息",
    "视频信息",
)
TEXT_UPLOAD_FAIL_HINTS: tuple[str, ...] = ("上传失败", "转码失败", "格式错误")
