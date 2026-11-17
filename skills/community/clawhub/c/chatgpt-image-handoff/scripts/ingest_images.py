#!/usr/bin/env python3
"""Import generated images, update job state, and build a contact sheet."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

from PIL import Image

from handoff_common import (
    BACKENDS,
    find_job,
    image_info,
    load_json,
    parse_dimensions,
    refresh_run_status,
    render_contact_sheet,
    save_json,
    sha256_file,
    utc_now,
)


def save_converted(source: Path, target: Path, target_size: tuple[int, int] | None) -> None:
    with Image.open(source) as opened:
        image = opened.copy()
    if target_size:
        image = image.resize(target_size, Image.Resampling.LANCZOS)
    suffix = target.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        image.convert("RGB").save(target, quality=95, optimize=True)
    elif suffix == ".webp":
        image.save(target, format="WEBP", quality=95, method=6)
    else:
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(target, format="PNG", optimize=True)


def import_image(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    source = args.source.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    job = find_job(state, args.job_id)
    previous_import = dict(job.get("import", {}))
    previous_qa = dict(job.get("visual_qa", {}))
    previous_text_policy_qa = dict(job.get("text_policy_qa", {}))
    if not source.is_file():
        raise SystemExit(f"Source image not found: {source}")

    source_info = image_info(source)
    source_checksum = sha256_file(source)
    inbox_name = f"{job['job_id']}-{source_checksum[:12]}{source.suffix.lower()}"
    inbox_path = handoff / "inbox" / inbox_name
    if not inbox_path.exists():
        inbox_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, inbox_path)

    expected = parse_dimensions(job["dimensions"])
    source_ratio = source_info["width"] / source_info["height"]
    expected_ratio = expected[0] / expected[1]
    ratio_difference = abs(source_ratio - expected_ratio) / expected_ratio
    target_size = None
    dimension_status = "exact"
    if (source_info["width"], source_info["height"]) != expected:
        if ratio_difference <= args.ratio_tolerance:
            target_size = expected
            dimension_status = "normalized_matching_ratio"
        else:
            dimension_status = "ratio_mismatch"

    output_path = handoff / "imported" / job["intended_filename"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.name}.tmp{output_path.suffix}")
    save_converted(inbox_path, temporary, target_size)
    new_checksum = sha256_file(temporary)
    same_output = False
    if output_path.exists():
        existing_checksum = sha256_file(output_path)
        if existing_checksum == new_checksum:
            same_output = True
            temporary.unlink()
        elif not args.replace:
            temporary.unlink()
            raise SystemExit(f"Different output already exists: {output_path}. Use --replace explicitly.")
        else:
            os.replace(temporary, output_path)
    else:
        os.replace(temporary, output_path)

    output_info = image_info(output_path)
    selected_backend = args.generation_backend or state.get("generation_runtime", {}).get("selected_backend")
    job["status"] = "imported"
    job["last_error"] = None
    job["generation_backend"] = selected_backend
    job["download"] = {"source_path": str(source), "detected_at": utc_now()}
    job["import"] = {
        "inbox_path": str(inbox_path.relative_to(handoff)),
        "output_path": str(output_path.relative_to(handoff)),
        "source_sha256": source_checksum,
        "output_sha256": sha256_file(output_path),
        "source_dimensions": f"{source_info['width']}x{source_info['height']}",
        "output_dimensions": f"{output_info['width']}x{output_info['height']}",
        "dimension_status": dimension_status,
        "imported_at": utc_now(),
    }
    same_import = (
        same_output
        and previous_import.get("source_sha256") == source_checksum
        and previous_import.get("output_sha256") == job["import"]["output_sha256"]
    )
    if same_import and previous_qa.get("status") in {"passed", "needs_revision"}:
        job["visual_qa"] = previous_qa
        if previous_text_policy_qa:
            job["text_policy_qa"] = previous_text_policy_qa
        job["status"] = "qa_passed" if previous_qa["status"] == "passed" else "needs_revision"
    else:
        job["human_confirmation"] = "pending"
        job["visual_qa"] = {
            "status": "pending" if dimension_status != "ratio_mismatch" else "needs_revision",
            "notes": None if dimension_status != "ratio_mismatch" else "source ratio does not match target",
        }
        job["text_policy_qa"] = {
            "status": (
                "pending"
                if job.get("text_policy", {}).get("mode") == "allowlist"
                else "not_applicable"
            ),
            "observed_extra_text": [],
            "matched_forbidden_patterns": [],
        }
        if dimension_status == "ratio_mismatch":
            job["status"] = "needs_revision"
    refresh_run_status(state)
    save_json(state_path, state)
    contact_sheet = render_contact_sheet(handoff, state)
    print(output_path)
    if contact_sheet:
        print(contact_sheet)


def mark_qa(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    job = find_job(state, args.job_id)
    if not job.get("import", {}).get("output_path"):
        raise SystemExit(f"Cannot mark QA before import: {args.job_id}")
    policy_mode = job.get("text_policy", {}).get("mode", "open")
    policy_status = args.text_policy_status
    observed_extra_text = args.observed_extra_text or []
    matched_forbidden_patterns = args.matched_forbidden_pattern or []
    if policy_mode == "allowlist":
        if args.status == "passed" and policy_status != "passed":
            raise SystemExit(
                f"Strict text policy must pass before visual QA can pass: {args.job_id}"
            )
        if args.status == "passed" and (observed_extra_text or matched_forbidden_patterns):
            raise SystemExit(
                f"Strict text policy cannot pass with extra or forbidden readable text: {args.job_id}"
            )
        if policy_status == "not_applicable":
            raise SystemExit(f"Strict text policy cannot be not_applicable: {args.job_id}")
        if policy_status == "needs_revision" and args.status != "needs_revision":
            raise SystemExit(f"Text policy failure requires needs_revision: {args.job_id}")
        if policy_status is None:
            policy_status = "needs_revision" if args.status == "needs_revision" else "pending"
    else:
        policy_status = policy_status or "not_applicable"
    job["visual_qa"] = {"status": args.status, "notes": args.notes, "checked_at": utc_now()}
    job["text_policy_qa"] = {
        "status": policy_status,
        "observed_extra_text": observed_extra_text,
        "matched_forbidden_patterns": matched_forbidden_patterns,
        "checked_at": utc_now(),
    }
    job["status"] = "qa_passed" if args.status == "passed" else "needs_revision"
    if args.status == "needs_revision":
        job["human_confirmation"] = "pending"
    refresh_run_status(state)
    save_json(state_path, state)
    print(state_path)


def mark_confirmation(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    job = find_job(state, args.job_id)
    if job.get("status") != "qa_passed":
        raise SystemExit(f"Cannot confirm an image before QA passes: {args.job_id}")
    job["human_confirmation"] = args.status
    job["confirmed_at"] = utc_now()
    refresh_run_status(state)
    save_json(state_path, state)
    print(state_path)


def update_state(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    job = find_job(state, args.job_id)
    job["status"] = args.status
    if args.increment_attempt:
        job["attempts"] = int(job.get("attempts", 0)) + 1
    if args.error is not None:
        job["last_error"] = args.error
    refresh_run_status(state)
    save_json(state_path, state)
    print(state_path)


def contact_sheet(args: argparse.Namespace) -> None:
    handoff = args.handoff.expanduser().resolve()
    state = load_json(handoff / "jobs.json")
    output = render_contact_sheet(handoff, state)
    if output is None:
        raise SystemExit("No imported images available")
    print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    importer = subparsers.add_parser("import", help="Copy and register one generated image")
    importer.add_argument("--handoff", required=True, type=Path)
    importer.add_argument("--job-id", required=True)
    importer.add_argument("--source", required=True, type=Path)
    importer.add_argument("--replace", action="store_true")
    importer.add_argument(
        "--generation-backend",
        choices=sorted(BACKENDS - {"auto"}),
        help="Record the backend that produced this specific imported output",
    )
    importer.add_argument("--ratio-tolerance", type=float, default=0.015)
    importer.set_defaults(func=import_image)

    qa = subparsers.add_parser("qa", help="Record visual QA after opening the image")
    qa.add_argument("--handoff", required=True, type=Path)
    qa.add_argument("--job-id", required=True)
    qa.add_argument("--status", required=True, choices=("passed", "needs_revision"))
    qa.add_argument("--notes")
    qa.add_argument(
        "--text-policy-status",
        choices=("passed", "needs_revision", "not_applicable"),
    )
    qa.add_argument("--observed-extra-text", action="append", default=[])
    qa.add_argument("--matched-forbidden-pattern", action="append", default=[])
    qa.set_defaults(func=mark_qa)

    confirmation = subparsers.add_parser("confirm", help="Record the user's reviewed image decision")
    confirmation.add_argument("--handoff", required=True, type=Path)
    confirmation.add_argument("--job-id", required=True)
    confirmation.add_argument("--status", required=True, choices=("approved", "rejected"))
    confirmation.set_defaults(func=mark_confirmation)

    state = subparsers.add_parser("state", help="Record a generation state transition")
    state.add_argument("--handoff", required=True, type=Path)
    state.add_argument("--job-id", required=True)
    state.add_argument(
        "--status",
        required=True,
        choices=("queued", "prompt_submitted", "generating", "downloaded", "failed"),
    )
    state.add_argument("--error")
    state.add_argument("--increment-attempt", action="store_true")
    state.set_defaults(func=update_state)

    sheet = subparsers.add_parser("contact-sheet", help="Refresh the imported-image overview")
    sheet.add_argument("--handoff", required=True, type=Path)
    sheet.set_defaults(func=contact_sheet)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
