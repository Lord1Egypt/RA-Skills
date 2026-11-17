"""LLM router tests: budget, rate limits, retries, rotation, strict schema."""

import asyncio
import json

import httpx
import pytest
import respx

from agentsafe.config import LLMProviderConfig
from agentsafe.llm.router import (
    AuditBudget,
    BudgetExhaustedError,
    LLMRouter,
    ProviderUnavailableError,
)

PROV_A = LLMProviderConfig(
    name="prov-a", base_url="https://a.test/v1", api_key="sk-a", model="m1", rpm_limit=60
)
PROV_B = LLMProviderConfig(
    name="prov-b", base_url="https://b.test/v1", api_key="sk-b", model="m2", rpm_limit=60
)


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, d: float) -> None:
        self.t += d


def _ok_body(content: dict) -> dict:
    return {
        "choices": [{"message": {"content": json.dumps(content)}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20},
    }


class SleepRecorder:
    def __init__(self, clock: FakeClock) -> None:
        self.sleeps: list[float] = []
        self.clock = clock

    async def __call__(self, d: float) -> None:
        self.sleeps.append(d)
        self.clock.advance(d)


def _router(providers=None, *, clock, sleeper, rpm=60, retries=2, client=None):
    return LLMRouter(
        providers or [PROV_A, PROV_B],
        global_rpm=rpm,
        request_timeout_seconds=5.0,
        max_retries_per_call=retries,
        http_client=client or httpx.AsyncClient(),
        sleeper=sleeper,
        clock=clock,
    )


class _Schema:
    """Minimal pydantic-like model is not enough - router needs pydantic."""

    pass


from pydantic import BaseModel  # noqa: E402


class OkPayload(BaseModel):
    answer: str


class TestBudget:
    def test_budget_exhausted(self):
        clock = FakeClock()
        b = AuditBudget(max_calls=2, deadline=100.0, clock=clock)
        b.record_call()
        b.record_call()
        with pytest.raises(BudgetExhaustedError, match="budget exhausted"):
            b.check()

    def test_budget_deadline(self):
        clock = FakeClock()
        b = AuditBudget(max_calls=100, deadline=10.0, clock=clock)
        clock.advance(11.0)
        with pytest.raises(BudgetExhaustedError, match="deadline"):
            b.check()

    def test_usage_summary(self):
        clock = FakeClock()
        b = AuditBudget(max_calls=10, deadline=100.0, clock=clock)
        b.record_call()
        b.record_success(
            type(
                "R", (), {"provider": "p", "model": "m", "prompt_tokens": 5, "completion_tokens": 7}
            )()
        )
        s = b.usage_summary()
        assert s["total_calls"] == 1
        assert s["prompt_tokens"] == 5 and s["completion_tokens"] == 7
        assert s["providers_used"] == ["p"] and s["models_used"] == ["m"]


class TestRouterCalls:
    @respx.mock
    async def test_success_strict_json(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        respx.post("https://a.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=_ok_body({"answer": "42"}))
        )
        payload, call = await router.complete_json(
            budget, [{"role": "user", "content": "hi"}], OkPayload
        )
        assert payload.answer == "42"
        assert call.provider == "prov-a"
        assert call.prompt_tokens == 10

    @respx.mock
    async def test_fenced_json_accepted(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        body = {
            "choices": [{"message": {"content": '```json\n{"answer": "ok"}\n```'}}],
            "usage": {},
        }
        respx.post("https://a.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=body)
        )
        payload, _ = await router.complete_json(
            budget, [{"role": "user", "content": "hi"}], OkPayload
        )
        assert payload.answer == "ok"

    @respx.mock
    async def test_invalid_json_repaired_once_then_fails(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep, retries=1)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        route = respx.post("https://a.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=_ok_body({"wrong": "shape"}))
        )
        with pytest.raises(ProviderUnavailableError):
            await router.complete_json(budget, [{"role": "user", "content": "hi"}], OkPayload)
        assert route.call_count == 2  # initial + 1 repair attempt
        assert budget.failed_calls == 1

    @respx.mock
    async def test_429_rotates_to_next_provider(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        respx.post("https://a.test/v1/chat/completions").mock(
            return_value=httpx.Response(429, json={})
        )
        respx.post("https://b.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=_ok_body({"answer": "b"}))
        )
        payload, call = await router.complete_json(
            budget, [{"role": "user", "content": "hi"}], OkPayload
        )
        assert call.provider == "prov-b"
        assert payload.answer == "b"

    @respx.mock
    async def test_timeout_rotates(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        respx.post("https://a.test/v1/chat/completions").mock(side_effect=httpx.ReadTimeout("t/o"))
        respx.post("https://b.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=_ok_body({"answer": "b"}))
        )
        payload, _ = await router.complete_json(
            budget, [{"role": "user", "content": "hi"}], OkPayload
        )
        assert payload.answer == "b"

    @respx.mock
    async def test_all_providers_429_raises_no_infinite_retry(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep, retries=2)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        respx.post("https://a.test/v1/chat/completions").mock(
            return_value=httpx.Response(429, json={})
        )
        respx.post("https://b.test/v1/chat/completions").mock(
            return_value=httpx.Response(429, json={})
        )
        with pytest.raises(ProviderUnavailableError):
            await router.complete_json(budget, [{"role": "user", "content": "hi"}], OkPayload)
        assert budget.failed_calls == 1
        # 429 cooldowns recorded for both providers
        assert router._providers[0].cooldown_until > 0
        assert router._providers[1].cooldown_until > 0

    @respx.mock
    async def test_permanent_400_marks_provider_dead(self):
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep)
        budget = router.start_audit(max_calls=5, deadline_seconds=60)
        respx.post("https://a.test/v1/chat/completions").mock(
            return_value=httpx.Response(401, json={})
        )
        respx.post("https://b.test/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=_ok_body({"answer": "b"}))
        )
        await router.complete_json(budget, [{"role": "user", "content": "hi"}], OkPayload)
        assert router._providers[0].permanent_failure == "HTTP 401"


class TestRateLimiter:
    @respx.mock
    async def test_global_rpm_enforced_under_concurrency(self):
        """3 concurrent calls with global_rpm=2: the third must wait for a
        window slot (sleeper advances the fake clock), never exceed the cap."""
        clock = FakeClock()
        sleep = SleepRecorder(clock)
        router = _router(clock=clock, sleeper=sleep, rpm=2)
        budget = router.start_audit(max_calls=10, deadline_seconds=600)

        def ok(request):
            return httpx.Response(200, json=_ok_body({"answer": "x"}))

        respx.post("https://a.test/v1/chat/completions").mock(side_effect=ok)
        respx.post("https://b.test/v1/chat/completions").mock(side_effect=ok)

        async def one():
            return await router.complete_json(
                budget, [{"role": "user", "content": "hi"}], OkPayload
            )

        results = await asyncio.gather(one(), one(), one(), return_exceptions=True)
        assert all(not isinstance(r, Exception) for r in results), results
        # At least one limiter wait happened (sliding window opened)
        assert any(s > 0 for s in sleep.sleeps)

    async def test_limiter_deadline_fail_fast(self):
        from agentsafe.llm.router import _SlidingWindowLimiter

        clock = FakeClock()
        sleep = SleepRecorder(clock)
        limiter = _SlidingWindowLimiter(1, clock)
        await limiter.acquire(sleep, deadline=clock())
        # Window full; next acquire would need ~60s but deadline is now:
        with pytest.raises(BudgetExhaustedError):
            await limiter.acquire(sleep, deadline=clock())

    async def test_per_provider_rpm(self):
        from agentsafe.llm.router import _SlidingWindowLimiter

        clock = FakeClock()
        sleep = SleepRecorder(clock)
        limiter = _SlidingWindowLimiter(2, clock)
        await limiter.acquire(sleep, None)
        await limiter.acquire(sleep, None)
        # third needs to wait for the window
        task = asyncio.create_task(limiter.acquire(sleep, deadline=clock() + 120))
        await asyncio.sleep(0)
        clock.advance(61.0)
        await asyncio.wait_for(task, timeout=1.0)

    def test_no_providers_rejected(self):
        with pytest.raises(ValueError):
            LLMRouter([], global_rpm=10)
