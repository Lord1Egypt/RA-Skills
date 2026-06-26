"""
GPT-6 Execution Engine Adapter

GPT-6 执行引擎适配器 - 适配 OpenAI GPT-6 模型

概述:
    GPT-6 是 OpenAI 第六代大语言模型，具备以下核心能力：
    - 200万 Token 超长上下文（context_2m）
    - 五模态 Symphony 多模态（文字/图像/音频/视频/代码）
    - 91% 智能体任务完成率（agent_completion_91）
    - OpenAI API 完全兼容

能力矩阵:
    - session_persistence:  True    会话保持
    - harness_control:     True    工具调用控制
    - sandbox:              True    沙箱隔离
    - credential_management: True   凭证管理（官方）
    - self_evolution:        False   暂不支持 M-A3 自进化
    - vertical_knowledge:    False   需自建垂直知识库
    - multimodal:           True    Symphony 五模态
    - context_2m:           True    200万 Token 上下文
    - agent_completion_91:  True    91% 任务完成率

配置:
    见 config/engines.yaml 中的 gpt6 配置项

API Reference:
    https://platform.openai.com/docs/api-reference

Change Log:
    - 2026-04-14: 初始版本（v3.0 新增 GPT-6 引擎）
"""

from __future__ import annotations

import asyncio
import logging
import time as _time
from typing import Any, AsyncIterator, Dict

from .engine_base import (
    AuthProfile,
    AuthKeyState,
    ExecutionEngine,
    ExecutionResult,
    NoAvailableKeyError,
    StreamChunk,
)
from .circuit_breaker import report_request_result

logger = logging.getLogger(__name__)


