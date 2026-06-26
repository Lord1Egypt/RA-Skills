#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def round_or_none(value, digits=6):
    if value is None:
        return None
    return round(value, digits)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize one video cleanup run and update persistent learnings.")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--input-video", required=True)
    parser.add_argument("--output-video", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--fps", required=True)
    parser.add_argument("--model")
    parser.add_argument("--image-size")
    parser.add_argument("--persistent-learnings")
    args = parser.parse_args()

    workdir = Path(args.workdir).resolve()
    usage_dir = workdir / "usage"
    frame_jobs_path = workdir / "frame_jobs.json"
    run_summary_path = workdir / "run_summary.json"
    self_improve_md_path = workdir / "self_improve.md"

    usage_files = sorted(usage_dir.glob("frame_*.json"))
    frame_jobs = load_json(frame_jobs_path) if frame_jobs_path.exists() else {"jobs": []}

    frame_count = len(usage_files)
    total_attempts = 0
    frames_with_multiple_attempts = 0
    accepted_frames = 0
    failed_frames = 0
    rejected_attempts = 0
    total_prompt_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    rejected_reason_counter = Counter()
    status_counter = Counter()
    attempt_length_counter = Counter()
    raw_outside_changed_ratios = []

    frame_summaries = []

    for usage_path in usage_files:
        payload = load_json(usage_path)
        usage = payload.get("usage_metadata") or {}
        prompt_tokens = int(usage.get("prompt_token_count") or 0)
        output_tokens = int(usage.get("candidates_token_count") or 0)
        all_tokens = int(usage.get("total_token_count") or 0)
        attempts = payload.get("attempts") or []

        total_prompt_tokens += prompt_tokens
        total_output_tokens += output_tokens
        total_tokens += all_tokens
        total_attempts += len(attempts)
        attempt_length_counter.update([len(attempts)])
        if len(attempts) > 1:
            frames_with_multiple_attempts += 1

        final_status = attempts[-1].get("status") if attempts else "unknown"
        status_counter.update([final_status])
        if final_status == "accepted":
            accepted_frames += 1
        else:
            failed_frames += 1

        frame_reasons = []
        raw_outside = None
        for attempt in attempts:
            if attempt.get("status") == "rejected":
                rejected_attempts += 1
                rejected_reason_counter.update(attempt.get("reasons") or [])
                frame_reasons.extend(attempt.get("reasons") or [])
            metrics = attempt.get("metrics") or {}
            if raw_outside is None and "raw_outside_changed_ratio" in metrics:
                raw_outside = metrics.get("raw_outside_changed_ratio")
            if "raw_outside_changed_ratio" in metrics:
                raw_outside_changed_ratios.append(metrics["raw_outside_changed_ratio"])

        frame_summaries.append(
            {
                "frame": usage_path.stem,
                "attempts": len(attempts),
                "final_status": final_status,
                "rejected_reasons": sorted(set(frame_reasons)),
                "prompt_tokens": prompt_tokens,
                "output_tokens": output_tokens,
                "total_tokens": all_tokens,
                "raw_outside_changed_ratio_first_seen": raw_outside,
            }
        )

    billing = (frame_jobs.get("billing") or {}) if isinstance(frame_jobs, dict) else {}
    estimated_spend_total_usd = billing.get("estimated_spend_total_usd")

    run_summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_video": str(Path(args.input_video).resolve()),
        "output_video": str(Path(args.output_video).resolve()),
        "workdir": str(workdir),
        "mode": args.mode,
        "fps": args.fps,
        "model": args.model,
        "image_size": args.image_size,
        "frame_count": frame_count,
        "accepted_frames": accepted_frames,
        "failed_frames": failed_frames,
        "total_attempts": total_attempts,
        "frames_with_multiple_attempts": frames_with_multiple_attempts,
        "rejected_attempts": rejected_attempts,
        "status_counter": dict(status_counter),
        "rejected_reason_counter": dict(rejected_reason_counter),
        "attempt_length_counter": {str(k): v for k, v in sorted(attempt_length_counter.items())},
        "token_usage": {
            "prompt_tokens": total_prompt_tokens,
            "output_tokens": total_output_tokens,
            "total_tokens": total_tokens,
        },
        "estimated_spend_total_usd": estimated_spend_total_usd,
        "quality_signals": {
            "max_raw_outside_changed_ratio": round_or_none(max(raw_outside_changed_ratios) if raw_outside_changed_ratios else None),
            "avg_raw_outside_changed_ratio": round_or_none(
                sum(raw_outside_changed_ratios) / len(raw_outside_changed_ratios) if raw_outside_changed_ratios else None
            ),
        },
        "top_takeaways": [
            "Masked-region repair quality can still vary from frame to frame.",
            "Unmasked pixels are preserved from the original frame, so the main visible scene stays stable.",
            "Gemini cost scales with frame count, and higher demo FPS increases spend.",
        ],
        "frames": frame_summaries,
    }
    run_summary_path.write_text(json.dumps(run_summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Self Improve Summary",
        "",
        f"- Input video: `{Path(args.input_video).resolve()}`",
        f"- Output video: `{Path(args.output_video).resolve()}`",
        f"- Workdir: `{workdir}`",
        f"- Mode: `{args.mode}`",
        f"- FPS: `{args.fps}`",
    ]
    if args.model:
        lines.append(f"- Model: `{args.model}`")
    if args.image_size:
        lines.append(f"- Image size: `{args.image_size}`")
    lines.extend(
        [
            f"- Frames processed: `{frame_count}`",
            f"- Frames with extra attempts: `{frames_with_multiple_attempts}`",
            f"- Total attempts: `{total_attempts}`",
            f"- Prompt tokens: `{total_prompt_tokens}`",
            f"- Output tokens: `{total_output_tokens}`",
        ]
    )
    if estimated_spend_total_usd is not None:
        lines.append(f"- Estimated spend: `${estimated_spend_total_usd:.4f}`")

    lines.extend(["", "## What Happened", ""])
    if rejected_reason_counter:
        lines.append(f"- Rejected attempt reasons: `{dict(rejected_reason_counter)}`")
    else:
        lines.append("- No content-validation rejections were recorded in this run.")
    if frames_with_multiple_attempts:
        lines.append(f"- `{frames_with_multiple_attempts}` frame(s) required more than one attempt.")
    else:
        lines.append("- Every frame completed in a single attempt.")
    avg_ratio = run_summary["quality_signals"]["avg_raw_outside_changed_ratio"]
    max_ratio = run_summary["quality_signals"]["max_raw_outside_changed_ratio"]
    if avg_ratio is not None and max_ratio is not None:
        lines.append(
            f"- Raw model edits outside the mask were observed before compositing. "
            f"Average raw outside-mask change ratio: `{avg_ratio}`; max: `{max_ratio}`."
        )

    lines.extend(
        [
            "",
            "## Current Learnings",
            "",
            "- Repair quality inside masked or covered regions is still not fully stable.",
            "- Preserving the original unmasked pixels is the main safeguard that keeps the visible scene consistent.",
            "- Demo-quality FPS increases visual smoothness, but it also increases Gemini cost.",
            "",
        ]
    )
    self_improve_md_path.write_text("\n".join(lines), encoding="utf-8")

    if args.persistent_learnings:
        learnings_path = Path(args.persistent_learnings).resolve()
        if learnings_path.exists():
            persistent = load_json(learnings_path)
        else:
            persistent = {
                "version": 1,
                "updated_at_utc": None,
                "runs": [],
                "aggregate": {
                    "runs": 0,
                    "total_frames": 0,
                    "total_estimated_spend_usd": 0.0,
                    "reason_counter": {},
                },
            }

        aggregate = persistent.setdefault("aggregate", {})
        aggregate["runs"] = int(aggregate.get("runs") or 0) + 1
        aggregate["total_frames"] = int(aggregate.get("total_frames") or 0) + frame_count
        aggregate["total_estimated_spend_usd"] = round(
            float(aggregate.get("total_estimated_spend_usd") or 0.0) + float(estimated_spend_total_usd or 0.0),
            6,
        )
        reason_counter = Counter(aggregate.get("reason_counter") or {})
        reason_counter.update(rejected_reason_counter)
        aggregate["reason_counter"] = dict(reason_counter)

        persistent["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
        persistent.setdefault("runs", []).append(
            {
                "generated_at_utc": run_summary["generated_at_utc"],
                "input_video": run_summary["input_video"],
                "output_video": run_summary["output_video"],
                "mode": args.mode,
                "fps": args.fps,
                "model": args.model,
                "image_size": args.image_size,
                "frame_count": frame_count,
                "frames_with_multiple_attempts": frames_with_multiple_attempts,
                "rejected_reason_counter": dict(rejected_reason_counter),
                "quality_signals": run_summary["quality_signals"],
                "estimated_spend_total_usd": estimated_spend_total_usd,
            }
        )
        learnings_path.write_text(json.dumps(persistent, indent=2) + "\n", encoding="utf-8")

    print(str(run_summary_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
