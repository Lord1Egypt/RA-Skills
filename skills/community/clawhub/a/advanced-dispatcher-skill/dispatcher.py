"""Deterministic routing engine for the Advanced Dispatcher skill.

Design goals:
- avoid Anthropic by default
- keep routing tables small and maintainable
- attach explicit cache-retention metadata to every run
- make tradeoff and build-pipeline routing testable and predictable
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


MODEL_ID_PATTERN = re.compile(r"^[a-z0-9-]+/[a-z0-9.-]+$")
CACHE_RETENTION_VALUES = {"long", "short"}
_FORCE_CLAUDE_FLAG = "--force-claude"
_LEGACY_FLAGS = ("--use-claude", "--force-opus", "--no-opus")


class RoutingError(ValueError):
    """Raised when a route cannot be constructed safely."""


class ModelCatalog:
    CODE_ARCH = "openai-codex/gpt-5.4"
    TRADEOFF_OPENAI = "openai-codex/gpt-5.3-codex"
    CODE_REVIEW = "openai-codex/gpt-5.3-codex"
    QUICK = "openai-codex/gpt-5.3-codex-spark"

    MATH = "opencode-go/glm-5"
    WEB = "opencode-go/minimax-m2.5"
    RESEARCH = "opencode-go/kimi-k2.5"

    SONNET = "anthropic/claude-sonnet-4-6"
    OPUS = "anthropic/claude-opus-4-6"


_STANDARD_DOMAIN_MODELS = {
    "code-architecture": ModelCatalog.CODE_ARCH,
    "math-algorithms": ModelCatalog.MATH,
    "web-brainstorming": ModelCatalog.WEB,
    "research-long-context": ModelCatalog.RESEARCH,
    "quick-scripts-formatting": ModelCatalog.QUICK,
}

_BUILDX_PATTERN = re.compile(r"^\s*buildx:\s*", re.IGNORECASE)
_BUILD_PATTERN = re.compile(r"^\s*build:\s*", re.IGNORECASE)
_BUILDQ_PATTERN = re.compile(r"^\s*buildq:\s*", re.IGNORECASE)

_TRADEOFF_PATTERNS = (
    re.compile(r"\bevaluate\s+tradeoffs?\b", re.IGNORECASE),
    re.compile(
        r"\bcompare\s+(?:approaches?|options?|designs?|architectures?)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bchoose\s+(?:between|among)\b", re.IGNORECASE),
    re.compile(
        r"\bwhich\s+(?:approach|option|design|architecture)\s+(?:is\s+)?better\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bjudge\s+(?:these|the)\s+(?:designs?|architectures?)\b",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True)
class ModelRun:
    model: str
    cache_retention: str
    role: str


@dataclass(frozen=True)
class PipelineStep:
    name: str
    run: ModelRun
    purpose: str


@dataclass(frozen=True)
class RoutePlan:
    mode: str
    primary: ModelRun | None = None
    parallel: tuple[ModelRun, ...] = ()
    judge: ModelRun | None = None
    pipeline: tuple[PipelineStep, ...] = ()
    reason: str = ""
    used_force_claude: bool = False


class DispatcherRouter:
    """Plan deterministic routes for spawned work."""

    def route(self, prompt: str, *, domain: str) -> RoutePlan:
        if not prompt or not prompt.strip():
            raise RoutingError("prompt must not be empty")

        domain_key = domain.strip().lower()
        if domain_key not in _STANDARD_DOMAIN_MODELS:
            raise RoutingError(
                "domain must be one of: code-architecture, math-algorithms, "
                "web-brainstorming, research-long-context, quick-scripts-formatting"
            )

        self._reject_legacy_flags(prompt)

        if self._is_buildx_request(prompt):
            return self._build_pipeline("buildx")
        if self._is_build_request(prompt):
            return self._build_pipeline("build")
        if self._is_buildq_request(prompt):
            return self._build_pipeline("buildq")
        if self._is_tradeoff_request(prompt):
            return self._tradeoff_route(prompt)
        return self._standard_route(domain_key, prompt)

    def _standard_route(self, domain_key: str, prompt: str) -> RoutePlan:
        model = _STANDARD_DOMAIN_MODELS[domain_key]
        if _FORCE_CLAUDE_FLAG in prompt:
            return RoutePlan(
                mode="standard",
                primary=self._run(model, role="primary"),
                reason=(
                    "standard routing; --force-claude applies only to tradeoff proposal generation"
                ),
                used_force_claude=True,
            )

        return RoutePlan(
            mode="standard",
            primary=self._run(model, role="primary"),
            reason=f"standard route for {domain_key}",
        )

    def _tradeoff_route(self, prompt: str) -> RoutePlan:
        if _FORCE_CLAUDE_FLAG in prompt:
            parallel = (
                self._run(ModelCatalog.SONNET, role="proposal"),
                self._run(ModelCatalog.OPUS, role="proposal"),
            )
            return RoutePlan(
                mode="tradeoff-force-claude",
                parallel=parallel,
                judge=self._run(ModelCatalog.CODE_ARCH, role="judge"),
                reason="tradeoff route with Claude forced only for proposal generation",
                used_force_claude=True,
            )

        parallel = (
            self._run(ModelCatalog.MATH, role="proposal"),
            self._run(ModelCatalog.TRADEOFF_OPENAI, role="proposal"),
        )
        return RoutePlan(
            mode="tradeoff",
            parallel=parallel,
            judge=self._run(ModelCatalog.CODE_ARCH, role="judge"),
            reason="default tradeoff route with GLM-5 and GPT-5.3-Codex proposals judged by GPT-5.4",
        )

    def _build_pipeline(self, level: str) -> RoutePlan:
        factories = {
            "buildq": self._buildq_steps,
            "build": self._build_steps,
            "buildx": self._buildx_steps,
        }
        steps = factories[level]()
        return RoutePlan(
            mode=level,
            pipeline=steps,
            reason=f"{level} delivery pipeline",
        )

    def _buildq_steps(self) -> tuple[PipelineStep, ...]:
        return (
            self._step("plan", ModelCatalog.CODE_ARCH, "choose implementation path and file plan"),
            self._step("implement", ModelCatalog.CODE_ARCH, "write core code"),
            self._step("test", ModelCatalog.MATH, "challenge correctness and edge cases"),
            self._step("simplify", ModelCatalog.CODE_REVIEW, "remove unnecessary complexity and duplication"),
            self._step("retest", ModelCatalog.MATH, "confirm simplification preserved behavior"),
        )

    def _build_steps(self) -> tuple[PipelineStep, ...]:
        return (
            self._step("parallel-plan-a", ModelCatalog.CODE_ARCH, "produce architecture and implementation outline"),
            self._step("parallel-plan-b", ModelCatalog.MATH, "challenge assumptions with an alternate plan"),
            self._step("judge-plan", ModelCatalog.CODE_ARCH, "choose architecture and emit blueprint"),
            self._step("boilerplate", ModelCatalog.QUICK, "scaffold files and repetitive structure"),
            self._step("implement", ModelCatalog.CODE_ARCH, "build main functionality"),
            self._step("test", ModelCatalog.MATH, "validate correctness"),
            self._step("simplify", ModelCatalog.CODE_REVIEW, "cut duplication and non-needed code"),
            self._step("retest", ModelCatalog.MATH, "verify simplified result"),
            self._step("review-resolve", ModelCatalog.CODE_ARCH, "perform PR-style review and fix pass"),
            self._step("final-test", ModelCatalog.MATH, "run final correctness check"),
        )

    def _buildx_steps(self) -> tuple[PipelineStep, ...]:
        return (
            self._step("parallel-plan-a", ModelCatalog.CODE_ARCH, "produce architecture and implementation outline"),
            self._step("parallel-plan-b", ModelCatalog.MATH, "challenge assumptions with an alternate plan"),
            self._step("judge-plan", ModelCatalog.CODE_ARCH, "choose architecture and emit blueprint, risks, and review checklist"),
            self._step("boilerplate", ModelCatalog.QUICK, "scaffold files and repetitive structure"),
            self._step("implement", ModelCatalog.CODE_ARCH, "build main functionality"),
            self._step("test", ModelCatalog.MATH, "validate correctness"),
            self._step("simplify", ModelCatalog.CODE_REVIEW, "cut duplication and non-needed code"),
            self._step("retest", ModelCatalog.MATH, "verify simplified result"),
            self._step("review-resolve-a", ModelCatalog.CODE_ARCH, "perform first PR-style review and fix pass"),
            self._step("test-a", ModelCatalog.MATH, "test after first review resolution"),
            self._step("review-resolve-b", ModelCatalog.RESEARCH, "perform second wide-context review and fix pass"),
            self._step("final-test", ModelCatalog.MATH, "run final correctness check"),
        )

    @classmethod
    def _step(cls, name: str, model: str, purpose: str) -> PipelineStep:
        return PipelineStep(name=name, run=cls._run(model, role=name), purpose=purpose)

    @staticmethod
    def _is_buildq_request(prompt: str) -> bool:
        return bool(_BUILDQ_PATTERN.search(prompt))

    @staticmethod
    def _is_build_request(prompt: str) -> bool:
        return bool(_BUILD_PATTERN.search(prompt))

    @staticmethod
    def _is_buildx_request(prompt: str) -> bool:
        return bool(_BUILDX_PATTERN.search(prompt))

    @staticmethod
    def _is_tradeoff_request(prompt: str) -> bool:
        return any(pattern.search(prompt) for pattern in _TRADEOFF_PATTERNS)

    @staticmethod
    def _reject_legacy_flags(prompt: str) -> None:
        found = [flag for flag in _LEGACY_FLAGS if flag in prompt]
        if found:
            raise RoutingError("unsupported legacy flags present: " + ", ".join(found))

    @staticmethod
    def _cache_for_model(model: str) -> str:
        DispatcherRouter._validate_models((model,))
        if model.startswith("openai-codex/"):
            return "long"
        if model.startswith("opencode-go/"):
            return "short"
        if model.startswith("anthropic/"):
            return "short"
        raise RoutingError(f"unsupported provider for cache policy: {model}")

    @classmethod
    def _run(cls, model: str, *, role: str) -> ModelRun:
        retention = cls._cache_for_model(model)
        if retention not in CACHE_RETENTION_VALUES:
            raise RoutingError(f"invalid cache retention value: {retention}")
        return ModelRun(model=model, cache_retention=retention, role=role)

    @staticmethod
    def _validate_models(models: Iterable[str]) -> None:
        invalid = [model for model in models if not MODEL_ID_PATTERN.match(model)]
        if invalid:
            raise RoutingError("invalid model id format: " + ", ".join(invalid))
