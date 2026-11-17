"""Dify Tool adapter for CN Model Gateway."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..adapters.base import ChatMessage
from ..router import ModelRouter


class DifyToolAdapter:
    """Wraps ModelRouter as a Dify tool node (compatible with Dify's tool interface)."""

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

    def get_dify_provider_config(self) -> Dict[str, Any]:
        """Get Dify provider config (YAML-like dict for Dify's tool provider).

        Returns:
            Provider configuration dict for Dify.
        """
        return {
            "provider": "cn-model-gateway",
            "label": {"en": "CN Model Gateway", "zh": "国产模型 MCP 服务器"},
            "description": {
                "en": "Unified gateway for Chinese AI models",
                "zh": "国产大模型统一网关 - DeepSeek/通义/智谱/Kimi/混元/豆包/MiniMax/零一万物/百川/阶跃星辰",
            },
            "icon": "🔌",
            "credentials_schema": [],
            "tools": [
                {
                    "name": "ask_model",
                    "label": {"en": "Ask Model", "zh": "向模型提问"},
                    "description": {"en": "Ask a Chinese AI model a question", "zh": "向国产模型提问"},
                    "parameters": [
                        {"name": "question", "label": {"en": "Question", "zh": "问题"}, "type": "string", "required": True},
                        {"name": "provider", "label": {"en": "Provider", "zh": "提供商"}, "type": "string", "required": False},
                        {"name": "model", "label": {"en": "Model", "zh": "模型"}, "type": "string", "required": False},
                        {"name": "temperature", "label": {"en": "Temperature", "zh": "温度"}, "type": "number", "required": False},
                    ],
                },
                {
                    "name": "compare_models",
                    "label": {"en": "Compare Models", "zh": "对比模型"},
                    "description": {"en": "Compare answers from multiple models", "zh": "向多个模型发送同一问题，返回对比结果"},
                    "parameters": [
                        {"name": "question", "label": {"en": "Question", "zh": "问题"}, "type": "string", "required": True},
                        {"name": "providers", "label": {"en": "Providers", "zh": "提供商列表"}, "type": "array", "required": False},
                    ],
                },
                {
                    "name": "list_providers",
                    "label": {"en": "List Providers", "zh": "列出提供商"},
                    "description": {"en": "List all configured and available model providers", "zh": "列出所有已配置且可用的模型提供商"},
                    "parameters": [],
                },
            ],
        }

    def handle_dify_request(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Handle a Dify tool request.

        Args:
            tool_name: Tool name ("ask_model", "compare_models", "list_providers")
            parameters: Tool parameters dict

        Returns:
            Tool execution result string.
        """
        try:
            if tool_name == "ask_model":
                return self.ask_model(
                    question=parameters.get("question", ""),
                    provider=parameters.get("provider", ""),
                    model=parameters.get("model", ""),
                    temperature=parameters.get("temperature", 0.7),
                )
            elif tool_name == "compare_models":
                return self.compare_models(
                    question=parameters.get("question", ""),
                    providers=parameters.get("providers"),
                )
            elif tool_name == "list_providers":
                return self.list_providers()
            else:
                return f"未知工具: {tool_name}"
        except Exception as e:
            return f"调用失败: {e}"
