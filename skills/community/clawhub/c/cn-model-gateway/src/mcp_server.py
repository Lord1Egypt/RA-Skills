"""MCP (Model Context Protocol) server - JSON-RPC 2.0 implementation.

v1.9.0: Added health_report tool + HealthScheduler integration (daily health check,
        morning report HTML, provider change radar with 3σ anomaly detection).
v1.8.0: Added batch async (batch_submit/batch_result), SSE heartbeat + reconnect,
        merged resources into single "网关状态" status resource.
"""
from __future__ import annotations

import json
import sys
import time
import threading
import traceback
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

from .adapters.base import ChatMessage
from .batch_queue import BatchQueue, BatchWorker
from .router import ModelRouter
from .router import (
    ERROR_PARAM_INVALID,
    ERROR_MODEL_UNAVAILABLE,
    ERROR_RATE_LIMITED,
    ERROR_INTERNAL,
    ERROR_PROVIDER_NOT_FOUND,
)
from .monitor import Monitor
from .scheduler import HealthScheduler


# SSE constants
SSE_HEARTBEAT_INTERVAL = 30  # seconds
SSE_CHUNK_BUFFER_SIZE = 200  # max chunks buffered per request for reconnect


class ChunkBuffer:
    """Ring buffer for streaming chunks, supports reconnect via request_id."""

    def __init__(self, max_size: int = SSE_CHUNK_BUFFER_SIZE) -> None:
        self._buffers: Dict[str, List[str]] = defaultdict(list)
        self._max_size = max_size
        self._lock = threading.Lock()

    def append(self, request_id: str, chunk: str) -> None:
        with self._lock:
            buf = self._buffers[request_id]
            buf.append(chunk)
            # trim to max_size
            if len(buf) > self._max_size:
                self._buffers[request_id] = buf[-self._max_size :]

    def get_since(self, request_id: str, last_index: int = 0) -> List[str]:
        """Get chunks since last_index (for reconnect)."""
        with self._lock:
            buf = self._buffers.get(request_id, [])
            return buf[last_index:]

    def clear(self, request_id: str) -> None:
        with self._lock:
            self._buffers.pop(request_id, None)


