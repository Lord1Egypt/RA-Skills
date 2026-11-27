#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROFILES = {"fast", "standard", "premium"}
STATUS_ORDER = ["planned", "created", "rendered", "read_back", "verified", "final"]
PROFILE_MIN_STATUS = {"fast": "created", "standard": "verified", "premium": "final"}
PROFILE_EDITABLE_THRESHOLDS = {"fast": 0.75, "standard": 0.9, "premium": 0.95}

REQUIRED_INTERNAL = {
    "fast": [
        "analysis/content-lock.md",
        "contracts/ppt-ir.json",
        "contracts/style-contract.json",
        "contracts/delivery-plan.json",
        "contracts/build-manifest.json",
    ],
    "standard": [
        "analysis/content-lock.md",
        "analysis/storyboard.md",
        "contracts/ppt-ir.json",
        "contracts/style-contract.json",
        "contracts/delivery-plan.json",
        "contracts/build-manifest.json",
        "qa/qa-report.json",
    ],
    "premium": [
        "analysis/content-lock.md",
        "analysis/storyboard.md",
        "contracts/ppt-ir.json",
        "contracts/style-contract.json",
        "contracts/asset-manifest.json",
        "contracts/delivery-plan.json",
        "contracts/build-manifest.json",
        "qa/qa-report.json",
        "renders/contact-sheet.png",
        "qa/benchmark-score.json",
    ],
}

REQUIRED_DELIVERY_ROLES = {
    "fast": ["pptx"],
    "standard": ["pptx", "preview_pdf", "verification_report"],
    "premium": ["pptx", "preview_pdf", "verification_report"],
}

ROLE_DEFAULTS = {
    "pptx": ("deck.pptx", ["outputs", "deck"]),
    "preview_pdf": ("deck-preview.pdf", ["outputs", "preview_pdf"]),
    "verification_report": ("verification-report.md", ["outputs", "verification_report"]),
    "assets": ("assets", ["outputs", "assets"]),
    "source_package": ("source-package", ["outputs", "source_package"]),
}

