#!/usr/bin/env python3
"""
Shared planning, profile-loading, and validation helpers for asking-until-100.
"""

from __future__ import annotations

from functools import lru_cache
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

from render_project_structure import (
    RepoObservations,
    infer_template,
    inspect_repo,
    is_build_task_prompt,
    render_project_structure,
    should_apply_repo_context,
)

CONFIG_FILENAME = ".asking-until-100.yaml"
DEFAULT_BUNDLED_PROFILE = "default-profile"

ALLOWED_RIGOR = ("low", "medium", "high", "highest")
ALLOWED_EXECUTION_GATES = ("block", "assumptions", "ask")
ALLOWED_REPORT_BASES = ("repo_plus_prompt", "prompt_only", "template_first")
DEFAULT_EXECUTION_GATE = "assumptions"
DEFAULT_REPORT_BASIS = "repo_plus_prompt"
DEFAULT_REPO_SCAN_MAX_DEPTH = 2
MODEL_ASSUMPTION_TARGET = {
    "family": "gpt-5.4",
    "reasoning_effort": "xhigh",
}
CANONICAL_TASK_TYPES = (
    "coding",
    "build",
    "architecture",
    "debugging",
    "discovery",
    "general",
)
CANONICAL_DIMENSIONS = (
    "goal",
    "success_criteria",
    "repo_state",
    "architecture",
    "product_behavior",
    "environment",
    "interfaces",
    "constraints",
    "runtime",
    "package_manager",
    "deploy_target",
    "ci_provider",
    "rollback",
    "logs",
    "evidence",
    "boundaries",
    "dependencies",
    "tradeoffs",
    "data_flow",
    "scale",
    "secrets",
    "timeline",
)

REQUIRED_TOP_KEYS = {"version", "model_assumptions", "behavior", "task_overrides"}
REQUIRED_BEHAVIOR_KEYS = {
    "target_readiness",
    "default_rigor",
    "max_initial_questions",
    "max_follow_up_questions",
    "include_answer_options",
    "thought_provoking_ratio",
    "report_for_high_rigor_coding",
}
ALLOWED_TOP_KEYS = REQUIRED_TOP_KEYS
ALLOWED_MODEL_ASSUMPTION_KEYS = {"family", "reasoning_effort"}
OPTIONAL_BEHAVIOR_KEYS = {
    "asking_intensity",
    "execution_gate",
    "report_basis",
    "repo_scan_max_depth",
}
ALLOWED_BEHAVIOR_KEYS = REQUIRED_BEHAVIOR_KEYS | OPTIONAL_BEHAVIOR_KEYS
ALLOWED_TASK_OVERRIDE_KEYS = {"rigor", "report_trigger", "required_dimensions"}
REPORT_TASK_TYPES = {"coding", "build"}
REPORT_SECTIONS = (
    "Working Hypothesis",
    "Architecture Questions",
    "Product Questions",
    "Constraint Questions",
    "Decision-Critical Unknowns",
)
TERM_SEPARATOR_PATTERN = r"[\s./_-]+"
INTENSITY_BEHAVIOR_FIELDS = (
    "target_readiness",
    "max_initial_questions",
    "max_follow_up_questions",
)
INTENSITY_LEVELS = (
    (0, 24, {"target_readiness": 70, "max_initial_questions": 2, "max_follow_up_questions": 1, "min_rigor": "low"}),
    (25, 49, {"target_readiness": 85, "max_initial_questions": 3, "max_follow_up_questions": 1, "min_rigor": "medium"}),
    (50, 74, {"target_readiness": 95, "max_initial_questions": 5, "max_follow_up_questions": 2, "min_rigor": "high"}),
    (75, 100, {"target_readiness": 100, "max_initial_questions": 6, "max_follow_up_questions": 4, "min_rigor": "highest"}),
)

TASK_SIGNAL_WEIGHTS: dict[str, tuple[tuple[str, int], ...]] = {
    "build": (
        ("ci/cd", 5),
        ("ci", 4),
        ("cd", 3),
        ("pipeline", 4),
        ("github actions", 4),
        ("gitlab ci", 4),
        ("circleci", 4),
        ("jenkins", 4),
        ("buildkite", 4),
        ("release", 3),
        ("rollback", 3),
        ("artifact", 2),
        ("artifacts", 2),
        ("package", 2),
        ("packaging", 2),
        ("publish", 2),
        ("publishing", 2),
        ("deploy", 2),
        ("deploys", 2),
        ("deployed", 2),
        ("deployment", 2),
        ("shipping", 1),
    ),
    "architecture": (
        ("architecture", 3),
        ("design", 3),
        ("system", 2),
        ("boundary", 2),
        ("boundaries", 2),
        ("tradeoff", 2),
        ("trade-off", 2),
        ("data flow", 2),
        ("module split", 2),
    ),
    "debugging": (
        ("traceback", 4),
        ("stack trace", 4),
        ("exception", 4),
        ("root cause", 4),
        ("repro", 3),
        ("reproduce", 3),
        ("error", 3),
        ("debug", 2),
        ("bug", 2),
        ("broken", 1),
        ("failing", 1),
        ("fix", 1),
    ),
    "discovery": (
        ("explore", 2),
        ("inspect", 2),
        ("understand", 2),
        ("audit", 2),
        ("investigate", 2),
        ("map", 2),
    ),
    "coding": (
        ("implement", 2),
        ("scaffold", 2),
        ("feature", 2),
        ("endpoint", 2),
        ("frontend", 2),
        ("backend", 2),
        ("api", 1),
        ("app", 1),
        ("service", 1),
        ("site", 1),
        ("cli", 1),
    ),
}
TASK_TYPE_PRIORITY = ("build", "architecture", "debugging", "discovery", "coding")