class MCPServer:
    """Minimal MCP server implementing JSON-RPC 2.0 over stdio."""

    def __init__(self, router: ModelRouter, monitor: Monitor) -> None:
        self.router = router
        self.monitor = monitor
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._resources: Dict[str, Dict[str, Any]] = {}
        self._prompts: Dict[str, Dict[str, Any]] = {}
        self._chunk_buffer = ChunkBuffer(SSE_CHUNK_BUFFER_SIZE)
        self._batch_queue = BatchQueue()
        self._batch_worker = BatchWorker(
            queue=self._batch_queue,
            router=router,
            monitor=monitor,
        )
        self._batch_worker.start()
        self._health_scheduler = HealthScheduler()
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register built-in tools, resources, and prompts."""
        # v1.8.0: 2 new MCP tools added (batch_submit, batch_result)
        self._tools = {
            "ask_model": {
                "name": "ask_model",
                "description": "向国产模型提问。providers 为空时自动选一家（带故障转移）；"
                                "指定 2 家及以上时返回对比结果。支持 Function Calling（tools 参数）。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "要提问的内容"},
                        "provider": {"type": "string", "description": "模型提供商名称（可选，留空自动选择）"},
                        "providers": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "多提供商对比列表（可选，指定 2 家及以上时返回对比）",
                        },
                        "model": {"type": "string", "description": "具体模型 ID（可选）"},
                        "temperature": {"type": "number", "description": "温度参数 0-2（可选）"},
                        "tools": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "Function Calling 工具定义列表（可选，指定后模型可返回 tool_calls）",
                        },
                    },
                    "required": ["question"],
                },
            },
            "describe_image": {
                "name": "describe_image",
                "description": "向视觉模型发送图片，返回图片描述或回答图片相关问题。"
                                "支持 Qwen-VL、GLM-4V、豆包视觉等多模态模型。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "image": {"type": "string", "description": "图片 URL / base64 / 文件路径"},
                        "prompt": {"type": "string", "description": "关于图片的问题（可选，默认\"请描述这张图片\"）"},
                        "provider": {"type": "string", "description": "模型提供商名称（可选，留空自动选择）"},
                        "model": {"type": "string", "description": "具体模型 ID（可选）"},
                    },
                    "required": ["image"],
                },
            },
            "embed_text": {
                "name": "embed_text",
                "description": "将文本转换为向量嵌入（embedding）。支持 deepseek、zhipu、doubao、tongyi 等提供商。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "texts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要嵌入的文本列表（至少 1 条，最多 100 条）",
                        },
                        "provider": {"type": "string", "description": "模型提供商名称（可选，留空自动选择）"},
                        "model": {"type": "string", "description": "嵌入模型 ID（可选，默认使用提供商推荐模型）"},
                    },
                    "required": ["texts"],
                },
            },
            "rerank": {
                "name": "rerank",
                "description": "对文档列表按查询相关性进行重排序。支持 zhipu 等提供商。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "查询文本"},
                        "documents": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "待排序的文档列表",
                        },
                        "provider": {"type": "string", "description": "模型提供商名称（可选，留空自动选择）"},
                        "model": {"type": "string", "description": "重排序模型 ID（可选）"},
                    },
                    "required": ["query", "documents"],
                },
            },
            "audio_transcribe": {
                "name": "audio_transcribe",
                "description": "将音频文件转换为文字（语音识别）。支持 zhipu、doubao 等提供商。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "audio": {"type": "string", "description": "音频文件 URL / base64 / 文件路径（支持 mp3/wav/flac 等格式）"},
                        "provider": {"type": "string", "description": "模型提供商名称（可选，留空自动选择）"},
                        "model": {"type": "string", "description": "语音识别模型 ID（可选）"},
                        "language": {"type": "string", "description": "音频语言（可选，默认自动检测）"},
                    },
                    "required": ["audio"],
                },
            },
            "video_understand": {
                "name": "video_understand",
                "description": "理解视频内容：抽取关键帧 → 视觉模型描述 → 拼接为完整视频摘要。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "video": {"type": "string", "description": "视频文件 URL / 文件路径"},
                        "prompt": {"type": "string", "description": "描述提示（可选，默认\"请描述这个视频的内容\"）"},
                        "provider": {"type": "string", "description": "模型提供商名称（可选，留空自动选择）"},
                        "model": {"type": "string", "description": "视觉模型 ID（可选）"},
                    },
                    "required": ["video"],
                },
            },
            "batch_submit": {
                "name": "batch_submit",
                "description": "提交批量任务列表，立即返回任务 ID。"
                                "后台顺序执行（复用硬件自适应并发），失败任务自动重试一次。"
                                "用 batch_result 轮询结果。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tasks": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "任务列表。每项包含 tool（ask_model/describe_image）和 arguments。",
                        },
                        "priority": {
                            "type": "integer",
                            "description": "优先级 0-9（默认 5，数字越小优先级越高）",
                        },
                    },
                    "required": ["tasks"],
                },
            },
            "batch_result": {
                "name": "batch_result",
                "description": "查询批量任务状态和结果。返回每个任务的执行状态、结果或错误详情。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "任务 ID（由 batch_submit 返回）"},
                        "include_items": {
                            "type": "boolean",
                            "description": "是否包含每个子项的详细结果（默认 false，仅返回汇总）",
                        },
                    },
                    "required": ["task_id"],
                },
            },
            "list_providers": {
                "name": "list_providers",
                "description": "列出所有已配置且可用的模型提供商。",
                "inputSchema": {"type": "object", "properties": {}},
            },
            "health_check": {
                "name": "health_check",
                "description": "检查所有已配置模型提供商的连通性。",
                "inputSchema": {"type": "object", "properties": {}},
            },
            "health_report": {
                "name": "health_report",
                "description": "生成每日健康晨报（本地 HTML），含各厂商成功率/延迟/配额余量 + 厂商变更雷达（3σ 异常检测）。"
                                "可选参数：save（是否保存到文件，默认 true）、days（统计天数，默认 1）。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "save": {"type": "boolean", "description": "是否保存 HTML 到本地文件（默认 true）"},
                        "days": {"type": "integer", "description": "统计天数（默认 1，最大 7）"},
                    },
                },
            },
        }

        # v1.8.0: merged config + usage into single status resource
        self._resources = {
            "status": {
                "uri": "cn-model-gateway://status",
                "name": "网关状态",
                "description": "查看当前配置、使用统计、配额告警（一屏汇总）",
                "mimeType": "application/json",
            },
        }

        self._prompts = {
            "code_review": {
                "name": "code_review",
                "description": "代码审查提示模板",
                "arguments": [
                    {"name": "code", "description": "要审查的代码", "required": True},
                    {"name": "language", "description": "编程语言", "required": False},
                ],
            },
            "translate": {
                "name": "translate",
                "description": "翻译提示模板（中英互译）",
                "arguments": [
                    {"name": "text", "description": "要翻译的文本", "required": True},
                    {"name": "target_lang", "description": "目标语言（zh/en/ja）", "required": True},
                ],
            },
        }

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle a single JSON-RPC 2.0 request. Returns response or None for notifications."""
        req_id = request.get("id")
        method = request.get("method", "")
        params = request.get("params", {})

        # MCP initialization
        if method == "initialize":
            return self._success(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False},
                },
                "serverInfo": {
                    "name": "cn-model-gateway",
                    "version": "1.9.0",
                    "description": "国产模型 MCP 服务器 - DeepSeek/通义/智谱/Kimi/混元/豆包/MiniMax/零一万物/百川/阶跃星辰 10 家一站式接入，含每日健康晨报与厂商变更雷达",
                },
            })

        # Tools
        if method == "tools/list":
            return self._success(req_id, {"tools": list(self._tools.values())})
        if method == "tools/call":
            return self._handle_tool_call(req_id, params)

        # Resources
        if method == "resources/list":
            return self._success(req_id, {"resources": list(self._resources.values())})
        if method == "resources/read":
            return self._handle_resource_read(req_id, params)

        # Prompts
        if method == "prompts/list":
            return self._success(req_id, {"prompts": list(self._prompts.values())})
        if method == "prompts/get":
            return self._handle_prompt_get(req_id, params)

        # Ping
        if method == "ping":
            return self._success(req_id, {})

        return self._error(req_id, -32601, f"未知方法: {method}")

    def _handle_tool_call(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name", "")
        args = params.get("arguments", {})
        handler: Optional[Callable] = getattr(self, f"_tool_{name}", None)
        if not handler:
            return self._error(req_id, ERROR_PARAM_INVALID, f"未知工具: {name}")
        try:
            result = handler(args)
            self.monitor.record_call(name, args, result)
            return self._success(req_id, {"content": [{"type": "text", "text": result}]})
        except Exception as e:
            return self._error(req_id, ERROR_INTERNAL, f"工具调用失败: {traceback.format_exc()}")

    def _tool_ask_model(self, args: Dict[str, Any]) -> str:
        """Unified ask tool: single provider or multi-provider compare."""
        question = args.get("question", "")
        if not question:
            raise ValueError("question 不能为空")

        tools = args.get("tools")
        kwargs: Dict[str, Any] = {}
        if args.get("model"):
            kwargs["model"] = args["model"]
        if args.get("temperature") is not None:
            kwargs["temperature"] = args["temperature"]
        if tools:
            kwargs["tools"] = tools

        providers = args.get("providers")
        if providers and len(providers) >= 2:
            return self._compare_models_internal(question, providers, **kwargs)

        provider = args.get("provider")
        msgs = [ChatMessage(role="user", content=question)]
        resp = self.router.chat(msgs, provider=provider, **kwargs)
        return self._format_response(resp)

    def _compare_models_internal(self, question: str, providers: List[str], **kwargs: Any) -> str:
        """Internal: compare multiple providers."""
        msgs = [ChatMessage(role="user", content=question)]
        results = self.router.compare_models(msgs, providers=providers, **kwargs)
        lines = [f"## 模型对比结果\n问题: {question}\n"]
        for provider, info in results.items():
            lines.append(f"### {provider}")
            if "error" in info:
                lines.append(f"  ❌ {info['error']}")
            else:
                lines.append(f"  模型: {info['model']}")
                lines.append(f"  耗时: {info['duration_ms']}ms")
                lines.append(f"  Token: {info['usage']}")
                lines.append(f"  回答: {info['content'][:200]}...")
            lines.append("")
        return "\n".join(lines)

    def _format_response(self, resp: Any) -> str:
        """Format a ChatResponse into display string."""
        lines = [
            f"[via {resp.provider}/{resp.model}]\n{resp.content}\n",
            f"---\n耗时: {resp.duration_ms}ms | ",
            f"Token: prompt={resp.usage.get('prompt_tokens', '?')}, ",
            f"completion={resp.usage.get('completion_tokens', '?')}",
        ]
        if resp.tool_calls:
            tc_lines = ["", "### Tool Calls:"]
            for tc in resp.tool_calls:
                tc_lines.append(f"  - {tc.name}({tc.arguments})")
            lines.append("\n".join(tc_lines))
        return "".join(lines)

    def _tool_describe_image(self, args: Dict[str, Any]) -> str:
        """Describe an image using vision models."""
        image = args.get("image", "")
        if not image:
            raise ValueError("image 不能为空")
        prompt = args.get("prompt", "请描述这张图片")
        provider = args.get("provider")
        model = args.get("model")

        adapter = None
        if provider:
            adapter = self.router.get_adapter(provider)
        else:
            available = self.router.list_available()
            if available:
                adapter = self.router.get_adapter(available[0])

        if not adapter:
            return "没有可用的模型提供商。请在 config.json 中填写 api_key。"

        try:
            resp = adapter.describe_image(image, prompt, model=model)
            return self._format_response(resp)
        except Exception as e:
            return f"图片描述失败: {e}"

    # --- v1.6.0: 4 new MCP tool handlers ---

    def _tool_embed_text(self, args: Dict[str, Any]) -> str:
        """Generate text embeddings."""
        texts = args.get("texts", [])
        if not texts:
            raise ValueError("texts 不能为空")
        provider = args.get("provider")
        model = args.get("model")

        adapter = None
        if provider:
            adapter = self.router.get_adapter(provider)
        else:
            for p in self.router.list_available():
                a = self.router.get_adapter(p)
                if a and hasattr(a, "embed_text"):
                    try:
                        from llm_core.adapters.base import BaseAdapter

                        if a.embed_text.__func__ is not BaseAdapter.embed_text:
                            adapter = a
                            break
                    except Exception:
                        pass
            if not adapter:
                available = self.router.list_available()
                if available:
                    adapter = self.router.get_adapter(available[0])

        if not adapter:
            return "没有可用的模型提供商。请在 config.json 中填写 api_key。"

        try:
            result = adapter.embed_text(texts, model=model)
            lines = [
                f"## 向量嵌入结果\n提供商: {result.provider}\n模型: {result.model}\n"
                f"耗时: {result.duration_ms}ms\nToken: {result.usage}\n",
                f"嵌入维度: {len(result.embeddings[0]) if result.embeddings else 0}",
                f"嵌入数量: {len(result.embeddings)}",
            ]
            return "\n".join(lines)
        except NotImplementedError as e:
            return f"该提供商不支持向量嵌入: {e}"
        except Exception as e:
            return f"向量嵌入失败: {e}"

    def _tool_rerank(self, args: Dict[str, Any]) -> str:
        """Rerank documents by relevance to query."""
        query = args.get("query", "")
        documents = args.get("documents", [])
        if not query or not documents:
            raise ValueError("query 和 documents 不能为空")
        provider = args.get("provider")
        model = args.get("model")

        adapter = None
        if provider:
            adapter = self.router.get_adapter(provider)
        else:
            for p in self.router.list_available():
                a = self.router.get_adapter(p)
                if a and hasattr(a, "rerank"):
                    from llm_core.adapters.base import BaseAdapter

                    if a.rerank.__func__ is not BaseAdapter.rerank:
                        adapter = a
                        break
            if not adapter:
                available = self.router.list_available()
                if available:
                    adapter = self.router.get_adapter(available[0])

        if not adapter:
            return "没有可用的模型提供商。请在 config.json 中填写 api_key。"

        try:
            result = adapter.rerank(query, documents, model=model)
            lines = [
                f"## 重排序结果\n提供商: {result.provider}\n模型: {result.model}\n"
                f"耗时: {result.duration_ms}ms\n",
            ]
            for i, score in enumerate(result.scores):
                doc_preview = (
                    documents[i][:50] + "..."
                    if len(documents[i]) > 50
                    else documents[i]
                )
                lines.append(f"  [{i + 1}] 相关度: {score:.4f} | {doc_preview}")
            return "\n".join(lines)
        except NotImplementedError as e:
            return f"该提供商不支持重排序: {e}"
        except Exception as e:
            return f"重排序失败: {e}"

    def _tool_audio_transcribe(self, args: Dict[str, Any]) -> str:
        """Transcribe audio to text."""
        audio = args.get("audio", "")
        if not audio:
            raise ValueError("audio 不能为空")
        provider = args.get("provider")
        model = args.get("model")
        language = args.get("language", "")

        adapter = None
        if provider:
            adapter = self.router.get_adapter(provider)
        else:
            for p in self.router.list_available():
                a = self.router.get_adapter(p)
                if a and hasattr(a, "audio_transcribe"):
                    from llm_core.adapters.base import BaseAdapter

                    if a.audio_transcribe.__func__ is not BaseAdapter.audio_transcribe:
                        adapter = a
                        break
            if not adapter:
                available = self.router.list_available()
                if available:
                    adapter = self.router.get_adapter(available[0])

        if not adapter:
            return "没有可用的模型提供商。请在 config.json 中填写 api_key。"

        try:
            kwargs = {}
            if language:
                kwargs["language"] = language
            result = adapter.audio_transcribe(audio, model=model, **kwargs)
            return (
                f"## 语音转文字结果\n提供商: {result.provider}\n模型: {result.model}\n"
                f"语言: {result.language}\n耗时: {result.duration_ms}ms\n\n"
                f"识别文本:\n{result.text}"
            )
        except NotImplementedError as e:
            return f"该提供商不支持语音转文字: {e}"
        except Exception as e:
            return f"语音转文字失败: {e}"

    def _tool_video_understand(self, args: Dict[str, Any]) -> str:
        """Understand video content via keyframe extraction + vision model."""
        video = args.get("video", "")
        if not video:
            raise ValueError("video 不能为空")
        prompt = args.get("prompt", "请描述这个视频的内容")
        provider = args.get("provider")
        model = args.get("model")

        adapter = None
        if provider:
            adapter = self.router.get_adapter(provider)
        else:
            for p in self.router.list_available():
                a = self.router.get_adapter(p)
                if a and hasattr(a, "video_understand"):
                    from llm_core.adapters.base import BaseAdapter

                    if a.video_understand.__func__ is not BaseAdapter.video_understand:
                        adapter = a
                        break
            if not adapter:
                available = self.router.list_available()
                if available:
                    adapter = self.router.get_adapter(available[0])

        if not adapter:
            return "没有可用的模型提供商。请在 config.json 中填写 api_key。"

        try:
            result = adapter.video_understand(video, prompt, model=model)
            return (
                f"## 视频理解结果\n提供商: {result.provider}\n模型: {result.model}\n"
                f"关键帧数: {result.keyframe_count}\n耗时: {result.duration_ms}ms\n\n"
                f"视频描述:\n{result.description}"
            )
        except NotImplementedError as e:
            return f"该提供商不支持视频理解: {e}"
        except Exception as e:
            return f"视频理解失败: {e}"

    # --- v1.8.0: batch async tool handlers ---

    def _tool_batch_submit(self, args: Dict[str, Any]) -> str:
        """Submit batch tasks for async execution."""
        tasks = args.get("tasks", [])
        if not tasks:
            raise ValueError("tasks 不能为空")
        if not isinstance(tasks, list):
            raise ValueError("tasks 必须是列表")
        priority = args.get("priority", 5)
        if not isinstance(priority, int) or priority < 0 or priority > 9:
            raise ValueError("priority 必须是 0-9 的整数")

        task_id = self._batch_queue.create_task(tasks, priority=priority)
        return (
            f"## 批量任务已提交\n任务 ID: `{task_id}`\n"
            f"任务数量: {len(tasks)}\n优先级: {priority}\n\n"
            f"使用 `batch_result` 工具查询结果。示例：\n"
            f'{{"tool": "batch_result", "arguments": {{"task_id": "{task_id}"}}}}'
        )

    def _tool_batch_result(self, args: Dict[str, Any]) -> str:
        """Query batch task status and results."""
        task_id = args.get("task_id", "")
        if not task_id:
            raise ValueError("task_id 不能为空")
        include_items = args.get("include_items", False)

        task = self._batch_queue.get_task(task_id)
        if not task:
            return f"任务 `{task_id}` 不存在或已过期清理。"

        lines = [
            f"## 批量任务状态\n"
            f"任务 ID: `{task_id}`\n"
            f"状态: {task["status"]}\n"
            f"优先级: {task.get("priority", 5)}\n"
            f"创建时间: {task["created_at"]}\n"
        ]

        if task.get("started_at"):
            lines.append(f"开始时间: {task['started_at']}")
        if task.get("finished_at"):
            lines.append(f"结束时间: {task['finished_at']}")

        items = self._batch_queue.list_items(task_id)
        total = len(items)
        done = sum(1 for i in items if i["status"] == "done")
        failed = sum(1 for i in items if i["status"] == "failed")
        pending = sum(1 for i in items if i["status"] in ("pending", "retrying"))
        running = sum(1 for i in items if i["status"] == "running")

        lines.append(
            f"\n进度: {done + failed}/{total}"
            f"（完成 {done}，失败 {failed}，"
            f"运行中 {running}，等待 {pending}）"
        )

        if include_items:
            lines.append("\n### 子项详情")
            for i, item in enumerate(items):
                lines.append(f"\n#### 子项 {i + 1}（{item['status']}）")
                lines.append(f"工具: {item['tool']}")
                if item.get("error"):
                    lines.append(f"错误: {item['error']}")
                if item.get("result"):
                    result_preview = item["result"][:200]
                    if len(item["result"]) > 200:
                        result_preview += "..."
                    lines.append(f"结果: {result_preview}")
                if item.get("retried"):
                    lines.append("（已自动重试）")

        return "\n".join(lines)

    def _tool_list_providers(self, args: Dict[str, Any]) -> str:
        available = self.router.list_available()
        all_providers = list(self.router._adapters.keys())
        lines = ["## 模型提供商状态"]
        for p in all_providers:
            status = "✅ 可用" if p in available else "❌ 不可用"
            lines.append(f"- {p}: {status}")
        if not all_providers:
            lines.append("尚未配置任何提供商。请在 config.json 中填写 api_key。")
        return "\n".join(lines)

    def _tool_health_check(self, args: Dict[str, Any]) -> str:
        results = {}
        for provider, adapter in self.router._adapters.items():
            try:
                ok = adapter.check_health()
                results[provider] = "✅ 正常" if ok else "❌ 异常"
            except Exception as e:
                results[provider] = f"❌ {e}"
        lines = ["## 健康检查"]
        for p, s in results.items():
            lines.append(f"- {p}: {s}")
        return "\n".join(lines)

    def _tool_health_report(self, args: Dict[str, Any]) -> str:
        """生成每日健康晨报。"""
        save = args.get("save", True)
        days = min(args.get("days", 1), 7)
        html = self._health_scheduler.generate_morning_report()
        path = None
        if save:
            path = self._health_scheduler.save_report()
        lines = ["## 每日健康晨报"]
        if path:
            lines.append(f"已保存到: {path}")
        lines.append("")
        # 提取纯文本摘要（去掉 HTML 标签）
        import re
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\n{3,}', '\n\n', text)
        lines.append(text[:2000])
        return "\n".join(lines)

    def _handle_resource_read(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        uri = params.get("uri", "")
        if uri == "cn-model-gateway://status":
            # v1.8.0: merged config + usage + quota alerts
            config_info = {}
            for provider, adapter in self.router._adapters.items():
                config_info[provider] = {
                    "available": adapter.is_available(),
                    "default_model": adapter.default_model,
                }
            usage_stats = self.monitor.get_stats()
            merged = {
                "config": config_info,
                "usage": usage_stats,
                "quota_alerts": self._compute_quota_alerts(usage_stats),
            }
            content = json.dumps(merged, ensure_ascii=False, indent=2)
            return self._success(req_id, {
                "contents": [{"uri": uri, "mimeType": "application/json", "text": content}]
            })
        return self._error(req_id, ERROR_PARAM_INVALID, f"未知资源: {uri}")

    def _compute_quota_alerts(self, usage_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compute quota alerts based on usage statistics."""
        alerts = []
        provider_stats = usage_stats.get("providers", {})
        for provider, stats in provider_stats.items():
            total_calls = stats.get("total_calls", 0)
            error_calls = stats.get("error_calls", 0)
            if total_calls > 0:
                error_rate = error_calls / total_calls
                if error_rate > 0.5 and total_calls >= 5:
                    alerts.append({
                        "provider": provider,
                        "level": "warning",
                        "message": f"错误率 {error_rate:.0%}（{error_calls}/{total_calls}）",
                    })
        return alerts

    def _handle_prompt_get(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name", "")
        arguments = params.get("arguments", {})
        prompt = self._prompts.get(name)
        if not prompt:
            return self._error(req_id, ERROR_PARAM_INVALID, f"未知 prompt: {name}")

        templates = {
            "code_review": self._build_code_review(arguments),
            "translate": self._build_translate(arguments),
        }
        messages = templates.get(name, [])
        return self._success(req_id, {
            "description": prompt["description"],
            "messages": messages,
        })

    @staticmethod
    def _build_code_review(args: Dict[str, Any]) -> List[Dict[str, Any]]:
        code = args.get("code", "")
        language = args.get("language", "python")
        return [
            {
                "role": "system",
                "content": f"你是一位资深 {language} 代码审查专家。请审查以下代码，指出潜在问题、安全隐患和改进建议。",
            },
            {"role": "user", "content": f"```{language}\n{code}\n```"},
        ]

    @staticmethod
    def _build_translate(args: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = args.get("text", "")
        target = args.get("target_lang", "en")
        lang_map = {"zh": "中文", "en": "英文", "ja": "日文"}
        target_name = lang_map.get(target, target)
        return [
            {
                "role": "system",
                "content": f"你是一位专业翻译。请将以下文本翻译为{target_name}，保持语义准确、表达自然。",
            },
            {"role": "user", "content": text},
        ]

    def _success(self, req_id: Any, result: Any) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def _error(self, req_id: Any, code: int, message: str) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    def run_stdio(self) -> None:
        """Run the MCP server over stdio (for Claude Code / Cursor / Cline)."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    self._send(self._error(None, -32700, f"JSON 解析错误: {e}"))
                    continue
                response = self.handle_request(request)
                if response is not None:
                    self._send(response)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self._send(self._error(None, ERROR_INTERNAL, f"服务器错误: {e}"))

    def _send(self, response: Dict[str, Any]) -> None:
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def shutdown(self) -> None:
        """Gracefully stop the batch worker and cleanup."""
        self._batch_worker.stop()
        self._health_scheduler.stop_scheduler()
