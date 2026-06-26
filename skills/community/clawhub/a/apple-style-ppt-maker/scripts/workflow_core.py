#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-genai>=1.0.0",
#   "pillow>=10.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""Shared utilities for the open-apple-style-ppt-maker skill."""

from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from shutil import copy2
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args: Any, **_kwargs: Any) -> bool:
        return False

DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_RESOLUTION = "2K"
DEFAULT_FORMAT = "webp"
ALLOWED_RESOLUTIONS = {"2K", "4K"}
ALLOWED_FORMATS = {"webp", "png", "jpg", "jpeg"}
ALLOWED_ASPECT_RATIO = "16:9"


class PlanValidationError(ValueError):
    """Raised when slides_plan.json does not satisfy the strict contract."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def find_and_load_env(plan_path: Path) -> Path | None:
    """Load the first discovered .env file from common locations."""
    script_dir = Path(__file__).resolve().parent
    candidates: list[Path] = [
        Path.cwd() / ".env",
        script_dir / ".env",
        plan_path.parent / ".env",
    ]
    candidates.extend(parent / ".env" for parent in plan_path.parent.parents)
    candidates.append(Path.home() / ".codex" / "skills" / "open-apple-style-ppt-maker" / ".env")

    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            load_dotenv(candidate, override=False)
            return candidate

    load_dotenv(override=False)
    return None


def load_plan(plan_path: Path) -> dict[str, Any]:
    if not plan_path.exists():
        raise PlanValidationError(f"Plan file not found: {plan_path}")
    payload = read_json(plan_path)
    validate_plan(payload)
    payload["slides"] = sorted(payload["slides"], key=lambda item: item["slide_number"])
    return payload


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise PlanValidationError(message)


def _expect_object(obj: Any, path: str) -> dict[str, Any]:
    _expect(isinstance(obj, dict), f"{path} must be an object")
    return obj


def _expect_list(obj: Any, path: str) -> list[Any]:
    _expect(isinstance(obj, list), f"{path} must be an array")
    return obj


def _expect_string(obj: Any, path: str, max_len: int = 300) -> str:
    _expect(isinstance(obj, str), f"{path} must be a string")
    value = obj.strip()
    _expect(bool(value), f"{path} must not be empty")
    _expect(len(value) <= max_len, f"{path} must be <= {max_len} chars")
    return value


def _expect_string_list(
    obj: Any,
    path: str,
    min_items: int = 1,
    max_items: int = 12,
    item_max_len: int = 240,
) -> list[str]:
    items = _expect_list(obj, path)
    _expect(min_items <= len(items) <= max_items, f"{path} must contain {min_items}..{max_items} items")
    out: list[str] = []
    for index, item in enumerate(items, start=1):
        out.append(_expect_string(item, f"{path}[{index}]", max_len=item_max_len))
    return out


def _expect_keys(obj: dict[str, Any], path: str, required: set[str], optional: set[str] | None = None) -> None:
    optional = optional or set()
    keys = set(obj.keys())
    missing = required - keys
    extra = keys - (required | optional)
    _expect(not missing, f"{path} missing key(s): {', '.join(sorted(missing))}")
    _expect(not extra, f"{path} has unsupported key(s): {', '.join(sorted(extra))}")


def validate_plan(plan: dict[str, Any]) -> None:
    root = _expect_object(plan, "plan")
    _expect_keys(root, "plan", {"project", "global_style_tokens", "slides", "output"})

    project = _expect_object(root["project"], "project")
    _expect_keys(project, "project", {"title", "language", "audience", "objective"}, {"subtitle"})
    _expect_string(project["title"], "project.title", max_len=160)
    _expect_string(project["language"], "project.language", max_len=32)
    _expect_string(project["audience"], "project.audience", max_len=200)
    _expect_string(project["objective"], "project.objective", max_len=260)
    if "subtitle" in project:
        _expect_string(project["subtitle"], "project.subtitle", max_len=200)

    tokens = _expect_object(root["global_style_tokens"], "global_style_tokens")
    _expect_keys(
        tokens,
        "global_style_tokens",
        {"aesthetic", "palette", "type_scale", "spacing_scale", "layout_system", "motion_rule"},
        {"icon_style", "image_style"},
    )
    _expect_string(tokens["aesthetic"], "global_style_tokens.aesthetic", max_len=200)
    _expect_string(tokens["spacing_scale"], "global_style_tokens.spacing_scale", max_len=120)
    _expect_string(tokens["layout_system"], "global_style_tokens.layout_system", max_len=120)
    _expect_string(tokens["motion_rule"], "global_style_tokens.motion_rule", max_len=120)
    if "icon_style" in tokens:
        _expect_string(tokens["icon_style"], "global_style_tokens.icon_style", max_len=120)
    if "image_style" in tokens:
        _expect_string(tokens["image_style"], "global_style_tokens.image_style", max_len=120)

    palette = _expect_object(tokens["palette"], "global_style_tokens.palette")
    _expect_keys(
        palette,
        "global_style_tokens.palette",
        {"background", "surface", "text_primary", "text_secondary", "accent"},
    )
    for key in ("background", "surface", "text_primary", "text_secondary", "accent"):
        _expect_string(palette[key], f"global_style_tokens.palette.{key}", max_len=30)

    type_scale = _expect_object(tokens["type_scale"], "global_style_tokens.type_scale")
    _expect_keys(type_scale, "global_style_tokens.type_scale", {"h1", "h2", "body", "caption"})
    for key in ("h1", "h2", "body", "caption"):
        _expect_string(type_scale[key], f"global_style_tokens.type_scale.{key}", max_len=50)

    slides = _expect_list(root["slides"], "slides")
    _expect(len(slides) > 0, "slides must not be empty")
    numbers: list[int] = []

    for idx, slide in enumerate(slides, start=1):
        slide_obj = _expect_object(slide, f"slides[{idx}]")
        _expect_keys(
            slide_obj,
            f"slides[{idx}]",
            {
                "slide_number",
                "slide_type",
                "objective",
                "on_slide_text",
                "visual_blueprint",
                "consistency_checks",
            },
        )

        number = slide_obj["slide_number"]
        _expect(isinstance(number, int), f"slides[{idx}].slide_number must be an integer")
        _expect(number > 0, f"slides[{idx}].slide_number must be > 0")
        numbers.append(number)

        _expect_string(slide_obj["slide_type"], f"slides[{idx}].slide_type", max_len=40)
        _expect_string(slide_obj["objective"], f"slides[{idx}].objective", max_len=260)

        on_slide = _expect_object(slide_obj["on_slide_text"], f"slides[{idx}].on_slide_text")
        _expect_keys(
            on_slide,
            f"slides[{idx}].on_slide_text",
            {"title"},
            {"subtitle", "body", "bullets", "stats", "footer", "callout"},
        )
        _expect_string(on_slide["title"], f"slides[{idx}].on_slide_text.title", max_len=120)
        if "subtitle" in on_slide:
            _expect_string(on_slide["subtitle"], f"slides[{idx}].on_slide_text.subtitle", max_len=180)
        if "body" in on_slide:
            _expect_string(on_slide["body"], f"slides[{idx}].on_slide_text.body", max_len=600)
        if "footer" in on_slide:
            _expect_string(on_slide["footer"], f"slides[{idx}].on_slide_text.footer", max_len=120)
        if "callout" in on_slide:
            _expect_string(on_slide["callout"], f"slides[{idx}].on_slide_text.callout", max_len=120)
        if "bullets" in on_slide:
            _expect_string_list(
                on_slide["bullets"],
                f"slides[{idx}].on_slide_text.bullets",
                min_items=1,
                max_items=8,
                item_max_len=140,
            )
        if "stats" in on_slide:
            _expect_string_list(
                on_slide["stats"],
                f"slides[{idx}].on_slide_text.stats",
                min_items=1,
                max_items=8,
                item_max_len=120,
            )

        visual = _expect_object(slide_obj["visual_blueprint"], f"slides[{idx}].visual_blueprint")
        _expect_keys(
            visual,
            f"slides[{idx}].visual_blueprint",
            {"composition", "key_elements", "imagery_hint", "avoid"},
            {"chart_hint"},
        )
        _expect_string(visual["composition"], f"slides[{idx}].visual_blueprint.composition", max_len=220)
        _expect_string(visual["imagery_hint"], f"slides[{idx}].visual_blueprint.imagery_hint", max_len=220)
        _expect_string_list(
            visual["key_elements"],
            f"slides[{idx}].visual_blueprint.key_elements",
            min_items=1,
            max_items=10,
            item_max_len=120,
        )
        _expect_string_list(
            visual["avoid"],
            f"slides[{idx}].visual_blueprint.avoid",
            min_items=1,
            max_items=10,
            item_max_len=120,
        )
        if "chart_hint" in visual:
            _expect_string(visual["chart_hint"], f"slides[{idx}].visual_blueprint.chart_hint", max_len=180)

        checks = _expect_object(slide_obj["consistency_checks"], f"slides[{idx}].consistency_checks")
        _expect_keys(checks, f"slides[{idx}].consistency_checks", {"must_keep", "must_avoid"})
        _expect_string_list(
            checks["must_keep"],
            f"slides[{idx}].consistency_checks.must_keep",
            min_items=1,
            max_items=10,
            item_max_len=140,
        )
        _expect_string_list(
            checks["must_avoid"],
            f"slides[{idx}].consistency_checks.must_avoid",
            min_items=1,
            max_items=10,
            item_max_len=140,
        )

    _expect(len(set(numbers)) == len(numbers), "slides.slide_number must be unique")
    sorted_numbers = sorted(numbers)
    expected_numbers = list(range(1, len(numbers) + 1))
    _expect(sorted_numbers == expected_numbers, "slides.slide_number must be a consecutive sequence starting at 1")

    output = _expect_object(root["output"], "output")
    _expect_keys(output, "output", {"aspect_ratio", "resolution", "format"}, {"output_dir"})
    _expect(output["aspect_ratio"] == ALLOWED_ASPECT_RATIO, "output.aspect_ratio must be 16:9")
    _expect(output["resolution"] in ALLOWED_RESOLUTIONS, "output.resolution must be one of: 2K, 4K")
    _expect(str(output["format"]).lower() in ALLOWED_FORMATS, "output.format must be one of: webp, png, jpg, jpeg")
    if "output_dir" in output:
        _expect_string(output["output_dir"], "output.output_dir", max_len=400)


def resolve_output_settings(
    plan: dict[str, Any],
    resolution_override: str | None,
    format_override: str | None,
) -> tuple[str, str]:
    resolution = (resolution_override or plan["output"]["resolution"] or DEFAULT_RESOLUTION).strip().upper()
    image_format = (format_override or plan["output"]["format"] or DEFAULT_FORMAT).strip().lower()

    if resolution not in ALLOWED_RESOLUTIONS:
        raise PlanValidationError(f"Unsupported resolution: {resolution}")
    if image_format not in ALLOWED_FORMATS:
        raise PlanValidationError(f"Unsupported format: {image_format}")

    return resolution, image_format


def resolve_output_dir(plan: dict[str, Any], output_dir_override: str | None) -> Path:
    if output_dir_override:
        output_dir = Path(output_dir_override)
    else:
        from_plan = plan["output"].get("output_dir")
        if from_plan:
            output_dir = Path(from_plan)
        else:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("outputs") / stamp

    if not output_dir.is_absolute():
        output_dir = (Path.cwd() / output_dir).resolve()

    return output_dir


def ensure_output_layout(output_dir: Path) -> dict[str, Path]:
    images = output_dir / "images"
    prompts = output_dir / "prompts"
    meta = output_dir / "meta"
    history = output_dir / "history"
    for directory in (output_dir, images, prompts, meta, history):
        directory.mkdir(parents=True, exist_ok=True)
    return {
        "root": output_dir,
        "images": images,
        "prompts": prompts,
        "meta": meta,
        "history": history,
        "manifest": output_dir / "deck_manifest.json",
    }


def get_api_key() -> str:
    key = os.getenv("APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "Missing API key. Set APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY or GEMINI_API_KEY."
        )
    return key


def get_genai_client():
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("google-genai is not installed. Run: pip install google-genai pillow python-dotenv") from exc
    return genai.Client(api_key=get_api_key())


def _extract_image_from_response(response: Any, image_path: Path) -> None:
    parts = getattr(response, "parts", None) or []
    for part in parts:
        if getattr(part, "inline_data", None) is not None:
            image = part.as_image()
            image.save(image_path)
            return

    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        candidate_parts = getattr(content, "parts", None) or []
        for part in candidate_parts:
            if getattr(part, "inline_data", None) is not None:
                image = part.as_image()
                image.save(image_path)
                return

    raise RuntimeError("Model response does not contain image data.")


def render_slide_image(
    client: Any,
    prompt: str,
    image_path: Path,
    resolution: str,
    model: str,
    retries: int = 3,
) -> None:
    from google.genai import types

    last_error: Exception | None = None
    image_path.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=ALLOWED_ASPECT_RATIO, image_size=resolution),
                ),
            )
            _extract_image_from_response(response, image_path)
            return
        except Exception as exc:  # pragma: no cover - depends on remote API behavior
            last_error = exc
            if attempt < retries:
                time.sleep(2**attempt)

    raise RuntimeError(f"Failed to generate image after {retries} attempts: {last_error}")


def _serialize_on_slide_text(on_slide_text: dict[str, Any]) -> str:
    lines: list[str] = [f'Title: "{on_slide_text["title"]}"']
    if "subtitle" in on_slide_text:
        lines.append(f'Subtitle: "{on_slide_text["subtitle"]}"')
    if "body" in on_slide_text:
        lines.append(f'Body: "{on_slide_text["body"]}"')
    if "bullets" in on_slide_text:
        lines.append("Bullets:")
        lines.extend(f'- "{item}"' for item in on_slide_text["bullets"])
    if "stats" in on_slide_text:
        lines.append("Stats:")
        lines.extend(f'- "{item}"' for item in on_slide_text["stats"])
    if "callout" in on_slide_text:
        lines.append(f'Callout: "{on_slide_text["callout"]}"')
    if "footer" in on_slide_text:
        lines.append(f'Footer: "{on_slide_text["footer"]}"')
    return "\n".join(lines)


def build_slide_prompt(
    plan: dict[str, Any],
    slide: dict[str, Any],
    total_slides: int,
    resolution: str,
    image_format: str,
    revision_note: str | None = None,
) -> str:
    project = plan["project"]
    tokens = plan["global_style_tokens"]
    visual = slide["visual_blueprint"]
    checks = slide["consistency_checks"]

    output_lines = [
        "You are an expert presentation designer.",
        "Generate exactly one slide image with a premium Apple-style minimalist aesthetic.",
        "",
        "Hard visual constraints:",
        "- Keep the same visual system across the full deck.",
        "- Use large whitespace and clear visual hierarchy.",
        "- Keep typography clean, precise, and highly legible.",
        "- Avoid neon effects, noisy textures, excessive gradients, and heavy glassmorphism.",
        "- Do not add extra logos, watermarks, or fake UI text.",
        "",
        f'Deck title: "{project["title"]}"',
        f'Deck audience: "{project["audience"]}"',
        f'Deck objective: "{project["objective"]}"',
        f'Deck language: "{project["language"]}"',
        f"Slide number: {slide['slide_number']} of {total_slides}",
        f'Slide type: "{slide["slide_type"]}"',
        f'Slide objective: "{slide["objective"]}"',
        "",
        "Global style tokens:",
        f'- aesthetic: "{tokens["aesthetic"]}"',
        f'- palette: background {tokens["palette"]["background"]}, surface {tokens["palette"]["surface"]}, '
        f'text_primary {tokens["palette"]["text_primary"]}, text_secondary {tokens["palette"]["text_secondary"]}, '
        f'accent {tokens["palette"]["accent"]}',
        f'- type_scale: h1 {tokens["type_scale"]["h1"]}, h2 {tokens["type_scale"]["h2"]}, '
        f'body {tokens["type_scale"]["body"]}, caption {tokens["type_scale"]["caption"]}',
        f'- spacing_scale: "{tokens["spacing_scale"]}"',
        f'- layout_system: "{tokens["layout_system"]}"',
        f'- motion_rule: "{tokens["motion_rule"]}"',
    ]

    if tokens.get("icon_style"):
        output_lines.append(f'- icon_style: "{tokens["icon_style"]}"')
    if tokens.get("image_style"):
        output_lines.append(f'- image_style: "{tokens["image_style"]}"')

    output_lines.extend(
        [
            "",
            "Text content (render text exactly as provided):",
            _serialize_on_slide_text(slide["on_slide_text"]),
            "",
            "Visual blueprint:",
            f'- composition: "{visual["composition"]}"',
            f'- imagery_hint: "{visual["imagery_hint"]}"',
            "- key_elements:",
        ]
    )
    output_lines.extend(f'  - "{item}"' for item in visual["key_elements"])
    if visual.get("chart_hint"):
        output_lines.append(f'- chart_hint: "{visual["chart_hint"]}"')
    output_lines.append("- avoid:")
    output_lines.extend(f'  - "{item}"' for item in visual["avoid"])

    output_lines.extend(
        [
            "",
            "Consistency checks:",
            "- must_keep:",
        ]
    )
    output_lines.extend(f'  - "{item}"' for item in checks["must_keep"])
    output_lines.append("- must_avoid:")
    output_lines.extend(f'  - "{item}"' for item in checks["must_avoid"])

    output_lines.extend(
        [
            "",
            f"Output requirements: one {ALLOWED_ASPECT_RATIO} slide image, resolution {resolution}, format {image_format}.",
        ]
    )

    if revision_note:
        output_lines.extend(
            [
                "",
                "Revision instruction for this generation:",
                revision_note.strip(),
                "",
                "Preserve the same deck-level style tokens while applying this revision only to the target slide.",
            ]
        )

    return "\n".join(output_lines).strip() + "\n"


def init_manifest(plan: dict[str, Any], resolution: str, image_format: str, model: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "project": plan["project"],
        "output": {
            "aspect_ratio": ALLOWED_ASPECT_RATIO,
            "resolution": resolution,
            "format": image_format,
            "model": model,
        },
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "slides": [],
    }


def load_or_init_manifest(
    manifest_path: Path,
    plan: dict[str, Any],
    resolution: str,
    image_format: str,
    model: str,
) -> dict[str, Any]:
    if manifest_path.exists():
        data = read_json(manifest_path)
        if isinstance(data, dict) and isinstance(data.get("slides"), list):
            return data
    return init_manifest(plan, resolution, image_format, model)


def find_manifest_slide(manifest: dict[str, Any], slide_number: int) -> dict[str, Any] | None:
    for item in manifest.get("slides", []):
        if item.get("slide_number") == slide_number:
            return item
    return None


def upsert_manifest_slide(manifest: dict[str, Any], slide_record: dict[str, Any]) -> None:
    slides = manifest.setdefault("slides", [])
    for index, item in enumerate(slides):
        if item.get("slide_number") == slide_record.get("slide_number"):
            slides[index] = slide_record
            manifest["updated_at"] = utc_now_iso()
            return
    slides.append(slide_record)
    slides.sort(key=lambda value: value["slide_number"])
    manifest["updated_at"] = utc_now_iso()


def snapshot_if_exists(path: Path, snapshot_dir: Path, suffix: str) -> Path | None:
    if not path.exists():
        return None
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / f"{path.stem}.{suffix}{path.suffix}"
    copy2(path, snapshot_path)
    return snapshot_path


def get_slide_by_number(slides: list[dict[str, Any]], slide_number: int) -> dict[str, Any]:
    for slide in slides:
        if slide["slide_number"] == slide_number:
            return slide
    raise PlanValidationError(f"Slide {slide_number} not found in plan.")