DIMENSION_SIGNALS = {
    "goal": ("build", "create", "implement", "fix", "design", "set up", "scaffold", "add"),
    "success_criteria": ("acceptance", "done", "success", "working", "ready", "must pass", "should"),
    "repo_state": (
        "existing",
        "current",
        "repo",
        "repository",
        "codebase",
        "already",
        "in this project",
        "monorepo",
    ),
    "architecture": (
        "architecture",
        "service",
        "app",
        "monorepo",
        "frontend",
        "backend",
        "api",
        "worker",
        "cli",
        "full-stack",
        "full stack",
    ),
    "product_behavior": ("user", "workflow", "feature", "behavior", "screen", "page", "endpoint", "flow"),
    "environment": ("local", "staging", "production", "docker", "container", "mac", "linux", "windows", "env"),
    "interfaces": (
        "api",
        "fastapi",
        "schema",
        "contract",
        "input",
        "output",
        "request",
        "response",
        "database",
        "db",
    ),
    "constraints": (
        "constraint",
        "deadline",
        "budget",
        "performance",
        "secure",
        "security",
        "maintainability",
        "maintainable",
        "compatible",
        "preserve",
        "without",
    ),
    "runtime": ("python", "node", "runtime", "version", "java", "ruby", "go", "deno"),
    "package_manager": ("npm", "pnpm", "yarn", "pip", "poetry", "uv", "cargo", "bundler"),
    "deploy_target": (
        "aws",
        "gcp",
        "azure",
        "vercel",
        "netlify",
        "kubernetes",
        "ecs",
        "serverless",
        "deploy",
        "deploys",
        "deployed",
        "fly.io",
    ),
    "ci_provider": ("github actions", "gitlab", "circleci", "jenkins", "buildkite", "ci"),
    "rollback": ("rollback", "revert", "fallback", "backout"),
    "logs": ("logs", "log", "output", "stderr", "stdout"),
    "evidence": ("error", "traceback", "stack trace", "repro", "reproduce", "failing command", "screenshot"),
    "boundaries": ("boundary", "boundaries", "ownership", "service split", "module split"),
    "dependencies": ("dependency", "dependencies", "integration", "third-party", "upstream", "downstream"),
    "tradeoffs": ("tradeoff", "trade-off", "prioritize", "priority", "latency", "cost"),
    "data_flow": ("data flow", "event", "queue", "stream", "ingest", "sync"),
    "scale": ("scale", "traffic", "throughput", "concurrency", "multi-tenant", "million"),
    "secrets": ("secret", "token", "credential", "apikey", "api key", "env var"),
    "timeline": ("today", "tomorrow", "urgent", "deadline", "this week", "milestone"),
}

SECTION_DIMENSIONS = {
    "Architecture Questions": (
        "repo_state",
        "architecture",
        "interfaces",
        "boundaries",
        "dependencies",
        "data_flow",
    ),
    "Product Questions": (
        "goal",
        "product_behavior",
        "success_criteria",
    ),
    "Constraint Questions": (
        "environment",
        "constraints",
        "runtime",
        "package_manager",
        "deploy_target",
        "ci_provider",
        "rollback",
        "logs",
        "evidence",
        "scale",
        "secrets",
        "timeline",
    ),
}

QUESTION_TEMPLATES: dict[str, dict[str, Any]] = {
    "goal": {
        "title": "What outcome matters most in this batch?",
        "why": "This sets the scope boundary before implementation details harden.",
        "hypothesis": "A thin, decision-revealing slice is likely better than solving every adjacent problem at once.",
        "options": ("thin first cut", "broader MVP", "strict parity with an existing flow", "other"),
    },
    "success_criteria": {
        "title": "What has to be true for this to count as done?",
        "why": "Acceptance criteria change how much polish, testing, and hardening is justified.",
        "hypothesis": "A working path plus targeted verification is probably the baseline unless you need release-ready hardening.",
        "options": ("usable happy path", "tests or checks pass", "production-ready handoff", "other"),
    },
    "repo_state": {
        "title": "What current repo state or layout should I preserve?",
        "why": "Existing structure and conventions constrain where new work should land.",
        "hypothesis": "The safest assumption is to fit the current layout unless you want a deliberate boundary change.",
        "options": ("extend existing area", "add a new package/module", "start a new app/service", "other"),
    },
    "architecture": {
        "title": "What implementation shape should I optimize for?",
        "why": "This changes boundaries, folders, dependencies, and sequencing.",
        "hypothesis": "A conventional single-repo shape is likely fine unless there is a scaling or ownership reason to split earlier.",
        "options": ("single app/module", "service plus client", "monorepo", "other"),
    },
    "product_behavior": {
        "title": "Which behavior or user flow is in scope first?",
        "why": "Behavioral scope affects data shape, edge cases, and testing depth.",
        "hypothesis": "The initial cut should probably cover one primary path unless there are must-have edge cases.",
        "options": ("single happy path", "a few core workflows", "full parity with an existing spec", "other"),
    },
    "environment": {
        "title": "Which environment constraints should I assume?",
        "why": "Environment details affect setup, compatibility, and validation commands.",
        "hypothesis": "Local development plus one primary target environment is probably enough unless you need a broader support matrix.",
        "options": ("local only", "local plus staging", "production target defined", "other"),
    },
    "interfaces": {
        "title": "Which interfaces or contracts are already fixed?",
        "why": "Stable interfaces limit how much internal structure can move.",
        "hypothesis": "There is probably an implied contract to preserve unless you are intentionally defining a new one.",
        "options": ("existing API/CLI contract", "existing data schema", "no fixed interface yet", "other"),
    },
    "constraints": {
        "title": "Which constraints are non-negotiable?",
        "why": "Hard constraints often matter more than the nominal feature request.",
        "hypothesis": "Delivery speed, compatibility, and maintainability are the likely tradeoffs unless you call out something stricter.",
        "options": ("ship quickly", "preserve existing stack", "performance/security first", "other"),
    },
    "runtime": {
        "title": "Which runtime and version should I target?",
        "why": "Runtime assumptions drive dependency, syntax, and tooling choices.",
        "hypothesis": "The repo probably already implies the runtime, but I should not guess if the version matters.",
        "options": ("existing repo runtime", "latest stable runtime", "specific pinned version", "other"),
    },
    "package_manager": {
        "title": "Which package manager or build tool is authoritative?",
        "why": "This affects lockfiles, commands, and CI parity.",
        "hypothesis": "The existing lockfile should win unless you are standardizing on a new tool.",
        "options": ("keep existing lockfile/tool", "switch to a new standard", "no preference", "other"),
    },
    "deploy_target": {
        "title": "What deploy or execution target should I design around?",
        "why": "Target environment changes artifact shape, configuration, and rollout strategy.",
        "hypothesis": "There is probably one primary deployment target even if multiple environments exist.",
        "options": ("local/dev only", "single cloud target", "container orchestrator", "other"),
    },
    "ci_provider": {
        "title": "Which CI system owns the build flow?",
        "why": "Provider choice changes config syntax, caching, secrets, and status checks.",
        "hypothesis": "Existing repo automation is the safest default unless there is a migration in flight.",
        "options": ("GitHub Actions", "GitLab CI", "another existing provider", "other"),
    },
    "rollback": {
        "title": "What rollback expectation should the plan preserve?",
        "why": "Rollback constraints change release slicing and deployment safety rails.",
        "hypothesis": "A simple revertable change set is usually enough unless you need zero-downtime or migration-safe rollback.",
        "options": ("simple git revert", "feature flag/fallback path", "migration-safe rollback", "other"),
    },
    "logs": {
        "title": "What logs or command output should I anchor on?",
        "why": "Without concrete output, build and failure analysis often devolve into guesswork.",
        "hypothesis": "There is probably a failing command or CI snippet that would cut down the search space immediately.",
        "options": ("local command output", "CI logs", "both", "other"),
    },
    "evidence": {
        "title": "What concrete evidence do we have for the failure or claim?",
        "why": "Good evidence separates real defects from assumptions about the system.",
        "hypothesis": "A minimal repro or exact error is likely enough to avoid a blind fix attempt.",
        "options": ("exact error output", "minimal repro", "failing test or command", "other"),
    },
    "boundaries": {
        "title": "Where should the system boundaries fall?",
        "why": "Boundary decisions determine ownership, coupling, and future extensibility.",
        "hypothesis": "A small number of explicit boundaries is better than a premature split into many moving parts.",
        "options": ("single bounded context", "few explicit modules/services", "broader split by team/domain", "other"),
    },
    "dependencies": {
        "title": "Which dependencies or integrations are fixed versus negotiable?",
        "why": "External dependencies strongly constrain viable implementation paths.",
        "hypothesis": "Only a subset of integrations are truly immovable, and identifying them early simplifies the design space.",
        "options": ("existing integrations are fixed", "some can change", "greenfield choice", "other"),
    },
    "tradeoffs": {
        "title": "Which tradeoff should break ties?",
        "why": "Competing architectural choices look similar until a priority is explicit.",
        "hypothesis": "Maintainability probably wins unless there is a latency, cost, or deadline driver you care about more.",
        "options": ("maintainability", "delivery speed", "performance/cost", "other"),
    },
    "data_flow": {
        "title": "What data flow or sequencing assumptions are already decided?",
        "why": "Data movement patterns change boundaries, persistence, and failure handling.",
        "hypothesis": "A straightforward request-response or linear pipeline is likely enough unless events or async fan-out are required.",
        "options": ("simple request/response", "batch or pipeline", "event-driven flow", "other"),
    },
    "scale": {
        "title": "What scale or load expectation should shape the plan?",
        "why": "Scale targets affect architecture long before optimization work begins.",
        "hypothesis": "Moderate internal or early external usage is probably the realistic baseline unless you expect large spikes immediately.",
        "options": ("small/internal", "moderate external", "high growth/high traffic", "other"),
    },
    "secrets": {
        "title": "Which secret or configuration boundaries matter here?",
        "why": "Credential handling changes local setup, CI, and deployment design.",
        "hypothesis": "Existing secret management should be reused unless you need a new provisioning path.",
        "options": ("reuse existing secrets flow", "introduce a new secret source", "local only for now", "other"),
    },
    "timeline": {
        "title": "What timeline pressure should change the depth of the solution?",
        "why": "Timeline changes whether the right move is a robust foundation or a narrower reversible cut.",
        "hypothesis": "A staged delivery is likely safer unless you truly need one-shot completeness.",
        "options": ("today/urgent", "this sprint", "can invest in foundation work", "other"),
    },
}

