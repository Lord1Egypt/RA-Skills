#!/usr/bin/env python3
"""Prepare optional ChatGPT ZIP batches and safely import returned archives."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import stat
import zipfile
from argparse import Namespace
from pathlib import Path, PurePosixPath
from typing import Any

from handoff_common import load_json, save_json, sha256_file, utc_now
from ingest_images import import_image


BATCH_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
RESUMABLE_STATUSES = {"queued", "failed", "needs_revision"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
MAX_ARCHIVE_FILES = 100
MAX_UNCOMPRESSED_BYTES = 300 * 1024 * 1024


def batch_root(handoff: Path, batch_id: str) -> Path:
    return handoff / "batches" / batch_id


def select_jobs(state: dict[str, Any], job_ids: list[str]) -> list[dict[str, Any]]:
    jobs = state.get("jobs", [])
    by_id = {job.get("job_id"): job for job in jobs}
    selected_ids = job_ids or [
        job["job_id"] for job in jobs if job.get("status") in RESUMABLE_STATUSES
    ]
    if not selected_ids:
        raise SystemExit("No resumable jobs selected")
    if len(set(selected_ids)) != len(selected_ids):
        raise SystemExit("Duplicate --job-id values are not allowed")
    missing = [job_id for job_id in selected_ids if job_id not in by_id]
    if missing:
        raise SystemExit(f"Unknown job ids: {', '.join(missing)}")
    selected = [by_id[job_id] for job_id in selected_ids]
    invalid = [
        job["job_id"] for job in selected if job.get("status") not in RESUMABLE_STATUSES
    ]
    if invalid:
        raise SystemExit(
            "ZIP batches only accept queued, failed, or needs_revision jobs: "
            + ", ".join(invalid)
        )
    return selected


def make_work_prompt(
    state: dict[str, Any],
    manifest: dict[str, Any],
    handoff: Path,
) -> str:
    job_sections: list[str] = []
    for job in manifest["jobs"]:
        prompt = (handoff / job["prompt_file"]).read_text(encoding="utf-8").strip()
        job_sections.append(f"## Job file: {job['prompt_file']}\n\n{prompt}")
    sections = "\n\n---\n\n".join(job_sections)
    filenames = "\n".join(f"- `{job['intended_filename']}`" for job in manifest["jobs"])
    return f"""# Optional ChatGPT native image ZIP batch

Run: `{state['run_id']}`
Batch: `{manifest['batch_id']}`

Create exactly {manifest['job_count']} independent image files from the job specifications below.
Native ChatGPT image generation is mandatory for every PNG. Render the approved readable text directly in each image.
Keep the visual series coherent, but do not combine jobs into a collage or contact sheet.

Do not replace native image generation with Python, Pillow, SVG, HTML, Canvas, code-generated graphics, deterministic rendering, screenshots, or placeholders. If the native image tool cannot generate every requested file in this batch, stop and list the missing filenames. A smaller native-image retry is preferable to a programmatically drawn substitute.

## Required image files

{filenames}

## Delivery contract

1. Generate every image as a separate file with the exact requested filename and aspect ratio.
2. Check each image against its approved readable-text list. Do not silently replace a failed image with a placeholder or programmatic graphic.
3. Create `qa-report.json` with one object per job containing `job_id`, `filename`, `status`, and `notes`.
4. Include a copy of `batch-manifest.json` using the manifest supplied after the jobs.
5. Put only the requested images, `qa-report.json`, and `batch-manifest.json` in one folder.
6. Compress that folder as `{manifest['archive_name']}` and attach the ZIP as the final deliverable.
7. If ZIP delivery or any image fails, report the exact missing filenames so the caller can resume only those jobs.

Local visual QA remains authoritative. Your `qa-report.json` is evidence, not automatic approval.

---

{sections}

---

## batch-manifest.json

