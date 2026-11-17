"""兼容别名 — 环境检测已迁入 env.py（v3.0 统一入口）

ZIP 版 environment.py 的功能已全部在本地 env.py 中实现，
且本地版更完整（增加 AgentType/ASR/LLM 能力检测）。

此文件保留向后兼容，内部全部委托到 env.py。
"""

from .env import (
    EnvironmentContext,
    get_environment_context as detect,
    get_environment_context,
    print_profile,
)