TASK_QUESTION_OVERRIDES: dict[str, dict[str, dict[str, Any]]] = {
    "coding": {
        "repo_state": {
            "title": "Which existing codepaths, packages, or folders should this change attach to?",
            "hypothesis": "I should extend the current app shape instead of inventing a parallel structure unless you want a new boundary.",
        },
        "architecture": {
            "title": "What code shape should the first implementation take?",
            "hypothesis": "A repo-local feature addition is probably safer than a brand-new service unless ownership or scaling forces a split.",
        },
        "product_behavior": {
            "title": "Which user-facing behavior needs to work first?",
            "hypothesis": "One primary flow is probably enough for the first pass unless you need a broader MVP.",
        },
        "interfaces": {
            "title": "Which API, data, or UI contracts are already committed?",
            "hypothesis": "At least one interface is probably implied by the existing repo or downstream consumers, so I should preserve it if it exists.",
        },
        "success_criteria": {
            "title": "What proof should I optimize for: tests, a usable slice, or production-ready hardening?",
            "hypothesis": "Passing verification plus a usable path is the likely bar unless release readiness is part of this batch.",
        },
    },
    "build": {
        "repo_state": {
            "title": "Am I extending an existing build/release path or introducing a new one?",
            "hypothesis": "The least risky move is to preserve the current repo layout and automation unless you want an intentional migration.",
        },
        "runtime": {
            "title": "Which runtime matrix should the build cover?",
            "hypothesis": "One pinned runtime is probably enough unless you explicitly need a compatibility matrix.",
        },
        "package_manager": {
            "title": "Which package manager and lockfile should the build trust?",
            "hypothesis": "The existing project lockfile should stay authoritative unless there is an active toolchain migration.",
        },
        "deploy_target": {
            "title": "What artifact or deployment target is the build trying to satisfy?",
            "hypothesis": "There is probably one main artifact target that should drive the pipeline instead of optimizing for every path at once.",
        },
        "ci_provider": {
            "title": "Which CI provider owns the canonical workflow?",
            "hypothesis": "I should fit the repo's existing automation platform unless you are migrating providers.",
        },
        "rollback": {
            "title": "What rollback posture should the pipeline keep intact?",
            "hypothesis": "A straightforward revert path is likely acceptable unless releases must remain migration-safe or zero-downtime.",
        },
        "logs": {
            "title": "Which failing output should I use as the anchor for the build plan?",
            "hypothesis": "The highest-value artifact is probably the exact failing command or CI step output.",
        },
        "success_criteria": {
            "title": "What makes this build/setup task successful?",
            "hypothesis": "A reproducible local command plus one passing CI path is probably the minimal meaningful target.",
        },
    },
    "architecture": {
        "boundaries": {
            "title": "Where do you want the primary boundaries or ownership lines to sit?",
        },
        "dependencies": {
            "title": "Which integrations or dependencies are fixed inputs to the design?",
        },
        "tradeoffs": {
            "title": "Which architectural tradeoff should break ties between options?",
        },
    },
    "debugging": {
        "evidence": {
            "title": "What exact failure evidence should the diagnosis be grounded in?",
            "hypothesis": "A single exact error or minimal repro is likely enough to avoid blind debugging.",
        },
    },
}

