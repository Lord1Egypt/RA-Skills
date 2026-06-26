#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from io import BytesIO
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image, ImageChops, ImageOps, ImageStat

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_IMAGE_SIZE = "1K"
DEFAULT_REQUEST_RETRIES = 3
BASE_PROMPT = (
    "This is a frame from a phone screen recording. "
    "Image 1 is the original frame. "
    "Image 2 is a binary mask. White mask areas mark unwanted overlays such as screen-recording UI, icons, "
    "counters, labels, text, watermarks, or other surface elements that should be removed. "
    "Black mask areas should stay unchanged. "
    "Keep the visible scene outside the white mask as close to the original frame as possible. "
    "Do not add, remove, duplicate, or invent animals, people, objects, or background elements. "
    "Do not change the subject count, pose, position, identity, or motion. "
    "Use your judgment inside the white mask to reconstruct the most natural original-looking underlying image content, "
    "but make the smallest necessary edit and avoid changing anything outside the masked overlay regions. "
    "Return exactly one cleaned image."
)
PROMPT_ADDONS = {
    "outside_mask_change": (
        "Do not modify any visible content outside the white mask. "
        "The hamster, wheel, bedding, bowl, and cage structure must stay identical outside the masked overlay regions."
    ),
    "flat_mask_fill": (
        "Do not replace the masked area with flat black, flat white, a blank panel, or any solid fill. "
        "Reconstruct natural scene texture and detail that matches nearby visible content."
    ),
    "no_output_image": (
        "This is an image editing task, not a planning task. "
        "Return exactly one edited image and no other modality."
    ),
}


def ensure_uploadable_mask(mask_path: Path) -> Path:
    if mask_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        return mask_path

    temp_dir = Path(tempfile.mkdtemp(prefix="gemini-mask-"))
    converted = temp_dir / "mask.png"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(mask_path),
            str(converted),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return converted


def load_images(input_path: Path, mask_path: Path) -> tuple[Image.Image, Image.Image]:
    input_image = Image.open(input_path).convert("RGB")
    mask_image = Image.open(mask_path).convert("L")
    if mask_image.size != input_image.size:
        mask_image = mask_image.resize(input_image.size, Image.Resampling.NEAREST)
    return input_image, mask_image


def build_prompt(base_prompt: str, extra_reasons: list[str]) -> str:
    parts = [base_prompt]
    for reason in extra_reasons:
        addon = PROMPT_ADDONS.get(reason)
        if addon and addon not in parts:
            parts.append(addon)
    return " ".join(parts)


def count_changed_pixels(diff_gray: Image.Image, allowed_mask: Image.Image, threshold: int = 18) -> float:
    diff_values = diff_gray.load()
    mask_values = allowed_mask.load()
    width, height = diff_gray.size
    changed = 0
    total = 0
    for y in range(height):
        for x in range(width):
            if mask_values[x, y] == 0:
                continue
            total += 1
            if diff_values[x, y] > threshold:
                changed += 1
    return 0.0 if total == 0 else changed / total


def normalize_candidate(original: Image.Image, candidate: Image.Image) -> Image.Image:
    candidate_rgb = candidate.convert("RGB")
    if candidate_rgb.size != original.size:
        candidate_rgb = candidate_rgb.resize(original.size, Image.Resampling.LANCZOS)
    return candidate_rgb


def composite_masked_candidate(original: Image.Image, mask_image: Image.Image, candidate_rgb: Image.Image) -> Image.Image:
    # Always preserve the unmasked area from the source frame so the model can only alter masked regions.
    return Image.composite(candidate_rgb, original, mask_image)


