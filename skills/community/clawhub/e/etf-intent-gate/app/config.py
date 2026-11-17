"""配置项：从环境变量 / .env 读取，集中管理。"""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    intent_llm_base_url: str = ""          # 如 https://open.bigmodel.cn/api/paas/v4
    intent_llm_api_key: str = ""           # 留空 => mock 模式
    intent_llm_model: str = "glm-4-flash"
    intent_llm_timeout_seconds: float = 5.0

    # 降级模式
    intent_degrade_mode: str = "conservative"  # conservative | loose

    # 输入长度
    intent_max_query_length: int = 2000

    # 平台能力边界（写入 LLM System Prompt）
    intent_platform_boundary: str = (
        "本平台仅做ETF/行业/指数投研信息分析，不提供买卖建议、不做个股荐股，"
        "不能预测涨跌，不提供投资决策。"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
