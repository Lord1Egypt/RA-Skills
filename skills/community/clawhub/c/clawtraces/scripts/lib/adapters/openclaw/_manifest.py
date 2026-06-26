# FILE_META
# INPUT:  output_dir path + mutation calls
# OUTPUT: manifest.json on disk (submitted / rejected state)
# POS:    skill lib adapters/openclaw — manifest persistence helpers
# MISSION: Atomic read/write of manifest.json, the per-user collection state file.

"""Manifest helpers for the OpenClaw adapter.

``manifest.json`` lives alongside trajectories in ``output_dir`` and tracks:

  - ``submitted``: filenames successfully uploaded (avoids re-upload)
  - ``rejected``: permanent rejects keyed by session_id (avoids re-scan).
                  Examples: sessions whose model doesn't match the whitelist,
                  cron-task sessions (if ``include_cron_tasks=False``), etc.

Kept small and dependency-free so both the legacy ``scan_and_convert.py``
path and the new adapter pipeline can share the exact same file layout.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone


MANIFEST_FILENAME = "manifest.json"


def load_manifest(output_dir: str) -> dict:
    manifest_path = os.path.join(output_dir, MANIFEST_FILENAME)
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"submitted": {}, "rejected": {}}


def save_manifest(output_dir: str, manifest: dict) -> None:
    manifest_path = os.path.join(output_dir, MANIFEST_FILENAME)
    tmp_path = manifest_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, manifest_path)


def record_rejection(
    output_dir: str,
    session_id: str,
    *,
    reason: str,
    detail: dict | None = None,
) -> None:
    """Persist a permanent reject so the session is not re-offered next scan."""
    manifest = load_manifest(output_dir)
    manifest.setdefault("rejected", {})
    entry: dict = {
        "reason": reason,
        "rejected_at": datetime.now(timezone.utc).isoformat(),
    }
    if detail:
        entry["detail"] = detail
    manifest["rejected"][session_id] = entry
    save_manifest(output_dir, manifest)
