"""Qwen-VL 客户端 - 视觉模型 API 调用封装

实现 Core 层定义的 VisualCheckerProtocol 接口。
只负责调用视觉模型 API 并返回原始结果，不包含业务规则判断。
"""

import os
import re
import base64
import logging
from typing import Optional, Dict, Any

from ...core.interfaces import VisualCheckerProtocol
from ...core.exceptions import ComplianceCheckerError

logger = logging.getLogger(__name__)


class VisualAPIError(ComplianceCheckerError):
    """视觉 API 调用错误"""

    pass


class ImageReadError(ComplianceCheckerError):
    """图片读取错误"""

    pass


class QwenVLClient(VisualCheckerProtocol):
    """
    视觉模型客户端 - 实现 VisualCheckerProtocol

    默认使用 Qwen3-VL-Flash (OpenAI 兼容模式)
    只负责调用 API 并返回原始检测结果，不做业务判断。
    """

    # 默认使用 OpenAI 兼容模式端点（支持 Qwen3-VL-Flash）
    DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    DEFAULT_MODEL = "qwen3-vl-flash"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        初始化视觉模型客户端

        Args:
            api_key: API 密钥（优先使用传入值，其次环境变量 VISION_API_KEY/LLM_API_KEY）
            base_url: API 基础 URL（优先使用传入值，其次环境变量 VISION_BASE_URL/LLM_BASE_URL）
            model: 模型名称（优先使用传入值，其次环境变量 VISION_MODEL，默认 qwen3-vl-flash）
        """
        # API Key: 优先使用传入值，其次 VISION_API_KEY（专用配置），最后 LLM_API_KEY
        if api_key:
            self.api_key = api_key
        else:
            vision_api_key = os.getenv("VISION_API_KEY", "").strip()
            self.api_key = (
                vision_api_key if vision_api_key else os.getenv("LLM_API_KEY", "").strip() or None
            )

        # Model: 优先使用传入值，其次 VISION_MODEL，最后默认值
        if model:
            self.model = model
        else:
            vision_model = os.getenv("VISION_MODEL", "").strip()
            self.model = vision_model if vision_model else self.DEFAULT_MODEL

        # Base URL: 优先使用传入值，其次 VISION_BASE_URL，最后 LLM_BASE_URL，最后默认值
        if base_url:
            self.base_url = base_url
        else:
            vision_base_url = os.getenv("VISION_BASE_URL", "").strip()
            llm_base_url = os.getenv("LLM_BASE_URL", "").strip()
            if vision_base_url:
                self.base_url = vision_base_url
            elif llm_base_url:
                self.base_url = llm_base_url
            else:
                self.base_url = self.DEFAULT_BASE_URL

        # 判断是否使用 OpenAI 兼容模式
        # OpenAI 兼容模式端点特征：包含 "compatible-mode" 或以 "/v1" 结尾
        self.use_openai_format = "compatible-mode" in self.base_url or self.base_url.rstrip(
            "/"
        ).endswith("/v1")

        if not self.api_key:
            logger.debug("Vision API key not set, visual inspection will be unavailable")

    def is_available(self) -> bool:
        """
        检查视觉检查器是否可用

        Returns:
            True 如果 API 已配置且可用
        """
        return self.api_key is not None and len(self.api_key) > 0

    async def test_connection(self) -> Dict[str, Any]:
        """
        测试 Vision API 连通性

        发送一个极简的检测请求，验证 API 配置是否正确。

        Returns:
            {
                "success": bool,
                "message": str,
                "latency_ms": float  # 响应延迟（毫秒）
            }
        """
        import time

        if not self.api_key:
            return {
                "success": False,
                "message": "Vision API key not configured",
                "latency_ms": 0.0,
            }

        # 创建一个 1x1 像素的透明 PNG 图片（最小有效图片）
        # PNG 格式：89 50 4E 47 0D 0A 1A 0A (文件头) + IHDR + IDAT + IEND
        minimal_png = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
            0x00, 0x00, 0x00, 0x0D,  # IHDR chunk length
            0x49, 0x48, 0x44, 0x52,  # IHDR
            0x00, 0x00, 0x00, 0x01,  # width: 1
            0x00, 0x00, 0x00, 0x01,  # height: 1
            0x08, 0x06, 0x00, 0x00, 0x00,  # 8-bit RGBA
            0x1F, 0x15, 0xC4, 0x89,  # IHDR CRC
            0x00, 0x00, 0x00, 0x0A,  # IDAT chunk length
            0x49, 0x44, 0x41, 0x54,  # IDAT
            0x78, 0x9C, 0x63, 0x60, 0x00, 0x00, 0x00, 0x02, 0x00, 0x01,
            0x12, 0xCB, 0xF9, 0xC5,  # IDAT data + CRC
            0x00, 0x00, 0x00, 0x00,  # IEND chunk length
            0x49, 0x45, 0x4E, 0x44,  # IEND
            0xAE, 0x42, 0x60, 0x82,  # IEND CRC
        ])

        start_time = time.time()
        try:
            # 发送一个简单的检测请求
            result = await self._chat_with_bytes(
                image_bytes=minimal_png,
                prompt="Is there a seal in this image? Answer yes or no.",
                temperature=0.0,  # 确定性输出
            )
            latency_ms = (time.time() - start_time) * 1000

            if result.get("success"):
                return {
                    "success": True,
                    "message": f"Vision API connected successfully ({self.model})",
                    "latency_ms": round(latency_ms, 2),
                }
            else:
                error_msg = result.get("error", "Unknown error")
                # 处理特定错误码
                if "unavailable" in result:
                    return {
                        "success": False,
                        "message": f"Vision API unavailable: {error_msg}",
                        "latency_ms": round(latency_ms, 2),
                    }
                return {
                    "success": False,
                    "message": f"Vision API test failed: {error_msg}",
                    "latency_ms": round(latency_ms, 2),
                }

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return {
                "success": False,
                "message": f"Vision API connection error: {str(e)}",
                "latency_ms": round(latency_ms, 2),
            }

    async def detect_seal(self, image_path: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        检测图片中的公章

        Args:
            image_path: 图片文件路径
            context: 检测提示词（由 Domain 层构建，包含业务规则）

        Returns:
            {
                "success": bool,
                "found": bool,
                "confidence": float,
                "reasoning": str,
                "location": str
            }

        Raises:
            ValueError: 未提供 context 提示词
        """
        # 必须由调用方提供业务提示词
        if not context:
            raise ValueError(
                "detect_seal 需要提供 context 参数（检测提示词）。"
                "请使用 Domain 层的 SEAL_DETECT_PROMPT 或自定义提示词。"
            )

        result = await self._chat(image_path, context)
        return self._format_detection_result(result, "seal")

    async def detect_seal_from_bytes(
        self, image_bytes: bytes, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从字节流检测图片中的公章

        Args:
            image_bytes: 图片字节流
            context: 检测提示词（由 Domain 层构建，包含业务规则）

        Returns:
            {
                "success": bool,
                "found": bool,
                "confidence": float,
                "reasoning": str,
                "location": str
            }

        Raises:
            ValueError: 未提供 context 提示词
        """
        if not context:
            raise ValueError(
                "detect_seal_from_bytes 需要提供 context 参数（检测提示词）。"
                "请使用 Domain 层的 SEAL_DETECT_PROMPT 或自定义提示词。"
            )

        result = await self._chat_with_bytes(image_bytes, context)
        return self._format_detection_result(result, "seal")

    async def detect_signature(
        self, image_path: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        检测图片中的签名

        Args:
            image_path: 图片文件路径
            context: 检测提示词（由 Domain 层构建，包含业务规则）

        Returns:
            {
                "success": bool,
                "found": bool,
                "confidence": float,
                "reasoning": str,
                "location": str
            }

        Raises:
            ValueError: 未提供 context 提示词
        """
        # 必须由调用方提供业务提示词
        if not context:
            raise ValueError(
                "detect_signature 需要提供 context 参数（检测提示词）。"
                "请使用 Domain 层的 SIGNATURE_DETECT_PROMPT 或自定义提示词。"
            )

        result = await self._chat(image_path, context)
        return self._format_detection_result(result, "signature")

    async def detect_signature_from_bytes(
        self, image_bytes: bytes, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从字节流检测图片中的签名

        Args:
            image_bytes: 图片字节流
            context: 检测提示词（由 Domain 层构建，包含业务规则）

        Returns:
            {
                "success": bool,
                "found": bool,
                "confidence": float,
                "reasoning": str,
                "location": str
            }

        Raises:
            ValueError: 未提供 context 提示词
        """
        if not context:
            raise ValueError(
                "detect_signature_from_bytes 需要提供 context 参数（检测提示词）。"
                "请使用 Domain 层的 SIGNATURE_DETECT_PROMPT 或自定义提示词。"
            )

        result = await self._chat_with_bytes(image_bytes, context)
        return self._format_detection_result(result, "signature")

    async def _chat(self, image_path: str, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        发送图片和提示词到视觉模型

        Args:
            image_path: 图片文件路径
            prompt: 文本提示词
            temperature: 采样温度

        Returns:
            原始 API 响应字典
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Vision API key not configured",
                "found": False,
                "confidence": 0.0,
                "reasoning": "Vision API key not configured",
                "content": None,
            }

        try:
            # 读取图片并转为 base64
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to read image {image_path}: {e}")
            raise ImageReadError(f"Failed to read image {image_path}: {e}") from e

        # 构建请求（根据端点类型选择格式）
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        if self.use_openai_format:
            # OpenAI 兼容格式
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
                "temperature": temperature,
            }
        else:
            # 阿里云原生 API 格式
            url = f"{self.base_url}/services/aigc/multimodal-generation/generation"
            payload = {
                "model": self.model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"image": f"data:image/png;base64,{image_base64}"},
                                {"text": prompt},
                            ],
                        }
                    ]
                },
                "parameters": {"temperature": temperature},
            }

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"视觉模型 API error: {resp.status} - {text}")
                        # 404 错误：模型或端点配置错误，标记为不可用
                        if resp.status == 404:
                            return {
                                "success": False,
                                "error": "视觉检查无法使用：模型或端点配置错误",
                                "found": False,
                                "confidence": 0.0,
                                "reasoning": "视觉检查无法使用：请检查 VISION_MODEL 和 VISION_BASE_URL 配置",
                                "content": None,
                                "unavailable": True,
                            }
                        raise VisualAPIError(f"API error: {resp.status} - {text}")

                    result = await resp.json()

                    # 解析响应（支持 OpenAI 兼容格式和阿里云原生格式）
                    content = self._extract_content_from_response(result)
                    if content is not None:
                        return {
                            "success": True,
                            "content": content,
                            "raw": result,
                        }

                    return {
                        "success": False,
                        "error": "Unexpected response format",
                        "content": None,
                        "raw": result,
                    }
        except VisualAPIError:
            raise
        except Exception as e:
            logger.error(f"Qwen-VL request failed: {e}")
            raise VisualAPIError(f"Qwen-VL request failed: {e}") from e

    async def _chat_with_bytes(
        self, image_bytes: bytes, prompt: str, temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        发送图片字节流和提示词到视觉模型

        Args:
            image_bytes: 图片字节流
            prompt: 文本提示词
            temperature: 采样温度

        Returns:
            原始 API 响应字典
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Vision API key not configured",
                "found": False,
                "confidence": 0.0,
                "reasoning": "Vision API key not configured",
                "content": None,
            }

        try:
            # 将字节流转为 base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to encode image bytes: {e}")
            raise ImageReadError(f"Failed to encode image bytes: {e}") from e

        # 构建请求（根据端点类型选择格式）
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        if self.use_openai_format:
            # OpenAI 兼容格式
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
                "temperature": temperature,
            }
        else:
            # 阿里云原生 API 格式
            url = f"{self.base_url}/services/aigc/multimodal-generation/generation"
            payload = {
                "model": self.model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"image": f"data:image/png;base64,{image_base64}"},
                                {"text": prompt},
                            ],
                        }
                    ]
                },
                "parameters": {"temperature": temperature},
            }

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"视觉模型 API error: {resp.status} - {text}")
                        # 404 错误：模型或端点配置错误，标记为不可用
                        if resp.status == 404:
                            return {
                                "success": False,
                                "error": "视觉检查无法使用：模型或端点配置错误",
                                "found": False,
                                "confidence": 0.0,
                                "reasoning": "视觉检查无法使用：请检查 VISION_MODEL 和 VISION_BASE_URL 配置",
                                "content": None,
                                "unavailable": True,
                            }
                        raise VisualAPIError(f"API error: {resp.status} - {text}")

                    result = await resp.json()

                    # 解析响应（支持 OpenAI 兼容格式和阿里云原生格式）
                    content = self._extract_content_from_response(result)
                    if content is not None:
                        return {
                            "success": True,
                            "content": content,
                            "raw": result,
                        }

                    return {
                        "success": False,
                        "error": "Unexpected response format",
                        "content": None,
                        "raw": result,
                    }
        except VisualAPIError:
            raise
        except Exception as e:
            logger.error(f"Qwen-VL request failed: {e}")
            raise VisualAPIError(f"Qwen-VL request failed: {e}") from e

    def _extract_content_from_response(self, result: Dict[str, Any]) -> Optional[str]:
        """
        从 API 响应中提取内容文本

        支持 OpenAI 兼容格式和阿里云原生格式
        """
        try:
            # OpenAI 兼容格式: choices[0].message.content
            if "choices" in result:
                choice = result["choices"][0]
                if "message" in choice:
                    content = choice["message"].get("content")
                else:
                    content = choice.get("text")

                # 处理列表格式（新版 API）
                if isinstance(content, list):
                    content = "\n".join(
                        [
                            item.get("text", "") if isinstance(item, dict) else str(item)
                            for item in content
                        ]
                    )
                return content

            # 阿里云原生格式: output.choices[0].message.content
            if "output" in result and "choices" in result["output"]:
                content = result["output"]["choices"][0]["message"]["content"]
                # 处理列表格式
                if isinstance(content, list):
                    content = "\n".join(
                        [
                            item.get("text", "") if isinstance(item, dict) else str(item)
                            for item in content
                        ]
                    )
                return content

            return None
        except (KeyError, IndexError, TypeError) as e:
            logger.warning(f"Failed to extract content from response: {e}")
            return None

    def _format_detection_result(
        self, api_result: Dict[str, Any], detection_type: str
    ) -> Dict[str, Any]:
        """
        将 API 原始结果格式化为 Protocol 约定的输出格式

        Args:
            api_result: _chat 方法返回的原始结果
            detection_type: 检测类型（"seal" 或 "signature"）

        Returns:
            符合 VisualCheckerProtocol 约定的字典
        """
        # 如果 API 调用失败，直接返回错误信息
        if not api_result.get("success", False):
            return {
                "success": False,
                "found": False,
                "confidence": 0.0,
                "reasoning": api_result.get("error", "Unknown error"),
                "location": "",
            }

        content = api_result.get("content", "")
        parsed = self._parse_detection_content(content)

        return {
            "success": True,
            "found": parsed["found"],
            "confidence": parsed["confidence"],
            "reasoning": parsed["reasoning"],
            "location": parsed["location"],
        }

    def _parse_detection_content(self, content: Any) -> Dict[str, Any]:
        """
        解析视觉模型的检测响应内容

        Args:
            content: API 返回的文本内容（字符串或列表）

        Returns:
            {
                "found": bool,
                "confidence": float,  # 0-1
                "location": str,
                "reasoning": str
            }
        """
        # 处理列表格式（新版 API 返回的是列表）
        if isinstance(content, list):
            content = "\n".join(
                [item.get("text", "") if isinstance(item, dict) else str(item) for item in content]
            )

        if not content or not isinstance(content, str):
            return {
                "found": False,
                "confidence": 0.0,
                "location": "",
                "reasoning": "Empty response",
            }

        content_lower = content.lower()

        # 判断是否存在
        found = False
        # 检查是否包含肯定表述（在明确回答区域）
        # 提取"是否存在"后面的回答（支持"是否存在："和"是否存在公章："等格式）
        existence_match = re.search(r"是否存在\w*[：:]\s*\[?(是|否|有|无|存在|不存在)\]?", content)
        if existence_match:
            answer = existence_match.group(1)
            found = answer in ["是", "有", "存在"]
        else:
            # 回退到关键词匹配
            positive_patterns = ["存在", "发现", "找到"]
            negative_patterns = ["不存在", "未找到", "未发现", "没有"]

            # 避免"是否"被误判为"否"
            has_positive = any(p in content for p in positive_patterns)
            has_negative = any(p in content for p in negative_patterns)

            if has_negative:
                found = False
            elif has_positive:
                found = True

        # 提取置信度
        confidence = 0.5
        if "高" in content:
            confidence = 0.9
        elif "中" in content:
            confidence = 0.6
        elif "低" in content:
            confidence = 0.3

        # 尝试提取数字置信度（支持 [0.95] 格式）
        num_match = re.search(r"置信度[:：]?\s*\[?(0?\.\d+|1\.0|1)\]?", content)
        if num_match:
            try:
                confidence = float(num_match.group(1))
            except ValueError:
                pass

        # 提取位置（简单实现）
        location = ""
        location_keywords = [
            "右下角",
            "左下角",
            "右上角",
            "左上角",
            "中央",
            "底部",
            "顶部",
            "页面中央",
        ]
        for kw in location_keywords:
            if kw in content:
                location = kw
                break

        return {
            "found": found,
            "confidence": confidence,
            "location": location,
            "reasoning": content[:300],  # 前300字符作为说明
        }