def validate_candidate(
    original: Image.Image,
    mask_image: Image.Image,
    candidate: Image.Image,
) -> tuple[bool, list[str], dict, Image.Image]:
    candidate_rgb = normalize_candidate(original, candidate)
    inverse_mask = ImageOps.invert(mask_image)
    raw_diff = ImageChops.difference(original, candidate_rgb)
    raw_outside_mean = sum(ImageStat.Stat(raw_diff, inverse_mask).mean) / 3.0
    raw_diff_gray = ImageOps.grayscale(raw_diff)
    raw_outside_changed_ratio = count_changed_pixels(raw_diff_gray, inverse_mask)

    composited = composite_masked_candidate(original, mask_image, candidate_rgb)
    composited_diff = ImageChops.difference(original, composited)
    composited_diff_gray = ImageOps.grayscale(composited_diff)
    outside_mean = sum(ImageStat.Stat(composited_diff, inverse_mask).mean) / 3.0
    outside_changed_ratio = count_changed_pixels(composited_diff_gray, inverse_mask)

    masked_gray = ImageOps.grayscale(composited)
    masked_stats = ImageStat.Stat(masked_gray, mask_image)
    masked_mean = masked_stats.mean[0]
    masked_stddev = masked_stats.stddev[0]

    reasons = []
    if outside_mean > 10.0 or outside_changed_ratio > 0.015:
        reasons.append("outside_mask_change")
    if masked_stddev < 7.5 and (masked_mean < 25 or masked_mean > 230):
        reasons.append("flat_mask_fill")

    metrics = {
        "raw_outside_mean_diff": round(raw_outside_mean, 4),
        "raw_outside_changed_ratio": round(raw_outside_changed_ratio, 6),
        "outside_mean_diff": round(outside_mean, 4),
        "outside_changed_ratio": round(outside_changed_ratio, 6),
        "masked_mean_luma": round(masked_mean, 4),
        "masked_stddev_luma": round(masked_stddev, 4),
        "candidate_size": list(candidate.size),
        "output_size_after_normalization": list(candidate_rgb.size),
    }
    return len(reasons) == 0, reasons, metrics, composited


def response_to_json(response: types.GenerateContentResponse) -> dict:
    return response.model_dump(mode="json") if hasattr(response, "model_dump") else {}


def extract_first_image(response: types.GenerateContentResponse, target_size: tuple[int, int]) -> Image.Image | None:
    candidates = response.candidates or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and inline_data.data:
                image = Image.open(BytesIO(inline_data.data)).convert("RGB")
                if image.size != target_size:
                    image = image.resize(target_size, Image.Resampling.LANCZOS)
                return image
    return None


def aggregate_usage(attempts: list[dict], model: str, image_size: str) -> dict:
    prompt_total = 0
    candidate_total = 0
    total_total = 0
    for attempt in attempts:
        usage = attempt.get("usage_metadata") or {}
        prompt_total += int(usage.get("prompt_token_count") or 0)
        candidate_total += int(usage.get("candidates_token_count") or 0)
        total_total += int(usage.get("total_token_count") or 0)
    return {
        "model": model,
        "image_size": image_size,
        "usage_metadata": {
            "prompt_token_count": prompt_total,
            "candidates_token_count": candidate_total,
            "total_token_count": total_total,
        },
        "attempts": attempts,
    }


