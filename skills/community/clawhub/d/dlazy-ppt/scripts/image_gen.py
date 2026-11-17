#!/usr/bin/env python3
"""CLI for dlazy-ppt slide image generation and editing via the dLazy tool API.

Every slide image this skill produces goes through here. Generation runs on
dLazy's hosted `gpt-image-2`; the skill talks to the tool API over HTTP with a
dLazy API key and never calls a model provider directly.

Reads DLAZY_API_KEY, and optionally DLAZY_BASE_URL for self-hosted deployments
and DLAZY_PPT_IMAGE_MODEL to pin a different dLazy image tool.
"""

from __future__ import annotations

import argparse
import asyncio
from io import BytesIO
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

import dlazy_client

DEFAULT_MODEL = "gpt-image-2"
# 16:9 at the largest size the tool offers below 4K. Slides are always 16:9, and
# the deck is assembled at this resolution, so a non-16:9 default would letterbox
# every page.
DEFAULT_SIZE = "2048x1152"
DEFAULT_QUALITY = "medium"
DEFAULT_OUTPUT_FORMAT = "png"
DEFAULT_CONCURRENCY = 5
DEFAULT_DOWNSCALE_SUFFIX = "-web"
DEFAULT_OUTPUT_PATH = "output/imagegen/output.png"

# Mirrors the tool's declared input schema. The API rejects anything else with a
# 400, so reject it locally where the message can name the allowed values.
ALLOWED_SIZES = {
    "1024x1024",
    "1536x1024",
    "1024x1536",
    "2048x2048",
    "2048x1152",
    "3840x2160",
    "2160x3840",
    "auto",
}
SIZES_16_9 = ("2048x1152", "3840x2160")
ALLOWED_QUALITIES = {"low", "medium", "high"}
ALLOWED_FORMATS = {"png", "jpeg", "webp"}

# The tool caps `prompt` at 2000 characters and rejects the whole call when it is
# exceeded. Slide prompts carry style plus content and get close, so this is
# checked before spending a call.
MAX_PROMPT_CHARS = 2000
MAX_INPUT_IMAGES = 5

MAX_IMAGE_BYTES = 50 * 1024 * 1024
MAX_BATCH_JOBS = 500
DEFAULT_RUNTIME_HOME = "~/.dlazy-ppt"
ENV_FIELDS = ("DLAZY_API_KEY", "DLAZY_BASE_URL", "DLAZY_PPT_IMAGE_MODEL")


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def _runtime_home() -> Path:
    return Path(os.getenv("DLAZY_PPT_HOME", DEFAULT_RUNTIME_HOME)).expanduser()


def _runtime_env_path() -> Path:
    return _runtime_home() / ".env"


def _load_runtime_env() -> None:
    path = _runtime_env_path()
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in ENV_FIELDS or os.getenv(key):
            continue
        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


def _default_model() -> str:
    return os.getenv("DLAZY_PPT_IMAGE_MODEL", DEFAULT_MODEL)


def _api_target_label() -> str:
    return f"dLazy tool API ({dlazy_client.base_url()})"


def _runtime_python_path() -> str:
    home = _runtime_home()
    if os.name == "nt":
        return str(home / ".venv" / "Scripts" / "python.exe")
    return str(home / ".venv" / "bin" / "python")


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _dependency_hint(package: str, *, upgrade: bool = False) -> str:
    package_arg = f"-U {package}" if upgrade else package
    runtime_python = _runtime_python_path()
    requirements = _skill_root() / "requirements.txt"
    return (
        "Install dlazy-ppt dependencies in the shared runtime first, for example "
        f"`python3 {_skill_root() / 'scripts' / 'dlazy_ppt_runtime.py'} bootstrap`, "
        f"or install {package} directly with `{runtime_python} -m pip install "
        f"{package_arg}`. Requirements file: `{requirements}`."
    )


