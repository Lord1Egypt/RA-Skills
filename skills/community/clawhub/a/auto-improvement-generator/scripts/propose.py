#!/usr/bin/env python3
"""Proposer for the first runnable generic-skill lane."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import (
    SCHEMA_VERSION,
    choose_doc_file,
    choose_guardrail_file,
    choose_reference_file,
    classify_feedback,
    compute_target_profile,
    expand_source,
    load_source_paths,
    normalize_target,
    protected_target,
    read_json,
    slugify,
    utc_now_iso,
    write_json,
)
from lib.state_machine import (
    DEFAULT_STATE_ROOT,
    ensure_tree,
    make_run_id,
    update_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Propose improvement candidates for generic-skill lane")
    parser.add_argument("--lane", default="generic-skill")
    parser.add_argument("--target", required=True, help="Target skill/file path")
    parser.add_argument("--source", action="append", default=[], help="Optional memory/learnings/.feedback source")
    parser.add_argument("--max-candidates", type=int, default=4)
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--trace", default=None, help="Path to a failure trace JSON from a previous run")
    return parser.parse_args()


def build_docs_candidate(target: Path, feedback_buckets: dict[str, list[str]], idx: int) -> dict | None:
    doc_file = choose_doc_file(target)
    if not doc_file:
        return None
    limitation_signal = feedback_buckets.get("limitations", [])
    example_signal = feedback_buckets.get("examples", [])
    rationale_parts = []
    if limitation_signal:
        rationale_parts.append("反馈提到用户会把 skill 误解为可直接执行/集成能力")
    if example_signal:
        rationale_parts.append("反馈提到 README/用法说明需要更明确的示例或边界")
    if not rationale_parts:
        rationale_parts.append("目标存在 Markdown 文档，可先做低风险文案补充来降低误用")
    lines = [
        "This skill is advisory/planning-oriented. It does not connect to external delivery platforms, schedule sends, or manage subscribers directly.",
        "When answering requests, keep the strategy inside the skill and explicitly call out when execution, analytics, or platform operations require a separate automation or operator workflow.",
    ]
    if example_signal:
        lines.append("For production usage, pair the skill with a separate execution lane/tool for actual publishing, scheduling, or analytics collection.")
    return {
        "id": f"cand-{idx:02d}-{slugify(doc_file.stem)}",
        "title": f"补充 {doc_file.name} 的执行边界说明",
        "target_path": str(doc_file),
        "category": "docs",
        "rationale": "；".join(rationale_parts),
        "risk_level": "low",
        "proposed_change_summary": "追加一个短的 operator note/limitations 补充段，明确这是策略型 skill，不直接代替外部执行工具。",
        "stage": "proposed",
        "source_refs": limitation_signal[:2] + example_signal[:1],
        "executor_support": True,
        "execution_plan": {
            "action": "append_markdown_section",
            "section_heading": "## Operator Notes",
            "content_lines": lines,
        },
    }


def build_reference_candidate(target: Path, feedback_buckets: dict[str, list[str]], idx: int) -> dict | None:
    reference_file = choose_reference_file(target)
    if not reference_file:
        return None
    workflow_signal = feedback_buckets.get("workflow", [])
    rationale = "反馈中提到执行流程/阶段推进需要更可见；references 目录适合补充 control-plane-friendly 说明。"
    lines = [
        "Stage artifacts should remain machine-readable so a later control plane can read current stage, truth anchor, and next owner without parsing free-form prose.",
        "Prefer explicit fields such as `stage`, `status`, `next_step`, `next_owner`, and `truth_anchor` in every receipt or state artifact.",
    ]
    if workflow_signal:
        lines.append("For manual review, keep a pending promotion receipt rather than silently leaving unpromoted edits in the working tree.")
    return {
        "id": f"cand-{idx:02d}-{slugify(reference_file.stem)}",
        "title": f"补充 {reference_file.name} 的状态推进说明",
        "target_path": str(reference_file),
        "category": "reference",
        "rationale": rationale,
        "risk_level": "low",
        "proposed_change_summary": "在 reference 文档末尾追加一小节，说明 machine-readable artifacts / truth_anchor / next_owner 字段约定。",
        "stage": "proposed",
        "source_refs": workflow_signal[:2],
        "executor_support": True,
        "execution_plan": {
            "action": "append_markdown_section",
            "section_heading": "## Control-Plane-Friendly Notes",
            "content_lines": lines,
        },
    }


def build_guardrail_candidate(target: Path, feedback_buckets: dict[str, list[str]], idx: int) -> dict | None:
    guardrail_file = choose_guardrail_file(target)
    if not guardrail_file:
        return None
    risk_signal = feedback_buckets.get("guardrails", []) or feedback_buckets.get("limitations", [])
    return {
        "id": f"cand-{idx:02d}-{slugify(guardrail_file.stem)}",
        "title": f"补充 {guardrail_file.name} 的保守执行说明",
        "target_path": str(guardrail_file),
        "category": "guardrail",
        "rationale": "反馈提到风险/边界，需要在 guardrail 文档里加一句保守执行原则，避免把规划性 skill 当成自动执行器。",
        "risk_level": "low",
        "proposed_change_summary": "追加简短 guardrail 条目：低风险文档才能自动 keep，其他候选应进入 pending/review。",
        "stage": "proposed",
        "source_refs": risk_signal[:2],
        "executor_support": True,
        "execution_plan": {
            "action": "append_markdown_section",
            "section_heading": "## Conservative Auto-Promote Rule",
            "content_lines": [
                "Only low-risk docs/reference/guardrail edits should be auto-kept in the first runnable version.",
                "Anything that changes prompt structure, workflow behavior, tests, or code paths should stay pending for explicit human promotion.",
            ],
        },
    }


def build_prompt_candidate(target: Path, feedback_buckets: dict[str, list[str]], idx: int) -> dict | None:
    prompt_target = target / "SKILL.md" if target.is_dir() else target
    if not prompt_target.exists():
        return None
    prompt_signal = feedback_buckets.get("prompt", []) or feedback_buckets.get("workflow", [])
    return {
        "id": f"cand-{idx:02d}-{slugify(prompt_target.stem)}-prompt",
        "title": "重构入口 prompt 的导航结构",
        "target_path": str(prompt_target.resolve()),
        "category": "prompt",
        "rationale": "入口 prompt/skill 导航重构可能影响触发行为与发现路径，属于中风险改动，第一版不自动执行。",
        "risk_level": "medium",
        "proposed_change_summary": "把长段提示改成更短的导航结构，保留更多约束前移到顶部。",
        "stage": "proposed",
        "source_refs": prompt_signal[:2],
        "executor_support": False,
        "execution_plan": {
            "action": "unsupported_manual_refactor",
            "notes": "留给后续 skill-evaluator/judge + human review。",
        },
    }


def build_tests_candidate(target: Path, feedback_buckets: dict[str, list[str]], idx: int) -> dict:
    test_signal = feedback_buckets.get("tests", [])
    target_path = target / "SKILL.md" if target.is_dir() else target
    return {
        "id": f"cand-{idx:02d}-{slugify(target.name)}-tests",
        "title": "为 skill 增加 smoke-check/validation 用例",
        "target_path": str(target_path.resolve()),
        "category": "tests",
        "rationale": "测试/验证资产对长期自动改进很重要，但会引入额外结构与约束，第一版只做候选保留，不自动落地。",
        "risk_level": "medium",
        "proposed_change_summary": "补一组 smoke examples 或校验清单，供后续 evaluator/control-plane 消费。",
        "stage": "proposed",
        "source_refs": test_signal[:2],
        "executor_support": False,
        "execution_plan": {
            "action": "unsupported_manual_test_addition",
            "notes": "待后续接 skill-evaluator / hidden benchmark 后实现。",
        },
    }


def build_workflow_candidate(target: Path, feedback_buckets: dict[str, list[str]], idx: int) -> dict:
    workflow_signal = feedback_buckets.get("workflow", [])
    target_path = target / "SKILL.md" if target.is_dir() else target
    return {
        "id": f"cand-{idx:02d}-{slugify(target.name)}-workflow",
        "title": "补充从建议到执行的 workflow adapter 说明",
        "target_path": str(target_path.resolve()),
        "category": "workflow",
        "rationale": "workflow 改动会影响未来 control-plane 接口与用户预期，当前版本应先进入 hold/pending，而不是自动改。",
        "risk_level": "medium",
        "proposed_change_summary": "增加执行流程图、adapter 接口说明或 orchestration 钩子文案。",
        "stage": "proposed",
        "source_refs": workflow_signal[:2],
        "executor_support": False,
        "execution_plan": {
            "action": "unsupported_manual_workflow_change",
            "notes": "后续在 richer adapter/control-plane 接入时实现。",
        },
    }


def load_failure_trace(trace_path: Path | None) -> dict | None:
    """Load a failure trace from a previous run."""
    if not trace_path or not trace_path.exists():
        return None
    return read_json(trace_path)


def adjust_candidates_from_trace(candidates: list, trace: dict) -> list:
    """Adjust candidate priorities based on failure trace."""
    failed_id = trace.get("candidate_id", "")
    failed_category = ""
    # Extract category from candidate_id (e.g., "cand-01-docs" -> "docs")
    parts = failed_id.split("-")
    if len(parts) >= 3:
        failed_category = parts[-1]

    adjusted = []
    for c in candidates:
        if c["category"] == failed_category:
            # Deprioritize the same category that failed
            c["rationale"] = (
                f"[Retry] Previous {failed_category} attempt failed: "
                f"{trace.get('reason', 'unknown')}. {c['rationale']}"
            )
            # Move to end
            adjusted.append(c)
        else:
            adjusted.insert(0, c)  # Boost alternatives
    return adjusted


def _find_evaluator_failures(feedback_entries: list[dict]) -> list[dict]:
    """Extract evaluator baseline failure data from source entries.

    Source entries from expand_source() have {path, kind, snippet} format,
    not the raw JSON content. We need to read the actual file if it looks
    like a baseline-failures JSON.
    """
    for entry in feedback_entries:
        if not isinstance(entry, dict):
            continue
        # Direct match (if raw JSON was passed)
        if entry.get("type") == "evaluator_baseline_failures":
            return entry.get("failed_tasks", [])
        # Match via source entry path
        entry_path = entry.get("path", "")
        if "baseline-failures" in entry_path or "eval-trace" in entry_path:
            try:
                data = read_json(Path(entry_path))
                if data.get("type") == "evaluator_baseline_failures":
                    return data.get("failed_tasks", [])
            except Exception:
                continue
    return []


def _llm_propose_skill_fix(target: Path, failed_tasks: list[dict]) -> dict | None:
    """Use LLM to propose a SKILL.md fix based on evaluator failures.

    Reads the current SKILL.md, sends it + failure details to claude -p,
    and asks for a targeted fix.
    """
    import shutil
    import subprocess
    import json as _json

    skill_md = target / "SKILL.md" if target.is_dir() else target
    if not skill_md.exists():
        return None
    if shutil.which("claude") is None:
        return None

    skill_content = skill_md.read_text(encoding="utf-8")
    failures_text = "\n".join(
        f"- Task '{t['task_id']}': {t.get('details', t.get('error', 'unknown'))}"
        for t in failed_tasks
    )

    prompt = (
        "You are improving a SKILL.md file based on evaluator task failures.\n\n"
        f"## Current SKILL.md\n```\n{skill_content[:3000]}\n```\n\n"
        f"## Failed Tasks\n{failures_text}\n\n"
        "Analyze why these tasks failed and propose a TARGETED change to SKILL.md "
        "that would fix the failures without breaking what already works.\n\n"
        "Respond with ONLY a JSON object:\n"
        '{{"section_heading": "## <heading to add/replace>", '
        '"action": "append_markdown_section" or "replace_markdown_section", '
        '"content_lines": ["line1", "line2", ...], '
        '"rationale": "why this fixes the failures"}}'
    )

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "json"],
            input=prompt, capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return None
        # Parse claude output
        try:
            claude_out = _json.loads(result.stdout)
            text = claude_out.get("result", result.stdout)
        except (_json.JSONDecodeError, TypeError):
            text = result.stdout
        # Extract JSON from response (may be wrapped in markdown)
        text = text.strip()
        # Find the first { and last } to extract JSON robustly
        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace >= 0 and last_brace > first_brace:
            text = text[first_brace:last_brace + 1]
        parsed = _json.loads(text)
        return {
            "id": "cand-01-eval-fix",
            "title": f"Fix SKILL.md based on {len(failed_tasks)} evaluator failure(s)",
            "target_path": str(skill_md.resolve()),
            "category": "prompt",
            "rationale": parsed.get("rationale", "LLM-proposed fix for evaluator failures"),
            "risk_level": "low",
            "proposed_change_summary": f"Targeted SKILL.md fix for failed tasks: {', '.join(t['task_id'] for t in failed_tasks)}",
            "stage": "proposed",
            "source_refs": [f"evaluator:{t['task_id']}" for t in failed_tasks],
            "executor_support": True,
            "execution_plan": {
                "action": parsed.get("action", "append_markdown_section"),
                "section_heading": parsed.get("section_heading", "## Output Format"),
                "content_lines": parsed.get("content_lines", []),
            },
        }
    except Exception:
        return None


def _find_correction_hotspots(feedback_entries: list[dict]) -> dict[str, int]:
    """Extract user correction hotspots from feedback.jsonl source entries.

    Returns a dimension -> count mapping of the most-corrected dimensions.
    """
    hotspots: dict[str, int] = {}
    for entry in feedback_entries:
        if not isinstance(entry, dict):
            continue
        entry_path = entry.get("path", "")
        if "feedback" not in entry_path or not entry_path.endswith(".jsonl"):
            continue
        try:
            import json as _json
            with open(entry_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = _json.loads(line)
                    except _json.JSONDecodeError:
                        continue
                    if event.get("outcome") in ("correction", "partial"):
                        dim = event.get("dimension_hint")
                        if dim:
                            hotspots[dim] = hotspots.get(dim, 0) + 1
        except OSError:
            continue
    return hotspots


def generate_candidates(target: Path, feedback_entries: list[dict], max_candidates: int) -> list[dict]:
    # Check for evaluator failure data first — this is the highest-signal input
    eval_failures = _find_evaluator_failures(feedback_entries)
    if eval_failures:
        llm_fix = _llm_propose_skill_fix(target, eval_failures)
        if llm_fix:
            # Put the evaluator-driven fix first, then add template candidates
            candidates = [llm_fix]
            # Still generate template candidates as fallbacks
            feedback_buckets = classify_feedback(feedback_entries)
            idx = 2
            for builder in [build_docs_candidate, build_reference_candidate]:
                c = builder(target, feedback_buckets, idx)
                if c:
                    candidates.append(c)
                    idx += 1
                if len(candidates) >= max_candidates:
                    break
            return candidates[:max_candidates]

    feedback_buckets = classify_feedback(feedback_entries)
    builders = [
        build_docs_candidate,
        build_reference_candidate,
        build_guardrail_candidate,
        build_prompt_candidate,
    ]
    candidates: list[dict] = []
    idx = 1
    for builder in builders:
        candidate = builder(target, feedback_buckets, idx)
        if candidate:
            candidates.append(candidate)
            idx += 1
        if len(candidates) >= max_candidates:
            return candidates[:max_candidates]
    for builder in (build_workflow_candidate, build_tests_candidate):
        if len(candidates) >= max_candidates:
            break
        candidates.append(builder(target, feedback_buckets, idx))
        idx += 1
    if not candidates:
        doc_file = choose_doc_file(target)
        if doc_file:
            candidates.append({
                "id": "cand-01-fallback-docs",
                "title": f"补充 {doc_file.name} 的使用边界",
                "target_path": str(doc_file),
                "category": "docs",
                "rationale": "即使没有外部反馈，文档澄清也是 generic-skill lane 最安全的第一步。",
                "risk_level": "low",
                "proposed_change_summary": "追加一个短的 operator note 说明此 skill 的边界。",
                "stage": "proposed",
                "source_refs": [],
                "executor_support": True,
                "execution_plan": {
                    "action": "append_markdown_section",
                    "section_heading": "## Operator Notes",
                    "content_lines": [
                        "This skill is advisory/planning-oriented and should be paired with external tooling for operational execution.",
                    ],
                },
            })
    return candidates[:max_candidates]


def main() -> int:
    args = parse_args()
    state_root = Path(args.state_root).expanduser().resolve()
    ensure_tree(state_root)
    target = normalize_target(args.target)
    run_id = args.run_id or make_run_id(target)

    source_paths = load_source_paths(target, args.source)
    source_entries: list[dict] = []
    for source in source_paths:
        source_entries.extend(expand_source(source))

    trace_path = Path(args.trace).expanduser().resolve() if args.trace else None
    failure_trace = load_failure_trace(trace_path)

    target_profile = compute_target_profile(target)
    candidates = generate_candidates(target, source_entries, args.max_candidates)

    if failure_trace:
        candidates = adjust_candidates_from_trace(candidates, failure_trace)

    for candidate in candidates:
        candidate["lane"] = args.lane
        candidate["protected_target"] = protected_target(candidate["target_path"])
        candidate["created_at"] = utc_now_iso()

    output_path = Path(args.output).expanduser().resolve() if args.output else state_root / "candidate_versions" / f"{run_id}.json"
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "lane": args.lane,
        "run_id": run_id,
        "stage": "proposed",
        "status": "success" if target_profile["exists"] else "target_missing",
        "created_at": utc_now_iso(),
        "target": target_profile,
        "input_sources": source_entries,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "next_step": "rank_candidates",
        "next_owner": "critic",
        "truth_anchor": str(output_path),
        "failure_trace_used": failure_trace is not None,
    }
    write_json(output_path, artifact)
    update_state(
        state_root,
        run_id=run_id,
        stage="proposed",
        status=artifact["status"],
        target_path=str(target),
        truth_anchor=str(output_path),
        extra={
            "candidate_count": len(candidates),
            "source_count": len(source_entries),
        },
    )
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