def is_retryable_request_error(exc: Exception) -> bool:
    message = str(exc).upper()
    return any(token in message for token in ["500", "502", "503", "504", "429", "INTERNAL", "UNAVAILABLE"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Edit a frame with Gemini Nano Banana 2 using an input frame and a binary mask.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--mask", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--image-size", default=os.environ.get("GEMINI_IMAGE_SIZE", DEFAULT_IMAGE_SIZE))
    parser.add_argument("--prompt", default=BASE_PROMPT)
    parser.add_argument("--prompt-addendum", default="")
    parser.add_argument("--api-key-env", default="GEMINI_API_KEY")
    parser.add_argument("--emit-response-json")
    parser.add_argument("--usage-output")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--request-retries", type=int, default=DEFAULT_REQUEST_RETRIES)
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(
            f"Missing API key. Set {args.api_key_env} before using Gemini Nano Banana 2.",
            file=sys.stderr,
        )
        return 2

    input_path = Path(args.input).resolve()
    mask_path = Path(args.mask).resolve()
    output_path = Path(args.output).resolve()
    if not input_path.exists():
        print(f"Input frame not found: {input_path}", file=sys.stderr)
        return 2
    if not mask_path.exists():
        print(f"Mask not found: {mask_path}", file=sys.stderr)
        return 2

    upload_mask_path = ensure_uploadable_mask(mask_path)
    original_image, mask_image = load_images(input_path, upload_mask_path)
    target_size = original_image.size

    client = genai.Client(api_key=api_key)
    failure_reasons: list[str] = []
    attempt_logs: list[dict] = []
    final_response_json = {}
    base_prompt = args.prompt
    if args.prompt_addendum.strip():
        base_prompt = f"{base_prompt} {args.prompt_addendum.strip()}"

    for attempt_index in range(1, args.max_attempts + 1):
        prompt = base_prompt if attempt_index == 1 else build_prompt(base_prompt, failure_reasons)
        parts = [
            types.Part.from_text(text=prompt),
            types.Part.from_bytes(data=input_path.read_bytes(), mime_type="image/png"),
            types.Part.from_bytes(data=upload_mask_path.read_bytes(), mime_type="image/png"),
        ]

        response = None
        last_exc: Exception | None = None
        for request_attempt in range(1, max(1, args.request_retries) + 1):
            try:
                response = client.models.generate_content(
                    model=args.model,
                    contents=[types.Content(role="user", parts=parts)],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                    ),
                )
                last_exc = None
                break
            except Exception as exc:
                last_exc = exc
                if request_attempt >= max(1, args.request_retries) or not is_retryable_request_error(exc):
                    break
                time.sleep(min(6, 1.5 * request_attempt))

        if response is None:
            print(f"Gemini request failed: {last_exc}", file=sys.stderr)
            return 1

        response_json = response_to_json(response)
        final_response_json = response_json
        usage_metadata = response_json.get("usage_metadata") or {}

        candidate_image = extract_first_image(response, target_size)
        if candidate_image is None:
            failure_reasons = list(dict.fromkeys(failure_reasons + ["no_output_image"]))
            attempt_logs.append(
                {
                    "attempt": attempt_index,
                    "status": "failed",
                    "reasons": ["no_output_image"],
                    "usage_metadata": usage_metadata,
                }
            )
            continue

        is_valid, reasons, metrics, final_image = validate_candidate(original_image, mask_image, candidate_image)
        attempt_logs.append(
            {
                "attempt": attempt_index,
                "status": "accepted" if is_valid else "rejected",
                "reasons": reasons,
                "metrics": metrics,
                "usage_metadata": usage_metadata,
            }
        )
        if is_valid:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            final_image.save(output_path, format="PNG")
            if args.emit_response_json:
                Path(args.emit_response_json).write_text(json.dumps(final_response_json, indent=2) + "\n", encoding="utf-8")
            if args.usage_output:
                usage_payload = aggregate_usage(attempt_logs, args.model, args.image_size)
                Path(args.usage_output).write_text(json.dumps(usage_payload, indent=2, default=str) + "\n", encoding="utf-8")
            print(str(output_path))
            return 0

        failure_reasons = list(dict.fromkeys(failure_reasons + reasons))

    if args.emit_response_json:
        Path(args.emit_response_json).write_text(json.dumps(final_response_json, indent=2) + "\n", encoding="utf-8")
    if args.usage_output:
        usage_payload = aggregate_usage(attempt_logs, args.model, args.image_size)
        Path(args.usage_output).write_text(json.dumps(usage_payload, indent=2, default=str) + "\n", encoding="utf-8")

    print(
        f"Gemini response did not pass validation after {args.max_attempts} attempt(s). "
        f"Reasons seen: {', '.join(failure_reasons) if failure_reasons else 'unknown'}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
