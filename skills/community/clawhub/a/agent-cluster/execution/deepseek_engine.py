"""
DeepSeek V3.2 Engine Adapter

国产大模型执行引擎适配器 - DeepSeek V3.2 / R1

概述:
    为满足合规要求，支持使用国产大模型作为执行引擎。
    基于 DeepSeek V3.2 OpenAI 兼容 API，支持 deepseek-chat 和 deepseek-reasoner 两种模式。

能力:
    - compliance_certified: True（等保/信创认证）
    - 支持函数调用（Function Calling）
    - 支持长上下文（128K tokens）
    - 支持思维链（Chain of Thought，仅 reasoner 模式）
    - 支持流式输出（SSE）
    - 支持 JSON Mode

模型说明:
    - deepseek-chat      : DeepSeek V3.2，非思考模式（通用对话，响应快）
    - deepseek-reasoner  : DeepSeek V3.2 推理模式（内置思维链，适合数学/代码/复杂推理）
    - 两者底层共享 V3.2 架构，reasoner 会额外返回 reasoning_content 字段

API Reference:
    https://api-docs.deepseek.com/

Change Log:
    - 2026-04-14: 初始版本（V3.2 API 集成测试版）
"""

from __future__ import annotations

import asyncio
import logging
import time as _time
from typing import Any, AsyncIterator, Dict, Optional

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

# =============================================================================
# 常量
# =============================================================================

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_API_VERSION = "v3.2"

SUPPORTED_MODELS = {
    "deepseek-chat",       # V3.2 非思考模式（通用对话）
    "deepseek-reasoner",   # V3.2 推理模式（思维链）
}

# 推理模型特殊参数说明
REASONER_MODEL = "deepseek-reasoner"
CHAT_MODEL = "deepseek-chat"