def _ensure_api_key(dry_run: bool) -> None:
    if dlazy_client.api_key():
        print(f"DLAZY_API_KEY is set. API target: {_api_target_label()}.", file=sys.stderr)
        return
    if dry_run:
        _warn(f"DLAZY_API_KEY is not set; dry-run only. API target: {_api_target_label()}.")
        return
    runtime_script = _skill_root() / "scripts" / "dlazy_ppt_runtime.py"
    config_doc = _skill_root() / "docs" / "image-model-configuration.md"
    _die(
        "DLAZY_API_KEY is not set.\n"
        f"Get a key from {dlazy_client.API_KEY_URL}, then configure the shared runtime once:\n"
        f'  python3 {runtime_script} config --api-key "your-dlazy-api-key"\n'
        f"Details: {config_doc}"
    )


def _read_prompt(prompt: Optional[str], prompt_file: Optional[str]) -> str:
    if prompt and prompt_file:
        _die("Use --prompt or --prompt-file, not both.")
    if prompt_file:
        if prompt_file == "-":
            return sys.stdin.read().strip()
        path = Path(prompt_file)
        if not path.exists():
            _die(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8").strip()
    if prompt:
        return prompt.strip()
    _die("Missing prompt. Use --prompt or --prompt-file.")
    return ""  # unreachable


def _check_image_paths(paths: Iterable[str]) -> List[Path]:
    resolved: List[Path] = []
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            _die(f"Image file not found: {path}")
        if path.stat().st_size > MAX_IMAGE_BYTES:
            _warn(f"Image exceeds 50MB limit: {path}")
        resolved.append(path)
    return resolved


def _normalize_output_format(fmt: Optional[str]) -> str:
    if not fmt:
        return DEFAULT_OUTPUT_FORMAT
    fmt = fmt.lower()
    if fmt == "jpg":
        fmt = "jpeg"
    if fmt not in ALLOWED_FORMATS:
        _die("output-format must be png, jpeg, jpg, or webp.")
    return fmt


def _validate_size(size: str) -> None:
    if size in ALLOWED_SIZES:
        return
    _die(
        f"size must be one of {', '.join(sorted(ALLOWED_SIZES))}. "
        f"Slides are 16:9, so use {' or '.join(SIZES_16_9)}."
    )


def _validate_quality(quality: str) -> None:
    if quality not in ALLOWED_QUALITIES:
        _die("quality must be one of low, medium, high.")


def _validate_prompt(prompt: str) -> None:
    """Reject an over-long prompt here rather than paying for a 400.

    The prompt cannot be split the way narration can — half a slide description
    renders half a slide — so an over-long prompt has to be shortened by the
    caller, and saying so is more useful than truncating silently.
    """
    if len(prompt) > MAX_PROMPT_CHARS:
        _die(
            f"prompt is {len(prompt)} characters; the image tool accepts at most "
            f"{MAX_PROMPT_CHARS}. Shorten the slide description or drop optional "
            "prompt fields (--scene, --materials, --negative)."
        )


def _validate_generate_payload(payload: Dict[str, Any]) -> None:
    n = int(payload.get("n", 1))
    if n < 1 or n > 10:
        _die("n must be between 1 and 10")
    _validate_size(str(payload.get("size", DEFAULT_SIZE)))
    _validate_quality(str(payload.get("quality", DEFAULT_QUALITY)))
    _validate_prompt(str(payload.get("prompt", "")))


def _tool_input(payload: Dict[str, Any], image_urls: Optional[List[str]] = None) -> Dict[str, Any]:
    """Translate the internal payload into the tool's declared input schema.

    `n` stays out of it: the tool renders one image per call, so repeat counts
    are handled by calling it repeatedly.
    """
    tool_input: Dict[str, Any] = {
        "prompt": payload["prompt"],
        "size": payload.get("size", DEFAULT_SIZE),
        "quality": payload.get("quality", DEFAULT_QUALITY),
        "imageFormat": payload.get("output_format", DEFAULT_OUTPUT_FORMAT),
    }
    if image_urls:
        tool_input["images"] = image_urls
    return tool_input


def _generate_images(payload: Dict[str, Any], image_urls: Optional[List[str]] = None) -> List[bytes]:
    """Render `n` images, one tool call each."""
    model = str(payload.get("model", DEFAULT_MODEL))
    tool_input = _tool_input(payload, image_urls)
    images: List[bytes] = []
    for _ in range(int(payload.get("n", 1))):
        images.extend(dlazy_client.generate_images(model, tool_input))
    return images


def _is_transient_error(exc: Exception) -> bool:
    """Whether a failed call is worth retrying.

    Rate limits and server-side hiccups clear on their own; a rejected prompt or
    a missing API key never will, and retrying those just burns the batch.
    """
    msg = str(exc).lower()
    if "429" in msg or "rate limit" in msg or "too many requests" in msg:
        return True
    if "timeout" in msg or "timed out" in msg or "connection reset" in msg:
        return True
    return any(f" ({code}" in msg for code in (500, 502, 503, 504))


async def _generate_with_retries(
    payload: Dict[str, Any],
    *,
    attempts: int,
    job_label: str,
) -> List[bytes]:
    last_exc: Optional[Exception] = None
    for attempt in range(1, attempts + 1):
        try:
            # The client is synchronous; a thread per in-flight job keeps the
            # batch concurrent without pulling in an async HTTP stack.
            return await asyncio.to_thread(_generate_images, payload)
        except Exception as exc:
            last_exc = exc
            if not _is_transient_error(exc) or attempt == attempts:
                raise
            sleep_s = min(60.0, 2.0**attempt)
            print(
                f"{job_label} attempt {attempt}/{attempts} failed ({exc}); "
                f"retrying in {sleep_s:.1f}s",
                file=sys.stderr,
            )
            await asyncio.sleep(sleep_s)
    raise last_exc or RuntimeError("unknown error")


def _upload_input_images(image_paths: List[Path]) -> List[str]:
    """Put local reference images where the model can read them."""
    if len(image_paths) > MAX_INPUT_IMAGES:
        _die(f"at most {MAX_INPUT_IMAGES} input images are supported, got {len(image_paths)}.")
    urls = []
    for path in image_paths:
        print(f"Uploading {path}", file=sys.stderr)
        urls.append(dlazy_client.upload_file(path))
    return urls


def _build_output_paths(
    out: str,
    output_format: str,
    count: int,
    out_dir: Optional[str],
) -> List[Path]:
    ext = "." + output_format

    if out_dir:
        out_base = Path(out_dir)
        out_base.mkdir(parents=True, exist_ok=True)
        return [out_base / f"image_{i}{ext}" for i in range(1, count + 1)]

    out_path = Path(out)
    if out_path.exists() and out_path.is_dir():
        out_path.mkdir(parents=True, exist_ok=True)
        return [out_path / f"image_{i}{ext}" for i in range(1, count + 1)]

    if out_path.suffix == "":
        out_path = out_path.with_suffix(ext)
    elif output_format and out_path.suffix.lstrip(".").lower() != output_format:
        _warn(
            f"Output extension {out_path.suffix} does not match output-format {output_format}."
        )

    if count == 1:
        return [out_path]

    return [
        out_path.with_name(f"{out_path.stem}-{i}{out_path.suffix}")
        for i in range(1, count + 1)
    ]


def _augment_prompt(args: argparse.Namespace, prompt: str) -> str:
    fields = _fields_from_args(args)
    return _augment_prompt_fields(args.augment, prompt, fields)


def _augment_prompt_fields(augment: bool, prompt: str, fields: Dict[str, Optional[str]]) -> str:
    if not augment:
        return prompt

    sections: List[str] = []
    if fields.get("use_case"):
        sections.append(f"Use case: {fields['use_case']}")
    sections.append(f"Primary request: {prompt}")
    if fields.get("scene"):
        sections.append(f"Scene/background: {fields['scene']}")
    if fields.get("subject"):
        sections.append(f"Subject: {fields['subject']}")
    if fields.get("style"):
        sections.append(f"Style/medium: {fields['style']}")
    if fields.get("composition"):
        sections.append(f"Composition/framing: {fields['composition']}")
    if fields.get("lighting"):
        sections.append(f"Lighting/mood: {fields['lighting']}")
    if fields.get("palette"):
        sections.append(f"Color palette: {fields['palette']}")
    if fields.get("materials"):
        sections.append(f"Materials/textures: {fields['materials']}")
    if fields.get("text"):
        sections.append(f"Text (verbatim): \"{fields['text']}\"")
    if fields.get("constraints"):
        sections.append(f"Constraints: {fields['constraints']}")
    if fields.get("negative"):
        sections.append(f"Avoid: {fields['negative']}")

    return "\n".join(sections)


def _fields_from_args(args: argparse.Namespace) -> Dict[str, Optional[str]]:
    return {
        "use_case": getattr(args, "use_case", None),
        "scene": getattr(args, "scene", None),
        "subject": getattr(args, "subject", None),
        "style": getattr(args, "style", None),
        "composition": getattr(args, "composition", None),
        "lighting": getattr(args, "lighting", None),
        "palette": getattr(args, "palette", None),
        "materials": getattr(args, "materials", None),
        "text": getattr(args, "text", None),
        "constraints": getattr(args, "constraints", None),
        "negative": getattr(args, "negative", None),
    }


def _print_request(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _derive_downscale_path(path: Path, suffix: str) -> Path:
    if suffix and not suffix.startswith("-") and not suffix.startswith("_"):
        suffix = "-" + suffix
    return path.with_name(f"{path.stem}{suffix}{path.suffix}")


def _downscale_image_bytes(image_bytes: bytes, *, max_dim: int, output_format: str) -> bytes:
    try:
        from PIL import Image
    except Exception:
        _die(f"Downscaling requires Pillow. {_dependency_hint('pillow')}")

    if max_dim < 1:
        _die("--downscale-max-dim must be >= 1")

    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        w, h = img.size
        scale = min(1.0, float(max_dim) / float(max(w, h)))
        target = (max(1, int(round(w * scale))), max(1, int(round(h * scale))))

        resized = img if target == (w, h) else img.resize(target, Image.Resampling.LANCZOS)

        fmt = output_format.lower()
        if fmt == "jpg":
            fmt = "jpeg"

        if fmt == "jpeg":
            if resized.mode in ("RGBA", "LA") or ("transparency" in getattr(resized, "info", {})):
                bg = Image.new("RGB", resized.size, (255, 255, 255))
                bg.paste(resized.convert("RGBA"), mask=resized.convert("RGBA").split()[-1])
                resized = bg
            else:
                resized = resized.convert("RGB")

        out = BytesIO()
        resized.save(out, format=fmt.upper())
        return out.getvalue()


def _write_and_downscale(
    images: List[bytes],
    outputs: List[Path],
    *,
    force: bool,
    downscale_max_dim: Optional[int],
    downscale_suffix: str,
    output_format: str,
) -> None:
    for idx, raw in enumerate(images):
        if idx >= len(outputs):
            break
        out_path = outputs[idx]
        if out_path.exists() and not force:
            _die(f"Output already exists: {out_path} (use --force to overwrite)")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        out_path.write_bytes(raw)
        print(f"Wrote {out_path}")

        if downscale_max_dim is None:
            continue

        derived = _derive_downscale_path(out_path, downscale_suffix)
        if derived.exists() and not force:
            _die(f"Output already exists: {derived} (use --force to overwrite)")
        derived.parent.mkdir(parents=True, exist_ok=True)
        resized = _downscale_image_bytes(raw, max_dim=downscale_max_dim, output_format=output_format)
        derived.write_bytes(resized)
        print(f"Wrote {derived}")


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:60] if value else "job"


def _normalize_job(job: Any, idx: int) -> Dict[str, Any]:
    if isinstance(job, str):
        prompt = job.strip()
        if not prompt:
            _die(f"Empty prompt at job {idx}")
        return {"prompt": prompt}
    if isinstance(job, dict):
        if "prompt" not in job or not str(job["prompt"]).strip():
            _die(f"Missing prompt for job {idx}")
        return job
    _die(f"Invalid job at index {idx}: expected string or object.")
    return {}  # unreachable


def _read_jobs_jsonl(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        _die(f"Input file not found: {p}")
    jobs: List[Dict[str, Any]] = []
    for line_no, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            item: Any
            if line.startswith("{"):
                item = json.loads(line)
            else:
                item = line
            jobs.append(_normalize_job(item, idx=line_no))
        except json.JSONDecodeError as exc:
            _die(f"Invalid JSON on line {line_no}: {exc}")
    if not jobs:
        _die("No jobs found in input file.")
    if len(jobs) > MAX_BATCH_JOBS:
        _die(f"Too many jobs ({len(jobs)}). Max is {MAX_BATCH_JOBS}.")
    return jobs


def _merge_non_null(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(dst)
    for k, v in src.items():
        if v is not None:
            merged[k] = v
    return merged


def _job_output_paths(
    *,
    out_dir: Path,
    output_format: str,
    idx: int,
    prompt: str,
    n: int,
    explicit_out: Optional[str],
) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = "." + output_format

    if explicit_out:
        base = Path(explicit_out)
        if base.suffix == "":
            base = base.with_suffix(ext)
        elif base.suffix.lstrip(".").lower() != output_format:
            _warn(
                f"Job {idx}: output extension {base.suffix} does not match output-format {output_format}."
            )
        base = out_dir / base.name
    else:
        slug = _slugify(prompt[:80])
        base = out_dir / f"{idx:03d}-{slug}{ext}"

    if n == 1:
        return [base]
    return [
        base.with_name(f"{base.stem}-{i}{base.suffix}")
        for i in range(1, n + 1)
    ]


async def _run_generate_batch(args: argparse.Namespace) -> int:
    jobs = _read_jobs_jsonl(args.input)
    out_dir = Path(args.out_dir)

    base_fields = _fields_from_args(args)
    base_payload = {
        "model": args.model,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
    }

    if args.dry_run:
        for i, job in enumerate(jobs, start=1):
            prompt = str(job["prompt"]).strip()
            fields = _merge_non_null(base_fields, job.get("fields", {}))
            # Allow flat job keys as well (use_case, scene, etc.)
            fields = _merge_non_null(fields, {k: job.get(k) for k in base_fields.keys()})
            augmented = _augment_prompt_fields(args.augment, prompt, fields)

            job_payload = dict(base_payload)
            job_payload["prompt"] = augmented
            job_payload = _merge_non_null(job_payload, {k: job.get(k) for k in base_payload.keys()})
            job_payload = {k: v for k, v in job_payload.items() if v is not None}

            _validate_generate_payload(job_payload)
            effective_output_format = _normalize_output_format(job_payload.get("output_format"))
            job_payload["output_format"] = effective_output_format

            n = int(job_payload.get("n", 1))
            outputs = _job_output_paths(
                out_dir=out_dir,
                output_format=effective_output_format,
                idx=i,
                prompt=prompt,
                n=n,
                explicit_out=job.get("out"),
            )
            downscaled = None
            if args.downscale_max_dim is not None:
                downscaled = [
                    str(_derive_downscale_path(p, args.downscale_suffix)) for p in outputs
                ]
            _print_request(
                {
                    "endpoint": f"{dlazy_client.base_url()}/api/cli/tool",
                    "job": i,
                    "model": job_payload["model"],
                    "calls": n,
                    "outputs": [str(p) for p in outputs],
                    "outputs_downscaled": downscaled,
                    "input": _tool_input(job_payload),
                }
            )
        return 0

    sem = asyncio.Semaphore(args.concurrency)

    any_failed = False

    async def run_job(i: int, job: Dict[str, Any]) -> Tuple[int, Optional[str]]:
        nonlocal any_failed
        prompt = str(job["prompt"]).strip()
        job_label = f"[job {i}/{len(jobs)}]"

        fields = _merge_non_null(base_fields, job.get("fields", {}))
        fields = _merge_non_null(fields, {k: job.get(k) for k in base_fields.keys()})
        augmented = _augment_prompt_fields(args.augment, prompt, fields)

        payload = dict(base_payload)
        payload["prompt"] = augmented
        payload = _merge_non_null(payload, {k: job.get(k) for k in base_payload.keys()})
        payload = {k: v for k, v in payload.items() if v is not None}

        n = int(payload.get("n", 1))
        _validate_generate_payload(payload)
        effective_output_format = _normalize_output_format(payload.get("output_format"))
        payload["output_format"] = effective_output_format
        outputs = _job_output_paths(
            out_dir=out_dir,
            output_format=effective_output_format,
            idx=i,
            prompt=prompt,
            n=n,
            explicit_out=job.get("out"),
        )
        try:
            async with sem:
                print(f"{job_label} starting", file=sys.stderr)
                started = time.time()
                images = await _generate_with_retries(
                    payload,
                    attempts=args.max_attempts,
                    job_label=job_label,
                )
                elapsed = time.time() - started
                print(f"{job_label} completed in {elapsed:.1f}s", file=sys.stderr)
            _write_and_downscale(
                images,
                outputs,
                force=args.force,
                downscale_max_dim=args.downscale_max_dim,
                downscale_suffix=args.downscale_suffix,
                output_format=effective_output_format,
            )
            return i, None
        except Exception as exc:
            any_failed = True
            print(f"{job_label} failed: {exc}", file=sys.stderr)
            if args.fail_fast:
                raise
            return i, str(exc)

    tasks = [asyncio.create_task(run_job(i, job)) for i, job in enumerate(jobs, start=1)]

    try:
        await asyncio.gather(*tasks)
    except Exception:
        for t in tasks:
            if not t.done():
                t.cancel()
        raise

    return 1 if any_failed else 0


def _generate_batch(args: argparse.Namespace) -> None:
    exit_code = asyncio.run(_run_generate_batch(args))
    if exit_code:
        raise SystemExit(exit_code)


def _generate(args: argparse.Namespace) -> None:
    prompt = _read_prompt(args.prompt, args.prompt_file)
    prompt = _augment_prompt(args, prompt)

    payload = {
        "model": args.model,
        "prompt": prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    output_format = _normalize_output_format(args.output_format)
    payload["output_format"] = output_format
    _validate_prompt(prompt)
    output_paths = _build_output_paths(args.out, output_format, args.n, args.out_dir)
    downscaled = None
    if args.downscale_max_dim is not None:
        downscaled = [str(_derive_downscale_path(p, args.downscale_suffix)) for p in output_paths]

    if args.dry_run:
        _print_request(
            {
                "endpoint": f"{dlazy_client.base_url()}/api/cli/tool",
                "model": payload["model"],
                "calls": int(payload.get("n", 1)),
                "outputs": [str(p) for p in output_paths],
                "outputs_downscaled": downscaled,
                "input": _tool_input(payload),
            }
        )
        return

    print(
        "Calling the dLazy image tool (generation). This can take up to a couple of minutes.",
        file=sys.stderr,
    )
    started = time.time()
    images = _generate_images(payload)
    elapsed = time.time() - started
    print(f"Generation completed in {elapsed:.1f}s.", file=sys.stderr)

    _write_and_downscale(
        images,
        output_paths,
        force=args.force,
        downscale_max_dim=args.downscale_max_dim,
        downscale_suffix=args.downscale_suffix,
        output_format=output_format,
    )


def _edit(args: argparse.Namespace) -> None:
    prompt = _read_prompt(args.prompt, args.prompt_file)
    prompt = _augment_prompt(args, prompt)

    image_paths = _check_image_paths(args.image)

    payload = {
        "model": args.model,
        "prompt": prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    output_format = _normalize_output_format(args.output_format)
    payload["output_format"] = output_format
    _validate_prompt(prompt)
    output_paths = _build_output_paths(args.out, output_format, args.n, args.out_dir)
    downscaled = None
    if args.downscale_max_dim is not None:
        downscaled = [str(_derive_downscale_path(p, args.downscale_suffix)) for p in output_paths]

    if args.dry_run:
        preview_input = _tool_input(payload, [str(p) for p in image_paths])
        _print_request(
            {
                "endpoint": f"{dlazy_client.base_url()}/api/cli/tool",
                "model": payload["model"],
                "calls": int(payload.get("n", 1)),
                "outputs": [str(p) for p in output_paths],
                "outputs_downscaled": downscaled,
                "note": "local paths under `images` are uploaded and replaced by their URLs",
                "input": preview_input,
            }
        )
        return

    print(
        f"Calling the dLazy image tool (edit) with {len(image_paths)} image(s).",
        file=sys.stderr,
    )
    started = time.time()
    image_urls = _upload_input_images(image_paths)
    images = _generate_images(payload, image_urls)

    elapsed = time.time() - started
    print(f"Edit completed in {elapsed:.1f}s.", file=sys.stderr)
    _write_and_downscale(
        images,
        output_paths,
        force=args.force,
        downscale_max_dim=args.downscale_max_dim,
        downscale_suffix=args.downscale_suffix,
        output_format=output_format,
    )


def _add_shared_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", default=_default_model())
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--size", default=DEFAULT_SIZE, choices=sorted(ALLOWED_SIZES))
    parser.add_argument("--quality", default=DEFAULT_QUALITY, choices=sorted(ALLOWED_QUALITIES))
    parser.add_argument("--output-format")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--out-dir")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--augment", dest="augment", action="store_true")
    parser.add_argument("--no-augment", dest="augment", action="store_false")
    parser.set_defaults(augment=True)

    # Prompt augmentation hints
    parser.add_argument("--use-case")
    parser.add_argument("--scene")
    parser.add_argument("--subject")
    parser.add_argument("--style")
    parser.add_argument("--composition")
    parser.add_argument("--lighting")
    parser.add_argument("--palette")
    parser.add_argument("--materials")
    parser.add_argument("--text")
    parser.add_argument("--constraints")
    parser.add_argument("--negative")

    # Post-processing (optional): generate an additional downscaled copy for fast web loading.
    parser.add_argument("--downscale-max-dim", type=int)
    parser.add_argument("--downscale-suffix", default=DEFAULT_DOWNSCALE_SUFFIX)


def main() -> int:
    _load_runtime_env()
    parser = argparse.ArgumentParser(
        description="Generate or edit slide images through the dLazy tool API"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate", help="Create a new image")
    _add_shared_args(gen_parser)
    gen_parser.set_defaults(func=_generate)

    batch_parser = subparsers.add_parser(
        "generate-batch",
        help="Generate multiple prompts concurrently (JSONL input)",
    )
    _add_shared_args(batch_parser)
    batch_parser.add_argument("--input", required=True, help="Path to JSONL file (one job per line)")
    batch_parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    batch_parser.add_argument("--max-attempts", type=int, default=3)
    batch_parser.add_argument("--fail-fast", action="store_true")
    batch_parser.set_defaults(func=_generate_batch)

    edit_parser = subparsers.add_parser("edit", help="Edit an existing image")
    _add_shared_args(edit_parser)
    edit_parser.add_argument("--image", action="append", required=True)
    edit_parser.set_defaults(func=_edit)

    args = parser.parse_args()
    if args.n < 1 or args.n > 10:
        _die("--n must be between 1 and 10")
    if getattr(args, "concurrency", 1) < 1 or getattr(args, "concurrency", 1) > 25:
        _die("--concurrency must be between 1 and 25")
    if getattr(args, "max_attempts", 3) < 1 or getattr(args, "max_attempts", 3) > 10:
        _die("--max-attempts must be between 1 and 10")
    if args.command == "generate-batch" and not args.out_dir:
        _die("generate-batch requires --out-dir")
    if getattr(args, "downscale_max_dim", None) is not None and args.downscale_max_dim < 1:
        _die("--downscale-max-dim must be >= 1")

    _validate_size(args.size)
    _validate_quality(args.quality)
    _ensure_api_key(args.dry_run)

    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