```json
{json.dumps(manifest, ensure_ascii=False, indent=2)}
```
"""


def prepare_batch(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    batch_id = args.batch_id.strip()
    if not BATCH_ID_PATTERN.fullmatch(batch_id):
        raise SystemExit(f"Unsafe batch id: {batch_id}")
    selected = select_jobs(state, args.job_id)
    root = batch_root(handoff, batch_id)
    root.mkdir(parents=True, exist_ok=True)
    archive_name = args.archive_name or f"{batch_id}.zip"
    if Path(archive_name).name != archive_name or Path(archive_name).suffix.lower() != ".zip":
        raise SystemExit("--archive-name must be a .zip basename")

    jobs: list[dict[str, Any]] = []
    for job in selected:
        prompt_path = handoff / job["prompt_file"]
        if not prompt_path.is_file():
            raise SystemExit(f"Missing prompt file: {prompt_path}")
        jobs.append(
            {
                "job_id": job["job_id"],
                "prompt_file": job["prompt_file"],
                "prompt_sha256": sha256_file(prompt_path),
                "intended_filename": job["intended_filename"],
                "dimensions": job["dimensions"],
                "reference_paths": job.get("reference_paths", []),
            }
        )

    manifest = {
        "schema_version": 1,
        "run_id": state["run_id"],
        "batch_id": batch_id,
        "delivery_mode": "chatgpt_native_zip_optional",
        "archive_name": archive_name,
        "job_count": len(jobs),
        "created_at": utc_now(),
        "jobs": jobs,
    }
    manifest_path = root / "batch-manifest.json"
    save_json(manifest_path, manifest)
    prompt_path = root / "work-prompt.md"
    prompt_path.write_text(make_work_prompt(state, manifest, handoff), encoding="utf-8")

    batches = state.setdefault("zip_batches", {})
    batches[batch_id] = {
        "status": "prepared",
        "delivery_mode": "chatgpt_native_zip_optional",
        "archive_name": archive_name,
        "manifest_file": str(manifest_path.relative_to(handoff)),
        "prompt_file": str(prompt_path.relative_to(handoff)),
        "job_ids": [job["job_id"] for job in jobs],
        "prepared_at": utc_now(),
        "import": {},
    }
    for job in selected:
        job["zip_batch_id"] = batch_id
        job["delivery_mode"] = "chatgpt_native_zip_optional"
    state["updated_at"] = utc_now()
    save_json(state_path, state)
    print(manifest_path)
    print(prompt_path)


def safe_archive_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = [member for member in archive.infolist() if not member.is_dir()]
    if len(members) > MAX_ARCHIVE_FILES:
        raise SystemExit(f"Archive contains too many files: {len(members)}")
    total_size = sum(member.file_size for member in members)
    if total_size > MAX_UNCOMPRESSED_BYTES:
        raise SystemExit(f"Archive expands beyond {MAX_UNCOMPRESSED_BYTES} bytes")
    for member in members:
        path = PurePosixPath(member.filename)
        if path.is_absolute() or ".." in path.parts:
            raise SystemExit(f"Unsafe archive path: {member.filename}")
        if member.flag_bits & 0x1:
            raise SystemExit(f"Encrypted archive member is not supported: {member.filename}")
        mode = (member.external_attr >> 16) & 0xFFFF
        if mode and stat.S_ISLNK(mode):
            raise SystemExit(f"Archive symlink is not allowed: {member.filename}")
    return members


def import_batch(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    batch = state.get("zip_batches", {}).get(args.batch_id)
    if not batch:
        raise SystemExit(f"Unknown ZIP batch: {args.batch_id}")
    manifest_path = handoff / batch["manifest_file"]
    manifest = load_json(manifest_path)
    source_archive = args.archive.expanduser().resolve()
    if not source_archive.is_file():
        raise SystemExit(f"Archive not found: {source_archive}")

    archive_checksum = sha256_file(source_archive)
    inbox_root = handoff / "inbox" / "zip-batches" / args.batch_id / archive_checksum[:12]
    inbox_root.mkdir(parents=True, exist_ok=True)
    preserved_archive = inbox_root / source_archive.name
    if not preserved_archive.exists():
        shutil.copy2(source_archive, preserved_archive)

    expected = {job["intended_filename"]: job for job in manifest["jobs"]}
    extracted: dict[str, Path] = {}
    metadata_files: dict[str, Path] = {}
    ignored: list[str] = []
    with zipfile.ZipFile(source_archive) as archive:
        members = safe_archive_members(archive)
        basename_map: dict[str, list[zipfile.ZipInfo]] = {}
        for member in members:
            basename_map.setdefault(PurePosixPath(member.filename).name, []).append(member)
        duplicates = [name for name, entries in basename_map.items() if len(entries) > 1]
        if duplicates:
            raise SystemExit("Duplicate archive basenames: " + ", ".join(sorted(duplicates)))

        for name, entries in basename_map.items():
            member = entries[0]
            if name in expected or name in {"qa-report.json", "batch-manifest.json"}:
                target = inbox_root / name
                with archive.open(member) as source, target.open("wb") as destination:
                    shutil.copyfileobj(source, destination)
                if name in expected:
                    extracted[name] = target
                else:
                    metadata_files[name] = target
            else:
                ignored.append(member.filename)

    imported_ids: list[str] = []
    missing_files = sorted(set(expected) - set(extracted))
    for filename, source in extracted.items():
        job = expected[filename]
        import_image(
            Namespace(
                handoff=handoff,
                source=source,
                job_id=job["job_id"],
                replace=args.replace,
                generation_backend=args.generation_backend,
                ratio_tolerance=args.ratio_tolerance,
            )
        )
        imported_ids.append(job["job_id"])

    qa_report_status = "absent"
    qa_report_path = metadata_files.get("qa-report.json")
    if qa_report_path:
        try:
            json.loads(qa_report_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SystemExit(f"Invalid qa-report.json: {error}") from error
        qa_report_status = "received_untrusted"

    state = load_json(state_path)
    current_batch = state["zip_batches"][args.batch_id]
    report = {
        "status": "complete" if not missing_files else "partial",
        "archive_source": str(source_archive),
        "archive_inbox_path": str(preserved_archive.relative_to(handoff)),
        "archive_sha256": archive_checksum,
        "imported_job_ids": imported_ids,
        "missing_files": missing_files,
        "ignored_archive_entries": ignored,
        "qa_report_status": qa_report_status,
        "imported_at": utc_now(),
    }
    current_batch["status"] = "imported_complete" if not missing_files else "imported_partial"
    current_batch["import"] = report
    report_path = batch_root(handoff, args.batch_id) / "batch-import-report.json"
    save_json(report_path, report)
    state["updated_at"] = utc_now()
    save_json(state_path, state)
    print(report_path)
    if missing_files:
        print("Missing: " + ", ".join(missing_files))


def fail_batch(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    batch = state.get("zip_batches", {}).get(args.batch_id)
    if not batch:
        raise SystemExit(f"Unknown ZIP batch: {args.batch_id}")
    if batch.get("status") in {"imported_complete", "imported_partial"}:
        raise SystemExit("Imported ZIP batches cannot be overwritten as failed")

    batch["status"] = "failed"
    batch["failure"] = {
        "reason": args.reason,
        "missing_files": args.missing_file,
        "serial_fallback_required": True,
        "failed_at": utc_now(),
    }
    state["updated_at"] = utc_now()
    save_json(state_path, state)
    print(state_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Create an optional ChatGPT ZIP batch pack")
    prepare.add_argument("--handoff", required=True, type=Path)
    prepare.add_argument("--batch-id", required=True)
    prepare.add_argument("--archive-name")
    prepare.add_argument("--job-id", action="append", default=[])
    prepare.set_defaults(func=prepare_batch)

    importer = subparsers.add_parser("import", help="Safely import a returned ZIP batch")
    importer.add_argument("--handoff", required=True, type=Path)
    importer.add_argument("--batch-id", required=True)
    importer.add_argument("--archive", required=True, type=Path)
    importer.add_argument(
        "--generation-backend",
        default="chatgpt_computer_use",
        choices=("chatgpt_computer_use", "manual_chatgpt_handoff"),
    )
    importer.add_argument("--replace", action="store_true")
    importer.add_argument("--ratio-tolerance", type=float, default=0.015)
    importer.set_defaults(func=import_batch)

    failure = subparsers.add_parser(
        "fail", help="Record a ZIP delivery failure and require serial fallback"
    )
    failure.add_argument("--handoff", required=True, type=Path)
    failure.add_argument("--batch-id", required=True)
    failure.add_argument("--reason", required=True)
    failure.add_argument("--missing-file", action="append", default=[])
    failure.set_defaults(func=fail_batch)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
