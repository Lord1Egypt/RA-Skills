#!/usr/bin/env python3
# FILE_META
# INPUT:  workspace directory (SOUL.md, memory/, cron/)
# OUTPUT: workspace-{agent_id}.zip + upload confirmation
# POS:    skill scripts — Step 5, depends on lib/pii_scrubber.py and lib/paths.py
# MISSION: Bundle and upload workspace configuration with PII scrubbing.
"""Bundle workspace config files into zip archives for submission.

Supports two-phase operation for user confirmation:
  1. --bundle-only: Create zip(s) locally, output scrubbing stats (no upload)
  2. --upload-only: Upload previously created zip(s)

Default (no flag): bundle + upload in one pass.

Usage:
    python workspace_bundle.py --output-dir PATH [--bundle-only | --upload-only]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(__file__))

from lib.auth import get_server_url, get_stored_key
from lib.harness import upload_harness
from lib.pii_scrubber import scrub_text_with_stats

from lib.paths import get_default_output_dir

DEFAULT_OUTPUT_DIR = get_default_output_dir()
MANIFEST_FILENAME = "manifest.json"

WORKSPACE_MD_FILES = [
    "SOUL.md",
    "USER.md",
    "TOOLS.md",
    "AGENTS.md",
    "BOOTSTRAP.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "MEMORY.md",
]


def _get_openclaw_state_dir() -> str:
    env_dir = os.environ.get("OPENCLAW_STATE_DIR")
    if env_dir:
        return env_dir
    return os.path.expanduser("~/.openclaw")


def load_manifest(output_dir: str) -> dict:
    manifest_path = os.path.join(output_dir, MANIFEST_FILENAME)
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"submitted": {}, "rejected": {}}


def discover_workspaces(output_dir: str) -> list[dict]:
    """Find unique workspaces from submitted sessions' stats files.

    Returns list of {"agent_id": str, "cwd": str}.
    """
    manifest = load_manifest(output_dir)
    submitted = manifest.get("submitted", {})

    seen_agents: dict[str, str] = {}  # agent_id -> cwd

    for filename in submitted:
        session_id = filename.replace(".trajectory.json", "")
        stats_path = os.path.join(output_dir, f"{session_id}.stats.json")

        if not os.path.isfile(stats_path):
            continue

        try:
            with open(stats_path, "r", encoding="utf-8") as f:
                stats = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        agent_id = stats.get("agent_id", "")
        cwd = stats.get("cwd", "")

        if not agent_id or not cwd:
            continue

        if agent_id not in seen_agents:
            seen_agents[agent_id] = cwd

    return [{"agent_id": aid, "cwd": cwd} for aid, cwd in seen_agents.items()]


def _read_and_scrub(file_path: str) -> tuple[str | None, dict[str, int]]:
    """Read a text file and scrub PII.

    Returns (scrubbed_content, pii_counts). Content is None for binary files.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        scrubbed, counts = scrub_text_with_stats(text)
        return scrubbed, counts
    except (UnicodeDecodeError, OSError):
        return None, {}


def create_workspace_bundle(agent_id: str, cwd: str, output_dir: str) -> tuple[str | None, dict]:
    """Create a zip bundle for one workspace.

    Returns (zip_path, scrub_report).
    scrub_report = {"files_scrubbed": [...], "total_redactions": N, "by_category": {...}}
    zip_path is None if no files were found.
    """
    zip_filename = f"workspace-{agent_id}.zip"
    zip_path = os.path.join(output_dir, zip_filename)

    file_count = 0
    state_dir = _get_openclaw_state_dir()

    # Scrub tracking
    files_scrubbed: list[dict] = []  # [{"file": "SOUL.md", "redactions": {"手机号": 2}}]
    total_counts: dict[str, int] = {}

    def _merge_counts(counts: dict[str, int], filename: str):
        if counts:
            files_scrubbed.append({"file": filename, "redactions": counts})
            for k, v in counts.items():
                total_counts[k] = total_counts.get(k, 0) + v

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Workspace md files (PII scrubbed)
        for md_name in WORKSPACE_MD_FILES:
            md_path = os.path.join(cwd, md_name)
            if os.path.isfile(md_path):
                content, counts = _read_and_scrub(md_path)
                if content is not None:
                    zf.writestr(md_name, content)
                    _merge_counts(counts, md_name)
                    file_count += 1

        # 2. memory/ directory (text files PII scrubbed)
        memory_dir = os.path.join(cwd, "memory")
        if os.path.isdir(memory_dir):
            for root, _dirs, files in os.walk(memory_dir):
                for fname in files:
                    full_path = os.path.join(root, fname)
                    arcname = os.path.join("memory", os.path.relpath(full_path, memory_dir))
                    content, counts = _read_and_scrub(full_path)
                    if content is not None:
                        zf.writestr(arcname, content)
                        _merge_counts(counts, arcname)
                    else:
                        zf.write(full_path, arcname)
                    file_count += 1

        # 3. cron/ directory (PII scrubbed)
        cron_dir = os.path.join(state_dir, "cron")
        if os.path.isdir(cron_dir):
            for root, _dirs, files in os.walk(cron_dir):
                for fname in files:
                    full_path = os.path.join(root, fname)
                    arcname = os.path.join("cron", os.path.relpath(full_path, cron_dir))
                    content, counts = _read_and_scrub(full_path)
                    if content is not None:
                        zf.writestr(arcname, content)
                        _merge_counts(counts, arcname)
                    else:
                        zf.write(full_path, arcname)
                    file_count += 1

        # 4. sessions/sessions.json (no scrub — only contains session metadata)
        sessions_json = os.path.join(state_dir, "agents", agent_id, "sessions", "sessions.json")
        if os.path.isfile(sessions_json):
            zf.write(sessions_json, os.path.join("sessions", "sessions.json"))
            file_count += 1

    if file_count == 0:
        os.remove(zip_path)
        return None, {}

    total_redactions = sum(total_counts.values())
    scrub_report = {
        "files_scrubbed": files_scrubbed,
        "total_redactions": total_redactions,
        "by_category": total_counts,
    }

    return zip_path, scrub_report


