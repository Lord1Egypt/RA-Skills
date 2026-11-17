"""AutoGPT Plugin adapter for CN Model Gateway."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..adapters.base import ChatMessage
from ..router import ModelRouter


class AutoGPTPluginAdapter:
    """Wraps ModelRouter as an AutoGPT Plugin (compatible with AutoGPT's plugin interface)."""

    def __init__(self, router: ModelRouter) -> None:
        self.router = router

    def ask_model(self, question: str, provider: str = "",
                  model: str = "", temperature: float = 0.7) -> str:
        """向国产模型提问。"""
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

    def handle_prompt(self, prompt: str) -> str:
        """Handle a raw prompt string (AutoGPT compatibility)."""
        return self.ask_model(prompt)

    def get_autogpt_commands(self) -> Dict[str, Any]:
        """Get AutoGPT-compatible command functions.

        Returns:
            Dict mapping command names to callable functions.
        """
        return {
            "ask_model": self.ask_model,
            "compare_models": self.compare_models,
            "list_providers": self.list_providers,
        }
