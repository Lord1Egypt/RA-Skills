"""Framework adapters for non-MCP agent frameworks.

Each adapter wraps the core ModelRouter to work with a specific agent framework.
All adapters use lazy imports so the core skill remains zero-dependency.
"""

from .langchain_tool import LangChainToolAdapter
from .autogpt_plugin import AutoGPTPluginAdapter
from .crewai_tool import CrewAIToolAdapter
from .coze_plugin import CozePluginAdapter
from .dify_tool import DifyToolAdapter

__all__ = [
    "LangChainToolAdapter",
    "AutoGPTPluginAdapter",
    "CrewAIToolAdapter",
    "CozePluginAdapter",
    "DifyToolAdapter",
]
