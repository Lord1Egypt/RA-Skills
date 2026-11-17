"""LangChain Tool adapter for CN Model Gateway."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..adapters.base import ChatMessage
from ..router import ModelRouter


class LangChainToolAdapter:
    """Wraps ModelRouter as a LangChain Tool (compatible with langchain.tools.tool)."""

    def __init__(self, router: ModelRouter) -> None:
        self.router = router

    def ask_model(self, question: str, provider: str = "",
                  model: str = "", temperature: float = 0.7) -> str:
        """向国产模型提问。

        Args:
            question: 要提问的内容
            provider: 模型提供商（deepseek/tongyi/zhipu/kimi/hunyuan/doubao/minimax/lingyi/baichuan/stepfun），留空自动选择
            model: 具体模型 ID（可选）
            temperature: 温度参数 0-2（可选）

        Returns:
            模型回答文本
        """
        msgs = [ChatMessage(role="user", content=question)]
        kwargs: Dict[str, Any] = {"temperature": temperature}
        if model:
            kwargs["model"] = model
        try:
            resp = self.router.chat(msgs, provider=provider or None, **kwargs)
            return resp.content
        except Exception as e:
            return f"调用失败: {e}"

    def compare_models(self, question: str,
                       providers: Optional[List[str]] = None) -> str:
        """向多个模型发送同一问题，返回对比结果。

        Args:
            question: 要提问的内容
            providers: 要对比的提供商列表（可选，默认全部可用）

        Returns:
            各模型回答对比文本
        """
        msgs = [ChatMessage(role="user", content=question)]
        try:
            results = self.router.compare_models(msgs, providers=providers)
            lines = [f"## 模型对比: {question}\n"]
            for p, info in results.items():
                lines.append(f"### {p}")
                if "error" in info:
                    lines.append(f"  ❌ {info['error']}")
                else:
                    lines.append(f"  回答: {info['content'][:150]}...")
                lines.append("")
            return "\n".join(lines)
        except Exception as e:
            return f"调用失败: {e}"

    def list_providers(self) -> str:
        """列出所有已配置且可用的模型提供商。"""
        try:
            available = self.router.list_available()
            return "可用提供商: " + ", ".join(available) if available else "暂无可用提供商"
        except Exception as e:
            return f"调用失败: {e}"

    def get_langchain_tool(self, name: str = "ask_model") -> Any:
        """Get a LangChain-compatible tool object (requires langchain to be installed).

        Usage:
            from langchain.tools import tool
            adapter = LangChainToolAdapter(router)
            lc_tool = adapter.get_langchain_tool("ask_model")

        Returns:
            A LangChain StructuredTool or None if langchain is not installed.
        """
        try:
            from langchain.tools import tool
        except ImportError:
            print("langchain 未安装。请运行: pip install langchain")
            return None

        if name == "ask_model":
            return tool(self.ask_model)
        elif name == "compare_models":
            return tool(self.compare_models)
        elif name == "list_providers":
            return tool(self.list_providers)
        else:
            raise ValueError(f"未知工具名: {name}")
