#!/usr/bin/env python3
import argparse
import json
import shlex
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_shell_value(value: str) -> str:
    return shlex.quote(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare run advice from persistent learnings.")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--fps", required=True)
    parser.add_argument("--concurrency")
    parser.add_argument("--model")
    parser.add_argument("--image-size")
    parser.add_argument("--persistent-learnings", required=True)
    args = parser.parse_args()

    workdir = Path(args.workdir).resolve()
    learnings_path = Path(args.persistent_learnings).resolve()
    run_advice_path = workdir / "run_advice.json"
    run_advice_md_path = workdir / "run_advice.md"
    run_advice_env_path = workdir / "run_advice.env"

    persistent = load_json(learnings_path) if learnings_path.exists() else {}
    aggregate = persistent.get("aggregate") or {}
    prior_runs = persistent.get("runs") or []
    total_prior_runs = int(aggregate.get("runs") or 0)
    avg_spend_per_frame = None
    total_frames = int(aggregate.get("total_frames") or 0)
    total_spend = float(aggregate.get("total_estimated_spend_usd") or 0.0)
    if total_frames > 0:
        avg_spend_per_frame = total_spend / total_frames

    requested_fps = float(args.fps)
    requested_concurrency = int(args.concurrency or 2)
    recommended_request_retries = 3
    recommended_concurrency = requested_concurrency
    prompt_addendums = []
    notes = []

    if total_prior_runs > 0:
        notes.append(f"Loaded learnings from {total_prior_runs} previous run(s).")

    if any((run.get("frames_with_multiple_attempts") or 0) > 0 for run in prior_runs):
        prompt_addendums.append(
            "Preserve frame continuity. Keep all visible content outside the mask unchanged and reconstruct only the masked overlay area."
        )
        notes.append("Previous runs needed extra attempts, so this run will reinforce masked-only editing.")

    reason_counter = aggregate.get("reason_counter") or {}
    if int(reason_counter.get("no_output_image") or 0) > 0:
        recommended_request_retries = max(recommended_request_retries, 3)
        notes.append("Previous runs saw missing-image responses, so request retries stay enabled.")

    if requested_fps >= 15:
        notes.append("High demo FPS increases Gemini cost because more frames must be edited.")
    if avg_spend_per_frame is not None and avg_spend_per_frame > 0.08:
        notes.append(
            f"Historical spend is about ${avg_spend_per_frame:.4f} per frame, so longer or higher-FPS runs can become expensive quickly."
        )

    if total_prior_runs > 0 and requested_concurrency > 2:
        recommended_concurrency = 2
        notes.append("Concurrency is capped at 2 by default when learnings exist, to stay conservative on provider stability.")

    advice = {
        "generated_from_prior_runs": total_prior_runs,
        "mode": args.mode,
        "fps": args.fps,
        "model": args.model,
        "image_size": args.image_size,
        "recommendations": {
            "prompt_addendums": prompt_addendums,
            "request_retries": recommended_request_retries,
            "concurrency": recommended_concurrency,
        },
        "notes": notes,
    }
    run_advice_path.write_text(json.dumps(advice, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Run Advice",
        "",
        f"- Prior runs loaded: `{total_prior_runs}`",
        f"- Requested FPS: `{args.fps}`",
        f"- Recommended request retries: `{recommended_request_retries}`",
        f"- Recommended concurrency: `{recommended_concurrency}`",
    ]
    if prompt_addendums:
        lines.append(f"- Prompt addendums: `{prompt_addendums}`")
    if notes:
        lines.extend(["", "## Notes", ""])
        lines.extend([f"- {note}" for note in notes])
    run_advice_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    shell_lines = [
        f"LEARNED_REQUEST_RETRIES={dump_shell_value(str(recommended_request_retries))}",
        f"LEARNED_CONCURRENCY={dump_shell_value(str(recommended_concurrency))}",
        f"LEARNED_PROMPT_ADDENDUM={dump_shell_value(' '.join(prompt_addendums))}",
    ]
    run_advice_env_path.write_text("\n".join(shell_lines) + "\n", encoding="utf-8")

    print(str(run_advice_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
