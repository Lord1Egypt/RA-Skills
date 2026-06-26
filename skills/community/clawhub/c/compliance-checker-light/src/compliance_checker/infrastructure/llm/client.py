"""
LLM 客户端模块

Infrastructure 层的 LLM 客户端实现，遵循 Core 层的 LLMClientProtocol。
将外部 HTTP 错误转化为 Core 层的统一异常。
"""

import asyncio
import logging
from typing import Optional

import yaml

try:
    import openai

    _has_openai = True
except ImportError:
    _has_openai = False
    logging.warning("openai 未安装，LLM 功能将不可用。请运行: pip install openai")

from ...core.exceptions import CheckExecutionError
from ...core.interfaces import LLMClientProtocol
from .config import LLMConfig

logger = logging.getLogger(__name__)


class LLMClient(LLMClientProtocol):
    """
    LLM 客户端

    Infrastructure 层的 LLM 客户端实现，遵循 Core 层的 LLMClientProtocol。
    封装 OpenAI 兼容 API 的调用，支持重试和错误处理。
    将外部 HTTP 错误转化为 Core 层的 CheckExecutionError。

    Attributes:
        config: LLM 配置对象
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 LLM 客户端

        Args:
            config: LLM 配置对象，包含 api_key、base_url 等配置

        Raises:
            ImportError: 如果 openai 包未安装
        """
        if not _has_openai:
            raise ImportError("使用 LLM 功能需要安装 openai: pip install openai")

        self.config = config
        self._client = openai.AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )

    async def complete(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2000) -> str:
        """
        调用 LLM 完成文本生成

        Args:
            prompt: 提示词
            temperature: 温度参数 (0-1，越低越确定)
            max_tokens: 最大生成 token 数

        Returns:
            生成的文本内容

        Raises:
            CheckExecutionError: API 调用失败时抛出，包含原始错误信息
        """
        try:
            response = await self._client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.config.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            if content is None:
                raise CheckExecutionError("LLM 返回空内容")

            logger.info(f"LLM 调用成功，生成 {len(content)} 字符")
            return content

        except openai.APIError as e:
            logger.error(f"LLM API 错误: {e}")
            raise CheckExecutionError(f"LLM API 错误: {e}") from e
        except openai.APITimeoutError as e:
            logger.error(f"LLM 请求超时: {e}")
            raise CheckExecutionError(f"LLM 请求超时: {e}") from e
        except openai.RateLimitError as e:
            logger.error(f"LLM 请求频率超限: {e}")
            raise CheckExecutionError(f"LLM 请求频率超限: {e}") from e
        except openai.AuthenticationError as e:
            logger.error(f"LLM API 认证失败: {e}")
            raise CheckExecutionError(f"LLM API 认证失败，请检查 API Key: {e}") from e
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            raise CheckExecutionError(f"LLM 调用失败: {e}") from e

    async def generate_yaml(self, prompt_text: str, temperature: float = 0.3) -> dict:
        """
        调用 LLM 生成 YAML 格式内容

        Args:
            prompt_text: 完整的提示词文本（由 Application 层构建）
            temperature: 温度参数

        Returns:
            解析后的 YAML 字典

        Raises:
            CheckExecutionError: LLM 调用失败或 YAML 解析失败
        """
        # 调用 LLM
        try:
            content = await self.complete(prompt_text, temperature=temperature)
        except CheckExecutionError:
            raise

        # 清理内容（去除可能的 markdown 代码块标记）
        content = self._clean_yaml_content(content)

        # 解析 YAML
        try:
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                raise CheckExecutionError("LLM 生成的内容不是有效的字典结构")
            if "checklist" not in data:
                raise CheckExecutionError("生成的 YAML 缺少 'checklist' 根节点")
            return data
        except yaml.YAMLError as e:
            logger.error(f"YAML 解析失败: {e}\n内容: {content[:500]}")
            raise CheckExecutionError(f"LLM 生成的内容不是有效的 YAML: {e}") from e

    def _clean_yaml_content(self, content: str) -> str:
        """
        清理 YAML 内容

        去除 markdown 代码块标记等

        Args:
            content: 原始内容

        Returns:
            清理后的内容
        """
        # 去除开头的 ```yaml 或 ```
        lines = content.strip().split("\n")

        # 找到第一个非空行
        start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith("```"):
                start_idx = i
                break

        # 找到最后一个非 ``` 行
        end_idx = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and not lines[i].strip().startswith("```"):
                end_idx = i + 1
                break

        return "\n".join(lines[start_idx:end_idx])
