#!/usr/bin/env python3
"""
debate_orchestrator_generic.py — Generic debate orchestrator
Coordinates the full debate lifecycle: init, evidence, rounds, synthesis.
Uses provider-agnostic tool names; runtime adapter maps to actual tools.
"""

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Options:
    topic: str
    rounds: int = 3
    output_format: str = "full_report"
    language: str = "bilingual"
    domain: str = "general"
    depth: str = "standard"
    mode: str = "balanced"
    speculation: str = "moderate"
    evidence_refresh: str = "hybrid"
    focus: list[str] = field(default_factory=list)
    allow_fallback: bool = True
    min_evidence: int = 10
    source_retries: int = 2
    min_args: int = 2
    min_rebuttals: int = 1
    step_timeout_sec: int = 300

    @classmethod
    def from_config(cls, config_path: str) -> "Options":
        with open(config_path) as f:
            cfg = json.load(f)
        depth_evidence = {"quick": 5, "standard": 10, "deep": 15}
        depth_args = {"quick": 2, "standard": 2, "deep": 3}
        depth = cfg.get("depth", "standard")
        return cls(
            topic=cfg["topic"],
            rounds=cfg.get("round_count", cfg.get("rounds", 3)),
            output_format=cfg.get("output_format", "full_report"),
            language=cfg.get("language", "bilingual"),
            domain=cfg.get("domain", "general"),
            depth=depth,
            mode=cfg.get("mode", "balanced"),
            speculation=cfg.get("speculation_level", "moderate"),
            evidence_refresh=cfg.get("evidence_refresh", "hybrid"),
            focus=cfg.get("focus_areas", []),
            min_evidence=depth_evidence.get(depth, 10),
            min_args=depth_args.get(depth, 2),
        )


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_script(script: str, args: list[str], cwd: str) -> subprocess.CompletedProcess:
    script_dir = Path(__file__).parent
    script_path = script_dir / script
    result = subprocess.run(
        ["bash", str(script_path)] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Script {script} failed: {result.stderr}", file=sys.stderr)
    return result


def append_audit(workspace: str, action: str, details: dict):
    audit_file = os.path.join(workspace, "logs", "audit_trail.jsonl")
    entry = json.dumps({
        "timestamp": timestamp(),
        "action": action,
        "details": details,
    })
    run_script("append-audit.sh", [audit_file, entry], workspace)


def validate_json(filepath: str, schema_type: str) -> bool:
    result = run_script("validate-json.sh", [filepath, schema_type], os.path.dirname(filepath))
    return result.returncode == 0


def read_json(filepath: str):
    with open(filepath) as f:
        return json.load(f)


def write_json(filepath: str, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_config(workspace: str, updates: dict):
    config_path = os.path.join(workspace, "config.json")
    config = read_json(config_path)
    config.update(updates)
    config["updated_at"] = timestamp()
    write_json(config_path, config)


# --- Runtime Adapter ---

MODEL_MAP = {
    "claude": {"fast": "sonnet", "balanced": "sonnet", "deep": "opus"},
    "codex": {"fast": "gpt-4o-mini", "balanced": "gpt-4o", "deep": "o1"},
}


def tier_to_model(tier: str, runtime: str) -> str:
    """Map generic tier name to provider-specific model name."""
    return MODEL_MAP.get(runtime, {}).get(tier, tier)


def detect_runtime() -> str:
    """Detect which agent runtime is available. Priority: claude > codex."""
    for cmd, name in [("claude", "claude"), ("codex", "codex")]:
        if shutil.which(cmd):
            return name
    return "none"


_RUNTIME: Optional[str] = None


def get_runtime() -> str:
    """Cached runtime detection."""
    global _RUNTIME
    if _RUNTIME is None:
        _RUNTIME = detect_runtime()
        print(f"[{timestamp()}] Detected runtime: {_RUNTIME}")
    return _RUNTIME


def dispatch_agent(step_id: str, prompt: str, model_tier: str = "balanced",
                   timeout_sec: int = 300) -> bool:
    """
    Execute a step via the detected agent runtime.

    Claude Code  → claude -p <prompt> --model <model>
    Codex        → codex -p <prompt> --model <model>
    None         → ERROR, returns False

    Returns True if step completed successfully (DONE:{step_id} marker found).
    """
    runtime = get_runtime()
    print(f"[{timestamp()}] Executing step: {step_id} (model: {model_tier}, runtime: {runtime})")
    print(f"[{timestamp()}] Prompt length: {len(prompt)} chars")

    model = tier_to_model(model_tier, runtime)

    if runtime == "claude":
        cmd = [
            "claude", "-p", prompt,
            "--model", model,
        ]
    elif runtime == "codex":
        cmd = [
            "codex", "-p", prompt,
            "--model", model,
        ]
    else:
        print(f"[{timestamp()}] ERROR: No agent runtime found (need 'claude' or 'codex' in PATH)",
              file=sys.stderr)
        return False

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""

        if result.returncode != 0:
            print(f"[{timestamp()}] Step {step_id} exited with code {result.returncode}",
                  file=sys.stderr)
            if stderr:
                print(f"[{timestamp()}] stderr: {stderr[:500]}", file=sys.stderr)

        success = f"DONE:{step_id}" in stdout
        if success:
            print(f"[{timestamp()}] Step {step_id} completed successfully")
        else:
            # Some runtimes don't output markers but still succeed
            print(f"[{timestamp()}] Step {step_id} finished (no DONE marker, "
                  f"exit code {result.returncode})")
            # Treat exit code 0 without marker as success (agent may not always emit marker)
            success = result.returncode == 0

        return success

    except subprocess.TimeoutExpired:
        print(f"[{timestamp()}] Step {step_id} TIMED OUT after {timeout_sec}s", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"[{timestamp()}] ERROR: Runtime '{runtime}' not found in PATH", file=sys.stderr)
        return False


def parallel_exec(tasks: list[tuple[str, str, str, int]]) -> dict[str, bool]:
    """
    Execute multiple dispatch_agent tasks in parallel.
    Each task: (step_id, prompt, model_tier, timeout_sec)
    Returns: {step_id: success_bool}
    """
    results = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = {
            executor.submit(dispatch_agent, sid, prompt, tier, timeout): sid
            for sid, prompt, tier, timeout in tasks
        }
        for future in as_completed(futures):
            sid = futures[future]
            try:
                results[sid] = future.result()
            except Exception as e:
                print(f"[{timestamp()}] Step {sid} raised exception: {e}", file=sys.stderr)
                results[sid] = False
    return results


def merge_new_evidence(workspace: str, round_num: int):
    """Merge new_evidence from Pro/Con turns into evidence_store."""
    evidence_path = os.path.join(workspace, "evidence", "evidence_store.json")
    evidence_store = read_json(evidence_path)

    existing_keys = {(e.get("url", ""), e.get("hash", "")) for e in evidence_store}

    for side in ["pro", "con"]:
        turn_path = os.path.join(workspace, "rounds", f"round_{round_num}", f"{side}_turn.json")
        if not os.path.exists(turn_path):
            continue
        turn = read_json(turn_path)
        new_evidence = turn.get("new_evidence", [])
        added = 0
        for item in new_evidence:
            key = (item.get("url", ""), item.get("hash", ""))
            if key not in existing_keys:
                item["discovered_by"] = side
                item["discovered_at_round"] = round_num
                evidence_store.append(item)
                existing_keys.add(key)
                added += 1
        if added > 0:
            print(f"[{timestamp()}] Merged {added} new evidence items from {side}")

    write_json(evidence_path, evidence_store)
    append_audit(workspace, "evidence_merged_from_turn", {
        "round": round_num,
        "total_items": len(evidence_store),
    })


def run_debate(workspace: str, opts: Options):
    """Run the full debate orchestration flow."""
    print(f"[{timestamp()}] Starting debate: {opts.topic}")
    print(f"[{timestamp()}] Rounds: {opts.rounds}, Depth: {opts.depth}, Mode: {opts.mode}")

    # Phase 1: Initialization
    print(f"\n{'='*60}")
    print(f"PHASE 1: INITIALIZATION")
    print(f"{'='*60}")

    # Step 1a: Source Ingest (broad)
    depth_queries = {"quick": 3, "standard": 5, "deep": 8}
    num_queries = depth_queries.get(opts.depth, 5)
    dispatch_agent(
        "source_ingest_round_0",
        f"Execute source-ingest.md: topic={opts.topic}, mode=broad, round=0, "
        f"depth={opts.depth}, num_queries={num_queries}. "
        f"Workspace: {workspace}",
        model_tier="balanced",
    )

    # Step 1b: Freshness Check
    dispatch_agent(
        "freshness_check_0",
        f"Execute freshness-check.md: workspace={workspace}",
        model_tier="balanced",
    )

    # Step 1c: Verify minimum evidence
    evidence_path = os.path.join(workspace, "evidence", "evidence_store.json")
    if os.path.exists(evidence_path):
        evidence = read_json(evidence_path)
        if len(evidence) < opts.min_evidence:
            print(f"[{timestamp()}] Warning: Only {len(evidence)} evidence items "
                  f"(minimum: {opts.min_evidence}). Retrying ingest...")
            for retry in range(opts.source_retries):
                dispatch_agent(
                    f"source_ingest_retry_{retry+1}",
                    f"Execute source-ingest.md: topic={opts.topic}, mode=broad, round=0, "
                    f"broaden keywords. Workspace: {workspace}",
                    model_tier="balanced",
                )
                evidence = read_json(evidence_path)
                if len(evidence) >= opts.min_evidence:
                    break

    update_config(workspace, {"status": "evidence_gathered"})
    append_audit(workspace, "evidence_added", {"round": 0, "mode": "broad"})

    # Phase 2: Debate Rounds
    for round_num in range(1, opts.rounds + 1):
        print(f"\n{'='*60}")
        print(f"PHASE 2: ROUND {round_num}/{opts.rounds}")
        print(f"{'='*60}")

        append_audit(workspace, "round_started", {"round": round_num})
        update_config(workspace, {"current_round": round_num, "status": "in_progress"})

        # Step 2a: Per-round evidence refresh
        needs_refresh = (
            opts.evidence_refresh == "per_round" or
            (opts.evidence_refresh == "hybrid" and round_num > 1)
        )
        if needs_refresh:
            print(f"[{timestamp()}] Per-round evidence refresh for round {round_num}")
            prev_ruling_path = os.path.join(
                workspace, "rounds", f"round_{round_num-1}", "judge_ruling.json"
            )
            search_focus = ""
            if os.path.exists(prev_ruling_path):
                ruling = read_json(prev_ruling_path)
                mrps = ruling.get("mandatory_response_points", [])
                flags = ruling.get("causal_validity_flags", [])
                search_focus = json.dumps({"mrps": mrps, "flags": flags})

            dispatch_agent(
                f"source_ingest_round_{round_num}",
                f"Execute source-ingest.md: topic={opts.topic}, mode=focused, "
                f"round={round_num}, search_focus={search_focus}. Workspace: {workspace}",
                model_tier="balanced",
            )
            dispatch_agent(
                f"freshness_check_round_{round_num}",
                f"Execute freshness-check.md: workspace={workspace}",
                model_tier="balanced",
            )
            append_audit(workspace, "per_round_evidence_ingest", {"round": round_num})

        # Step 2b: Parallel Pro + Con
        print(f"[{timestamp()}] Launching Pro and Con in parallel")
        prev_round_context = ""
        if round_num > 1:
            prev_round_context = (
                f"Read round {round_num-1} data: "
                f"rounds/round_{round_num-1}/pro_turn.json, "
                f"rounds/round_{round_num-1}/con_turn.json, "
                f"rounds/round_{round_num-1}/judge_ruling.json"
            )

        pro_prompt = (
            f"Execute debate-turn.md: side=pro, round={round_num}, topic={opts.topic}, "
            f"mode={opts.mode}, speculation={opts.speculation}, depth={opts.depth}. "
            f"{prev_round_context}. Workspace: {workspace}"
        )
        con_prompt = (
            f"Execute debate-turn.md: side=con, round={round_num}, topic={opts.topic}, "
            f"mode={opts.mode}, speculation={opts.speculation}, depth={opts.depth}. "
            f"{prev_round_context}. Workspace: {workspace}"
        )

        parallel_results = parallel_exec([
            (f"debate_turn_pro_round_{round_num}", pro_prompt, "balanced", opts.step_timeout_sec),
            (f"debate_turn_con_round_{round_num}", con_prompt, "balanced", opts.step_timeout_sec),
        ])
        for sid, ok in parallel_results.items():
            if not ok:
                print(f"[{timestamp()}] WARNING: {sid} did not complete successfully")

        # Step 2c: Validate outputs
        print(f"[{timestamp()}] Validating turn outputs")
        for side in ["pro", "con"]:
            turn_path = os.path.join(
                workspace, "rounds", f"round_{round_num}", f"{side}_turn.json"
            )
            if os.path.exists(turn_path):
                if not validate_json(turn_path, f"{side}_turn"):
                    print(f"[{timestamp()}] Validation failed for {side}_turn, retrying...")
                    # Max 2 retries
                    for retry in range(2):
                        dispatch_agent(
                            f"debate_turn_{side}_round_{round_num}_retry_{retry+1}",
                            f"Re-execute debate-turn.md: fix JSON validation errors. "
                            f"side={side}, round={round_num}. Workspace: {workspace}",
                            model_tier="balanced",
                        )
                        if validate_json(turn_path, f"{side}_turn"):
                            break

        append_audit(workspace, "pro_turn_complete", {"round": round_num})
        append_audit(workspace, "con_turn_complete", {"round": round_num})

        # Step 2d: Judge audit
        print(f"[{timestamp()}] Judge audit for round {round_num}")
        dispatch_agent(
            f"judge_audit_round_{round_num}",
            f"Execute judge-audit.md: round={round_num}. Workspace: {workspace}",
            model_tier="deep",
        )

        judge_path = os.path.join(
            workspace, "rounds", f"round_{round_num}", "judge_ruling.json"
        )
        if os.path.exists(judge_path):
            validate_json(judge_path, "judge_ruling")

        append_audit(workspace, "judge_ruling_complete", {"round": round_num})

        # Step 2e: Post-round processing
        print(f"[{timestamp()}] Post-round processing")
        dispatch_agent(
            f"claim_ledger_update_round_{round_num}",
            f"Execute claim-ledger-update.md: round={round_num}. Workspace: {workspace}",
            model_tier="balanced",
        )

        merge_new_evidence(workspace, round_num)

        update_config(workspace, {
            "current_round": round_num,
            "status": f"round_{round_num}_complete",
        })

    # Phase 3: Final Output
    print(f"\n{'='*60}")
    print(f"PHASE 3: FINAL OUTPUT")
    print(f"{'='*60}")

    dispatch_agent(
        "final_synthesis",
        f"Execute final-synthesis.md: workspace={workspace}",
        model_tier="deep",
    )

    report_path = os.path.join(workspace, "reports", "final_report.json")
    if os.path.exists(report_path):
        validate_json(report_path, "final_report")

    update_config(workspace, {"status": "complete"})
    append_audit(workspace, "report_generated", {"workspace": workspace})

    print(f"\n[{timestamp()}] Debate complete!")
    print(f"  Report: {os.path.join(workspace, 'reports', 'debate_report.md')}")
    print(f"  JSON:   {report_path}")


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <workspace_dir> <config_or_topic> [rounds]")
        sys.exit(1)

    workspace = sys.argv[1]
    config_or_topic = sys.argv[2]
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    if os.path.isfile(config_or_topic):
        opts = Options.from_config(config_or_topic)
    else:
        # Initialize workspace
        run_script("init-workspace.sh", [workspace, config_or_topic, str(rounds)], ".")
        opts = Options(topic=config_or_topic, rounds=rounds)

    run_debate(workspace, opts)


if __name__ == "__main__":
    main()
