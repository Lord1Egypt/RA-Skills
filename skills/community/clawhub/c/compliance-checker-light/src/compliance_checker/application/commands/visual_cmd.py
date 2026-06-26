"""
visual 子命令 - 视觉质检

检测文档中的印章、签名等视觉元素。
将用户原始 target 字符串透传到 Qwen-VL 的 Prompt 中，
让多模态模型发挥细粒度识别能力。
"""

import logging
import os
import tempfile
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def _classify_target(target: str) -> str:
    """
    将 target 字符串映射到检测类型。

    Args:
        target: 用户指定的检测目标（如"公章"、"法人签字"、"发票专用章"）

    Returns:
        检测类型: "seal" 或 "signature"
    """
    if "签" in target:
        return "signature"
    if "章" in target:
        return "seal"
    # 默认按印章处理
    return "seal"


def _build_seal_prompt(target: str) -> str:
    """
    构造印章检测 Prompt，保留用户原始 target 描述。

    Args:
        target: 用户原始 target 字符串（如"发票专用章"、"骑缝章"、"公章"）

    Returns:
        定制化 Prompt
    """
    return f"""请仔细检查这张图片，判断是否存在"{target}"。

请按以下格式回答：
1. 是否存在{target}：[是/否]
2. 置信度：[高/中/低]
3. 位置描述：[如"右下角"、"页面中央"等]
4. 说明：[简要说明判断依据]

请确保回答简洁明确。"""


def _build_signature_prompt(target: str) -> str:
    """
    构造签名检测 Prompt，保留用户原始 target 描述。

    Args:
        target: 用户原始 target 字符串（如"法人签字"、"经办人签名"）

    Returns:
        定制化 Prompt
    """
    return f"""请仔细检查这张图片，判断是否存在"{target}"。

请按以下格式回答：
1. 是否存在{target}：[是/否]
2. 置信度：[高/中/低]
3. 位置描述：[如"签字栏"、"页面底部"等]
4. 说明：[简要说明判断依据]

请确保回答简洁明确。"""


def _is_image_file(file_path: str) -> bool:
    """判断是否为图片文件"""
    return Path(file_path).suffix.lower() in (
        ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"
    )


def _is_pdf_file(file_path: str) -> bool:
    """判断是否为 PDF 文件"""
    return Path(file_path).suffix.lower() == ".pdf"


async def _detect_single_target(
    visual_client, image_path: str, target: str
) -> dict:
    """
    对单个 target 执行检测。

    Args:
        visual_client: 视觉客户端实例
        image_path: 图片文件路径
        target: 用户原始 target 字符串

    Returns:
        {found, confidence, location, reasoning}
    """
    detect_type = _classify_target(target)

    if detect_type == "seal":
        prompt = _build_seal_prompt(target)
        result = await visual_client.detect_seal(
            image_path=image_path, context=prompt
        )
    else:
        prompt = _build_signature_prompt(target)
        result = await visual_client.detect_signature(
            image_path=image_path, context=prompt
        )

    if result.get("success"):
        return {
            "found": result.get("found", False),
            "confidence": round(result.get("confidence", 0.0), 2),
            "location": result.get("location", ""),
            "reasoning": result.get("reasoning", ""),
        }
    else:
        return {
            "found": False,
            "confidence": 0.0,
            "location": "",
            "reasoning": result.get("error", "检测失败"),
        }


async def _detect_single_target_from_bytes(
    visual_client, image_bytes: bytes, target: str
) -> dict:
    """
    对单个 target 执行字节流检测（用于 PDF 转换后的图片）。
    """
    detect_type = _classify_target(target)

    has_bytes_method = hasattr(visual_client, "detect_seal_from_bytes")

    if has_bytes_method:
        if detect_type == "seal":
            prompt = _build_seal_prompt(target)
            result = await visual_client.detect_seal_from_bytes(
                image_bytes=image_bytes, context=prompt
            )
        else:
            prompt = _build_signature_prompt(target)
            result = await visual_client.detect_signature_from_bytes(
                image_bytes=image_bytes, context=prompt
            )
    else:
        # 回退到临时文件方式
        import asyncio

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        try:
            result_dict = await _detect_single_target(
                visual_client, tmp_path, target
            )
            return result_dict
        finally:
            try:
                await asyncio.to_thread(os.unlink, tmp_path)
            except Exception:
                pass

    if result.get("success"):
        return {
            "found": result.get("found", False),
            "confidence": round(result.get("confidence", 0.0), 2),
            "location": result.get("location", ""),
            "reasoning": result.get("reasoning", ""),
        }
    else:
        return {
            "found": False,
            "confidence": 0.0,
            "location": "",
            "reasoning": result.get("error", "检测失败"),
        }


async def run_visual(file: str, targets: List[str]) -> dict:
    """
    执行 visual 子命令。

    Args:
        file: 文件路径
        targets: 检测目标列表（如 ["公章", "法人签字"]）

    Returns:
        {target_name: {found, confidence, location, reasoning}}
    """
    file_path = Path(file)
    if not file_path.is_file():
        raise FileNotFoundError(f"文件不存在: {file}")

    if not targets:
        raise ValueError("--targets 不能为空")

    # 获取视觉客户端
    from ..bootstrap import create_container

    container = create_container()
    visual_client = container.visual_client

    if not visual_client or not visual_client.is_available():
        return {
            target: {
                "found": False,
                "confidence": 0.0,
                "location": "",
                "reasoning": "视觉检测服务不可用，请检查 API 配置",
            }
            for target in targets
        }

    result = {}

    if _is_image_file(file):
        # 图片文件：直接检测
        for target in targets:
            result[target] = await _detect_single_target(
                visual_client, file, target
            )

    elif _is_pdf_file(file):
        # PDF 文件：转为图片后检测
        pdf_converter = container.pdf_converter
        if not pdf_converter:
            return {
                target: {
                    "found": False,
                    "confidence": 0.0,
                    "location": "",
                    "reasoning": "PDF 转换器不可用",
                }
                for target in targets
            }

        images = await pdf_converter.convert_to_images(file)
        if not images:
            return {
                target: {
                    "found": False,
                    "confidence": 0.0,
                    "location": "",
                    "reasoning": "PDF 转换失败：未生成任何图片",
                }
                for target in targets
            }

        # 对每个 target，逐页检测，找到即停
        for target in targets:
            target_found = False
            for page_idx, image_bytes in enumerate(images):
                page_result = await _detect_single_target_from_bytes(
                    visual_client, image_bytes, target
                )
                if page_result["found"]:
                    page_result["reasoning"] = (
                        f"第 {page_idx + 1} 页: {page_result['reasoning']}"
                    )
                    result[target] = page_result
                    target_found = True
                    break

            if not target_found:
                result[target] = {
                    "found": False,
                    "confidence": 0.0,
                    "location": "",
                    "reasoning": f"已检查 {len(images)} 页，未找到{target}",
                }
    else:
        raise ValueError(f"不支持的文件格式: {file_path.suffix}")

    return result