def upload_workspace(server_url: str, secret_key: str, zip_path: str, agent_id: str) -> dict:
    """Upload a workspace zip to the server.

    Thin wrapper over the generic harness uploader: OpenClaw workspace is
    just one harness scope (adapter='openclaw', scope_type='agent',
    scope_id=<agent_id>). Delegating here keeps a single code path for
    every adapter's harness upload; new adapters plug in at
    ``lib/harness/`` without touching this file.
    """
    with open(zip_path, "rb") as f:
        zip_bytes = f.read()
    return upload_harness(server_url, secret_key, "openclaw", "agent", agent_id, zip_bytes)


def main():
    parser = argparse.ArgumentParser(description="Bundle and upload workspace config files")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR,
                        help="Directory with stats files and manifest")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bundle-only", action="store_true",
                       help="Only create zip bundles locally (no upload)")
    group.add_argument("--upload-only", action="store_true",
                       help="Only upload previously created workspace zips")
    args = parser.parse_args()

    output_dir = args.output_dir
    workspaces = discover_workspaces(output_dir)

    if not workspaces:
        print(json.dumps({"error": "no_workspaces", "message": "No workspace info found in submitted stats"}))
        sys.exit(0)

    # ── Bundle-only mode ──
    if args.bundle_only:
        results = []
        for ws in workspaces:
            agent_id = ws["agent_id"]
            cwd = ws["cwd"]

            if not os.path.isdir(cwd):
                continue

            zip_path, scrub_report = create_workspace_bundle(agent_id, cwd, output_dir)
            if not zip_path:
                continue

            zip_size = os.path.getsize(zip_path)
            results.append({
                "agent_id": agent_id,
                "cwd": cwd,
                "zip_file": os.path.basename(zip_path),
                "zip_size": zip_size,
                "scrub_report": scrub_report,
            })

        print(json.dumps({"workspaces": results}, ensure_ascii=False))
        return

    # ── Upload-only mode ──
    if args.upload_only:
        key = get_stored_key()
        if not key:
            print(json.dumps({"error": "not_authenticated"}))
            sys.exit(1)

        server_url = get_server_url()
        results = []

        for ws in workspaces:
            agent_id = ws["agent_id"]
            zip_path = os.path.join(output_dir, f"workspace-{agent_id}.zip")

            if not os.path.isfile(zip_path):
                continue

            print(f"  Uploading workspace-{agent_id}.zip...", file=sys.stderr)
            result = upload_workspace(server_url, key, zip_path, agent_id)

            if "error" in result:
                print(f"  Upload failed: {result['error']}", file=sys.stderr)
                results.append({"agent_id": agent_id, "status": "error", "error": result["error"]})
            else:
                print(f"  Upload OK", file=sys.stderr)
                results.append({"agent_id": agent_id, "status": "ok", "filename": result.get("filename", "")})

            # Clean up local zip after upload
            try:
                os.remove(zip_path)
            except OSError:
                pass

        print(json.dumps({"workspaces": results}))
        return

    # ── Default: bundle + upload ──
    key = get_stored_key()
    if not key:
        print(json.dumps({"error": "not_authenticated"}))
        sys.exit(1)

    server_url = get_server_url()
    results = []

    for ws in workspaces:
        agent_id = ws["agent_id"]
        cwd = ws["cwd"]

        if not os.path.isdir(cwd):
            print(f"  Workspace directory not found, skipping: {cwd}", file=sys.stderr)
            continue

        print(f"  Bundling workspace: {cwd} (agent: {agent_id})...", file=sys.stderr)
        zip_path, scrub_report = create_workspace_bundle(agent_id, cwd, output_dir)

        if not zip_path:
            print(f"  No files found, skipping", file=sys.stderr)
            continue

        zip_size = os.path.getsize(zip_path)
        print(f"  Created {os.path.basename(zip_path)} ({zip_size} bytes)", file=sys.stderr)

        if scrub_report.get("total_redactions", 0) > 0:
            print(f"  PII scrubbed: {scrub_report['total_redactions']} redactions", file=sys.stderr)

        print(f"  Uploading...", file=sys.stderr)
        result = upload_workspace(server_url, key, zip_path, agent_id)

        if "error" in result:
            print(f"  Upload failed: {result['error']}", file=sys.stderr)
            results.append({"agent_id": agent_id, "status": "error", "error": result["error"]})
        else:
            print(f"  Upload OK", file=sys.stderr)
            results.append({"agent_id": agent_id, "status": "ok", "filename": result.get("filename", "")})

        # Clean up local zip
        try:
            os.remove(zip_path)
        except OSError:
            pass

    print(json.dumps({"workspaces": results}))


if __name__ == "__main__":
    main()
