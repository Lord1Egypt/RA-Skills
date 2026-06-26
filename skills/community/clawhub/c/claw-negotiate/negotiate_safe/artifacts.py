"""Executed artifact helper functions for negotiate_safe."""
from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path


def build_artifact_uri(
    session_id: str,
    pdf_path: Path,  # noqa: ARG001 - local path intentionally not leaked
    creator_pending_id: str = "",
    creator_role: str = "",
) -> str:
    """Build the sshsign artifact URI shared between creator and joiner."""
    base = f"sshsign://session/{session_id}/executed.pdf"
    params = []
    if creator_pending_id:
        params.append(f"creator_pending={urllib.parse.quote(creator_pending_id)}")
    if creator_role:
        params.append(f"creator_role={urllib.parse.quote(creator_role)}")
    if params:
        return base + "?" + "&".join(params)
    return base


def parse_artifact_uri(uri: str) -> tuple[str, str]:
    """Extract (creator_pending_id, creator_role) from a session artifact URI."""
    if "?" not in uri:
        return "", ""
    query = uri.split("?", 1)[1]
    params = urllib.parse.parse_qs(query)
    return (
        params.get("creator_pending", [""])[0],
        params.get("creator_role", [""])[0],
    )


def write_counterparty_pending(
    output_dir: Path,
    session_id: str,  # noqa: ARG001 - neg_id comes from mint.json
    role: str,
    pending_id: str,
) -> None:
    """Write the counterparty pending id where upstream finalize expects it."""
    try:
        mint = json.loads((output_dir / "mint.json").read_text())
        neg_id = mint.get("negotiation_id") or ""
        founder_cfg = mint.get("founder_config_path") or ""
        investor_cfg = mint.get("investor_config_path") or ""
        anchor = founder_cfg or investor_cfg
        if not anchor or not neg_id:
            return
        neg_dir = Path(anchor).parent
        neg_output = neg_dir / "output"
        neg_output.mkdir(parents=True, exist_ok=True)
        pending_file = neg_output / f"{neg_id}_{role}_pending.txt"
        pending_file.write_text(pending_id.strip() + "\n")
    except (OSError, json.JSONDecodeError, KeyError) as e:
        sys.stderr.write(f"writing counterparty pending: {e}\n")