UNKNOWN_EXPLANATIONS = {
    "goal": "The intended outcome is still broad enough that the implementation could optimize for the wrong target.",
    "success_criteria": "The finish line is underspecified, so verification depth and scope could drift.",
    "repo_state": "The current repo shape may invalidate a clean-room plan.",
    "architecture": "System shape is still open, which blocks safe sequencing and folder/layout decisions.",
    "product_behavior": "Behavior scope is unclear, so it is easy to overbuild or miss the intended flow.",
    "environment": "Environment assumptions can invalidate commands, tooling, or compatibility decisions.",
    "interfaces": "Contract changes could break downstream consumers or UI/data expectations.",
    "constraints": "Unstated constraints can dominate all other design choices.",
    "runtime": "Runtime assumptions affect dependencies, syntax, and CI coverage.",
    "package_manager": "Toolchain ambiguity can create the wrong commands and lockfile churn.",
    "deploy_target": "Deployment target changes artifact shape and release strategy.",
    "ci_provider": "CI ownership changes workflow syntax, caching, and secret wiring.",
    "rollback": "Rollback expectations determine how safely the change can be shipped.",
    "logs": "Missing output leaves build investigation too speculative.",
    "evidence": "Without concrete evidence, debugging can easily target the wrong cause.",
    "boundaries": "Boundary decisions still have multiple plausible answers.",
    "dependencies": "Fixed integrations can rule out otherwise reasonable approaches.",
    "tradeoffs": "Tie-break priorities are still unstated.",
    "data_flow": "Flow sequencing is still uncertain enough to change architecture choices.",
    "scale": "Load assumptions can make a simple design either sufficient or dangerously naive.",
    "secrets": "Credential handling may impose integration or deployment constraints.",
    "timeline": "Delivery pressure may require a narrower or more reversible approach.",
}

TASK_HYPOTHESES = {
    "coding": "The safest starting point is a repo-local implementation increment until the missing details justify a new boundary or broader scope.",
    "build": "The safest starting point is to preserve the existing toolchain and release path until the missing delivery details justify a migration.",
    "architecture": "A small number of explicit boundaries is likely better than prematurely splitting the system in too many directions.",
    "debugging": "The best next move is to anchor on exact evidence rather than hypothesizing about root causes too early.",
    "discovery": "A narrow map of the current system is probably more useful than a speculative redesign.",
    "general": "A minimal, reversible next step is safer than a broad plan when key dimensions are still missing.",
}


@dataclass(frozen=True)
class QuestionPlan:
    section: str
    dimension: str
    title: str
    why: str
    hypothesis: str
    options: tuple[str, ...]


@dataclass(frozen=True)
class ProfileResolution:
    profile: dict[str, Any]
    sources: tuple[str, ...]
    bundled_profile: Path | None
    repo_profile: Path | None
    explicit_override: Path | None


@dataclass(frozen=True)
class PlanningResult:
    task_type: str
    mode: str
    execution_gate: str
    repo_context_applied: bool
    readiness: int
    target_readiness: int
    rigor: str
    required_dimensions: tuple[str, ...]
    present_dimensions: tuple[str, ...]
    missing_dimensions: tuple[str, ...]
    blocking_dimensions: tuple[str, ...]
    working_hypothesis: str
    structure_template: str | None
    sections: tuple[tuple[str, tuple[QuestionPlan, ...]], ...]
    decision_unknowns: tuple[str, ...]
    repo_signals_summary: tuple[str, ...]


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _rigor_rank(rigor: str) -> int:
    return ALLOWED_RIGOR.index(rigor)


def _max_rigor(left: str, right: str) -> str:
    return left if _rigor_rank(left) >= _rigor_rank(right) else right


def _intensity_behavior(intensity: int) -> dict[str, Any]:
    for lower, upper, behavior in INTENSITY_LEVELS:
        if lower <= intensity <= upper:
            return deepcopy(behavior)
    raise ValueError(f"asking_intensity must be between 0 and 100, got {intensity}")