PRIVATE_PATTERNS = [
    ("DELIVERY_PRIVATE_PATH_LEAK", re.compile(r"(/Users/[^\s'\"<>]+|/tmp/[^\s'\"<>]+|[A-Za-z]:\\Users\\[^\s'\"<>]+)")),
    ("DELIVERY_SECRET_LEAK", re.compile(r"(?i)(api[_-]?key|secret|token|bearer)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")),
    ("DELIVERY_TEMP_FILE_INCLUDED", re.compile(r"(?i)(tmp|temp|debug|scratch)[/_-]")),
    ("DELIVERY_UNDECLARED_PRIVATE_ASSET", re.compile(r"(?i)(localhost|127\.0\.0\.1|file://|private|internal-only)")),
]


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def git_commit() -> str | None:
    """Return the Git HEAD of the PPTSmith source that produced this delivery."""
    try:
        completed = subprocess.run(
            ["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "HEAD"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value if re.fullmatch(r"[0-9a-f]{40}", value) else None


def load_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def status_at_least(status: str, expected: str) -> bool:
    if status == "failed":
        return False
    try:
        return STATUS_ORDER.index(status) >= STATUS_ORDER.index(expected)
    except ValueError:
        return False


def calculate_delivery_status(
    *,
    profile: str,
    build_manifest: dict[str, Any],
    qa_report: dict[str, Any] | None,
    benchmark_score: dict[str, Any] | None,
    pptx_path: Path | None = None,
) -> str:
    if profile not in PROFILES:
        raise ValueError(f"Unknown profile: {profile}")
    if build_manifest.get("status") == "failed" or build_manifest.get("failed_stage") or build_manifest.get("errors"):
        return "failed"
    stages = build_manifest.get("stages") if isinstance(build_manifest.get("stages"), dict) else {}
    metrics = merged_metrics(build_manifest, qa_report, benchmark_score)
    build_status = str(build_manifest.get("status", "planned"))
    deck_declared = bool(_get_nested(build_manifest, ["outputs", "deck"]))
    created = deck_declared or bool(stages.get("built")) or build_status in {"created", "rendered", "read_back", "verified", "final"}
    if not created:
        return "planned"

    render_status = _render_status(qa_report)
    rendered = bool(stages.get("rendered")) or render_status == "passed" or build_status in {"rendered", "final"}
    read_back = _inspection_succeeded(qa_report, pptx_path)

    qa_error_count = int(metrics.get("qa_error_count") or 0)
    qa_fatal_count = int(metrics.get("qa_fatal_count") or 0)
    whole_slide_raster_count = int(metrics.get("whole_slide_raster_count") or 0)
    editable_core_ratio = _float_or_default(metrics.get("editable_core_ratio"), 0.0)
    rubric_score = _float_or_default(metrics.get("rubric_score"), 0.0)
    rubric_trusted = bool(
        benchmark_score
        and benchmark_score.get("manual_review_required") is False
        and benchmark_score.get("overall_status") in {"passed", "warning"}
        and isinstance(benchmark_score.get("scorer"), dict)
        and benchmark_score["scorer"].get("type") in {"human_reference", "model"}
        and _rubric_binding_matches(benchmark_score, build_manifest, pptx_path, _render_report(qa_report))
    )
    fallbacks = build_manifest.get("fallbacks") if isinstance(build_manifest.get("fallbacks"), list) else []
    fallbacks_disclosed = all(isinstance(item, dict) and item.get("reason_codes") for item in fallbacks)

    if qa_error_count > 0 or qa_fatal_count > 0:
        return "failed"
    if not read_back:
        return "rendered" if rendered else "created"

    editable_ok = editable_core_ratio >= PROFILE_EDITABLE_THRESHOLDS[profile]
    base_verified = editable_ok and whole_slide_raster_count == 0
    if profile == "fast":
        return "verified" if base_verified else "read_back"
    if profile == "standard":
        return "verified" if base_verified else "read_back"

    premium_final = (
        rendered
        and read_back
        and base_verified
        and rubric_trusted
        and rubric_score >= 14
        and fallbacks_disclosed
        and render_status == "passed"
    )
    if premium_final:
        return "final"
    if rendered and read_back and base_verified:
        return "verified"
    return "read_back"


def merged_metrics(build_manifest: dict[str, Any], qa_report: dict[str, Any] | None, benchmark_score: dict[str, Any] | None) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for source in (build_manifest.get("metrics"), qa_report.get("metrics") if qa_report else None, benchmark_score):
        if isinstance(source, dict):
            metrics.update({key: value for key, value in source.items() if value is not None})
    if "rubric_score" not in metrics and benchmark_score:
        score = benchmark_score.get("total_score") or benchmark_score.get("rubric_score")
        if score is not None:
            metrics["rubric_score"] = score
    if qa_report and "qa_error_count" not in metrics:
        metrics["qa_error_count"] = sum(1 for issue in qa_report.get("issues", []) if isinstance(issue, dict) and issue.get("severity") == "error")
        metrics["qa_fatal_count"] = sum(1 for issue in qa_report.get("issues", []) if isinstance(issue, dict) and issue.get("severity") == "fatal")
    return metrics


def invalid_trust_ratios(metrics: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("editable_core_ratio", "native_text_ratio", "rasterized_area_ratio"):
        value = metrics.get(key)
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) or not 0.0 <= float(value) <= 1.0:
            errors.append(f"DELIVERY_INVALID_TRUST_RATIO: {key}={value!r}")
    return errors


def build_delivery_manifest(
    *,
    profile: str,
    status: str,
    build_manifest: dict[str, Any],
    qa_report: dict[str, Any] | None,
    benchmark_score: dict[str, Any] | None,
    files: list[dict[str, Any]],
    privacy: dict[str, Any],
    zip_path: Path | None,
    commit_sha: str | None,
) -> dict[str, Any]:
    renderer = {"name": None, "version": None}
    render_report = _render_report(qa_report)
    if isinstance(render_report, dict):
        renderer = {"name": render_report.get("engine"), "version": render_report.get("engine_version")}
    raw_builder = build_manifest.get("builder", "unknown")
    if isinstance(raw_builder, dict):
        builder_value = str(raw_builder.get("selected", "unknown"))
        builder_version = str(raw_builder.get("version") or build_manifest.get("builder_profile", "unknown"))
    else:
        builder_value = str(raw_builder)
        builder_version = str(build_manifest.get("builder_version", build_manifest.get("builder_profile", "unknown")))
    builder_entry = {
        "name": builder_value,
        "version": builder_version,
    }
    manifest = {
        "schema_version": "1.0",
        "deck_id": str(build_manifest.get("deck_id", "deck")),
        "build_id": str(build_manifest.get("build_id", "build")),
        "profile": profile,
        "status": status,
        "generated_at": iso_now(),
        "files": files,
        "builder": builder_entry,
        "renderer": renderer,
        "metrics": merged_metrics(build_manifest, qa_report, benchmark_score),
        "fallbacks": build_manifest.get("fallbacks", []) if isinstance(build_manifest.get("fallbacks"), list) else [],
        "known_limitations": known_limitations(build_manifest, qa_report, status),
        "privacy": privacy,
        "resume": {
            "resume_from": build_manifest.get("resume_from"),
            "last_successful_stage": build_manifest.get("last_successful_stage"),
            "failed_stage": build_manifest.get("failed_stage"),
            "checkpoints": "checkpoints/" if (Path(".ppt-work") / "checkpoints").exists() else None,
        },
    }
    if zip_path is not None:
        manifest["package_zip"] = {"path": zip_path.name, "hash": sha256_file(zip_path)}
    if commit_sha is not None:
        manifest["commit_sha"] = commit_sha
    return manifest


def known_limitations(build_manifest: dict[str, Any], qa_report: dict[str, Any] | None, status: str) -> list[str]:
    limitations = list(build_manifest.get("warnings", []) or [])
    if qa_report:
        for issue in qa_report.get("issues", []) or []:
            if isinstance(issue, dict) and issue.get("issue_code") == "RENDER_ENGINE_UNAVAILABLE":
                limitations.append("Renderer unavailable; visual status is capped honestly.")
    if status != "final":
        limitations.append(f"Trusted delivery status is {status}, not final.")
    return [str(item) for item in limitations]


def _render_report(qa_report: dict[str, Any] | None) -> dict[str, Any] | None:
    if not qa_report:
        return None
    evidence = qa_report.get("evidence")
    if isinstance(evidence, dict) and isinstance(evidence.get("render_report"), dict):
        return evidence["render_report"]
    return None


def _render_status(qa_report: dict[str, Any] | None) -> str:
    report = _render_report(qa_report)
    if isinstance(report, dict):
        return str(report.get("status", "not_run"))
    return "not_run"


def _inspection_succeeded(qa_report: dict[str, Any] | None, pptx_path: Path | None) -> bool:
    evidence = qa_report.get("evidence") if isinstance(qa_report, dict) else None
    inspection = evidence.get("structural_inspection") if isinstance(evidence, dict) else None
    if not isinstance(inspection, dict) or inspection.get("status") != "passed":
        return False
    expected = inspection.get("pptx_sha256")
    return bool(pptx_path and pptx_path.is_file() and isinstance(expected, str) and expected == sha256_file(pptx_path))


def _canonical_render_report(report: dict[str, Any]) -> dict[str, Any]:
    def clean(value: Any, key: str = "") -> Any:
        if isinstance(value, dict):
            return {name: clean(item, name) for name, item in sorted(value.items())}
        if isinstance(value, list):
            return [clean(item, key) for item in value]
        if isinstance(value, str) and key in {"pptx", "pdf", "pdf_path", "image"}:
            # Keep binding stable when trusted artifacts are relocated or
            # renamed during packaging. Their bytes are hashed separately.
            return f"<{key}>"
        return value
    return clean(report)


def _render_report_sha256(report: dict[str, Any]) -> str:
    data = json.dumps(_canonical_render_report(report), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _render_evidence_sha256(report: dict[str, Any]) -> str | None:
    slides = report.get("slides")
    if not isinstance(slides, list) or not slides:
        return None
    digest = hashlib.sha256()
    for item in sorted((item for item in slides if isinstance(item, dict)), key=lambda item: int(item.get("slide_index") or 0)):
        image = item.get("image")
        if not isinstance(image, str) or not Path(image).is_file():
            return None
        digest.update(str(item.get("slide_index")).encode("ascii"))
        digest.update(bytes.fromhex(sha256_file(Path(image)).split(":", 1)[1]))
    return "sha256:" + digest.hexdigest()


def _rubric_binding_matches(
    benchmark_score: dict[str, Any], build_manifest: dict[str, Any],
    pptx_path: Path | None, render_report: dict[str, Any] | None,
) -> bool:
    binding = benchmark_score.get("evidence_binding")
    return bool(
        isinstance(binding, dict)
        and pptx_path
        and pptx_path.is_file()
        and isinstance(render_report, dict)
        and render_report.get("status") == "passed"
        and benchmark_score.get("build_id") == build_manifest.get("build_id") == binding.get("build_id")
        and benchmark_score.get("deck_id") == build_manifest.get("deck_id") == binding.get("deck_id")
        and benchmark_score.get("case_id") == binding.get("case_id")
        and binding.get("pptx_sha256") == sha256_file(pptx_path)
        and binding.get("render_report_sha256") == _render_report_sha256(render_report)
        and binding.get("render_evidence_sha256") == _render_evidence_sha256(render_report)
    )


def _float_or_default(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _get_nested(data: dict[str, Any], keys: list[str]) -> Any:
    cursor: Any = data
    for key in keys:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(key)
    return cursor


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def pptx_readable(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
    except zipfile.BadZipFile:
        return False
    return "[Content_Types].xml" in names and "ppt/presentation.xml" in names


def resolve_role_path(role: str, build_manifest: dict[str, Any], workdir: Path) -> Path:
    default_name, keys = ROLE_DEFAULTS[role]
    raw = _get_nested(build_manifest, keys) or default_name
    path = Path(str(raw))
    candidates = []
    if path.is_absolute():
        candidates.append(path)
    else:
        candidates.extend([workdir / path, workdir / "builds" / "final" / path, workdir.parent / path])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def copy_artifact(role: str, source: Path, output: Path, *, required: bool) -> dict[str, Any]:
    target = output / (source.name if source.name else role)
    if source.is_dir():
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        hash_value = sha256_tree(target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        hash_value = sha256_file(target)
    return {"role": role, "path": target.name, "required": required, "hash": hash_value}


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(item.relative_to(path)).encode("utf-8"))
        digest.update(item.read_bytes())
    return "sha256:" + digest.hexdigest()


def scan_privacy(output: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        if path.suffix.lower() not in {".json", ".md", ".txt", ".xml", ".rels", ".html", ".csv"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path.relative_to(output))
        for code, pattern in PRIVATE_PATTERNS:
            if pattern.search(text) or pattern.search(rel):
                issues.append({"code": code, "file": rel})
    return {
        "contains_private_assets": any(issue["code"] == "DELIVERY_UNDECLARED_PRIVATE_ASSET" for issue in issues),
        "contains_external_links": False,
        "issues": issues,
    }


def write_zip(output: Path) -> Path:
    zip_path = output.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in output.rglob("*") if p.is_file()):
            archive.write(path, path.relative_to(output.parent))
    return zip_path


def package_delivery(args: argparse.Namespace) -> tuple[int, list[str]]:
    workdir = args.workdir
    profile = args.profile
    errors: list[str] = []
    build_path = workdir / "contracts" / "build-manifest.json"
    qa_path = workdir / "qa" / "qa-report.json"
    benchmark_path = workdir / "qa" / "benchmark-score.json"
    build_manifest = load_json(build_path)
    if not build_manifest:
        return 1, [f"Missing build manifest: {build_path}"]
    qa_report = load_json(qa_path)
    benchmark_score = load_json(benchmark_path)
    metrics = merged_metrics(build_manifest, qa_report, benchmark_score)
    if args.strict:
        errors.extend(invalid_trust_ratios(metrics))

    for rel in REQUIRED_INTERNAL[profile]:
        if not (workdir / rel).exists():
            errors.append(f"Missing required internal artifact: {rel}")

    status = calculate_delivery_status(
        profile=profile,
        build_manifest=build_manifest,
        qa_report=qa_report,
        benchmark_score=benchmark_score,
        pptx_path=resolve_role_path("pptx", build_manifest, workdir),
    )
    if args.strict and not status_at_least(status, PROFILE_MIN_STATUS[profile]):
        errors.append(f"Trusted status {status} does not meet {profile} requirement {PROFILE_MIN_STATUS[profile]}")

    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    staging = output.parent / f".{output.name}.staging-{os.getpid()}"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    files: list[dict[str, Any]] = []
    roles = list(REQUIRED_DELIVERY_ROLES[profile])
    # Standard visual rendering is best-effort by contract. Do not invent a PDF
    # when the verifier truthfully reports that no renderer ran; Premium still
    # requires it and remains non-final/blocked.
    if profile == "standard" and _render_status(qa_report) in {"not_run", "unavailable"}:
        roles.remove("preview_pdf")
    if args.include_assets:
        roles.append("assets")
    if args.include_sources:
        roles.append("source_package")
    for role in roles:
        source = resolve_role_path(role, build_manifest, workdir)
        required = role in REQUIRED_DELIVERY_ROLES[profile]
        if not source.exists():
            if required:
                errors.append(f"Missing required delivery file for {role}: {source}")
            continue
        if role == "pptx" and not pptx_readable(source):
            errors.append(f"PPTX package is not readable: {source}")
        files.append(copy_artifact(role, source, staging, required=required))

    privacy = scan_privacy(staging)
    if args.strict and privacy["issues"]:
        for item in privacy["issues"]:
            errors.append(f"{item['code']}: {item['file']}")

    if errors:
        shutil.rmtree(staging, ignore_errors=True)
        return 1, errors

    zip_path = write_zip(staging) if args.zip else None
    manifest = build_delivery_manifest(
        profile=profile,
        status=status,
        build_manifest=build_manifest,
        qa_report=qa_report,
        benchmark_score=benchmark_score,
        files=files,
        privacy=privacy,
        zip_path=zip_path,
        commit_sha=git_commit(),
    )
    manifest_in_output = args.manifest.parent.resolve() == output
    staged_manifest = staging / args.manifest.name if manifest_in_output else staging / "delivery-manifest.json"
    staged_manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    # The manifest must not claim a hash for itself. Rewriting the file after
    # computing that hash changes its bytes, so a self-entry can never be
    # truthful. External release checksums may cover the manifest as a whole.
    staging.replace(output)
    if not manifest_in_output:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output / staged_manifest.name, args.manifest)
    return 0, []


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package article-html-to-ppt user-facing delivery files and manifest.")
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--zip", action="store_true")
    parser.add_argument("--include-assets", action="store_true")
    parser.add_argument("--include-sources", action="store_true")
    parser.add_argument("--keep-workdir", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--resume-from")
    parser.add_argument("--json-output", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args: argparse.Namespace | None = None
    try:
        args = parse_args(argv)
        code, errors = package_delivery(args)
        if args.json_output:
            print(json.dumps({"ok": code == 0, "errors": errors}, indent=2))
        else:
            for error in errors:
                print(error, file=sys.stderr)
        return code
    except Exception as exc:
        if args is not None:
            shutil.rmtree(args.output, ignore_errors=True)
            for staging in args.output.resolve().parent.glob(f".{args.output.name}.staging-*"):
                shutil.rmtree(staging, ignore_errors=True)
        print(f"package_delivery: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
