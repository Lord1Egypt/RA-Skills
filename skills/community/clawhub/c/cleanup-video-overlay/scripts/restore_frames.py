#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import shlex
import subprocess
import sys
import threading
import time
from pathlib import Path

IMAGE_OUTPUT_PRICES = {
    "0.5K": 0.045,
    "1K": 0.067,
    "2K": 0.101,
    "4K": 0.151,
}

GEMINI_31_FLASH_IMAGE_PREVIEW_INPUT_PRICE_PER_M = 0.50
GEMINI_31_FLASH_IMAGE_PREVIEW_OUTPUT_PRICE_PER_M = 60.00


def usd(amount: float) -> str:
    return f"${amount:.4f}"


def load_usage(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def estimate_gemini_cost(total_frames: int, image_size: str) -> tuple[float, str]:
    image_cost = IMAGE_OUTPUT_PRICES.get(image_size, IMAGE_OUTPUT_PRICES["1K"])
    total = total_frames * image_cost
    basis = (
        f"Estimated on {total_frames} image outputs at {image_size}, "
        f"using {usd(image_cost)} per image as the base output cost."
    )
    return total, basis


def usage_costs(usage_payload: dict) -> tuple[int, int, float]:
    usage = usage_payload.get("usage_metadata") or {}
    prompt_tokens = int(usage.get("promptTokenCount") or usage.get("prompt_token_count") or 0)
    output_tokens = int(usage.get("candidatesTokenCount") or usage.get("candidates_token_count") or 0)
    cost = (
        prompt_tokens * GEMINI_31_FLASH_IMAGE_PREVIEW_INPUT_PRICE_PER_M / 1_000_000
        + output_tokens * GEMINI_31_FLASH_IMAGE_PREVIEW_OUTPUT_PRICE_PER_M / 1_000_000
    )
    return prompt_tokens, output_tokens, cost


def retry_summary(usage_payload: dict) -> tuple[int, list[str]]:
    attempts = usage_payload.get("attempts") or []
    rejected = []
    for attempt in attempts:
        if attempt.get("status") == "rejected":
            rejected.extend(attempt.get("reasons") or [])
    return len(attempts), sorted(set(rejected))


def main():
    parser = argparse.ArgumentParser(description="Run an external frame editor command over a directory of frames.")
    parser.add_argument("--frames-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--editor-cmd", required=True)
    parser.add_argument("--mask", required=True)
    parser.add_argument("--glob", default="frame_*.png")
    parser.add_argument("--manifest-output")
    parser.add_argument("--progress-mode", choices=["none", "generic", "gemini-nano-banana-2"], default="generic")
    parser.add_argument("--image-size", default="1K")
    parser.add_argument("--usage-dir")
    parser.add_argument("--concurrency", type=int, default=1)
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    mask_path = Path(args.mask).resolve()

    if not frames_dir.exists():
        raise SystemExit(f"Frames directory not found: {frames_dir}")
    if not mask_path.exists():
        raise SystemExit(f"Mask not found: {mask_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    frames = sorted(frames_dir.glob(args.glob))
    if not frames:
        raise SystemExit(f"No frames found in {frames_dir} matching {args.glob}")

    usage_dir = Path(args.usage_dir).resolve() if args.usage_dir else None
    if usage_dir:
        usage_dir.mkdir(parents=True, exist_ok=True)

    total_frames = len(frames)
    if args.progress_mode == "gemini-nano-banana-2":
        estimated_total, basis = estimate_gemini_cost(total_frames, args.image_size)
        print(
            f"[budget] Gemini Nano Banana 2 will process {total_frames} frame(s). "
            f"Base estimated cost: {usd(estimated_total)}. {basis} "
            "Actual billed total may be slightly higher because prompt/input tokens are billed separately.",
            file=sys.stderr,
            flush=True,
        )
    elif args.progress_mode == "generic":
        print(f"[progress] Preparing to process {total_frames} frame(s).", file=sys.stderr, flush=True)

    jobs = []
    start_time = time.time()
    cumulative_prompt_tokens = 0
    cumulative_output_tokens = 0
    cumulative_cost = 0.0
    completed = 0
    progress_lock = threading.Lock()

    def process_one(index: int, frame: Path):
        output_frame = output_dir / frame.name
        usage_path = usage_dir / f"{frame.stem}.json" if usage_dir else None
        command = args.editor_cmd.format(
            input=str(frame),
            mask=str(mask_path),
            output=str(output_frame),
            index=index,
            usage_output=str(usage_path) if usage_path else "",
        )
        try:
            subprocess.run(shlex.split(command), check=True)
        except subprocess.CalledProcessError as exc:
            raise SystemExit(
                f"Frame editor failed on frame {frame.name} with exit code {exc.returncode}: {command}"
            ) from exc
        if not output_frame.exists():
            raise SystemExit(f"Editor command did not create expected output: {output_frame}")

        job = {
            "index": index,
            "input": str(frame),
            "mask": str(mask_path),
            "output": str(output_frame),
            "command": command,
        }
        return job, usage_path

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        future_map = {
            executor.submit(process_one, index, frame): (index, frame)
            for index, frame in enumerate(frames)
        }
        for future in concurrent.futures.as_completed(future_map):
            job, usage_path = future.result()
            with progress_lock:
                completed += 1

            if usage_path and usage_path.exists():
                usage_payload = load_usage(usage_path)
                prompt_tokens, output_tokens, frame_cost = usage_costs(usage_payload)
                cumulative_prompt_tokens += prompt_tokens
                cumulative_output_tokens += output_tokens
                cumulative_cost += frame_cost
                job["usage"] = usage_payload
                attempts, rejected_reasons = retry_summary(usage_payload)
                if attempts > 1:
                    job["self_improvement"] = {
                        "attempts": attempts,
                        "rejected_reasons": rejected_reasons,
                    }
                if args.progress_mode == "gemini-nano-banana-2":
                    elapsed = time.time() - start_time
                    retry_note = ""
                    if attempts > 1:
                        retry_note = f"; attempts={attempts}; rejected_reasons={','.join(rejected_reasons) or 'none'}"
                    print(
                        f"[progress] {completed}/{total_frames} frames done; "
                        f"frame={Path(job['input']).name}; elapsed={elapsed:.1f}s; "
                        f"cumulative_prompt_tokens={cumulative_prompt_tokens}; "
                        f"cumulative_output_tokens={cumulative_output_tokens}; "
                        f"estimated_spend_so_far={usd(cumulative_cost)}{retry_note}",
                        file=sys.stderr,
                        flush=True,
                    )
            elif args.progress_mode in {"generic", "gemini-nano-banana-2"}:
                elapsed = time.time() - start_time
                print(
                    f"[progress] {completed}/{total_frames} frames done; frame={Path(job['input']).name}; elapsed={elapsed:.1f}s",
                    file=sys.stderr,
                    flush=True,
                )

            jobs.append(job)

    manifest = {"jobs": jobs}
    if args.progress_mode == "gemini-nano-banana-2":
        manifest["billing"] = {
            "model": "gemini-3.1-flash-image-preview",
            "image_size": args.image_size,
            "estimated_prompt_tokens_total": cumulative_prompt_tokens,
            "estimated_output_tokens_total": cumulative_output_tokens,
            "estimated_spend_total_usd": round(cumulative_cost, 6),
        }
        print(
            f"[budget] Completed {total_frames} frame(s). "
            f"Estimated billed usage: prompt_tokens={cumulative_prompt_tokens}, "
            f"output_tokens={cumulative_output_tokens}, total={usd(cumulative_cost)}",
            file=sys.stderr,
            flush=True,
        )

    if args.manifest_output:
        manifest_path = Path(args.manifest_output)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(str(output_dir))


if __name__ == "__main__":
    main()
