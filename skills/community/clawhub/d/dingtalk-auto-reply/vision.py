#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vision.py —— 多模态图片识别层。

描述单张/批量图片：复用 CodeBuddy Agent SDK（多模态），与文本回复同一后端、
零额外配置、图片不出域。视觉模型用 VISION_MODEL（默认跟随文本主模型 CODEBUDDY_MODEL），
可用环境变量单独指定 CodeBuddy 侧的视觉模型。

SDK 可用性（_SDK_AVAILABLE）与 SDK 调用原语均来自 runtime.py。
"""
import os, asyncio
from runtime import (
    _SDK_AVAILABLE, _sdk_query, CodeBuddyAgentOptions, AppendSystemPrompt,
    AssistantMessage, TextBlock, ResultMessage,
    CHINA_EDITION, CODEBUDDY_API_KEY, CODEBUDDY_MODEL, CODEBUDDY_CMD,
    VISION_ENABLED, VISION_MODEL,
    log_debug, DISALLOWED_TOOLS, build_sdk_env, build_image_block, VISION_PROMPT,
)

# 单张图片识别超时（秒）：与文本生成同量级，防止异常图/大图卡死
VISION_TIMEOUT = 120


def describe_image(path):
    """识别单张图片，返回中文描述；失败/未配返回空串。
    统一走 CodeBuddy Agent SDK（与文本回复同一后端、同一视觉模型 VISION_MODEL）。
    注：VISION_ENABLED == _SDK_AVAILABLE（runtime 定义），此处一次守卫即可。"""
    if not VISION_ENABLED:
        return ""
    async def _run():
        async def _img_msgs():
            yield {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": VISION_PROMPT},
                        build_image_block(path),
                    ],
                },
            }
        options = CodeBuddyAgentOptions(
            system_prompt="你是视觉描述助手，只输出对图片的客观中文描述，不要发挥。",
            model=VISION_MODEL,
            permission_mode="bypassPermissions",
            disallowed_tools=DISALLOWED_TOOLS,
            codebuddy_code_path=CODEBUDDY_CMD if CODEBUDDY_CMD and os.path.exists(CODEBUDDY_CMD) else None,
            env=build_sdk_env(),
        )
        chunks = []
        async for message in _sdk_query(prompt=_img_msgs(), options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        chunks.append(block.text)
        return "".join(chunks).strip()
    try:
        return asyncio.run(asyncio.wait_for(_run(), timeout=VISION_TIMEOUT))
    except Exception as e:
        log_debug(f"[vision] describe error: {e}")
        return ""


def describe_images(paths):
    """批量识别，返回拼接的中文描述；无有效图返回空串。"""
    descs = []
    for p, ok in paths:
        if ok:
            d = describe_image(p)
            if d:
                descs.append(d)
    return "\n".join(f"- {d}" for d in descs) if descs else ""