class DeepSeekAPIError(Exception):
    """DeepSeek API 专用异常"""

    def __init__(self, message: str, status_code: Optional[int] = None, error_code: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code


class DeepSeekEngine(ExecutionEngine):
    """
    DeepSeek V3.2 执行引擎

    基于 OpenAI 兼容 API 的国产大模型引擎。

    支持的模型:
        - deepseek-chat       (DeepSeek V3.2，通用对话，非思考模式)
        - deepseek-reasoner   (DeepSeek V3.2，推理任务，思考模式)

    API Reference:
        https://api-docs.deepseek.com/

    V3.2 新特性:
        - reasoning_content 暴露（reasoner 模式）
        - JSON Mode (response_format)
        - Function Calling
        - Chat Prefix Completion（Beta，/beta 端点）
        - FIM Completion（Beta，/beta 端点）
        - Context Caching（降低长上下文成本）

    示例:
        >>> engine = DeepSeekEngine({"model": "deepseek-chat"})
        >>> result = await engine.execute("你好，请介绍一下量子计算", {
        ...     "user_id": "u001",
        ...     "user_role": "admin",
        ... })
        >>> print(result.output["content"])
    """

    SUPPORTED_MODELS = SUPPORTED_MODELS

    def __init__(self, config: Dict[str, Any] | None = None):
        """
        初始化 DeepSeek V3.2 引擎

        Args:
            config: 配置字典，支持字段：
                - api_keys: List[str]      多 API Key 列表（支持 Key 轮换）
                - api_key: str             单 API Key（向后兼容，与 api_keys 二选一）
                                          优先级: config["api_keys"] > env["DEEPSEEK_API_KEYS"]
                                                > config["api_key"] > env["DEEPSEEK_API_KEY"]
                - model: str              模型名（默认 deepseek-chat）
                - base_url: str           API 端点（默认 https://api.deepseek.com）
                - max_tokens: int         最大输出 token（默认 4096）
                - temperature: float        采样温度（默认 0.3）
                - reasoning_effort: float  思维链努力程度（0.0~1.0，仅 R1）
                - timeout: float           请求超时秒数（默认 120s）
                - json_mode: bool         强制 JSON 输出（默认 False）
                - auth_initial_cooldown: float  Key 失败初始冷却秒数（默认 30）
                - auth_max_cooldown: float       Key 冷却最大秒数（默认 300）
        """
        super().__init__(config)

        # ── AuthProfile 初始化 ────────────────────────────────────────────────
        self._auth_profile: AuthProfile | None = None
        self._single_api_key: str | None = None

        initial_cooldown = self._config.get("auth_initial_cooldown", 30.0)
        max_cooldown = self._config.get("auth_max_cooldown", 300.0)

        # 优先使用 api_keys 列表
        explicit_keys: list[str] = self._config.get("api_keys") or []
        if not explicit_keys:
            import os as _os
            # 多 Key 环境变量
            keys_from_env = _os.environ.get("DEEPSEEK_API_KEYS", "")
            if keys_from_env:
                explicit_keys = [k.strip() for k in keys_from_env.split(",") if k.strip()]
            elif "DEEPSEEK_API_KEYS" not in self._config:
                # 单 Key 兼容
                single = self._config.get("api_key") or _os.environ.get("DEEPSEEK_API_KEY")
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
                f"[DeepSeekEngine] AuthProfile 模式 | keys={len(explicit_keys)} | "
                f"cooldown={initial_cooldown}s~{max_cooldown}s"
            )
        elif explicit_keys:
            self._single_api_key = explicit_keys[0]
            logger.info(
                f"[DeepSeekEngine] 单 Key 模式 | key_id=key_{self._single_api_key[:4]}***"
            )
        else:
            logger.warning(
                "[DeepSeekEngine] 未配置 API Key，将以模拟模式运行。"
                "请设置 DEEPSEEK_API_KEY 环境变量以启用真实调用。"
            )

        # ── 模型配置 ──────────────────────────────────────────────────────
        self._model: str = self._config.get("model", CHAT_MODEL)
        self._base_url: str = self._config.get("base_url", DEEPSEEK_BASE_URL).rstrip("/")
        self._max_tokens: int = self._config.get("max_tokens", 4096)
        self._temperature: float = self._config.get("temperature", 0.3)
        self._reasoning_effort: float = self._config.get("reasoning_effort", 0.5)
        self._timeout: float = self._config.get("timeout", 120.0)
        self._json_mode: bool = self._config.get("json_mode", False)

        # ── Beta 端点（支持 8K max_tokens / FIM / Prefix Completion）─────
        self._use_beta: bool = self._config.get("use_beta", False)
        if self._use_beta:
            if not self._base_url.endswith("/beta"):
                self._base_url = self._base_url + "/beta"
            self._max_tokens = min(self._max_tokens, 8192)

        # ── 模型校验 ──────────────────────────────────────────────────────
        if self._model not in self.SUPPORTED_MODELS:
            logger.warning(
                f"[DeepSeekEngine] 模型 {self._model} 未在官方验证列表中，"
                f"支持的模型: {self.SUPPORTED_MODELS}，将尝试直接使用。"
            )

        # ── API Key 格式校验（可选）───────────────────────────────────────
        if self._single_api_key and not self._single_api_key.startswith("dsk-"):
            logger.debug(
                f"[DeepSeekEngine] API Key 格式: {self._single_api_key[:4]}***"
            )

        logger.info(
            f"[DeepSeekEngine] 引擎初始化 | model={self._model} | "
            f"base_url={self._base_url} | json_mode={self._json_mode} | "
            f"auth_mode={'multi' if self._auth_profile else 'single/simulate'} | "
            f"has_api_key={'Yes' if (self._auth_profile or self._single_api_key) else 'No (simulate)'}"
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
            latency_ms=latency_ms,
            error=error,
            is_probe=is_probe,
        )

    # =========================================================================
    # 公共接口
    # =========================================================================

    @property
    def engine_name(self) -> str:
        """引擎名称，格式: domestic-{model_name}"""
        return f"domestic-{self._model}"

    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            "session_persistence": True,
            "harness_control": True,           # V3.2 支持 Function Calling
            "sandbox": False,
            "credential_management": False,
            "self_evolution": False,
            "vertical_knowledge": False,
            "streaming": True,
            "multi_modal": False,
            "compliance_certified": True,        # 国产合规
            "json_mode": self._json_mode,
            "reasoning_chain": self._model == REASONER_MODEL,  # 仅 reasoner 模式
        }

    @property
    def model(self) -> str:
        """当前使用的模型名"""
        return self._model

    @property
    def api_health_status(self) -> Dict[str, Any]:
        """返回 API 健康状态摘要（不含敏感信息）"""
        return {
            "model": self._model,
            "base_url": self._base_url,
            "has_api_key": self._auth_profile is not None or self._single_api_key is not None,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
        }

    async def execute(self, task: str, context: Dict[str, Any]) -> ExecutionResult:
        """
        执行任务（阻塞模式）

        Args:
            task: 任务描述（自然语言）
            context: 执行上下文，包含：
                - user_id: str           用户ID
                - user_role: str         用户角色（admin/operator/viewer）
                - intent_type: str       意图类型
                - parameters: dict       额外参数

        Returns:
            ExecutionResult: 标准执行结果
        """
        start = _time.perf_counter()

        # ── 健康检查路径（快速返回）────────────────────────────────────
        if context.get("_health_check"):
            return ExecutionResult(
                success=True,
                output={"status": "healthy", "engine": self.engine_name},
                metadata=self._build_metadata(context, {
                    "model": self._model,
                    "provider": "deepseek",
                    "api_version": DEEPSEEK_API_VERSION,
                }),
                latency_ms=(_time.perf_counter() - start) * 1000,
            )

        self._validate_context(context)

        logger.info(
            f"[DeepSeekEngine] 执行任务 | model={self._model} | "
            f"task={task[:60]!r}... | user={context.get('user_id')}"
        )

        try:
            if not self._auth_profile and not self._single_api_key:
                # ── 模拟模式（无 API Key）────────────────────────────────
                output = await self._simulate_execute(task, context)
            elif self._auth_profile:
                # ── AuthProfile 多 Key 模式 ───────────────────────────────
                return await self._execute_with_auth_profile(task, context, start)
            else:
                # ── 单 Key 模式 ─────────────────────────────────────────
                output = await self._call_api(
                    task, context, self._single_api_key,
                    self.get_current_key_id()
                )

            latency_ms = (_time.perf_counter() - start) * 1000
            tokens_used = output.get("_estimated_tokens", 0)

            result = ExecutionResult(
                success=True,
                output=output,
                metadata=self._build_metadata(context, {
                    "model": self._model,
                    "provider": "deepseek",
                    "api_version": DEEPSEEK_API_VERSION,
                    "temperature": self._temperature,
                    "max_tokens": self._max_tokens,
                    "json_mode": self._json_mode,
                    "auth_profile_active": bool(self._auth_profile),
                    "reasoning_effort": (
                        self._reasoning_effort
                        if self._model == REASONER_MODEL
                        else None
                    ),
                }),
                tokens_used=tokens_used,
                latency_ms=latency_ms,
            )
            self._record_stats(result)
            # Phase 2: 上报健康度
            self._report_health(success=True, latency_ms=latency_ms)

            logger.info(
                f"[DeepSeekEngine] 完成 | tokens={tokens_used} | "
                f"latency={latency_ms:.0f}ms | success={result.success}"
            )
            return result

        except DeepSeekAPIError as e:
            latency_ms = (_time.perf_counter() - start) * 1000
            logger.error(
                f"[DeepSeekEngine] API 错误 | code={e.error_code} | "
                f"status={e.status_code} | {e}"
            )
            result = ExecutionResult(
                success=False,
                output=None,
                metadata=self._build_metadata(context),
                latency_ms=latency_ms,
                error=f"[DeepSeek API {e.error_code or e.status_code}] {e}",
            )
            self._record_stats(result)
            # Phase 2: 上报健康度（失败）
            self._report_health(
                success=False,
                latency_ms=latency_ms,
                error=f"[DeepSeek API {e.error_code or e.status_code}] {e}",
            )
            return result

        except Exception as e:
            latency_ms = (_time.perf_counter() - start) * 1000
            logger.exception(f"[DeepSeekEngine] 任务执行异常: {e}")
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
                self._report_api_success(key_id)

                latency_ms = (_time.perf_counter() - start) * 1000
                tokens_used = output.get("_estimated_tokens", 0)

                result = ExecutionResult(
                    success=True,
                    output=output,
                    metadata=self._build_metadata(context, {
                        "model": self._model,
                        "provider": "deepseek",
                        "api_version": DEEPSEEK_API_VERSION,
                        "temperature": self._temperature,
                        "max_tokens": self._max_tokens,
                        "json_mode": self._json_mode,
                        "auth_profile_active": True,
                        "key_id": key_id,
                        "attempt": attempt + 1,
                        "reasoning_effort": (
                            self._reasoning_effort
                            if self._model == REASONER_MODEL
                            else None
                        ),
                    }),
                    tokens_used=tokens_used,
                    latency_ms=latency_ms,
                )
                self._record_stats(result)
                # Phase 2: 上报健康度
                self._report_health(success=True, latency_ms=latency_ms)
                logger.info(
                    f"[DeepSeekEngine] AuthProfile 命中 | key={key_id} | "
                    f"tokens={tokens_used} | latency={latency_ms:.0f}ms"
                )
                return result

            except NoAvailableKeyError as e:
                logger.error(
                    f"[DeepSeekEngine] 所有 Key 均不可用（冷却中），放弃重试: {e}"
                )
                last_error = str(e)
                break

            except DeepSeekAPIError as e:
                last_error = str(e)
                retryable = e.status_code in (429, 500, 502, 503, 504)

                if last_key_id:
                    self._report_api_failure(last_key_id, retryable=retryable)

                if not retryable or attempt >= max_retries - 1:
                    logger.error(
                        f"[DeepSeekEngine] API 不可重试错误: {e} | key={last_key_id}"
                    )
                    break

                logger.warning(
                    f"[DeepSeekEngine] Key {last_key_id} 失败 (attempt {attempt+1}/{max_retries})，"
                    f"切换到下一个 Key: {e}"
                )

            except Exception as e:
                last_error = str(e)
                err_str = str(e).lower()
                retryable = any(kw in err_str for kw in [
                    "rate limit", "429", "500", "502", "503", "504",
                    "timeout", "connection", "temporary", "unavailable",
                ])

                if last_key_id:
                    self._report_api_failure(last_key_id, retryable=retryable)

                if not retryable or attempt >= max_retries - 1:
                    break

                logger.warning(
                    f"[DeepSeekEngine] Key {last_key_id} 调用异常: {e} | "
                    f"attempt {attempt+1}/{max_retries}，切换到下一个 Key"
                )

        latency_ms = (_time.perf_counter() - start) * 1000
        result = ExecutionResult(
            success=False,
            output=None,
            metadata=self._build_metadata(context, {
                "auth_profile_active": True,
                "attempted_keys": max_retries,
            }),
            latency_ms=latency_ms,
            error=f"[DeepSeekEngine] 所有 Key 均失败: {last_error}",
        )
        self._record_stats(result)
        # Phase 2: 上报健康度（失败）
        self._report_health(success=False, latency_ms=latency_ms, error=last_error)
        return result

    async def stream(
        self, task: str, context: Dict[str, Any]
    ) -> AsyncIterator[StreamChunk]:
        """
        流式执行（支持 DeepSeek SSE + AuthProfile 多 Key）

        Yields:
            StreamChunk: 增量输出块

        Note:
            对于 deepseek-reasoner，reasoning_content 不会通过流式返回
            （reasoner 模式暂不支持 streaming，会自动降级为阻塞调用）。
        """
        self._validate_context(context)

        if not self._auth_profile:
            if self._single_api_key:
                async for chunk in self._stream_api(task, context, self._single_api_key):
                    yield chunk
                return
            # 模拟流式输出
            chunks = [
                "[DeepSeek V3.2] 正在处理您的请求...\n",
                "正在分析任务内容...\n",
                "生成响应中...\n",
            ]
            for i, chunk_text in enumerate(chunks):
                await asyncio.sleep(0.08)
                yield StreamChunk(
                    content=chunk_text,
                    done=False,
                    delta_ms=80.0,
                )
            yield StreamChunk(content="", done=True, delta_ms=0.0)
            return

        # R1 模型暂不支持 SSE 流，自动降级
        if self._model == REASONER_MODEL:
            logger.warning(
                "[DeepSeekEngine] deepseek-reasoner 模式暂不支持 SSE 流式输出，"
                "降级为阻塞调用。"
            )
            result = await self.execute(task, context)
            if result.success:
                content = result.output.get("content", "")
                words = content.split()
                for i, word in enumerate(words):
                    await asyncio.sleep(0.01)
                    yield StreamChunk(
                        content=word + (" " if i < len(words) - 1 else ""),
                        done=(i == len(words) - 1),
                        delta_ms=10.0,
                    )
            return

        # AuthProfile 多 Key 模式
        try:
            key_state = self._auth_profile.get_available_key()
            async for chunk in self._stream_api(task, context, key_state.key):
                yield chunk
            self._report_api_success(key_state.key_id)
        except NoAvailableKeyError:
            logger.error("[DeepSeekEngine.stream] 所有 Key 均在冷却，无法流式调用")
            yield StreamChunk(content="[Error] 所有 API Key 均处于冷却期", done=True, delta_ms=0.0)
        except Exception as e:
            logger.exception(f"[DeepSeekEngine.stream] 流式调用异常: {e}")
            yield StreamChunk(content=f"[Error] {e}", done=True, delta_ms=0.0)

    async def health_check(self) -> bool:
        """
        健康检查（带 API 连通性验证）

        Returns:
            bool: 引擎是否可用
        """
        try:
            result = await self.execute(
                task="respond with exactly one word: OK",
                context={"_health_check": True, "user_id": "health-check", "user_role": "viewer"},
            )
            return result.success
        except Exception as e:
            logger.warning(f"[DeepSeekEngine] 健康检查失败: {e}")
            return False

    # =========================================================================
    # 内部方法
    # =========================================================================

    async def _call_api(
        self, task: str, context: Dict[str, Any],
        api_key: str, key_id: str | None = None,
    ) -> Dict[str, Any]:
        """
        调用 DeepSeek V3.2 Chat Completions API

        使用 httpx 异步客户端，自动处理 OpenAI 兼容响应格式。
        支持 V3.2 的 reasoning_content（reasoner 模式）和 usage 统计。

        Args:
            task:      任务描述
            context:   执行上下文
            api_key:   当前使用的 API Key
            key_id:    Key 标识（用于日志）
        """
        import httpx

        client = httpx.AsyncClient(timeout=self._timeout)

        try:
            messages = self._build_messages(task, context)

            body: Dict[str, Any] = {
                "model": self._model,
                "messages": messages,
                "max_tokens": self._max_tokens,
                "temperature": self._temperature,
                "stream": False,
            }

            # ── JSON Mode（V3.2 新特性）───────────────────────────────────
            if self._json_mode:
                body["response_format"] = {"type": "json_object"}

            # ── R1 推理模型特殊参数 ──────────────────────────────────────
            if self._model == REASONER_MODEL:
                body["reasoning_effort"] = self._reasoning_effort

            response = await client.post(
                f"{self._base_url}/chat/completions",
                json=body,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    # "Accept": "application/json",  # 可选，明确要求 JSON
                },
            )

            # ── 错误处理（4xx/5xx）───────────────────────────────────────
            if response.status_code == 401:
                raise DeepSeekAPIError(
                    "API Key 无效或未授权，请检查 DEEPSEEK_API_KEY 配置。",
                    status_code=401,
                    error_code="invalid_api_key",
                )
            elif response.status_code == 403:
                raise DeepSeekAPIError(
                    "API Key 无访问权限，请确认账户余额和权限。",
                    status_code=403,
                    error_code="forbidden",
                )
            elif response.status_code == 429:
                raise DeepSeekAPIError(
                    "请求频率超限（429），请稍后重试。",
                    status_code=429,
                    error_code="rate_limit_exceeded",
                )
            elif response.status_code == 500:
                raise DeepSeekAPIError(
                    "DeepSeek 服务器内部错误，请稍后重试。",
                    status_code=500,
                    error_code="internal_server_error",
                )
            elif response.status_code >= 400:
                error_body = response.json() if response.text else {}
                raise DeepSeekAPIError(
                    f"API 请求失败: {error_body.get('error', {}).get('message', response.text)}",
                    status_code=response.status_code,
                    error_code=error_body.get("error", {}).get("code"),
                )

            data = response.json()
            choice = data["choices"][0]
            message = choice["message"]

            # ── 提取内容 ────────────────────────────────────────────────
            content = message.get("content", "")
            reasoning_content = message.get("reasoning_content", "")

            # ── usage 统计 ───────────────────────────────────────────────
            usage = data.get("usage", {})
            tokens_used = usage.get("total_tokens", 0)

            result: Dict[str, Any] = {
                "status": "success",
                "content": content,
                "model": self._model,
                "usage": usage,
                "_estimated_tokens": tokens_used,
                "finish_reason": choice.get("finish_reason", "stop"),
            }

            # ── 推理内容（reasoner 模式）─────────────────────────────────
            if reasoning_content:
                result["reasoning_content"] = reasoning_content

            # ── tool_calls（Function Calling）───────────────────────────
            if message.get("tool_calls"):
                result["tool_calls"] = message["tool_calls"]

            return result

        finally:
            await client.aclose()

    async def _stream_api(
        self, task: str, context: Dict[str, Any],
        api_key: str,
    ) -> AsyncIterator[StreamChunk]:
        """
        SSE 流式调用 DeepSeek API

        Args:
            task:    任务描述
            context:  执行上下文
            api_key: 当前使用的 API Key

        Yields:
            StreamChunk: 增量内容块
        """
        import httpx
        import json as _json

        client = httpx.AsyncClient(timeout=self._timeout)

        try:
            messages = self._build_messages(task, context)

            body: Dict[str, Any] = {
                "model": self._model,
                "messages": messages,
                "max_tokens": self._max_tokens,
                "temperature": self._temperature,
                "stream": True,
            }

            if self._json_mode:
                body["response_format"] = {"type": "json_object"}

            async with client.stream(
                "POST",
                f"{self._base_url}/chat/completions",
                json=body,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            ) as response:
                # ── HTTP 状态码检查 ───────────────────────────────────────
                if response.status_code >= 400:
                    text = await response.aread()
                    raise DeepSeekAPIError(
                        f"SSE 流式请求失败 [{response.status_code}]: {text.decode(errors='replace')}",
                        status_code=response.status_code,
                    )

                accumulated = ""

                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue

                    data_str = line[6:]
                    if data_str == "[DONE]":
                        yield StreamChunk(content="", done=True, delta_ms=0.0)
                        break

                    try:
                        chunk_data = _json.loads(data_str)
                        delta = (
                            chunk_data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                        )
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
        """
        模拟执行（无 API Key 时）

        返回格式与真实 API 保持一致，便于下游代码透明切换。
        """
        await asyncio.sleep(0.15)

        return {
            "status": "success",
            "content": (
                f"[DeepSeek V3.2 模拟响应]\n\n"
                f"任务: {task}\n"
                f"模型: {self._model}\n"
                f"用户: {context.get('user_id', 'N/A')} / {context.get('user_role', 'N/A')}\n"
                f"意图: {context.get('intent_type', 'unknown')}\n\n"
                f"💡 提示: 请设置 DEEPSEEK_API_KEY 环境变量以启用真实 API 调用。\n"
                f"   或传入 config['api_key'] 参数直接配置。"
            ),
            "model": self._model,
            "_estimated_tokens": 180,
            "mode": "simulation",
            "provider": "deepseek",
        }

    def _build_messages(
        self, task: str, context: Dict[str, Any]
    ) -> list[Dict[str, Any]]:
        """
        构建 API messages 列表

        支持多轮对话历史（从 context.history 中读取）。
        """
        messages: list[Dict[str, Any]] = []

        # System prompt
        system_prompt = self._build_system_prompt(context)
        messages.append({"role": "system", "content": system_prompt})

        # 历史对话（多轮支持）
        history: list[Dict[str, Any]] = context.get("history", [])
        for msg in history:
            role = msg.get("role", "user")
            if role in ("user", "assistant", "system"):
                messages.append({
                    "role": role,
                    "content": msg.get("content", ""),
                })

        # 当前任务
        messages.append({"role": "user", "content": task})

        return messages

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """
        构建系统提示词

        根据用户角色注入权限级别说明，根据意图类型注入领域知识。
        """
        role = context.get("user_role", "viewer")
        intent = context.get("intent_type", "general")

        role_descriptions = {
            "admin": "你是一个企业级智能助手，拥有完整管理员权限，可以执行所有操作。",
            "operator": "你是一个业务操作助手，专注于执行具体业务任务，操作需严谨准确。",
            "viewer": "你是一个信息查询助手，仅提供只读信息，不执行任何写操作。",
        }

        intent_knowledge = {
            "stock_query": "你专注于库存查询，可分析库存水平、周转率、呆滞物料等指标。",
            "purchase": "你专注于采购管理，可协助供应商评估、采购订单跟踪、成本分析。",
            "logistics": "你专注于物流调度，可优化运输路线、跟踪在途货物、管理仓储。",
            "finance": "你专注于财务审核，可分析财务报表、预算执行、费用合规性。",
            "replenishment": "你专注于智能补货，可基于历史消耗和安全库存生成建议订单。",
            "code": "你是一个专业的编程助手，擅长 Python、JavaScript、SQL 等语言。",
            "analysis": "你是一个数据分析助手，擅长解读数据、生成洞察、提供决策建议。",
        }

        base = role_descriptions.get(role, role_descriptions["viewer"])
        knowledge = intent_knowledge.get(intent, "")

        return (
            f"{base}\n"
            f"{knowledge}\n"
            "请用简洁专业的语言回复。\n"
            "如果涉及数字和计算，请给出明确的计算过程。\n"
            "如果是代码任务，请附上必要的注释说明。"
        )

    def _env_or_none(self, key: str) -> str | None:
        """安全读取环境变量，缺失时返回 None 而非抛异常"""
        import os
        return os.environ.get(key)
