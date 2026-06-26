#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import statistics
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REQUIRED_PROFILE_FIELDS = {
    "id",
    "name",
    "domains",
    "roles",
    "routing_keywords",
    "bio_arc",
    "canonical_works",
    "signature_ideas",
    "reasoning_kernel",
    "preferred_evidence",
    "critique_style",
    "blind_spots",
    "advantage_knowledge_base",
    "question_playbook",
    "domain_relevance",
    "quote_bank",
    "source_refs",
    "source_confidence",
    "freshness",
    "usage_boundaries",
}

SCORING_AXES = ("breadth", "depth", "thickness", "effectiveness")


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def ensure_layout(root: Path) -> None:
    for name in (
        "domains",
        "candidates",
        "source_dossiers",
        "promotion_audits",
        "experts",
        "councils",
        "scoring_reports",
        "build_logs",
        "gap_analyses",
    ):
        (root / name).mkdir(parents=True, exist_ok=True)


def init_root(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    domain_id = slugify(args.domain)
    domain_path = root / "domains" / f"{domain_id}.json"
    if not domain_path.exists():
        write_json(
            domain_path,
            {
                "id": domain_id,
                "name": args.domain,
                "topic": args.topic or args.domain,
                "created_at": now_iso(),
                "updated_at": now_iso(),
                "coverage_axes": [],
                "active_experts": [],
                "candidate_experts": [],
            },
        )
    rebuild_index(root)
    state_path = root / "pipeline_state.json"
    if not state_path.exists():
        init_pipeline_state(root, domain_id, "", max_iterations=10)
    print(f"Initialized expert forum root: {root}")


def add_candidate(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    expert_id = args.expert_id or slugify(args.name)
    payload = {
        "id": expert_id,
        "name": args.name,
        "domain": slugify(args.domain),
        "reason": args.reason or "",
        "status": "candidate",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    write_json(root / "candidates" / f"{expert_id}.json", payload)
    print(f"Queued candidate: {expert_id}")


def add_source(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    expert_id = args.expert_id
    dossier_path = root / "source_dossiers" / f"{expert_id}.json"
    dossier = read_json(
        dossier_path,
        {
            "expert_id": expert_id,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "sources": [],
        },
    )
    source_id = args.source_id or slugify(f"{expert_id}-{args.tier.upper()}-{args.title}")[:80]
    source = {
        "id": source_id,
        "title": args.title,
        "url": args.url,
        "tier": args.tier.upper(),
        "note": args.note or "",
        "added_at": now_iso(),
    }
    dossier["sources"] = [item for item in dossier.get("sources", []) if item.get("id") != source_id]
    dossier["sources"].append(source)
    dossier["updated_at"] = now_iso()
    write_json(dossier_path, dossier)
    print(f"Added Tier {source['tier']} source for {expert_id}: {source_id}")


def audit_candidate(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    dossier_path = root / "source_dossiers" / f"{args.expert_id}.json"
    dossier = read_json(dossier_path, {"expert_id": args.expert_id, "sources": []})
    counts = {"A": 0, "B": 0, "C": 0}
    for source in dossier.get("sources", []):
        tier = str(source.get("tier", "")).upper()
        if tier in counts:
            counts[tier] += 1
    blockers: list[str] = []
    if counts["A"] < 1:
        blockers.append("missing_tier_a_source")
    if counts["B"] < 1:
        blockers.append("missing_tier_b_source")
    promotion_allowed = not blockers
    weighted_score = round(min(1.0, (counts["A"] * 0.45) + (counts["B"] * 0.3) + min(counts["C"], 2) * 0.05), 3)
    audit = {
        "expert_id": args.expert_id,
        "generated_at": now_iso(),
        "promotion_status": "promotion_allowed" if promotion_allowed else "blocked",
        "promotion_allowed": promotion_allowed,
        "blockers": blockers,
        "source_counts": counts,
        "source_confidence": {
            "level": "high" if weighted_score >= 0.75 else "medium" if weighted_score >= 0.45 else "low",
            "weighted_score": weighted_score,
            "rationale": "Computed from source-tier coverage; human review should still check claim-source alignment.",
        },
        "tier_c_core_claim_allowed": False,
    }
    write_json(root / "promotion_audits" / f"{args.expert_id}.json", audit)
    print(json.dumps(audit, indent=2, ensure_ascii=False))


def write_profile_skeleton(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    audit = read_json(root / "promotion_audits" / f"{args.expert_id}.json", {})
    if not audit.get("promotion_allowed") and not args.allow_unpromoted:
        raise SystemExit(
            f"Candidate {args.expert_id} has not passed promotion audit. "
            "Run audit or pass --allow-unpromoted for a candidate skeleton."
        )
    dossier = read_json(root / "source_dossiers" / f"{args.expert_id}.json", {"sources": []})
    source_refs = [source.get("id") for source in dossier.get("sources", []) if source.get("id")]
    profile = {
        "id": args.expert_id,
        "name": args.name,
        "domains": [slugify(args.domain)],
        "roles": ["domain_reviewer"],
        "routing_keywords": [],
        "bio_arc": "",
        "canonical_works": [],
        "signature_ideas": [],
        "reasoning_kernel": {
            "core_questions": [],
            "decision_rules": [],
            "failure_taxonomy": [],
            "preferred_abstractions": [],
        },
        "preferred_evidence": [],
        "critique_style": [],
        "blind_spots": [],
        "advantage_knowledge_base": {
            "canonical_concepts": [],
            "favorite_benchmarks": [],
            "known_debates": [],
            "anti_patterns": [],
        },
        "question_playbook": [],
        "domain_relevance": {
            "summary": "",
            "best_used_for": [],
            "avoid_using_for": [],
        },
        "quote_bank": [],
        "source_refs": source_refs,
        "source_confidence": audit.get("source_confidence", {"level": "low", "weighted_score": 0, "rationale": ""}),
        "freshness": {
            "status": "mixed",
            "last_checked": now_iso()[:10],
            "notes": "Skeleton generated; fill from source dossier before active use.",
        },
        "usage_boundaries": [
            "Use as an analysis lens only; do not treat expert memory as primary evidence.",
            "Do not imitate private personality or fabricate beliefs.",
        ],
    }
    expert_root = root / "experts" / args.expert_id
    write_json(expert_root / "profile.json", profile)
    write_text(
        expert_root / "distillate.md",
        f"# {args.name}\n\n"
        "## Public Evidence Base\n\n"
        f"- Fill from `source_dossiers/{args.expert_id}.json`.\n\n"
        "## Career And Idea Arc\n\n"
        "TODO\n\n"
        "## Signature Reasoning Kernel\n\n"
        "TODO\n\n"
        "## What This Expert Will Catch\n\n"
        "TODO\n\n"
        "## What This Expert May Miss\n\n"
        "TODO\n\n"
        "## Best Routing Situations\n\n"
        "TODO\n\n"
        "## Source Notes And Freshness\n\n"
        "TODO\n",
    )
    rebuild_index(root)
    print(f"Wrote profile skeleton: {expert_root / 'profile.json'}")


def rebuild_index(root: Path) -> dict[str, Any]:
    ensure_layout(root)
    domains = sorted(path.stem for path in (root / "domains").glob("*.json"))
    candidates = sorted(path.stem for path in (root / "candidates").glob("*.json"))
    experts: list[dict[str, Any]] = []
    for profile_path in sorted((root / "experts").glob("*/profile.json")):
        profile = read_json(profile_path, {})
        experts.append(
            {
                "id": profile.get("id", profile_path.parent.name),
                "name": profile.get("name", profile_path.parent.name),
                "domains": profile.get("domains", []),
                "roles": profile.get("roles", []),
                "source_confidence": profile.get("source_confidence", {}),
                "freshness": profile.get("freshness", {}),
            }
        )
    index = {
        "version": "expert_forum_index_v1",
        "generated_at": now_iso(),
        "domains": domains,
        "candidate_count": len(candidates),
        "expert_count": len(experts),
        "experts": experts,
    }
    write_json(root / "forum_index.json", index)
    return index


def index_root(args: argparse.Namespace) -> None:
    index = rebuild_index(args.root.expanduser())
    print(json.dumps(index, indent=2, ensure_ascii=False))


def validate_root(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    errors: list[str] = []
    warnings: list[str] = []
    for profile_path in sorted((root / "experts").glob("*/profile.json")):
        profile = read_json(profile_path, {})
        missing = sorted(REQUIRED_PROFILE_FIELDS - set(profile))
        if missing:
            errors.append(f"{profile_path}: missing fields {', '.join(missing)}")
        source_confidence = profile.get("source_confidence", {})
        if args.strict and source_confidence.get("level") == "low":
            warnings.append(f"{profile_path}: low source confidence")
        source_refs = profile.get("source_refs", [])
        if args.strict and not source_refs:
            errors.append(f"{profile_path}: no source_refs")
    result = {
        "status": "failed" if errors else "passed",
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# New commands: discover, fill, council, score, coverage, refresh, build, report
# ---------------------------------------------------------------------------


def weighted_median(values: list[float], weights: list[float]) -> float:
    """Compute the weighted median of values given weights."""
    if not values:
        return 0.0
    pairs = sorted(zip(values, weights), key=lambda p: p[0])
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    cumulative = 0.0
    for value, weight in pairs:
        cumulative += weight
        if cumulative >= total_weight / 2:
            return value
    return pairs[-1][0]


def clamp_score(value: float) -> int:
    return max(0, min(25, int(value)))


def find_project_root(path: Path) -> Path:
    start = path if path.is_dir() else path.parent
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def read_text_file(path: Path, max_chars: int = 250_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def collect_artifact(path_value: str | None) -> dict[str, Any]:
    """Collect lightweight artifact signals for standalone scoring.

    The CLI cannot run an LLM council by itself, so it uses transparent,
    reproducible signals: sections, tables, stats, manifests, tests, references,
    limitations, and claim-boundary language. This makes the command usable
    outside SKILL mode while keeping the report auditable.
    """
    if not path_value:
        return {
            "path": "",
            "exists": False,
            "project_root": str(Path.cwd()),
            "text": "",
            "files": [],
            "word_count": 0,
            "line_count": 0,
        }

    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    project_root = find_project_root(path) if path.exists() else Path.cwd()

    files: list[Path] = []
    text_parts: list[str] = []
    if path.is_file():
        files = [path]
        text_parts.append(read_text_file(path))
    elif path.is_dir():
        suffixes = {".md", ".txt", ".json", ".csv", ".py", ".toml", ".yaml", ".yml"}
        for file_path in sorted(path.rglob("*")):
            if file_path.is_file():
                files.append(file_path)
                if file_path.suffix.lower() in suffixes and sum(len(t) for t in text_parts) < 350_000:
                    text_parts.append(read_text_file(file_path, max_chars=80_000))

    text = "\n".join(text_parts)
    return {
        "path": str(path),
        "exists": path.exists(),
        "project_root": str(project_root),
        "text": text,
        "files": [str(file_path) for file_path in files],
        "word_count": len(re.findall(r"\w+", text)),
        "line_count": text.count("\n") + 1 if text else 0,
    }


def text_has(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def count_regex(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def sentence_overclaim_count(text: str) -> int:
    """Count unsupported-looking overclaim sentences.

    Rejected or negated claims are not counted; this is intentionally simple and
    auditable rather than semantically magical.
    """
    bad = 0
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        lowered = re.sub(r"\s+", " ", sentence.lower())
        if "|" in sentence:
            continue
        if not any(term in lowered for term in ("universal", "universally", "generally better", "semantic correctness", "semantic-correctness", "architecture-level")):
            continue
        if any(
            marker in lowered
            for marker in (
                "not ",
                "no ",
                "rejected",
                "does not",
                "do not",
                "future",
                "limitation",
                "separate",
                "separates",
                "blocked",
                "outside",
                "rather than",
                "claim ledger",
            )
        ):
            continue
        bad += 1
    return bad


def artifact_signals(artifact: dict[str, Any], root: Path, domain: dict[str, Any]) -> dict[str, Any]:
    text = artifact["text"]
    project_root = Path(artifact["project_root"])
    files = [Path(item) for item in artifact["files"]]
    file_names = " ".join(str(path.relative_to(project_root)) if path.is_absolute() and project_root in path.parents else str(path) for path in files)
    lower_text = text.lower()
    readme_text = read_text_file(project_root / "README.md", max_chars=80_000)
    companion_text = text + "\n" + readme_text
    companion_lower = companion_text.lower()
    coverage_axes = domain.get("coverage_axes", [])

    signals = {
        "exists": artifact["exists"],
        "word_count": artifact["word_count"],
        "section_count": count_regex(text, r"^#{1,3}\s+"),
        "table_count": count_regex(text, r"^\|.*\|$"),
        "numeric_count": count_regex(text, r"\b\d+(?:\.\d+)?\s*(?:%|pp|/|records|tasks|models|modes)?\b"),
        "has_abstract": "## abstract" in lower_text or re.search(r"^# .+\n\n## Abstract", text, re.I | re.M) is not None,
        "has_introduction": "introduction" in lower_text,
        "has_related_work": "related work" in lower_text or "positioning" in lower_text,
        "has_method": text_has(text, ["method", "study design", "data", "outcomes", "compared arms"]),
        "has_results": "results" in lower_text,
        "has_discussion": "discussion" in lower_text,
        "has_limitations": "limitations" in lower_text,
        "has_conclusion": "conclusion" in lower_text,
        "has_references": "references" in lower_text or "bibliography" in lower_text,
        "has_data_availability": "data availability" in lower_text or "artifact availability" in lower_text or "asset traceability" in lower_text,
        "has_claim_ledger": "claim ledger" in lower_text or "claim_support" in lower_text or "claim-support" in lower_text,
        "has_semantic_oracle_boundary": text_has(text, ["semantic oracle", "semantic correctness remains", "not semantic-correctness evidence", "future semantic"]),
        "has_uncertainty": text_has(text, ["confidence interval", "interval", "wilson", "p-value", "discordance", "mcnemar"]),
        "has_paired_analysis": text_has(text, ["paired", "discordance", "csl-only", "direct-only"]),
        "has_failure_taxonomy": "failure taxonomy" in lower_text or "failure-stage" in lower_text,
        "has_token_cap": text_has(text, ["token", "cap-hit", "truncation"]),
        "has_full_matrix": "18-row" in lower_text or count_regex(text, r"^\| `[^`]+` \| `(?:default|think|no_think)` \|") >= 12,
        "has_figures": ".svg" in lower_text or "figure 1" in lower_text,
        "has_tests": "pytest" in companion_lower or "tests/" in file_names or any("test" in path.name.lower() for path in files) or (project_root / "tests").exists(),
        "has_scripts": "analysis/" in file_names or any(path.suffix == ".py" for path in files) or (project_root / "analysis").exists() or (project_root / "semantic_oracle").exists(),
        "has_manifest": "manifest" in companion_lower or (project_root / "clean_research_assets" / "MANIFEST.csv").exists(),
        "has_clean_assets": "clean_research_assets" in companion_lower or (project_root / "clean_research_assets").exists(),
        "has_repro_commands": "python3 " in companion_text or "pytest" in companion_text or "reproduce" in companion_lower,
        "coverage_axes_mentioned": sum(
            1
            for axis in coverage_axes
            if axis.lower().replace("-", " ") in lower_text
            or axis.lower() in lower_text
            or all(part in lower_text for part in axis.lower().split("-"))
        ),
        "coverage_axes_total": len(coverage_axes),
        "overclaim_count": sentence_overclaim_count(text),
        "placeholder_count": text.count("TODO") + text.lower().count("should use"),
    }
    return signals


def axis_score(axis: str, signals: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    evidence: list[str] = []
    gaps: list[str] = []
    score = 0

    if not signals["exists"]:
        return 0, [], ["Artifact path does not exist"]

    if axis == "breadth":
        checks = [
            ("abstract", signals["has_abstract"]),
            ("introduction", signals["has_introduction"]),
            ("related work / positioning", signals["has_related_work"]),
            ("method or study design", signals["has_method"]),
            ("results", signals["has_results"]),
            ("discussion", signals["has_discussion"]),
            ("limitations", signals["has_limitations"]),
            ("conclusion", signals["has_conclusion"]),
            ("claim ledger", signals["has_claim_ledger"]),
            ("semantic-oracle boundary", signals["has_semantic_oracle_boundary"]),
            ("artifact/data availability", signals["has_data_availability"]),
            ("references", signals["has_references"]),
        ]
        score = 10 + sum(1 for _, ok in checks if ok)
        if signals["coverage_axes_total"]:
            score += min(3, round(3 * signals["coverage_axes_mentioned"] / signals["coverage_axes_total"]))
            evidence.append(f"Mentions {signals['coverage_axes_mentioned']}/{signals['coverage_axes_total']} domain coverage axes")
        for name, ok in checks:
            if ok:
                evidence.append(f"Includes {name}")
            else:
                gaps.append(f"Missing {name}")

    elif axis == "depth":
        checks = [
            ("sample sizes and numeric results", signals["numeric_count"] >= 20),
            ("uncertainty reporting", signals["has_uncertainty"]),
            ("paired analysis", signals["has_paired_analysis"]),
            ("full matrix or broad subgroup accounting", signals["has_full_matrix"]),
            ("task/failure heterogeneity", signals["has_failure_taxonomy"]),
            ("token/cap diagnostics", signals["has_token_cap"]),
            ("tables", signals["table_count"] >= 3),
            ("limitations tied to evidence", signals["has_limitations"] and signals["has_semantic_oracle_boundary"]),
        ]
        score = 9 + 2 * sum(1 for _, ok in checks if ok)
        for name, ok in checks:
            if ok:
                evidence.append(f"Has {name}")
            else:
                gaps.append(f"Needs {name}")

    elif axis == "thickness":
        checks = [
            ("clean asset package", signals["has_clean_assets"]),
            ("manifest", signals["has_manifest"]),
            ("scripts or implementation files", signals["has_scripts"]),
            ("tests or verification commands", signals["has_tests"]),
            ("reproducibility commands", signals["has_repro_commands"]),
            ("figure assets", signals["has_figures"]),
            ("claim discipline", signals["has_claim_ledger"]),
            ("no placeholders", signals["placeholder_count"] == 0),
        ]
        score = 9 + 2 * sum(1 for _, ok in checks if ok)
        for name, ok in checks:
            if ok:
                evidence.append(f"Includes {name}")
            else:
                gaps.append(f"Missing or weak: {name}")

    elif axis == "effectiveness":
        checks = [
            ("answers the research question", signals["has_abstract"] and signals["has_conclusion"]),
            ("main claim bounded", signals["has_claim_ledger"] and signals["overclaim_count"] == 0),
            ("semantic correctness separated", signals["has_semantic_oracle_boundary"]),
            ("results support narrative", signals["has_results"] and signals["has_uncertainty"]),
            ("reader can trace artifacts", signals["has_data_availability"] and signals["has_manifest"]),
            ("submission-like completeness", signals["has_references"] and signals["has_related_work"]),
            ("polished surface", signals["placeholder_count"] == 0 and signals["word_count"] >= 1800),
        ]
        score = 11 + 2 * sum(1 for _, ok in checks if ok)
        for name, ok in checks:
            if ok:
                evidence.append(f"Artifact {name}")
            else:
                gaps.append(f"Artifact does not yet {name}")
        if signals["overclaim_count"]:
            score -= min(5, signals["overclaim_count"])
            gaps.append(f"Potential overclaim sentences: {signals['overclaim_count']}")

    return clamp_score(score), evidence, gaps


def expert_vote(axis: str, base: int, profile: dict[str, Any], signals: dict[str, Any]) -> int:
    eid = profile.get("id", "")
    vote = base
    if eid == "controlled-natural-language":
        if axis in ("breadth", "effectiveness") and signals["has_semantic_oracle_boundary"]:
            vote += 1
        if signals["overclaim_count"]:
            vote -= 2
    elif eid == "dsl-language-engineering":
        if axis in ("depth", "thickness") and text_has(profile.get("domain_relevance", {}).get("summary", ""), ["DSL"]):
            vote += 0
        if axis in ("depth", "effectiveness") and not signals["has_method"]:
            vote -= 2
    elif eid == "llm-code-evaluation":
        if axis == "depth" and not signals["has_paired_analysis"]:
            vote -= 3
        if axis == "effectiveness" and not signals["has_semantic_oracle_boundary"]:
            vote -= 2
    elif eid == "program-synthesis-verification":
        if axis == "effectiveness" and signals["has_semantic_oracle_boundary"]:
            vote += 1
        if axis == "effectiveness" and "semantic" in signals and not signals["has_semantic_oracle_boundary"]:
            vote -= 3
    elif eid == "statistical-analysis":
        if axis == "depth" and signals["has_uncertainty"] and signals["has_paired_analysis"]:
            vote += 1
        if axis == "depth" and not signals["has_full_matrix"]:
            vote -= 2
    elif eid == "reproducibility-governance":
        if axis == "thickness" and signals["has_manifest"] and signals["has_clean_assets"]:
            vote += 1
        if axis in ("breadth", "effectiveness") and not signals["has_data_availability"]:
            vote -= 2
    return clamp_score(vote)


def normalized_council_weights(root: Path, council: dict[str, Any]) -> tuple[list[dict[str, Any]], list[float]]:
    members: list[dict[str, Any]] = []
    weights: list[float] = []
    for member in council.get("members", []):
        profile = read_json(root / "experts" / member.get("expert_id", "") / "profile.json", {})
        source_weight = float(profile.get("source_confidence", {}).get("weighted_score", 0.5) or 0.5)
        role_multiplier = {"chair": 1.5, "reviewer": 1.2, "advocate": 1.0, "skeptic": 1.0, "overclaim-skeptic": 1.1}.get(member.get("role", ""), 1.0)
        weight = float(member.get("weight", 0.1) or 0.1) * source_weight * role_multiplier
        members.append({"member": member, "profile": profile})
        weights.append(weight)
    total = sum(weights)
    if total <= 0 and weights:
        weights = [1 / len(weights)] * len(weights)
    elif total > 0:
        weights = [w / total for w in weights]
    return members, weights


def load_pipeline_state(root: Path) -> dict[str, Any]:
    return read_json(root / "pipeline_state.json", {})


def save_pipeline_state(root: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    write_json(root / "pipeline_state.json", state)


def init_pipeline_state(root: Path, domain: str, target_repo: str, max_iterations: int) -> dict[str, Any]:
    state = {
        "domain": domain,
        "current_phase": "init",
        "iteration": 0,
        "max_iterations": max_iterations,
        "last_score": {"total": 0, "breadth": 0, "depth": 0, "thickness": 0, "effectiveness": 0},
        "status": "running",
        "started_at": now_iso(),
        "updated_at": now_iso(),
        "target_repo": target_repo,
        "github_branch": f"council-pilot/{domain}",
        "active_council": "",
        "experts_added_mid_loop": [],
        "history": [],
        "build_failures": 0,
        "score_regressions": 0,
    }
    save_pipeline_state(root, state)
    return state


# --- discover ---------------------------------------------------------------


def discover_experts(args: argparse.Namespace) -> None:
    """Discover expert candidates. In standalone mode reads from --from-file."""
    root = args.root.expanduser()
    ensure_layout(root)
    domain_id = slugify(args.domain)

    if args.from_file:
        candidates_data = read_json(Path(args.from_file), {"candidates": []})
    else:
        print(json.dumps({
            "status": "standalone_mode",
            "message": (
                "In standalone mode, provide --from-file with a JSON file containing "
                "a 'candidates' array. Each entry: {name, reason, sources: [{title, url, tier, note}]}. "
                "Under SKILL mode, the skill handles web search directly."
            ),
        }, indent=2))
        return

    discovered: list[str] = []
    for entry in candidates_data.get("candidates", []):
        expert_id = slugify(entry.get("name", ""))
        if not expert_id:
            continue
        candidate_payload = {
            "id": expert_id,
            "name": entry.get("name", ""),
            "domain": domain_id,
            "reason": entry.get("reason", ""),
            "status": "auto_discovered",
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        write_json(root / "candidates" / f"{expert_id}.json", candidate_payload)

        dossier: dict[str, Any] = {
            "expert_id": expert_id,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "sources": [],
        }
        for src in entry.get("sources", []):
            tier = str(src.get("tier", "C")).upper()
            source_id = slugify(f"{expert_id}-{tier}-{src.get('title', '')}")[:80]
            dossier["sources"].append({
                "id": source_id,
                "title": src.get("title", ""),
                "url": src.get("url", ""),
                "tier": tier,
                "note": src.get("note", ""),
                "added_at": now_iso(),
            })
        write_json(root / "source_dossiers" / f"{expert_id}.json", dossier)
        discovered.append(expert_id)

    rebuild_index(root)
    result = {"status": "discovered", "count": len(discovered), "experts": discovered}
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- fill -------------------------------------------------------------------


def fill_profile(args: argparse.Namespace) -> None:
    """Output a structured fill prompt for an expert profile. SKILL mode handles LLM calls."""
    root = args.root.expanduser()
    expert_id = args.expert_id
    profile_path = root / "experts" / expert_id / "profile.json"
    profile = read_json(profile_path, None)
    if profile is None:
        raise SystemExit(f"No profile found for {expert_id}. Run 'profile' first.")

    dossier = read_json(root / "source_dossiers" / f"{expert_id}.json", {"sources": []})
    audit = read_json(root / "promotion_audits" / f"{expert_id}.json", {})

    empty_fields = [k for k in REQUIRED_PROFILE_FIELDS if not profile.get(k)]
    if isinstance(profile.get("bio_arc"), str) and profile["bio_arc"] == "":
        empty_fields.append("bio_arc (empty string)")
    if isinstance(profile.get("reasoning_kernel"), dict):
        rk = profile["reasoning_kernel"]
        if all(not rk.get(k) for k in ("core_questions", "decision_rules", "failure_taxonomy", "preferred_abstractions")):
            empty_fields.append("reasoning_kernel (all sub-fields empty)")

    fill_prompt = {
        "expert_id": expert_id,
        "promotion_allowed": audit.get("promotion_allowed", False),
        "source_count": len(dossier.get("sources", [])),
        "sources_by_tier": {},
        "empty_fields": empty_fields,
        "instructions": (
            "Fill each empty field using source content. Follow references/profile-contract.md. "
            "Tier C sources cannot define bio_arc, signature_ideas, critique_style, or quote_bank. "
            "Preserve source disagreements rather than smoothing them away."
        ),
    }
    for src in dossier.get("sources", []):
        tier = src.get("tier", "?")
        fill_prompt["sources_by_tier"].setdefault(tier, []).append({
            "id": src.get("id"),
            "title": src.get("title"),
            "url": src.get("url"),
        })

    if args.dry_run:
        print(json.dumps(fill_prompt, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({
            "status": "fill_required",
            "message": (
                "In standalone mode, use --dry-run to see the fill prompt. "
                "Under SKILL mode, the skill handles LLM-driven filling directly."
            ),
            "empty_field_count": len(empty_fields),
        }, indent=2, ensure_ascii=False))


# --- council ----------------------------------------------------------------


def _auto_assign_roles(members_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Auto-assign council roles based on expert profile strengths."""
    role_scores: dict[str, dict[str, float]] = {}
    for m in members_data:
        eid = m["expert_id"]
        profile = m.get("_profile", {})
        sc = profile.get("source_confidence", {}).get("weighted_score", 0)
        rk_count = sum(len(v) for v in profile.get("reasoning_kernel", {}).values() if isinstance(v, list))
        critique_count = len(profile.get("critique_style", []))
        works_count = len(profile.get("canonical_works", []))
        blindspot_count = len(profile.get("blind_spots", []))
        keywords_count = len(profile.get("routing_keywords", []))

        role_scores[eid] = {
            "chair": sc * 0.4 + keywords_count * 0.3 + rk_count * 0.3,
            "reviewer": critique_count * 0.5 + rk_count * 0.3 + sc * 0.2,
            "advocate": works_count * 0.5 + rk_count * 0.3 + sc * 0.2,
            "skeptic": blindspot_count * 0.5 + critique_count * 0.3 + sc * 0.2,
        }

    assigned: dict[str, str] = {}
    for role in ("chair", "skeptic", "reviewer", "advocate"):
        best_eid = ""
        best_score = -1.0
        for eid, scores in role_scores.items():
            if eid in assigned:
                continue
            if scores[role] > best_score:
                best_score = scores[role]
                best_eid = eid
        if best_eid:
            assigned[best_eid] = role

    result: list[dict[str, Any]] = []
    n = len(members_data)
    base_weight = round(min(0.3, 1.0 / max(n, 1)), 3)
    for m in members_data:
        eid = m["expert_id"]
        role = assigned.get(eid, "reviewer")
        multiplier = {"chair": 1.5, "reviewer": 1.2, "advocate": 1.0, "skeptic": 1.0}.get(role, 1.0)
        result.append({
            "expert_id": eid,
            "role": role,
            "weight": round(min(0.3, base_weight * multiplier), 3),
            "joined_at": now_iso(),
            "fast_tracked": m.get("fast_tracked", False),
        })
    return result


def council_create(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    domain_id = slugify(args.domain)
    council_id = slugify(args.name) if args.name else f"{domain_id}-main"

    expert_ids = args.experts.split(",") if args.experts else []
    if not expert_ids:
        for p in sorted((root / "experts").glob("*/profile.json")):
            expert_ids.append(p.parent.name)

    if len(expert_ids) < 2:
        raise SystemExit("Council needs at least 2 experts. Discover and promote more experts first.")

    members_data: list[dict[str, Any]] = []
    routing_rules: list[dict[str, Any]] = []
    all_keywords: dict[str, list[str]] = {}

    for eid in expert_ids:
        profile = read_json(root / "experts" / eid / "profile.json", {})
        members_data.append({"expert_id": eid, "_profile": profile, "fast_tracked": False})
        for kw in profile.get("routing_keywords", []):
            all_keywords.setdefault(kw, []).append(eid)

    for kw, eids in all_keywords.items():
        routing_rules.append({"keyword": kw, "expert_ids": eids})

    members = _auto_assign_roles(members_data)

    council = {
        "id": council_id,
        "name": args.name or council_id,
        "domain": domain_id,
        "members": members,
        "routing_rules": routing_rules,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "scoring_history_refs": [],
    }
    write_json(root / "councils" / f"{council_id}.json", council)

    state = load_pipeline_state(root)
    state["active_council"] = council_id
    save_pipeline_state(root, state)

    print(json.dumps({"status": "created", "council_id": council_id, "members": members}, indent=2, ensure_ascii=False))


def council_add_member(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    council_path = root / "councils" / f"{args.council_id}.json"
    council = read_json(council_path, None)
    if council is None:
        raise SystemExit(f"Council {args.council_id} not found.")

    existing = {m["expert_id"] for m in council.get("members", [])}
    if args.expert_id in existing:
        raise SystemExit(f"Expert {args.expert_id} already in council.")
    if len(existing) >= 10:
        raise SystemExit("Council size limit (10) reached. Split into sub-councils or remove a member.")

    profile = read_json(root / "experts" / args.expert_id / "profile.json", {})
    role = args.role or "reviewer"
    n = len(council["members"]) + 1
    base_weight = round(min(0.3, 1.0 / n), 3)
    multiplier = {"chair": 1.5, "reviewer": 1.2, "advocate": 1.0, "skeptic": 1.0}.get(role, 1.0)

    new_member = {
        "expert_id": args.expert_id,
        "role": role,
        "weight": round(min(0.3, base_weight * multiplier), 3),
        "joined_at": now_iso(),
        "fast_tracked": args.fast_track,
    }
    council["members"].append(new_member)

    for kw in profile.get("routing_keywords", []):
        found = False
        for rule in council.get("routing_rules", []):
            if rule["keyword"] == kw:
                rule["expert_ids"].append(args.expert_id)
                found = True
                break
        if not found:
            council.setdefault("routing_rules", []).append({"keyword": kw, "expert_ids": [args.expert_id]})

    total_weight = sum(m["weight"] for m in council["members"])
    if total_weight > 0:
        for m in council["members"]:
            m["weight"] = round(m["weight"] / total_weight, 3)

    council["updated_at"] = now_iso()
    write_json(council_path, council)
    print(json.dumps({"status": "member_added", "council_id": args.council_id, "member": new_member}, indent=2, ensure_ascii=False))


def council_list(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    councils: list[dict[str, Any]] = []
    for path in sorted((root / "councils").glob("*.json")):
        c = read_json(path, {})
        councils.append({"id": c.get("id", path.stem), "name": c.get("name", ""), "members": len(c.get("members", [])), "domain": c.get("domain", "")})
    print(json.dumps(councils, indent=2, ensure_ascii=False))


def council_show(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    council = read_json(root / "councils" / f"{args.council_id}.json", None)
    if council is None:
        raise SystemExit(f"Council {args.council_id} not found.")
    print(json.dumps(council, indent=2, ensure_ascii=False))


def manage_council(args: argparse.Namespace) -> None:
    action = args.council_action
    if action == "create":
        council_create(args)
    elif action == "add-member":
        council_add_member(args)
    elif action == "list":
        council_list(args)
    elif action == "show":
        council_show(args)
    else:
        raise SystemExit(f"Unknown council action: {action}")


# --- score ------------------------------------------------------------------


def score_artifact(args: argparse.Namespace) -> None:
    """Score an artifact against the expert council."""
    root = args.root.expanduser()
    domain_id = slugify(args.domain)
    ensure_layout(root)

    state = load_pipeline_state(root)
    council_id = args.council_id or state.get("active_council", "")
    if not council_id:
        raise SystemExit("No active council. Run 'council create' first.")

    council = read_json(root / "councils" / f"{council_id}.json", None)
    if council is None:
        raise SystemExit(f"Council {council_id} not found.")

    iteration = state.get("iteration", 0) + 1
    domain = read_json(root / "domains" / f"{domain_id}.json", {})
    artifact = collect_artifact(args.artifact)
    signals = artifact_signals(artifact, root, domain)
    members, weights = normalized_council_weights(root, council)

    axes: list[dict[str, Any]] = []
    for axis in SCORING_AXES:
        base_score, evidence, gaps = axis_score(axis, signals)
        votes: dict[str, int] = {}
        vote_values: list[float] = []
        for item in members:
            profile = item["profile"]
            expert_id = profile.get("id") or item["member"].get("expert_id", "")
            vote = expert_vote(axis, base_score, profile, signals)
            votes[expert_id] = vote
            vote_values.append(vote)
        final_score = clamp_score(weighted_median(vote_values, weights) if vote_values else base_score)
        axes.append({
            "axis": axis,
            "score": final_score,
            "base_score": base_score,
            "evidence": evidence,
            "gaps": gaps,
            "expert_votes": votes,
            "weighted_median": final_score,
        })

    total = sum(axis["score"] for axis in axes)
    verdict = "converged" if total == 100 else "needs_work"
    recommendations: list[str] = []
    for axis in axes:
        for gap in axis["gaps"][:3]:
            if gap not in recommendations:
                recommendations.append(f"{axis['axis']}: {gap}")
    if signals["placeholder_count"]:
        recommendations.insert(0, "Remove placeholder language such as TODO or 'should use'.")
    if signals["overclaim_count"]:
        recommendations.insert(0, "Rewrite potential overclaim sentences or mark them explicitly as rejected/limitations.")
    if not recommendations:
        recommendations.append("Artifact satisfies the standalone scoring checks; use SKILL-mode council review for any remaining qualitative polish.")

    report = {
        "domain": domain_id,
        "artifact_path": args.artifact or "",
        "iteration": iteration,
        "council_id": council_id,
        "mode": "standalone-real-score",
        "artifact_signals": {
            key: signals[key]
            for key in sorted(signals)
            if key not in {"text"}
        },
        "axes": axes,
        "score": {
            "total": total,
            **{axis["axis"]: axis["score"] for axis in axes},
        },
        "total": total,
        "verdict": verdict,
        "generated_at": now_iso(),
        "recommendations": recommendations[:12],
    }

    timestamp = now_iso().replace(":", "-").replace("T", "_").replace("Z", "")
    report_path = root / "scoring_reports" / f"{domain_id}_{timestamp}.json"
    write_json(report_path, report)

    state["iteration"] = iteration
    state["last_score"] = report["score"]
    state["current_phase"] = "score"
    state.setdefault("history", []).append({
        "iteration": iteration,
        "scores": report["score"],
        "action": f"score {args.artifact or '<baseline>'}",
        "report": str(report_path),
        "generated_at": report["generated_at"],
    })
    if verdict == "converged":
        state["status"] = "scored_converged"
    else:
        state["status"] = "needs_work"
    save_pipeline_state(root, state)

    council.setdefault("scoring_history_refs", []).append(str(report_path.relative_to(root)))
    council["updated_at"] = now_iso()
    write_json(root / "councils" / f"{council_id}.json", council)

    print(json.dumps(report, indent=2, ensure_ascii=False))


# --- coverage ---------------------------------------------------------------


def analyze_coverage(args: argparse.Namespace) -> None:
    """Analyze expert coverage gaps for a domain."""
    root = args.root.expanduser()
    domain_id = slugify(args.domain)
    ensure_layout(root)

    domain = read_json(root / "domains" / f"{domain_id}.json", {})
    coverage_axes = domain.get("coverage_axes", [])
    if not coverage_axes:
        coverage_axes = [domain.get("topic", domain_id)]

    expert_keywords: dict[str, set[str]] = {}
    expert_domains_map: dict[str, list[str]] = {}
    for profile_path in sorted((root / "experts").glob("*/profile.json")):
        profile = read_json(profile_path, {})
        eid = profile.get("id", profile_path.parent.name)
        expert_keywords[eid] = set(profile.get("routing_keywords", []))
        expert_domains_map[eid] = profile.get("domains", [])

    covered: set[str] = set()
    uncovered: set[str] = set()
    for axis in coverage_axes:
        axis_lower = axis.lower()
        is_covered = any(axis_lower in " ".join(kws).lower() for kws in expert_keywords.values())
        if is_covered:
            covered.add(axis)
        else:
            uncovered.add(axis)

    matrix: dict[str, dict[str, bool]] = {}
    for axis in coverage_axes:
        matrix[axis] = {}
        for eid, kws in expert_keywords.items():
            matrix[axis][eid] = axis.lower() in " ".join(kws).lower()

    result = {
        "domain": domain_id,
        "coverage_axes": coverage_axes,
        "expert_count": len(expert_keywords),
        "covered": sorted(covered),
        "uncovered": sorted(uncovered),
        "coverage_matrix": matrix,
        "recommendations": [
            f"Add expert for: {axis}" for axis in sorted(uncovered)
        ] if uncovered else ["Coverage looks good"],
        "generated_at": now_iso(),
    }

    timestamp = now_iso().replace(":", "-").replace("T", "_").replace("Z", "")
    write_json(root / "gap_analyses" / f"{domain_id}_{timestamp}.json", result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


# --- refresh ----------------------------------------------------------------


def refresh_sources(args: argparse.Namespace) -> None:
    """Check source freshness for expert profiles."""
    root = args.root.expanduser()
    ensure_layout(root)
    reports: list[dict[str, Any]] = []

    for dossier_path in sorted((root / "source_dossiers").glob("*.json")):
        dossier = read_json(dossier_path, {})
        expert_id = dossier.get("expert_id", dossier_path.stem)
        profile_path = root / "experts" / expert_id / "profile.json"
        if not profile_path.exists():
            continue

        profile = read_json(profile_path, {})
        freshness = profile.get("freshness", {})
        source_count = len(dossier.get("sources", []))
        last_checked = freshness.get("last_checked", "never")

        if args.stale_only and freshness.get("status") not in ("stale", "mixed"):
            continue

        reports.append({
            "expert_id": expert_id,
            "source_count": source_count,
            "freshness_status": freshness.get("status", "unknown"),
            "last_checked": last_checked,
            "needs_refresh": freshness.get("status") in ("stale", "mixed"),
        })

        if args.force:
            profile.setdefault("freshness", {})["status"] = "stale"
            profile["freshness"]["notes"] = "Force-refreshed; re-distill from sources."
            write_json(profile_path, profile)

    print(json.dumps({"status": "analyzed", "experts": reports, "total": len(reports)}, indent=2, ensure_ascii=False))


# --- build ------------------------------------------------------------------


def trigger_build(args: argparse.Namespace) -> None:
    """Record build context in pipeline state. Actual build runs in SKILL mode."""
    root = args.root.expanduser()
    ensure_layout(root)
    domain_id = slugify(args.domain)

    state = load_pipeline_state(root)
    state["current_phase"] = "build"
    state["domain"] = domain_id
    if args.target_repo:
        state["target_repo"] = args.target_repo
    save_pipeline_state(root, state)

    build_context = {
        "domain": domain_id,
        "council_id": state.get("active_council", ""),
        "iteration": state.get("iteration", 0),
        "last_score": state.get("last_score", {}),
        "target_repo": state.get("target_repo", ""),
        "build_command": args.build_command or "auto-detect",
        "generated_at": now_iso(),
    }

    timestamp = now_iso().replace(":", "-").replace("T", "_").replace("Z", "")
    write_json(root / "build_logs" / f"{domain_id}_{timestamp}_context.json", build_context)
    print(json.dumps(build_context, indent=2, ensure_ascii=False))


# --- report -----------------------------------------------------------------


def generate_report(args: argparse.Namespace) -> None:
    """Generate a comprehensive maturity report."""
    root = args.root.expanduser()
    domain_id = slugify(args.domain)

    state = load_pipeline_state(root)
    domain = read_json(root / "domains" / f"{domain_id}.json", {})
    council_id = state.get("active_council", "")
    council = read_json(root / "councils" / f"{council_id}.json", {})
    last_score = state.get("last_score", {})

    scoring_files = sorted((root / "scoring_reports").glob(f"{domain_id}_*.json"))
    latest_report = read_json(scoring_files[-1], {}) if scoring_files else {}

    experts_summary: list[dict[str, Any]] = []
    for member in council.get("members", []):
        eid = member.get("expert_id", "")
        profile = read_json(root / "experts" / eid / "profile.json", {})
        experts_summary.append({
            "id": eid,
            "role": member.get("role", ""),
            "confidence": profile.get("source_confidence", {}).get("level", "unknown"),
            "weight": member.get("weight", 0),
        })

    report_data = {
        "domain": domain_id,
        "domain_name": domain.get("name", domain_id),
        "topic": domain.get("topic", ""),
        "iteration": state.get("iteration", 0),
        "max_iterations": state.get("max_iterations", 10),
        "status": state.get("status", "unknown"),
        "started_at": state.get("started_at", ""),
        "updated_at": state.get("updated_at", ""),
        "scores": {
            "total": last_score.get("total", 0),
            "breadth": last_score.get("breadth", 0),
            "depth": last_score.get("depth", 0),
            "thickness": last_score.get("thickness", 0),
            "effectiveness": last_score.get("effectiveness", 0),
        },
        "council": {
            "id": council_id,
            "member_count": len(council.get("members", [])),
            "members": experts_summary,
        },
        "history": state.get("history", []),
        "latest_scoring_report": latest_report,
        "generated_at": now_iso(),
    }

    if args.format == "markdown":
        lines = [
            f"# Maturity Report: {domain.get('name', domain_id)}",
            "",
            f"**Domain**: {domain_id}",
            f"**Iteration**: {report_data['iteration']} / {report_data['max_iterations']}",
            f"**Status**: {report_data['status']}",
            "",
            "## Score Summary",
            "",
            "| Axis | Score | Max |",
            "|------|-------|-----|",
            f"| Breadth | {last_score.get('breadth', 0)} | 25 |",
            f"| Depth | {last_score.get('depth', 0)} | 25 |",
            f"| Thickness | {last_score.get('thickness', 0)} | 25 |",
            f"| Effectiveness | {last_score.get('effectiveness', 0)} | 25 |",
            f"| **Total** | **{last_score.get('total', 0)}** | **100** |",
            "",
            "## Expert Council",
            "",
            "| Expert | Role | Confidence | Weight |",
            "|--------|------|-----------|--------|",
        ]
        for e in experts_summary:
            lines.append(f"| {e['id']} | {e['role']} | {e['confidence']} | {e['weight']} |")
        lines.append("")

        # Iteration History
        history = state.get("history", [])
        if history:
            lines.append("## Iteration History")
            lines.append("")
            lines.append("| Iteration | Total | Breadth | Depth | Thickness | Effectiveness | Action |")
            lines.append("|-----------|-------|---------|-------|-----------|--------------|--------|")
            for entry in history:
                s = entry.get("scores", {})
                if not entry.get("action") and not s.get("total"):
                    continue
                lines.append(
                    f"| {entry.get('iteration', '?')} "
                    f"| {s.get('total', 0)} "
                    f"| {s.get('breadth', 0)} "
                    f"| {s.get('depth', 0)} "
                    f"| {s.get('thickness', 0)} "
                    f"| {s.get('effectiveness', 0)} "
                    f"| {entry.get('action', '')} |"
                )
            lines.append("")

        # Gaps from latest scoring report
        if latest_report:
            all_gaps: list[str] = []
            for ax in latest_report.get("axes", []):
                all_gaps.extend(ax.get("gaps", []))
            if all_gaps:
                lines.append("## Coverage Gaps")
                lines.append("")
                for gap in all_gaps[:10]:
                    lines.append(f"- {gap}")
                lines.append("")

            recs = latest_report.get("recommendations", [])
            if recs:
                lines.append("## Recommendations")
                lines.append("")
                for rec in recs:
                    lines.append(f"- {rec}")
                lines.append("")

        lines.append(f"Generated by Council Pilot at {now_iso()}")
        output = "\n".join(lines)
        if args.output:
            write_text(Path(args.output), output)
            print(f"Report written to {args.output}")
        else:
            print(output)
    else:
        if args.output:
            write_json(Path(args.output), report_data)
            print(f"Report written to {args.output}")
        else:
            print(json.dumps(report_data, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build source-gated expert forums for Codex skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- original commands ---

    init = subparsers.add_parser("init")
    init.add_argument("--root", type=Path, required=True)
    init.add_argument("--domain", required=True)
    init.add_argument("--topic")
    init.set_defaults(func=init_root)

    candidate = subparsers.add_parser("candidate")
    candidate.add_argument("--root", type=Path, required=True)
    candidate.add_argument("--domain", required=True)
    candidate.add_argument("--name", required=True)
    candidate.add_argument("--expert-id")
    candidate.add_argument("--reason")
    candidate.set_defaults(func=add_candidate)

    source = subparsers.add_parser("source")
    source.add_argument("--root", type=Path, required=True)
    source.add_argument("--expert-id", required=True)
    source.add_argument("--source-id")
    source.add_argument("--tier", choices=("A", "B", "C", "a", "b", "c"), required=True)
    source.add_argument("--title", required=True)
    source.add_argument("--url", required=True)
    source.add_argument("--note")
    source.set_defaults(func=add_source)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--root", type=Path, required=True)
    audit.add_argument("--expert-id", required=True)
    audit.set_defaults(func=audit_candidate)

    profile = subparsers.add_parser("profile")
    profile.add_argument("--root", type=Path, required=True)
    profile.add_argument("--domain", required=True)
    profile.add_argument("--expert-id", required=True)
    profile.add_argument("--name", required=True)
    profile.add_argument("--allow-unpromoted", action="store_true")
    profile.set_defaults(func=write_profile_skeleton)

    index = subparsers.add_parser("index")
    index.add_argument("--root", type=Path, required=True)
    index.set_defaults(func=index_root)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--root", type=Path, required=True)
    validate.add_argument("--strict", action="store_true")
    validate.set_defaults(func=validate_root)

    # --- new commands ---

    discover = subparsers.add_parser("discover", help="Discover expert candidates from file or SKILL mode")
    discover.add_argument("--root", type=Path, required=True)
    discover.add_argument("--domain", required=True)
    discover.add_argument("--from-file", help="JSON file with candidate data")
    discover.set_defaults(func=discover_experts)

    fill = subparsers.add_parser("fill", help="Output fill prompt for expert profile")
    fill.add_argument("--root", type=Path, required=True)
    fill.add_argument("--expert-id", required=True)
    fill.add_argument("--dry-run", action="store_true", help="Output fill prompt without modifying")
    fill.set_defaults(func=fill_profile)

    council = subparsers.add_parser("council", help="Manage expert councils")
    council_sub = council.add_subparsers(dest="council_action", required=True)

    council_create_p = council_sub.add_parser("create")
    council_create_p.add_argument("--root", type=Path, required=True)
    council_create_p.add_argument("--domain", required=True)
    council_create_p.add_argument("--name")
    council_create_p.add_argument("--experts", help="Comma-separated expert IDs (default: all)")
    council_create_p.set_defaults(func=manage_council, council_action="create")

    council_add = council_sub.add_parser("add-member")
    council_add.add_argument("--root", type=Path, required=True)
    council_add.add_argument("--council-id", required=True)
    council_add.add_argument("--expert-id", required=True)
    council_add.add_argument("--role", choices=("chair", "reviewer", "advocate", "skeptic"))
    council_add.add_argument("--fast-track", action="store_true")
    council_add.set_defaults(func=manage_council, council_action="add-member")

    council_list_p = council_sub.add_parser("list")
    council_list_p.add_argument("--root", type=Path, required=True)
    council_list_p.set_defaults(func=manage_council, council_action="list")

    council_show_p = council_sub.add_parser("show")
    council_show_p.add_argument("--root", type=Path, required=True)
    council_show_p.add_argument("--council-id", required=True)
    council_show_p.set_defaults(func=manage_council, council_action="show")

    score = subparsers.add_parser("score", help="Score artifact against expert council")
    score.add_argument("--root", type=Path, required=True)
    score.add_argument("--domain", required=True)
    score.add_argument("--artifact", help="Path to artifact to score")
    score.add_argument("--council-id")
    score.set_defaults(func=score_artifact)

    coverage = subparsers.add_parser("coverage", help="Analyze expert coverage gaps")
    coverage.add_argument("--root", type=Path, required=True)
    coverage.add_argument("--domain", required=True)
    coverage.set_defaults(func=analyze_coverage)

    refresh = subparsers.add_parser("refresh", help="Check source freshness")
    refresh.add_argument("--root", type=Path, required=True)
    refresh.add_argument("--stale-only", action="store_true")
    refresh.add_argument("--force", action="store_true", help="Force mark stale for re-distillation")
    refresh.set_defaults(func=refresh_sources)

    build = subparsers.add_parser("build", help="Record build context for SKILL mode")
    build.add_argument("--root", type=Path, required=True)
    build.add_argument("--domain", required=True)
    build.add_argument("--target-repo", help="Target repository path or URL")
    build.add_argument("--build-command", help="Build command override")
    build.set_defaults(func=trigger_build)

    report = subparsers.add_parser("report", help="Generate maturity report")
    report.add_argument("--root", type=Path, required=True)
    report.add_argument("--domain", required=True)
    report.add_argument("--format", choices=("json", "markdown"), default="json")
    report.add_argument("--output", help="Output file path")
    report.set_defaults(func=generate_report)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