class GPT6Engine(ExecutionEngine):
    """
    GPT-6 执行引擎

    封装 OpenAI GPT-6 API，兼容 OpenAI Chat Completions 接口格式。

    核心能力:
        - 200万 Token 超长上下文窗口
        - Symphony 五模态（文字/图像/音频/视频/代码）
        - 91% 智能体任务完成率
        - OpenAI API 完全兼容

    使用场景:
        - 超长文档分析（合同/报告/技术文档）
        - 多模态任务（图文混合理解）
        - 复杂智能体任务（多步骤推理+工具调用）
        - 高吞吐量并发任务

    API Reference:
        https://platform.openai.com/docs/api-reference
    """

    # 支持的模型列表
    SUPPORTED_MODELS = {
        "gpt-6",           # GPT-6 标准版
        "gpt-6-turbo",     # GPT-6 Turbo 快速版
        "gpt-6-32k",       # GPT-6 32K 上下文版本（已由 context_2m 取代）
    }

    def __init__(self, config: Dict[str, Any] | None = None):
        """
        初始化 GPT-6 引擎

        Args:
            config: 配置字典，支持字段：
                - api_keys: List[str]       多 API Key 列表（支持 Key 轮换）
                - api_key: str              单 API Key（向后兼容，与 api_keys 二选一）
                - api_key_env: str           API Key 环境变量名（默认 OPENAI_API_KEY）
                - api_keys_env: str          多 API Key 环境变量名（逗号分隔，默认 OPENAI_API_KEYS）
                - model: str                模型名称（默认 gpt-6）
                - base_url: str             API 端点（默认 https://api.openai.com/v1）
                - max_tokens: int           最大输出 token（默认 4096，生产环境建议 8192）
                - temperature: float         温度参数（默认 0.3）
                - timeout: float            请求超时（秒，默认 120）
                - context_window: int       最大上下文 token（默认 2000000）
                - auth_initial_cooldown: float  Key 失败初始冷却秒数（默认 30）
                - auth_max_cooldown: float  Key 冷却最大秒数（默认 300）
        """
        super().__init__(config)
        self._api_key_env = self._config.get("api_key_env", "OPENAI_API_KEY")
        self._model = self._config.get("model", "gpt-6")
        self._base_url = self._config.get(
            "base_url", "https://api.openai.com/v1"
        )
        self._max_tokens = self._config.get("max_tokens", 4096)
        self._temperature = self._config.get("temperature", 0.3)
        self._timeout = self._config.get("timeout", 120.0)
        self._context_window = self._config.get("context_window", 2000000)

        # ── AuthProfile 初始化 ────────────────────────────────────────────────
        self._auth_profile: AuthProfile | None = None
        self._single_api_key: str | None = None  # 向后兼容单 Key

        initial_cooldown = self._config.get("auth_initial_cooldown", 30.0)
        max_cooldown = self._config.get("auth_max_cooldown", 300.0)

        # 优先使用 api_keys 列表
        explicit_keys: list[str] = self._config.get("api_keys") or []
        if not explicit_keys:
            # 尝试从环境变量读取多个 Key
            env_keys_str = self._config.get("api_keys_env") or "OPENAI_API_KEYS"
            import os as _os
            keys_from_env = _os.environ.get(env_keys_str, "")
            if keys_from_env:
                explicit_keys = [k.strip() for k in keys_from_env.split(",") if k.strip()]
            elif "OPENAI_API_KEYS" not in self._config:
                # 兼容单 Key 模式（向后兼容）
                single = self._config.get("api_key") or _os.environ.get(self._api_key_env)
                if single:
                    self._single_api_key = single
                    explicit_keys = [single]

        if len(explicit_keys) > 1:
            self._auth_profile = AuthProfile(
                keys=explicit_keys,
                initial_cooldown=initial_cooldown,
                max_cooldown=max_cooldown,
            )
            logger.info(
                f"[GPT6Engine] AuthProfile 模式 | keys={len(explicit_keys)} | "
                f"cooldown={initial_cooldown}s~{max_cooldown}s"
            )
        elif explicit_keys:
            self._single_api_key = explicit_keys[0]
            logger.info(
                f"[GPT6Engine] 单 Key 模式 | key_id=key_{self._single_api_key[:4]}***"
            )
        else:
            logger.warning(
                "[GPT6Engine] 未配置任何 API Key，将以模拟模式运行。"
            )

        if self._model not in self.SUPPORTED_MODELS:
            logger.warning(
                f"[GPT6Engine] 模型 {self._model} 未在验证列表中，"
                f"支持的模型: {self.SUPPORTED_MODELS}"
            )

        logger.info(
            f"[GPT6Engine] 初始化完成, model={self._model}, "
            f"context_window={self._context_window:,}, "
            f"auth_mode={'multi' if self._auth_profile else 'single/simulate'}"
        )

    # ── AuthProfile 集成接口 ──────────────────────────────────────────────────

    @property
    def auth_profile(self) -> AuthProfile | None:
        """返回当前 AuthProfile（无多 Key 时返回 None）"""
        return self._auth_profile

    def get_current_key_id(self) -> str | None:
        """获取当前生效的 Key ID（用于日志脱敏）"""
        if self._auth_profile and self._auth_profile._keys:
            return self._auth_profile._keys[0].key_id
        if self._single_api_key:
            return f"key_{self._single_api_key[:4]}***"
        return None

    def _report_api_success(self, key_id: str) -> None:
        """通知 AuthProfile 某 Key 调用成功"""
        if self._auth_profile:
            self._auth_profile.report_success(key_id)

    def _report_api_failure(self, key_id: str, retryable: bool = True) -> float | None:
        """通知 AuthProfile 某 Key 调用失败，返回退避时长"""
        if self._auth_profile:
            return self._auth_profile.report_failure(key_id, retryable)
        return None

    # ── Phase 2: 健康度上报 ───────────────────────────────────────────────

    def _report_health(
        self,
        success: bool,
        latency_ms: float,
        error: str | None = None,
        is_probe: bool = False,
    ) -> Dict[str, Any]:
        """
        报告模型健康度（GlobalCircuitBreaker + ModelHealthRegistry）

        在每次 execute() 调用结束时调用，确保健康度数据持续更新。

        Args:
            success:    请求是否成功
            latency_ms: 延迟（毫秒）
            error:      错误信息（失败时）
            is_probe:   是否为探测请求

        Returns:
            Dict: report_request_result 返回值
        """
        return report_request_result(
            model=self._model,
            success=success,
            error=error,
            is_probe=is_probe,
        )

    @property
    def engine_name(self) -> str:
        return "gpt-6"

    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            "session_persistence": True,
            "harness_control": True,
            "sandbox": True,
            "credential_management": True,
            "self_evolution": False,
            "vertical_knowledge": False,
            "streaming": True,
            "multi_modal": True,               # Symphony 五模态
            "context_2m": True,                 # 200万 Token 上下文
            "agent_completion_91": True,        # 91% 任务完成率
        }

    async def execute(self, task: str, context: Dict[str, Any]) -> ExecutionResult:
        """
        通过 GPT-6 执行任务（支持 AuthProfile 多 Key 轮换）

        当配置了多个 Key 时，执行流程:
            1. 从 AuthProfile 获取可用 Key（Round-Robin + 冷却过滤）
            2. 调用 API
            3a. 成功 → report_success 重置退避
            3b. 失败（可重试）→ report_failure 进入冷却，自动切换下一个 Key 重试
            3c. 失败（不可重试）→ 直接报告失败

        Args:
            task: 任务描述
            context: 执行上下文

        Returns:
            ExecutionResult: 标准执行结果
        """
        start = _time.perf_counter()

        # ── 健康检查快速通道 ─────────────────────────────────────────────────
        if context.get("_health_check"):
            return ExecutionResult(
                success=True,
                output={
                    "status": "healthy",
                    "engine": self.engine_name,
                    "model": self._model,
                    "context_window": self._context_window,
                    "auth_mode": "multi" if self._auth_profile else "single/simulate",
                    "key_count": len(self._auth_profile._keys) if self._auth_profile else 1,
                },
                metadata=self._build_metadata(context),
                latency_ms=(_time.perf_counter() - start) * 1000,
            )

        self._validate_context(context)

        key_id_hint = self.get_current_key_id()
        logger.info(
            f"[GPT6Engine] 执行任务: {task[:80]}... "
            f"(model={self._model}, user={context.get('user_id')}, key={key_id_hint})"
        )

        # ── 模拟模式（无任何 Key）──────────────────────────────────────────
        if not self._auth_profile and not self._single_api_key:
            return await self._simulate_and_finish(task, context, start)

        # ── AuthProfile 多 Key 模式：自动重试切换 ───────────────────────────
        if self._auth_profile:
            return await self._execute_with_auth_profile(task, context, start)

        # ── 单 Key 模式 ───────────────────────────────────────────────────
        return await self._execute_single_key(task, context, start)

    async def _execute_with_auth_profile(
        self, task: str, context: Dict[str, Any], start: float
    ) -> ExecutionResult:
        """使用 AuthProfile 多 Key 轮换执行（自动重试）"""
        max_retries = len(self._auth_profile._keys) if self._auth_profile else 1
        last_error: str | None = None
        last_key_id: str | None = None

        for attempt in range(max_retries):
            try:
                key_state = self._auth_profile.get_available_key()
                key_id = key_state.key_id
                last_key_id = key_id
                api_key = key_state.key

                output = await self._call_api(task, context, api_key, key_id)

                # 成功：重置退避状态
                self._report_api_success(key_id)

                latency_ms = (_time.perf_counter() - start) * 1000
                result = ExecutionResult(
                    success=True,
                    output=output,
                    metadata=self._build_metadata(context, {
                        "model": self._model,
                        "provider": "openai",
                        "temperature": self._temperature,
                        "context_window": self._context_window,
                        "capabilities": self.capabilities,
                        "key_id": key_id,
                        "auth_profile_active": True,
                        "attempt": attempt + 1,
                    }),
                    tokens_used=output.get("_estimated_tokens", 0),
                    latency_ms=latency_ms,
                )
                self._record_stats(result)
                # Phase 2: 上报健康度
                self._report_health(success=True, latency_ms=latency_ms)
                return result

            except NoAvailableKeyError as e:
                logger.error(
                    f"[GPT6Engine] 所有 Key 均不可用（冷却中），放弃重试: {e}"
                )
                last_error = str(e)
                break

            except Exception as e:
                last_error = str(e)
                err_str = str(e).lower()
                # 判断是否可重试
                retryable = any(kw in err_str for kw in [
                    "rate limit", "429", "500", "502", "503", "504",
                    "timeout", "connection", "temporary", "unavailable",
                ])

                if last_key_id:
                    self._report_api_failure(last_key_id, retryable=retryable)

                if not retryable or attempt >= max_retries - 1:
                    logger.error(
                        f"[GPT6Engine] API 调用不可重试失败: {e} | key={last_key_id}"
                    )
                    break

                logger.warning(
                    f"[GPT6Engine] Key {last_key_id} 调用失败 (attempt {attempt+1}/{max_retries})，"
                    f"切换到下一个 Key: {e}"
                )

        # 所有 Key 都失败
        latency_ms = (_time.perf_counter() - start) * 1000
        result = ExecutionResult(
            success=False,
            output=None,
            metadata=self._build_metadata(context, {
                "model": self._model,
                "auth_profile_active": True,
                "attempted_keys": max_retries,
            }),
            latency_ms=latency_ms,
            error=f"[GPT6Engine] 所有 Key 均失败: {last_error}",
        )
        self._record_stats(result)
        # Phase 2: 上报健康度（失败）
        self._report_health(success=False, latency_ms=latency_ms, error=last_error)
        return result

    async def _execute_single_key(
        self, task: str, context: Dict[str, Any], start: float
    ) -> ExecutionResult:
        """单 Key 执行（向后兼容）"""
        try:
            output = await self._call_api(
                task, context, self._single_api_key,
                self.get_current_key_id()
            )
            latency_ms = (_time.perf_counter() - start) * 1000
            result = ExecutionResult(
                success=True,
                output=output,
                metadata=self._build_metadata(context, {
                    "model": self._model,
                    "provider": "openai",
                    "temperature": self._temperature,
                    "context_window": self._context_window,
                    "capabilities": self.capabilities,
                    "auth_profile_active": False,
                }),
                tokens_used=output.get("_estimated_tokens", 0),
                latency_ms=latency_ms,
            )
            self._record_stats(result)
            # Phase 2: 上报健康度
            self._report_health(success=True, latency_ms=latency_ms)
            return result

        except Exception as e:
            latency_ms = (_time.perf_counter() - start) * 1000
            logger.exception(f"[GPT6Engine] 任务执行异常: {e}")
            result = ExecutionResult(
                success=False,
                output=None,
                metadata=self._build_metadata(context),
                latency_ms=latency_ms,
                error=str(e),
            )
            self._record_stats(result)
            # Phase 2: 上报健康度（失败）
            self._report_health(success=False, latency_ms=latency_ms, error=str(e))
            return result

    async def _simulate_and_finish(
        self, task: str, context: Dict[str, Any], start: float
    ) -> ExecutionResult:
        """模拟模式执行（无 API Key）"""
        output = await self._simulate_execute(task, context)
        latency_ms = (_time.perf_counter() - start) * 1000
        result = ExecutionResult(
            success=True,
            output=output,
            metadata=self._build_metadata(context, {
                "model": self._model,
                "provider": "openai",
                "simulated": True,
            }),
            tokens_used=output.get("_estimated_tokens", 0),
            latency_ms=latency_ms,
        )
        self._record_stats(result)
        return result

    async def stream(
        self, task: str, context: Dict[str, Any]
    ) -> AsyncIterator[StreamChunk]:
        """
        流式执行（支持 GPT-6 SSE + AuthProfile 多 Key）

        Args:
            task: 任务描述
            context: 执行上下文

        Yields:
            StreamChunk: 增量输出块
        """
        self._validate_context(context)

        # ── 模拟模式或单 Key ─────────────────────────────────────────────
        if not self._auth_profile:
            if self._single_api_key:
                async for chunk in self._stream_api(task, context, self._single_api_key):
                    yield chunk
            else:
                chunks = [
                    f"[GPT-6 {self._model}] 处理中",
                    "。正在分析任务...",
                    f"\n上下文窗口: {self._context_window:,} tokens\n",
                    f"提示: 请设置 OPENAI_API_KEY 环境变量以启用真实 GPT-6 调用。",
                ]
                for i, chunk_text in enumerate(chunks):
                    await asyncio.sleep(0.15)
                    yield StreamChunk(
                        content=chunk_text,
                        done=False,
                        delta_ms=150.0,
                    )
                yield StreamChunk(content="", done=True, delta_ms=0.0)
            return

        # ── AuthProfile 多 Key 模式 ────────────────────────────────────
        try:
            key_state = self._auth_profile.get_available_key()
            async for chunk in self._stream_api(task, context, key_state.key):
                yield chunk
            self._report_api_success(key_state.key_id)
        except NoAvailableKeyError:
            logger.error("[GPT6Engine.stream] 所有 Key 均在冷却，无法流式调用")
            yield StreamChunk(content="[Error] 所有 API Key 均处于冷却期", done=True, delta_ms=0.0)
        except Exception as e:
            logger.exception(f"[GPT6Engine.stream] 流式调用异常: {e}")
            yield StreamChunk(content=f"[Error] {e}", done=True, delta_ms=0.0)

    # -------------------------------------------------------------------------
    # 内部方法
    # -------------------------------------------------------------------------

    async def _call_api(
        self, task: str, context: Dict[str, Any],
        api_key: str, key_id: str | None = None,
    ) -> Dict[str, Any]:
        """
        调用 GPT-6 OpenAI API

        使用 httpx 白名单客户端（生产环境需在 SECURITY_WHITELIST 中添加域名）

        Args:
            task:      任务描述
            context:   执行上下文
            api_key:   当前使用的 API Key
            key_id:    Key 标识（用于日志）
        """
        import httpx
        import os

        # 优先使用白名单客户端（安全环境）
        allowed = os.environ.get("OPENAI_WHITELIST_ENABLED", "false").lower()
        if allowed == "true":
            try:
                from src.security.httpx_whitelist import create_whitelist_async_client
                client = create_whitelist_async_client()
            except (ImportError, ValueError):
                client = httpx.AsyncClient(timeout=self._timeout)
        else:
            client = httpx.AsyncClient(timeout=self._timeout)

        messages = [
            {"role": "system", "content": self._build_system_prompt(context)},
            {"role": "user", "content": task},
        ]

        body = {
            "model": self._model,
            "messages": messages,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "stream": False,
        }

        try:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                json=body,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "content": data["choices"][0]["message"]["content"],
                "model": self._model,
                "usage": data.get("usage", {}),
                "_estimated_tokens": data.get("usage", {}).get("total_tokens", 0),
                "capabilities": list(k for k, v in self.capabilities.items() if v),
            }
        finally:
            await client.aclose()

    async def _stream_api(
        self, task: str, context: Dict[str, Any],
        api_key: str,
    ) -> AsyncIterator[StreamChunk]:
        """SSE 流式调用 GPT-6 API"""
        import httpx
        import os

        allowed = os.environ.get("OPENAI_WHITELIST_ENABLED", "false").lower()
        if allowed == "true":
            try:
                from src.security.httpx_whitelist import create_whitelist_async_client
                client = create_whitelist_async_client()
            except (ImportError, ValueError):
                client = httpx.AsyncClient(timeout=self._timeout)
        else:
            client = httpx.AsyncClient(timeout=self._timeout)

        messages = [
            {"role": "system", "content": self._build_system_prompt(context)},
            {"role": "user", "content": task},
        ]

        body = {
            "model": self._model,
            "messages": messages,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "stream": True,
        }

        try:
            async with client.stream(
                "POST",
                f"{self._base_url}/chat/completions",
                json=body,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            ) as response:
                response.raise_for_status()
                accumulated = ""

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            yield StreamChunk(content="", done=True, delta_ms=0.0)
                            break

                        import json as _json
                        try:
                            chunk_data = _json.loads(data_str)
                            delta = chunk_data["choices"][0]["delta"].get("content", "")
                            if delta:
                                accumulated += delta
                                yield StreamChunk(
                                    content=delta,
                                    done=False,
                                    delta_ms=0.0,
                                )
                        except (_json.JSONDecodeError, KeyError, IndexError):
                            continue

                yield StreamChunk(content="", done=True, delta_ms=0.0)
        finally:
            await client.aclose()

    async def _simulate_execute(
        self, task: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """模拟执行（无 API Key 时）"""
        await asyncio.sleep(0.25)

        return {
            "status": "success",
            "content": (
                f"[GPT-6 {self._model}] 模拟响应\n\n"
                f"任务: {task[:80]}\n"
                f"用户: {context.get('user_id', 'N/A')}\n"
                f"角色: {context.get('user_role', 'N/A')}\n"
                f"上下文窗口: {self._context_window:,} tokens\n\n"
                f"已启用能力: {', '.join(k for k, v in self.capabilities.items() if v)}\n\n"
                f"提示: 请设置 {self._api_key_env} 环境变量以启用真实 GPT-6 调用。"
            ),
            "model": self._model,
            "_estimated_tokens": 220,
            "mode": "simulation",
        }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """构建系统提示词"""
        role = context.get("user_role", "viewer")
        role_descriptions = {
            "admin": "你是企业级智能助手，具有完整权限，可执行任意操作。",
            "operator": "你是业务操作助手，专注于执行具体任务，精准高效。",
            "viewer": "你是信息查询助手，仅提供只读信息和建议。",
        }
        base = role_descriptions.get(role, role_descriptions["viewer"])
        return (
            base + "\n"
            "你基于 GPT-6 提供服务，具备以下核心能力：\n"
            "- 200万 Token 超长上下文（可处理整本书籍/合同/代码库）\n"
            "- Symphony 五模态（文字/图像/音频/视频/代码）\n"
            "- 高可靠性智能体任务执行\n"
            "你专注于塑化行业企业级任务，"
            "包括库存查询、采购管理、物流调度、财务审核、技术文档分析等。\n"
            "请用简洁专业的语言回复，发挥 GPT-6 的推理和上下文优势。"
        )

    def _env_or_none(self, key: str) -> str | None:
        """从环境变量读取，返回 None 而非抛异常"""
        import os
        return os.environ.get(key)
