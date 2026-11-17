"""LLM router: OpenAI-compatible providers with rotation, RPM limits, budgets.

Honest limits (documented, not hidden):
- The GLOBAL RPM limit is enforced inside THIS PROCESS ONLY. Multi-replica
  deployments need a shared limiter or a single-replica deployment; the MCP
  service here assumes a single process.
- Free-provider RPMs are NOT summed into a capacity promise; actual model IDs,
  quotas and limits are whatever the deployed accounts actually allow.
- API keys never appear in logs or exceptions.

Response validation is STRICT: JSON parsed and validated against a pydantic
model; parse failures get at most `max_retries` repair attempts, never a
lenient regex fallback.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections import deque
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass, field
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

logger = logging.getLogger("agentSAFE.llm")

COOLDOWN_RATE_LIMIT_SECONDS = 60.0
COOLDOWN_SERVER_ERROR_SECONDS = 15.0


class LLMRouterError(RuntimeError):
    pass


class BudgetExhaustedError(LLMRouterError):
    """Per-audit call budget or deadline exceeded - stop calling, don't retry."""


class ProviderUnavailableError(LLMRouterError):
    """No healthy provider within the audit deadline."""


class SchemaValidationError(LLMRouterError):
    """LLM output failed strict JSON/schema validation after limited retries."""


@dataclass
class LLMCallResult:
    content: str
    provider: str
    model: str
    duration_seconds: float
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


@dataclass
class _ProviderRuntime:
    name: str
    base_url: str
    api_key: str
    model: str
    rpm_limit: int
    max_output_tokens: int | None
    cooldown_until: float = 0.0
    permanent_failure: str | None = None
    window: deque = field(default_factory=deque)
    calls: int = 0
    failures: int = 0


class _SlidingWindowLimiter:
    """Process-local sliding-window RPM limiter, correct under concurrency."""

    def __init__(self, rpm: int, clock: Callable[[], float]) -> None:
        self._window_seconds = 60.0
        self._rpm = max(1, rpm)
        self._clock = clock
        self._events: deque = deque()
        self._lock = asyncio.Lock()

    async def acquire(
        self, sleeper: Callable[[float], Awaitable[None]], deadline: float | None
    ) -> None:
        while True:
            async with self._lock:
                now = self._clock()
                while self._events and now - self._events[0] >= self._window_seconds:
                    self._events.popleft()
                if len(self._events) < self._rpm:
                    self._events.append(now)
                    return
                wait = self._window_seconds - (now - self._events[0]) + 0.01
                if deadline is not None and now + wait > deadline:
                    raise BudgetExhaustedError(
                        f"rate limit wait {wait:.1f}s would exceed audit deadline"
                    )
            await sleeper(wait)


@dataclass
class AuditBudget:
    """Per-audit hard budget: max calls + total deadline + token accounting."""

    max_calls: int
    deadline: float
    clock: Callable[[], float]
    calls_made: int = 0
    failed_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    providers_used: set = field(default_factory=set)
    models_used: set = field(default_factory=set)

    def check(self) -> None:
        if self.calls_made >= self.max_calls:
            raise BudgetExhaustedError(
                f"LLM budget exhausted: {self.calls_made}/{self.max_calls} calls used"
            )
        if self.clock() > self.deadline:
            raise BudgetExhaustedError("LLM audit deadline exceeded")

    def record_call(self) -> None:
        self.calls_made += 1

    def record_success(self, result: LLMCallResult) -> None:
        self.providers_used.add(result.provider)
        self.models_used.add(result.model)
        if result.prompt_tokens is not None:
            self.prompt_tokens += result.prompt_tokens
        if result.completion_tokens is not None:
            self.completion_tokens += result.completion_tokens

    def record_failure(self) -> None:
        self.failed_calls += 1

    def usage_summary(self) -> dict[str, Any]:
        return {
            "total_calls": self.calls_made,
            "failed_calls": self.failed_calls,
            "prompt_tokens": self.prompt_tokens or None,
            "completion_tokens": self.completion_tokens or None,
            "providers_used": sorted(self.providers_used),
            "models_used": sorted(self.models_used),
        }