def _normalize_profile_layer(data: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(data)
    behavior = normalized.get("behavior")
    if not isinstance(behavior, dict) or "asking_intensity" not in behavior:
        return normalized

    asking_intensity = behavior["asking_intensity"]
    if not isinstance(asking_intensity, int):
        return normalized

    derived = _intensity_behavior(asking_intensity)
    for key in INTENSITY_BEHAVIOR_FIELDS:
        if key not in behavior:
            behavior[key] = derived[key]
    return normalized


def _intensity_min_rigor(profile: dict[str, Any]) -> str:
    behavior = profile.get("behavior", {})
    intensity = behavior.get("asking_intensity")
    if not isinstance(intensity, int):
        return behavior.get("default_rigor", "medium")
    return _intensity_behavior(intensity)["min_rigor"]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def assets_dir() -> Path:
    return skill_root() / "assets"


def available_bundled_profiles() -> tuple[str, ...]:
    return tuple(
        sorted(
            path.stem
            for path in assets_dir().iterdir()
            if path.is_file() and path.suffix in {".yaml", ".yml"}
        )
    )


def bundled_profile_path(profile_name: str | Path | None = None) -> Path:
    if profile_name is None:
        return assets_dir() / f"{DEFAULT_BUNDLED_PROFILE}.yaml"

    candidate = Path(profile_name)
    if candidate.exists():
        return candidate.resolve()

    if candidate.is_absolute() or candidate.parent != Path("."):
        raise ValueError(f"bundled profile path '{profile_name}' does not exist")

    normalized = str(profile_name)
    if not normalized.endswith((".yaml", ".yml")):
        normalized = f"{normalized}.yaml"

    bundled_path = (assets_dir() / normalized).resolve()
    if bundled_path.exists():
        return bundled_path

    available = ", ".join(available_bundled_profiles())
    raise ValueError(
        f"unknown bundled profile '{profile_name}'; available bundled profiles: {available}"
    )


def discover_repo_profile(start_dir: Path | None = None) -> Path | None:
    current = (start_dir or Path.cwd()).resolve()
    for candidate_dir in (current, *current.parents):
        candidate = candidate_dir / CONFIG_FILENAME
        if candidate.exists():
            return candidate
    return None


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        raise

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level content must be a mapping")
    return data


@lru_cache(maxsize=None)
def _compiled_term_pattern(term: str) -> re.Pattern[str]:
    parts = re.findall(r"[a-z0-9]+", term.lower())
    if not parts:
        raise ValueError(f"cannot compile an empty term pattern from {term!r}")
    pattern = r"\b" + TERM_SEPARATOR_PATTERN.join(re.escape(part) for part in parts) + r"\b"
    return re.compile(pattern)


def _matches_term(lowered_prompt: str, term: str) -> bool:
    return _compiled_term_pattern(term).search(lowered_prompt) is not None


def _matches_any_term(lowered_prompt: str, terms: tuple[str, ...]) -> bool:
    return any(_matches_term(lowered_prompt, term) for term in terms)


def _error(source: Path | str, message: str) -> str:
    return f"{source}: {message}"


def validate_bundled_model_assumptions(data: dict[str, Any], source: Path | str) -> list[str]:
    model_assumptions = data.get("model_assumptions")
    if not isinstance(model_assumptions, dict):
        return [_error(source, "model_assumptions must be a mapping")]

    errors: list[str] = []
    for key, expected in MODEL_ASSUMPTION_TARGET.items():
        if model_assumptions.get(key) != expected:
            errors.append(
                _error(
                    source,
                    f"bundled profile model_assumptions.{key} must be '{expected}'",
                )
            )
    return errors


def validate_profile_data(
    data: dict[str, Any],
    source: Path | str,
    *,
    allow_partial: bool = False,
) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return [_error(source, "top-level content must be a mapping")]

    unexpected_top = set(data.keys()) - ALLOWED_TOP_KEYS
    if unexpected_top:
        errors.append(
            _error(source, f"unexpected top-level keys: {', '.join(sorted(unexpected_top))}")
        )

    if not allow_partial:
        missing_top = REQUIRED_TOP_KEYS - set(data.keys())
        if missing_top:
            errors.append(_error(source, f"missing top-level keys: {', '.join(sorted(missing_top))}"))

    if "version" in data:
        version = data.get("version")
        if not isinstance(version, int) or version < 1:
            errors.append(_error(source, "version must be an integer greater than or equal to 1"))

    model_assumptions = data.get("model_assumptions")
    if model_assumptions is None:
        if not allow_partial:
            errors.append(_error(source, "model_assumptions must be a mapping"))
    elif not isinstance(model_assumptions, dict):
        errors.append(_error(source, "model_assumptions must be a mapping"))
    else:
        unexpected_model = set(model_assumptions.keys()) - ALLOWED_MODEL_ASSUMPTION_KEYS
        if unexpected_model:
            errors.append(
                _error(
                    source,
                    f"unexpected model_assumptions keys: {', '.join(sorted(unexpected_model))}",
                )
            )
        if not allow_partial:
            missing_model = ALLOWED_MODEL_ASSUMPTION_KEYS - set(model_assumptions.keys())
            if missing_model:
                errors.append(
                    _error(source, f"missing model_assumptions keys: {', '.join(sorted(missing_model))}")
                )
        for key in ALLOWED_MODEL_ASSUMPTION_KEYS:
            if key in model_assumptions:
                value = model_assumptions[key]
                if not isinstance(value, str) or not value.strip():
                    errors.append(_error(source, f"model_assumptions.{key} must be a non-empty string"))

    behavior = data.get("behavior")
    if behavior is None:
        if not allow_partial:
            errors.append(_error(source, "behavior must be a mapping"))
    elif not isinstance(behavior, dict):
        errors.append(_error(source, "behavior must be a mapping"))
    else:
        unexpected_behavior = set(behavior.keys()) - ALLOWED_BEHAVIOR_KEYS
        if unexpected_behavior:
            errors.append(
                _error(source, f"unexpected behavior keys: {', '.join(sorted(unexpected_behavior))}")
            )
        if not allow_partial:
            missing_behavior = REQUIRED_BEHAVIOR_KEYS - set(behavior.keys())
            if missing_behavior:
                errors.append(
                    _error(source, f"missing behavior keys: {', '.join(sorted(missing_behavior))}")
                )
        if "default_rigor" in behavior and behavior["default_rigor"] not in ALLOWED_RIGOR:
            errors.append(_error(source, f"default_rigor must be one of {list(ALLOWED_RIGOR)}"))
        if "asking_intensity" in behavior:
            intensity = behavior["asking_intensity"]
            if not isinstance(intensity, int) or not 0 <= intensity <= 100:
                errors.append(_error(source, "asking_intensity must be an integer between 0 and 100"))
        if "execution_gate" in behavior and behavior["execution_gate"] not in ALLOWED_EXECUTION_GATES:
            errors.append(
                _error(source, f"execution_gate must be one of {list(ALLOWED_EXECUTION_GATES)}")
            )
        if "report_basis" in behavior and behavior["report_basis"] not in ALLOWED_REPORT_BASES:
            errors.append(
                _error(source, f"report_basis must be one of {list(ALLOWED_REPORT_BASES)}")
            )
        if "target_readiness" in behavior:
            readiness = behavior["target_readiness"]
            if not isinstance(readiness, int) or not 0 <= readiness <= 100:
                errors.append(
                    _error(source, "target_readiness must be an integer between 0 and 100")
                )
        for key in ("max_initial_questions", "max_follow_up_questions"):
            if key in behavior:
                value = behavior[key]
                if not isinstance(value, int) or value < 0:
                    errors.append(_error(source, f"{key} must be a non-negative integer"))
        if "repo_scan_max_depth" in behavior:
            depth = behavior["repo_scan_max_depth"]
            if not isinstance(depth, int) or depth < 1:
                errors.append(_error(source, "repo_scan_max_depth must be an integer greater than or equal to 1"))
        if "thought_provoking_ratio" in behavior:
            ratio = behavior["thought_provoking_ratio"]
            if not isinstance(ratio, (int, float)) or not 0.0 <= float(ratio) <= 1.0:
                errors.append(_error(source, "thought_provoking_ratio must be between 0.0 and 1.0"))
        for key in ("include_answer_options", "report_for_high_rigor_coding"):
            if key in behavior and not isinstance(behavior[key], bool):
                errors.append(_error(source, f"{key} must be a boolean"))

    task_overrides = data.get("task_overrides")
    if task_overrides is None:
        if not allow_partial:
            errors.append(_error(source, "task_overrides must be a mapping"))
    elif not isinstance(task_overrides, dict):
        errors.append(_error(source, "task_overrides must be a mapping"))
    else:
        if not allow_partial:
            missing_tasks = set(CANONICAL_TASK_TYPES) - set(task_overrides.keys())
            if missing_tasks:
                errors.append(
                    _error(source, f"missing task overrides: {', '.join(sorted(missing_tasks))}")
                )
        for task_name, override in task_overrides.items():
            if task_name not in CANONICAL_TASK_TYPES:
                allowed = ", ".join(CANONICAL_TASK_TYPES)
                errors.append(
                    _error(source, f"task override '{task_name}' is invalid; allowed task types: {allowed}")
                )
                continue
            if not isinstance(override, dict):
                errors.append(_error(source, f"task override '{task_name}' must be a mapping"))
                continue

            unexpected_override = set(override.keys()) - ALLOWED_TASK_OVERRIDE_KEYS
            if unexpected_override:
                errors.append(
                    _error(
                        source,
                        f"task override '{task_name}' has unexpected keys: {', '.join(sorted(unexpected_override))}",
                    )
                )

            if not allow_partial:
                missing_override = ALLOWED_TASK_OVERRIDE_KEYS - set(override.keys())
                if missing_override:
                    errors.append(
                        _error(
                            source,
                            f"task override '{task_name}' missing keys: {', '.join(sorted(missing_override))}",
                        )
                    )

            if "rigor" in override and override["rigor"] not in ALLOWED_RIGOR:
                errors.append(_error(source, f"task override '{task_name}' has invalid rigor '{override['rigor']}'"))

            if "report_trigger" in override and not isinstance(override["report_trigger"], bool):
                errors.append(_error(source, f"task override '{task_name}' report_trigger must be boolean"))

            if "required_dimensions" in override:
                required_dimensions = override["required_dimensions"]
                if not isinstance(required_dimensions, list) or not required_dimensions:
                    errors.append(
                        _error(
                            source,
                            f"task override '{task_name}' requires a non-empty dimension list",
                        )
                    )
                else:
                    seen_dimensions: set[str] = set()
                    for dimension in required_dimensions:
                        if not isinstance(dimension, str) or not dimension.strip():
                            errors.append(
                                _error(
                                    source,
                                    f"task override '{task_name}' dimensions must be non-empty strings",
                                )
                            )
                            continue
                        if dimension not in CANONICAL_DIMENSIONS:
                            allowed = ", ".join(CANONICAL_DIMENSIONS)
                            errors.append(
                                _error(
                                    source,
                                    f"task override '{task_name}' uses invalid dimension '{dimension}'; allowed dimensions: {allowed}",
                                )
                            )
                        if dimension in seen_dimensions:
                            errors.append(
                                _error(
                                    source,
                                    f"task override '{task_name}' repeats dimension '{dimension}'",
                                )
                            )
                        seen_dimensions.add(dimension)

    return errors


def _load_layer(path: Path, *, allow_partial: bool) -> dict[str, Any]:
    data = _normalize_profile_layer(load_yaml_mapping(path))
    errors = validate_profile_data(data, path, allow_partial=allow_partial)
    if path.resolve().parent == assets_dir().resolve():
        errors.extend(validate_bundled_model_assumptions(data, path))
    if errors:
        raise ValueError("\n".join(errors))
    return data


def load_effective_profile(
    *,
    explicit_override: Path | None = None,
    bundled_profile: str | Path | None = None,
    cwd: Path | None = None,
) -> ProfileResolution:
    effective_profile = _load_layer(
        bundled_profile_path(DEFAULT_BUNDLED_PROFILE),
        allow_partial=False,
    )
    sources = ["defaults"]

    bundled_path = bundled_profile_path(bundled_profile)
    effective_profile = deep_merge(effective_profile, _load_layer(bundled_path, allow_partial=False))
    sources.append(f"bundled:{bundled_path.name}")

    repo_profile = discover_repo_profile(cwd)
    if repo_profile is not None:
        effective_profile = deep_merge(effective_profile, _load_layer(repo_profile, allow_partial=True))
        sources.append(f"repo-local:{repo_profile.name}")

    if explicit_override is not None:
        explicit_override = explicit_override.resolve()
        effective_profile = deep_merge(
            effective_profile,
            _load_layer(explicit_override, allow_partial=True),
        )
        sources.append(f"explicit:{explicit_override.name}")

    effective_profile = _normalize_profile_layer(effective_profile)
    merged_errors = validate_profile_data(effective_profile, "effective-profile", allow_partial=False)
    if merged_errors:
        raise ValueError("\n".join(merged_errors))

    return ProfileResolution(
        profile=effective_profile,
        sources=tuple(sources),
        bundled_profile=bundled_path if bundled_path.exists() else None,
        repo_profile=repo_profile,
        explicit_override=explicit_override,
    )


def _repo_root_from_inputs(repo_root: Path | None, cwd: Path | None) -> Path | None:
    if repo_root is not None:
        return repo_root.resolve()
    if cwd is not None:
        return cwd.resolve()
    return Path.cwd().resolve()


def _repo_dimensions(repo_observations: RepoObservations | None) -> set[str]:
    if repo_observations is None or not repo_observations.has_repo:
        return set()

    present = {"repo_state"}
    if repo_observations.archetype_hint is not None:
        present.add("architecture")
    if repo_observations.runtime_signals:
        present.add("runtime")
    if repo_observations.package_manager_signals:
        present.add("package_manager")
    if repo_observations.ci_signals:
        present.add("ci_provider")
    if repo_observations.deploy_signals:
        present.add("deploy_target")
    if any(path.startswith("src/routes") or path.endswith("/routes") for path in repo_observations.tree_paths):
        present.add("interfaces")
    if any(path.startswith(".github/workflows") or path.startswith("ci/") for path in repo_observations.tree_paths):
        present.add("environment")
    return present


def _repo_signal_summary(repo_observations: RepoObservations | None) -> tuple[str, ...]:
    if repo_observations is None or not repo_observations.has_repo:
        return ()

    summary: list[str] = ["repo:detected"]
    if repo_observations.archetype_hint:
        summary.append(f"shape:{repo_observations.archetype_hint}")
    if repo_observations.runtime_signals:
        summary.append(f"runtime:{', '.join(repo_observations.runtime_signals)}")
    if repo_observations.package_manager_signals:
        summary.append(f"package-manager:{', '.join(repo_observations.package_manager_signals)}")
    if repo_observations.ci_signals:
        summary.append(f"ci:{', '.join(repo_observations.ci_signals)}")
    if repo_observations.deploy_signals:
        summary.append(f"deploy:{', '.join(repo_observations.deploy_signals)}")
    return tuple(summary)


def _resolve_execution_gate(profile: dict[str, Any], task_type: str, rigor: str) -> str:
    configured = profile.get("behavior", {}).get("execution_gate")
    if configured in ALLOWED_EXECUTION_GATES:
        return configured
    if task_type in REPORT_TASK_TYPES and rigor == "highest":
        return "block"
    return DEFAULT_EXECUTION_GATE


def _default_blocking_dimensions(execution_gate: str, missing_dimensions: tuple[str, ...]) -> tuple[str, ...]:
    if execution_gate in {"block", "ask"}:
        return missing_dimensions
    return ()


def infer_task_type(prompt: str, explicit_task_type: str | None = None) -> str:
    if explicit_task_type is not None:
        if explicit_task_type not in CANONICAL_TASK_TYPES:
            allowed = ", ".join(CANONICAL_TASK_TYPES)
            raise ValueError(f"invalid task type '{explicit_task_type}'; allowed task types: {allowed}")
        return explicit_task_type

    lowered = prompt.lower()
    scores = {
        task_type: sum(
            weight for term, weight in signals if _matches_term(lowered, term)
        )
        for task_type, signals in TASK_SIGNAL_WEIGHTS.items()
    }
    if is_build_task_prompt(prompt):
        scores["build"] += 4
    best_score = max(scores.values(), default=0)
    if best_score == 0:
        return "general"

    for task_type in TASK_TYPE_PRIORITY:
        if scores.get(task_type, 0) == best_score:
            return task_type
    return "general"


def infer_present_dimensions(
    prompt: str,
    repo_observations: RepoObservations | None = None,
) -> set[str]:
    lowered = prompt.lower()
    present: set[str] = set()

    if len(prompt.split()) >= 4:
        present.add("goal")

    for dimension, signals in DIMENSION_SIGNALS.items():
        if _matches_any_term(lowered, signals):
            present.add(dimension)

    if "existing" in lowered or "current" in lowered:
        present.add("repo_state")

    present.update(_repo_dimensions(repo_observations))
    return present


def _task_config(profile: dict[str, Any], task_type: str) -> dict[str, Any]:
    task_overrides = profile.get("task_overrides", {})
    general = task_overrides.get("general", {})
    return deep_merge(general, task_overrides.get(task_type, {}))


def choose_mode(
    task_type: str,
    *,
    rigor: str,
    report_trigger: bool,
    report_for_high_rigor_coding: bool,
    readiness: int,
    target_readiness: int,
    required_dimensions: tuple[str, ...],
    missing_dimensions: tuple[str, ...],
) -> str:
    gap_count = len(missing_dimensions)
    gap_ratio = gap_count / max(1, len(required_dimensions))
    readiness_gap = max(0, target_readiness - readiness)

    report_allowed = (
        task_type in REPORT_TASK_TYPES and report_trigger and report_for_high_rigor_coding
    )
    if report_allowed:
        if rigor == "highest" and gap_count >= 1:
            return "report"
        if rigor == "high" and (gap_ratio >= 0.5 or readiness_gap >= 35):
            return "report"

    if gap_count == 0 and readiness_gap == 0:
        if rigor == "low":
            return "fast"
        if rigor == "medium":
            return "guided"
        return "deep"

    if rigor in {"high", "highest"} and (gap_count >= 2 or readiness_gap >= 15):
        return "deep"
    if gap_count >= 1 or readiness_gap > 0 or rigor == "medium":
        return "guided"
    return "fast"


def assess_prompt(
    prompt: str,
    profile: dict[str, Any],
    explicit_task_type: str | None = None,
    *,
    repo_root: Path | None = None,
    repo_root_explicit: bool | None = None,
) -> PlanningResult:
    task_type = infer_task_type(prompt, explicit_task_type)
    task_config = _task_config(profile, task_type)
    required_dimensions = tuple(task_config.get("required_dimensions", ()))
    behavior = profile.get("behavior", {})
    repo_scan_max_depth = behavior.get("repo_scan_max_depth", DEFAULT_REPO_SCAN_MAX_DEPTH)
    report_basis = behavior.get("report_basis", DEFAULT_REPORT_BASIS)
    if repo_root_explicit is None:
        repo_root_explicit = repo_root is not None
    candidate_repo_root = _repo_root_from_inputs(repo_root, None)
    candidate_repo_observations = inspect_repo(candidate_repo_root, max_depth=repo_scan_max_depth)
    repo_context_applied = (
        report_basis == DEFAULT_REPORT_BASIS
        and should_apply_repo_context(
            prompt,
            task_type=task_type,
            repo_observations=candidate_repo_observations,
            repo_root_explicit=repo_root_explicit,
        )
    )
    repo_observations = candidate_repo_observations if repo_context_applied else None
    present_dimensions = tuple(
        dimension
        for dimension in required_dimensions
        if dimension in infer_present_dimensions(prompt, repo_observations)
    )
    missing_dimensions = tuple(
        dimension for dimension in required_dimensions if dimension not in present_dimensions
    )

    readiness = round(100 * len(present_dimensions) / max(1, len(required_dimensions)))
    target_readiness = behavior.get("target_readiness", 100)
    rigor = _max_rigor(
        task_config.get("rigor", behavior.get("default_rigor", "medium")),
        _intensity_min_rigor(profile),
    )
    mode = choose_mode(
        task_type,
        rigor=rigor,
        report_trigger=bool(task_config.get("report_trigger", False)),
        report_for_high_rigor_coding=bool(
            behavior.get("report_for_high_rigor_coding", True)
        ),
        readiness=readiness,
        target_readiness=target_readiness,
        required_dimensions=required_dimensions,
        missing_dimensions=missing_dimensions,
    )
    execution_gate = _resolve_execution_gate(profile, task_type, rigor)
    blocking_dimensions = _default_blocking_dimensions(execution_gate, missing_dimensions)

    question_limit = None
    if mode != "report":
        question_limit = behavior.get("max_initial_questions", 4)
    sections = build_sections(
        task_type,
        missing_dimensions,
        limit=question_limit,
    )
    structure_template = (
        infer_template(prompt, task_type=task_type)
        if mode == "report" and task_type in REPORT_TASK_TYPES
        else None
    )

    return PlanningResult(
        task_type=task_type,
        mode=mode,
        execution_gate=execution_gate,
        repo_context_applied=repo_context_applied,
        readiness=readiness,
        target_readiness=target_readiness,
        rigor=rigor,
        required_dimensions=required_dimensions,
        present_dimensions=present_dimensions,
        missing_dimensions=missing_dimensions,
        blocking_dimensions=blocking_dimensions,
        working_hypothesis=build_working_hypothesis(task_type, missing_dimensions),
        structure_template=structure_template,
        sections=sections,
        decision_unknowns=missing_dimensions,
        repo_signals_summary=_repo_signal_summary(repo_observations),
    )


def _question_template(task_type: str, dimension: str) -> dict[str, Any]:
    template = deepcopy(QUESTION_TEMPLATES[dimension])
    template.update(TASK_QUESTION_OVERRIDES.get(task_type, {}).get(dimension, {}))
    return template


def build_sections(
    task_type: str,
    missing_dimensions: tuple[str, ...],
    *,
    limit: int | None,
) -> tuple[tuple[str, tuple[QuestionPlan, ...]], ...]:
    planned_sections: list[tuple[str, tuple[QuestionPlan, ...]]] = []
    planned_count = 0
    seen_dimensions: set[str] = set()

    for section_name in REPORT_SECTIONS[1:4]:
        questions: list[QuestionPlan] = []
        for dimension in SECTION_DIMENSIONS[section_name]:
            if dimension not in missing_dimensions:
                continue
            if dimension in seen_dimensions:
                continue
            if limit is not None and planned_count >= limit:
                break
            template = _question_template(task_type, dimension)
            questions.append(
                QuestionPlan(
                    section=section_name,
                    dimension=dimension,
                    title=template["title"],
                    why=template["why"],
                    hypothesis=template["hypothesis"],
                    options=tuple(template["options"]),
                )
            )
            planned_count += 1
            seen_dimensions.add(dimension)
        planned_sections.append((section_name, tuple(questions)))

    return tuple(planned_sections)


def build_working_hypothesis(task_type: str, missing_dimensions: tuple[str, ...]) -> str:
    base = TASK_HYPOTHESES.get(task_type, TASK_HYPOTHESES["general"])
    if not missing_dimensions:
        return f"{base} The prompt already covers the configured readiness dimensions."

    top_gaps = ", ".join(missing_dimensions[:3])
    return f"{base} The biggest remaining unknowns are {top_gaps}."


def render_question(question: QuestionPlan, *, include_answer_options: bool) -> list[str]:
    lines = [
        f"- {question.title}",
        f"  Why this matters: {question.why}",
        f"  Working hypothesis: {question.hypothesis}",
    ]
    if include_answer_options:
        lines.append("  Suggested answers:")
        lines.extend(f"  - {option}" for option in question.options)
    lines.append("  Free-form: provide your own answer if none of the options fit.")
    return lines


def _format_dimension_list(dimensions: tuple[str, ...]) -> str:
    return ", ".join(dimensions) if dimensions else "none"


def render_preview_text(
    prompt: str,
    *,
    explicit_task_type: str | None = None,
    explicit_override: Path | None = None,
    bundled_profile: str | Path | None = None,
    cwd: Path | None = None,
    repo_root: Path | None = None,
) -> str:
    resolution = load_effective_profile(
        explicit_override=explicit_override,
        bundled_profile=bundled_profile,
        cwd=cwd,
    )
    effective_repo_root = _repo_root_from_inputs(repo_root, cwd)
    result = assess_prompt(
        prompt,
        resolution.profile,
        explicit_task_type,
        repo_root=effective_repo_root,
        repo_root_explicit=repo_root is not None,
    )
    behavior = resolution.profile.get("behavior", {})
    include_answer_options = bool(behavior.get("include_answer_options", True))
    report_basis = behavior.get("report_basis", DEFAULT_REPORT_BASIS)
    repo_scan_max_depth = behavior.get("repo_scan_max_depth", DEFAULT_REPO_SCAN_MAX_DEPTH)

    lines = [
        f"Task type: {result.task_type}",
        f"Mode: {result.mode}",
        f"Rigor: {result.rigor}",
        f"Execution Gate: {result.execution_gate}",
        f"Readiness: {result.readiness}/{result.target_readiness}",
        f"Profile sources: {' -> '.join(resolution.sources)}",
        f"Report basis: {report_basis}",
        f"Repo context: {'applied' if result.repo_context_applied else 'not applied'}",
        f"Required dimensions: {_format_dimension_list(result.required_dimensions)}",
        f"Missing dimensions: {_format_dimension_list(result.missing_dimensions)}",
    ]
    if result.repo_context_applied:
        lines.extend(
            [
                f"Repo scan root: {effective_repo_root}",
                f"Repo scan max depth: {repo_scan_max_depth}",
                f"Repo signals: {', '.join(result.repo_signals_summary)}",
            ]
        )

    if result.mode == "report":
        lines.append("")
        if result.structure_template is not None:
            lines.extend(
                [
                    "Provisional Project Structure",
                    render_project_structure(
                        prompt,
                        task_type=result.task_type,
                        report_basis=report_basis,
                        repo_root=effective_repo_root,
                        repo_scan_max_depth=repo_scan_max_depth,
                        repo_root_explicit=repo_root is not None,
                        apply_repo_context=result.repo_context_applied,
                    ),
                    "",
                ]
            )
        lines.extend(
            [
                "Working Hypothesis",
                f"- {result.working_hypothesis}",
                f"- Execution gate summary: {result.execution_gate}",
                f"- Blocking dimensions: {_format_dimension_list(result.blocking_dimensions)}",
            ]
        )
        if result.repo_signals_summary:
            lines.append(f"- Repo signals summary: {', '.join(result.repo_signals_summary)}")
        section_map = dict(result.sections)
        for section_name in REPORT_SECTIONS[1:4]:
            lines.extend(["", section_name])
            questions = section_map.get(section_name, ())
            if not questions:
                if result.repo_context_applied:
                    lines.append("- No critical gaps remain in this section after prompt and repo inspection.")
                else:
                    lines.append("- No critical gaps remain in this section from the prompt alone.")
                continue
            for question in questions:
                lines.extend(render_question(question, include_answer_options=include_answer_options))
        lines.extend(["", "Decision-Critical Unknowns"])
        if result.decision_unknowns:
            for dimension in result.decision_unknowns:
                lines.append(f"- {dimension}: {UNKNOWN_EXPLANATIONS[dimension]}")
        else:
            lines.append("- No decision-critical unknowns remain under the configured profile.")
        return "\n".join(lines)

    lines.extend(
        [
            "",
            "Working Hypothesis",
            f"- {result.working_hypothesis}",
            f"- Execution gate summary: {result.execution_gate}",
            f"- Blocking dimensions: {_format_dimension_list(result.blocking_dimensions)}",
        ]
    )
    if result.repo_signals_summary:
        lines.append(f"- Repo signals summary: {', '.join(result.repo_signals_summary)}")
    for section_name, questions in result.sections:
        if not questions:
            continue
        lines.extend(["", section_name])
        for question in questions:
            lines.extend(render_question(question, include_answer_options=include_answer_options))

    lines.extend(["", "Decision-Critical Unknowns"])
    if result.decision_unknowns:
        for dimension in result.decision_unknowns:
            lines.append(f"- {dimension}: {UNKNOWN_EXPLANATIONS[dimension]}")
    else:
        lines.append("- No decision-critical unknowns remain under the configured profile.")
    return "\n".join(lines)


def render_profile_explanation(
    *,
    explicit_override: Path | None = None,
    bundled_profile: str | Path | None = None,
    cwd: Path | None = None,
) -> str:
    resolution = load_effective_profile(
        explicit_override=explicit_override,
        bundled_profile=bundled_profile,
        cwd=cwd,
    )

    behavior = resolution.profile.get("behavior", {})
    lines = ["Source order:"]
    lines.extend(f"- {source}" for source in resolution.sources)
    if "asking_intensity" in behavior:
        derived = _intensity_behavior(behavior["asking_intensity"])
        lines.extend(
            [
                "",
                "Derived from asking_intensity",
                f"- asking_intensity: {behavior['asking_intensity']}",
                f"- target_readiness: {derived['target_readiness']}",
                f"- max_initial_questions: {derived['max_initial_questions']}",
                f"- max_follow_up_questions: {derived['max_follow_up_questions']}",
                f"- min_rigor floor: {derived['min_rigor']}",
            ]
        )
    lines.extend(["", "Effective profile", yaml.safe_dump(resolution.profile, sort_keys=False).rstrip()])
    return "\n".join(lines)
