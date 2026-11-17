"""CrewAI Tool adapter for CN Model Gateway."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..adapters.base import ChatMessage
from ..router import ModelRouter


class CrewAIToolAdapter:
    """Wraps ModelRouter as a CrewAI Tool (compatible with crewai_tools.BaseTool)."""

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
        """向多个模型发送同一问题，返回对比结果。"""
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

    def get_crewai_tools(self) -> List[Any]:
        """Get CrewAI-compatible tool objects (requires crewai-tools to be installed).

        Usage:
            adapter = CrewAIToolAdapter(router)
            tools = adapter.get_crewai_tools()

        Returns:
            List of CrewAI tool objects.
        """
        try:
            from crewai_tools import BaseTool
        except ImportError:
            print("crewai-tools 未安装。请运行: pip install crewai-tools")
            return []

        class AskModelTool(BaseTool):
            name: str = "ask_model"
            description: str = "向国产模型提问"

            def _run(self, question: str, provider: str = "",
                     model: str = "", temperature: float = 0.7) -> str:
                return self.ask_model(question, provider, model, temperature)

        class CompareModelsTool(BaseTool):
            name: str = "compare_models"
            description: str = "向多个模型发送同一问题，返回对比结果"

            def _run(self, question: str, providers: Optional[List[str]] = None) -> str:
                return self.compare_models(question, providers)

        class ListProvidersTool(BaseTool):
            name: str = "list_providers"
            description: str = "列出所有已配置且可用的模型提供商"

            def _run(self) -> str:
                return self.list_providers()

        return [
            AskModelTool(),
            CompareModelsTool(),
            ListProvidersTool(),
        ]
