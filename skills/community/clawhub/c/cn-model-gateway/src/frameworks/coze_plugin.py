"""Coze (扣子) Plugin adapter for CN Model Gateway."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ..adapters.base import ChatMessage
from ..router import ModelRouter


class CozePluginAdapter:
    """Wraps ModelRouter as a Coze plugin (compatible with Coze's OpenAPI plugin interface)."""

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

    def get_openapi_spec(self) -> Dict[str, Any]:
        """Get OpenAPI 3.0 spec for Coze plugin integration.

        Returns:
            OpenAPI specification dict that can be imported into Coze.
        """
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "CN Model Gateway",
                "description": "国产大模型统一网关 - DeepSeek/通义/智谱/Kimi/混元/豆包/MiniMax/零一万物/百川/阶跃星辰",
                "version": "1.0.0",
            },
            "paths": {
                "/ask_model": {
                    "post": {
                        "summary": "向国产模型提问",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "question": {"type": "string", "description": "要提问的内容"},
                                            "provider": {"type": "string", "description": "模型提供商"},
                                            "model": {"type": "string", "description": "具体模型 ID"},
                                            "temperature": {"type": "number", "description": "温度参数"},
                                        },
                                        "required": ["question"],
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "成功",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "content": {"type": "string"},
                                                "provider": {"type": "string"},
                                                "model": {"type": "string"},
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    }
                },
                "/compare_models": {
                    "post": {
                        "summary": "向多个模型发送同一问题，返回对比结果",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "question": {"type": "string"},
                                            "providers": {"type": "array", "items": {"type": "string"}},
                                        },
                                        "required": ["question"],
                                    }
                                }
                            }
                        },
                    }
                },
                "/list_providers": {
                    "get": {
                        "summary": "列出所有已配置且可用的模型提供商",
                    }
                },
            },
        }

    def handle_coze_request(self, path: str, method: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a Coze plugin request.

        Args:
            path: API path (e.g., "/ask_model")
            method: HTTP method ("get" or "post")
            body: Request body dict

        Returns:
            Response dict with status code and content.
        """
        try:
            if path == "/ask_model" and method == "post":
                result = self.ask_model(
                    question=body.get("question", ""),
                    provider=body.get("provider", ""),
                    model=body.get("model", ""),
                    temperature=body.get("temperature", 0.7),
                )
                return {"status": 200, "content": result}
            elif path == "/compare_models" and method == "post":
                result = self.compare_models(
                    question=body.get("question", ""),
                    providers=body.get("providers"),
                )
                return {"status": 200, "content": result}
            elif path == "/list_providers" and method == "get":
                result = self.list_providers()
                return {"status": 200, "content": result}
            else:
                return {"status": 404, "content": f"未知接口: {method} {path}"}
        except Exception as e:
            return {"status": 500, "content": str(e)}