class LLMRouter:
    """Routes bounded LLM calls across configured providers.

    Per-call flow: budget check -> provider selection (healthy first) ->
    per-provider RPM + global RPM acquire -> HTTP with timeout -> strict
    schema validation with limited repair retries -> accounting.
    """

    def __init__(
        self,
        providers: Sequence[Any],
        *,
        global_rpm: int = 10,
        request_timeout_seconds: float = 90.0,
        max_retries_per_call: int = 2,
        default_max_output_tokens: int = 3000,
        max_concurrent_calls: int = 4,
        http_client: httpx.AsyncClient | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
        clock: Callable[[], float] | None = None,
    ) -> None:
        if not providers:
            raise ValueError("LLMRouter requires at least one provider")
        self._providers = [
            _ProviderRuntime(
                name=p.name,
                base_url=p.base_url,
                api_key=p.api_key,
                model=p.model,
                rpm_limit=p.rpm_limit,
                max_output_tokens=p.max_output_tokens,
            )
            for p in providers
        ]
        self._request_timeout = request_timeout_seconds
        self._max_retries = max_retries_per_call
        self._default_tokens = default_max_output_tokens
        self._sleeper = sleeper or asyncio.sleep
        self._clock = clock or time.monotonic
        self._global_limiter = _SlidingWindowLimiter(global_rpm, self._clock)
        self._provider_limiters = {
            p.name: _SlidingWindowLimiter(p.rpm_limit, self._clock) for p in self._providers
        }
        self._client = http_client or httpx.AsyncClient(
            timeout=httpx.Timeout(request_timeout_seconds, connect=request_timeout_seconds),
        )
        self._semaphore = asyncio.Semaphore(max(1, max_concurrent_calls))

    async def aclose(self) -> None:
        await self._client.aclose()

    def start_audit(self, *, max_calls: int, deadline_seconds: float) -> AuditBudget:
        return AuditBudget(
            max_calls=max_calls,
            deadline=self._clock() + deadline_seconds,
            clock=self._clock,
        )

    def _healthy(self) -> list[_ProviderRuntime]:
        now = self._clock()
        return [
            p for p in self._providers if p.permanent_failure is None and now >= p.cooldown_until
        ]

    def _cooldown(self, p: _ProviderRuntime, seconds: float, reason: str) -> None:
        p.cooldown_until = max(p.cooldown_until, self._clock() + seconds)
        p.failures += 1
        logger.warning("llm provider=%s cooling down %.0fs (%s)", p.name, seconds, reason)

    async def complete_json(
        self,
        budget: AuditBudget,
        messages: Sequence[dict[str, str]],
        schema_model: type[BaseModelT],
        *,
        max_output_tokens: int | None = None,
    ) -> tuple[BaseModelT, LLMCallResult]:
        """One logical call (against the audit budget) with strict validation.

        Provider-level failures rotate to the next provider; the whole logical
        call gets at most `1 + max_retries_per_call` HTTP attempts total.
        """
        budget.check()
        budget.record_call()

        attempts = 0
        max_attempts = 1 + self._max_retries
        last_error: Exception | str | None = None
        current_messages = list(messages)
        repair_provider: _ProviderRuntime | None = None

        while attempts < max_attempts:
            providers = self._healthy()
            if not providers:
                waiters = [p for p in self._providers if p.permanent_failure is None]
                if not waiters:
                    raise ProviderUnavailableError("all LLM providers are permanently failed")
                soonest = min(p.cooldown_until for p in waiters)
                wait = soonest - self._clock()
                if wait > 0 and self._clock() + wait <= budget.deadline:
                    logger.info("all providers cooling down; waiting %.1fs", wait)
                    await self._sleeper(wait)
                    continue
                raise ProviderUnavailableError(
                    f"no healthy provider within audit deadline (cooldown {wait:.0f}s)"
                )

            if repair_provider is not None:
                # schema-repair retry stays on the same provider: the failure
                # was output formatting, not provider health.
                p = repair_provider
                repair_provider = None
            else:
                p = providers[attempts % len(providers)]
            tokens = max_output_tokens or p.max_output_tokens or self._default_tokens
            payload = {
                "model": p.model,
                "messages": current_messages,
                "max_tokens": tokens,
                "temperature": 0,
            }
            await self._provider_limiters[p.name].acquire(self._sleeper, budget.deadline)
            await self._global_limiter.acquire(self._sleeper, budget.deadline)

            started = self._clock()
            try:
                async with self._semaphore:
                    resp = await self._client.post(
                        f"{p.base_url}/chat/completions",
                        json=payload,
                        headers={"Authorization": f"Bearer {p.api_key}"},
                    )
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                self._cooldown(p, COOLDOWN_SERVER_ERROR_SECONDS, f"transport: {exc}")
                last_error = exc
                attempts += 1
                continue

            duration = self._clock() - started
            if resp.status_code == 429:
                self._cooldown(p, COOLDOWN_RATE_LIMIT_SECONDS, "HTTP 429")
                last_error = LLMRouterError(f"{p.name}: 429")
                attempts += 1
                continue
            if resp.status_code >= 500:
                self._cooldown(p, COOLDOWN_SERVER_ERROR_SECONDS, f"HTTP {resp.status_code}")
                last_error = LLMRouterError(f"{p.name}: HTTP {resp.status_code}")
                attempts += 1
                continue
            if resp.status_code >= 400:
                # 400/401/403/404: permanent for this provider (bad key/model/payload)
                p.permanent_failure = f"HTTP {resp.status_code}"
                logger.error(
                    "llm provider=%s permanently failed: HTTP %d (body not logged)",
                    p.name,
                    resp.status_code,
                )
                last_error = LLMRouterError(f"{p.name}: HTTP {resp.status_code}")
                attempts += 1
                continue

            try:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage") or {}
            except (ValueError, KeyError, TypeError, IndexError):
                self._cooldown(p, COOLDOWN_SERVER_ERROR_SECONDS, "malformed response body")
                last_error = LLMRouterError(f"{p.name}: malformed response")
                attempts += 1
                continue

            result = LLMCallResult(
                content=content,
                provider=p.name,
                model=p.model,
                duration_seconds=duration,
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
            )
            p.calls += 1
            logger.info(
                "llm ok provider=%s model=%s duration=%.2fs prompt_tokens=%s completion_tokens=%s",
                p.name,
                p.model,
                duration,
                result.prompt_tokens,
                result.completion_tokens,
            )

            validated, schema_error = _validate_json_strict(content, schema_model)
            if validated is not None:
                budget.record_success(result)
                return validated, result
            # Strict validation failed: one repair attempt reusing the same provider
            # slot budget; if retries exhausted the call fails loudly.
            last_error = schema_error
            logger.warning(
                "llm provider=%s schema validation failed (%s); attempts=%d",
                p.name,
                schema_error,
                attempts + 1,
            )
            if attempts + 1 >= max_attempts:
                break
            current_messages = [
                *messages,
                {"role": "assistant", "content": content},
                {
                    "role": "user",
                    "content": (
                        "Your previous reply was NOT valid JSON for the required schema "
                        f"({schema_error}). Respond again with ONLY a valid JSON object "
                        "matching the schema. No markdown, no commentary."
                    ),
                },
            ]
            repair_provider = p
            attempts += 1

        budget.record_failure()
        if isinstance(last_error, SchemaValidationError):
            raise last_error
        raise ProviderUnavailableError(
            f"LLM call failed after {max_attempts} attempts: {last_error}"
        )


BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def _validate_json_strict(
    content: str, schema_model: type[BaseModelT]
) -> tuple[BaseModelT | None, str | None]:
    """Strict JSON validation. Fenced ```json blocks are unwrapped (standard LLM
    formatting); anything else must parse cleanly. No regex content guessing."""
    text = (content or "").strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc.msg}"
    try:
        return schema_model.model_validate(parsed), None
    except Exception as exc:
        return None, f"schema violation: {str(exc)[:300]}"
