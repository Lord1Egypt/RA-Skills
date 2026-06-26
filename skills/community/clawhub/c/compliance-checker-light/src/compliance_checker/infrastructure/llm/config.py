"""
LLM 配置模块

Infrastructure 层的 LLM 配置数据类。
所有配置通过构造函数传入，不直接读取环境变量。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """
    LLM 配置数据类

    所有配置项通过构造函数传入，实现配置与代码的解耦。
    由 Application 层的 bootstrap 从环境变量读取后传入。

    Attributes:
        api_key: API 密钥
        base_url: API 端点 URL
        model: 模型名称
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
        system_prompt: 系统提示词
    """

    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    timeout: int = 60
    max_retries: int = 3
    system_prompt: str = (
        "你是一个严谨的数据处理助手，请严格按照要求的格式（如 JSON 或 YAML）输出，不要附带多余的解释。"
    )
