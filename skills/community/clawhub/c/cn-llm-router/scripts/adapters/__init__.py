"""适配器包：统一 chat() 接口，归一各家请求 / 响应 / 错误。"""

from .base import AdapterError, AdapterBase
from .openai_compat import OpenAICompatAdapter
from .ernie import ErnieAdapter
from .spark import SparkAdapter

# 适配器注册表：adapter 类型名 → 类
REGISTRY = {
    "openai_compat": OpenAICompatAdapter,
    "ernie": ErnieAdapter,
    "spark": SparkAdapter,
}


def build(adapter_type, provider_cfg):
    """按 adapter 类型构造适配器实例。"""
    cls = REGISTRY.get(adapter_type)
    if not cls:
        raise AdapterError("不支持的适配器类型: %s" % adapter_type)
    return cls(provider_cfg)
