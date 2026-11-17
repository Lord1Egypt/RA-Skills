"""Approved Phase 15.2 PDFium package and wheel identities."""

from __future__ import annotations

import json
import platform
from pathlib import Path
import sys
from typing import Any

from .errors import PDFOCRError, PDFOCRErrorCode


RENDERER_ID = "pypdfium2"
RENDERER_VERSION = "5.13.0"
ENGINE_VERSION = "153.0.7999.0"
ENGINE_BUILD = 7999
ENGINE_ORIGIN = "pdfium-binaries"
ENGINE_FLAGS: tuple[str, ...] = ()

_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "governance" / "pdfium-renderer-artifacts.json"


def _platform_key() -> str:
    machine = platform.machine().lower()
    if sys.platform.startswith("linux"):
        os_name = "linux"
    elif sys.platform == "darwin":
        os_name = "macos"
    elif sys.platform == "win32":
        os_name = "windows"
    else:
        raise PDFOCRError("platform has no approved PDFium wheel", PDFOCRErrorCode.RASTERIZATION_FAILED)

    if machine in {"x86_64", "amd64"}:
        arch = "x86_64"
    elif machine in {"aarch64", "arm64"}:
        arch = "arm64"
    else:
        raise PDFOCRError("architecture has no approved PDFium wheel", PDFOCRErrorCode.RASTERIZATION_FAILED)
    return f"{os_name}_{arch}"


def load_approved_artifact() -> dict[str, str]:
    """Load and validate the approved wheel for the running platform."""

    try:
        manifest: dict[str, Any] = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        raise PDFOCRError("approved PDFium artifact manifest is unavailable", PDFOCRErrorCode.RASTERIZATION_FAILED) from exc

    expected_engine = {
        "name": "PDFium",
        "version": ENGINE_VERSION,
        "build": ENGINE_BUILD,
        "origin": ENGINE_ORIGIN,
        "flags": [],
        "v8": False,
        "xfa": False,
    }
    if manifest.get("package") != {"name": RENDERER_ID, "version": RENDERER_VERSION}:
        raise PDFOCRError("approved PDFium wrapper identity is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)
    if manifest.get("engine") != expected_engine:
        raise PDFOCRError("approved PDFium engine identity is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)
    policy = manifest.get("install_policy")
    if not isinstance(policy, dict) or policy.get("only_binary") != ":all:" or policy.get("source_build_fallback") is not False:
        raise PDFOCRError("approved PDFium wheel-only policy is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)

    platform_key = _platform_key()
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise PDFOCRError("approved PDFium artifact list is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)
    matches = [item for item in artifacts if isinstance(item, dict) and item.get("platform") == platform_key]
    if len(matches) != 1:
        raise PDFOCRError("approved PDFium wheel identity is ambiguous", PDFOCRErrorCode.RASTERIZATION_FAILED)
    artifact = matches[0]
    filename, digest = artifact.get("filename"), artifact.get("sha256")
    if not isinstance(filename, str) or "/" in filename or "\\" in filename:
        raise PDFOCRError("approved PDFium wheel filename is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)
    if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise PDFOCRError("approved PDFium wheel digest is invalid", PDFOCRErrorCode.RASTERIZATION_FAILED)
    return {"platform": platform_key, "filename": filename, "sha256": digest}


def approved_build_identity(artifact: dict[str, str]) -> str:
    """Return the canonical architecture-approved build identity."""

    return (
        f"pypi-wheel:{artifact['filename']}@sha256:{artifact['sha256']}"
        f"|pdfium-build:{ENGINE_BUILD}|origin:{ENGINE_ORIGIN}|flags:none"
    )
