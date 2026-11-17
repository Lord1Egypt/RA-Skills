"""Detection probes for products / profiles.

A probe returns an :class:`InstallState` based on the available
evidence on the local device.  Probes are pure-Python where possible
(``shutil.which`` + filesystem inspection) and never reach the
network.
"""

from __future__ import annotations

import os
import plistlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterable
from xml.parsers.expat import ExpatError


class InstallState(str, Enum):
    INSTALLED = "installed"
    CONFIGURED_ONLY = "configured-only"
    COMPATIBILITY_ONLY = "compatibility-only"
    CLOUD_CONNECTED = "cloud-connected"
    LEGACY = "legacy"
    AMBIGUOUS = "ambiguous"
    NOT_DETECTED = "not-detected"


@dataclass(frozen=True)
class ProbeResult:
    product: str
    profile: str
    state: InstallState
    evidence: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "product": self.product,
            "profile": self.profile,
            "state": self.state.value,
            "evidence": list(self.evidence),
        }


def probe_binary(
    product: str,
    profile: str,
    binary_names: Iterable[str],
    *,
    version_command: Iterable[str] | None = None,
    require_version: bool = False,
) -> ProbeResult:
    """Locate a binary in ``$PATH`` and capture its version."""
    names = list(binary_names)
    if not names:
        return ProbeResult(product, profile, InstallState.NOT_DETECTED, ())
    for name in names:
        path = shutil.which(name)
        if path:
            evidence = [f"binary:{path}"]
            if version_command:
                try:
                    proc = subprocess.run(
                        list(version_command),
                        capture_output=True,
                        text=True,
                        timeout=2,
                        check=False,
                    )
                    if require_version and proc.returncode != 0:
                        continue
                    stdout = proc.stdout.strip() if proc.returncode == 0 else ""
                    if stdout:
                        evidence.append(f"version:{stdout.splitlines()[0][:64]}")
                except (OSError, subprocess.SubprocessError):
                    if require_version:
                        continue
            elif require_version:
                continue
            return ProbeResult(product, profile, InstallState.INSTALLED, tuple(evidence))
    return ProbeResult(product, profile, InstallState.NOT_DETECTED, ())


_SHARED_COMPATIBILITY_SUFFIXES = (
    ".agents/skills",
    ".agents",
)


def _is_shared_compatibility_path(path: Path) -> bool:
    p_posix = path.as_posix()
    if path.name in {"AGENTS.md", ".mcp.json"}:
        return True
    if any(p_posix.endswith(suf) for suf in _SHARED_COMPATIBILITY_SUFFIXES):
        return True
    # Generic workspace-level "skills" without a product-specific dot directory (e.g. .cursor, .cline)
    if path.name == "skills" and not any(part.startswith(".") and part != ".agents" for part in path.parts):
        return True
    return False


def probe_file_signature(
    product: str,
    profile: str,
    candidate_paths: Iterable[Path | str],
    *,
    workspace: Path | None = None,
    home: Path | None = None,
) -> ProbeResult:
    """Check whether any of the candidate paths exists on disk.

    Supports exact paths, globs (e.g. ``github.copilot-*``), home resolution,
    and workspace-relative resolution.
    """
    effective_home = resolve_home(home)
    compatibility_match: ProbeResult | None = None
    for raw in candidate_paths:
        p_str = str(raw)
        if p_str.startswith("~"):
            target_str = str(effective_home) + p_str[1:]
        elif workspace is not None and not (p_str.startswith("/") or re.match(r"^[a-zA-Z]:", p_str)):
            target_str = str(workspace / p_str)
        else:
            target_str = p_str

        target_path = Path(target_str)
        try:
            paths = (
                sorted(target_path.parent.glob(target_path.name))
                if any(char in target_str for char in ("*", "?", "["))
                else [target_path]
            )
            for path in paths:
                if not path.exists():
                    continue
                state = (
                    InstallState.COMPATIBILITY_ONLY
                    if _is_shared_compatibility_path(path)
                    else InstallState.INSTALLED
                    if path.is_dir() or path.is_file()
                    else InstallState.CONFIGURED_ONLY
                )
                result = ProbeResult(product, profile, state, (f"file:{path}",))
                if state is not InstallState.COMPATIBILITY_ONLY:
                    return result
                compatibility_match = compatibility_match or result
        except OSError:
            continue
    return compatibility_match or ProbeResult(product, profile, InstallState.NOT_DETECTED, ())


DARWIN_BUNDLE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]{0,255}$")


def probe_app_bundle(
    product: str,
    profile: str,
    *,
    darwin_bundle_id: str | None = None,
    home: Path | None = None,
) -> ProbeResult:
    """Best-effort macOS app-bundle probe."""
    if (
        not darwin_bundle_id
        or sys.platform != "darwin"
        or not DARWIN_BUNDLE_ID_RE.fullmatch(darwin_bundle_id)
    ):
        return ProbeResult(product, profile, InstallState.NOT_DETECTED, ())

    def matches(app: Path) -> bool:
        try:
            if app.suffix != ".app" or not app.is_dir():
                return False
            document = plistlib.loads((app / "Contents" / "Info.plist").read_bytes())
            return isinstance(document, dict) and document.get("CFBundleIdentifier") == darwin_bundle_id
        except (OSError, ValueError, plistlib.InvalidFileException, ExpatError):
            return False

    # Parse XML and binary plists and compare the actual identifier exactly.
    for app_dir in (Path("/Applications"), resolve_home(home) / "Applications"):
        try:
            apps = sorted(app_dir.glob("*.app"))
        except OSError:
            continue
        for app in apps:
            if matches(app):
                return ProbeResult(
                    product, profile, InstallState.INSTALLED, (f"app-bundle:{app}",),
                )

    # 2. Try mdfind for Spotlight index lookup
    try:
        proc = subprocess.run(
            ["mdfind", f"kMDItemCFBundleIdentifier == '{darwin_bundle_id}'"],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            for found_app in proc.stdout.splitlines():
                if matches(Path(found_app)):
                    return ProbeResult(
                        product, profile, InstallState.INSTALLED,
                        (f"app-bundle:{found_app}",),
                    )
    except (OSError, subprocess.SubprocessError):
        pass

    return ProbeResult(product, profile, InstallState.NOT_DETECTED, ())


def resolve_home(home: Path | None) -> Path:
    """Pick the home directory honoring ``HOME`` overrides."""
    if home is not None:
        return home.resolve()
    env_home = os.environ.get("HOME")
    if env_home:
        # Guard against stale or foreign-format values (e.g. an MSYS-style
        # path leaking into native Windows Python, where it cannot exist).
        candidate = Path(env_home)
        if candidate.is_dir():
            return candidate.resolve()
    return Path.home().resolve()


def detect_product(
    product: str,
    profile: str,
    *,
    binary: Iterable[str] | None = None,
    version_command: Iterable[str] | None = None,
    file_signature: Iterable[Path | str] | None = None,
    home: Path | None = None,
    workspace: Path | None = None,
    app_bundle_id: str | None = None,
) -> ProbeResult:
    """Run a small, deterministic detection probe for one product."""
    fallback = ProbeResult(product, profile, InstallState.NOT_DETECTED, ())
    if binary:
        result = probe_binary(
            product, profile, binary, version_command=version_command
        )
        if result.state is InstallState.INSTALLED:
            return result
    if file_signature:
        result = probe_file_signature(
            product,
            profile,
            file_signature,
            workspace=workspace,
            home=home,
        )
        if result.state is not InstallState.NOT_DETECTED:
            if result.state is InstallState.INSTALLED:
                return result
            fallback = result
    if app_bundle_id:
        result = probe_app_bundle(product, profile, darwin_bundle_id=app_bundle_id, home=home)
        if result.state is InstallState.INSTALLED:
            return result
    return fallback


def detect_profile(
    product: str,
    profile: str,
    *,
    binaries: Iterable[str] = (),
    version_command: Iterable[str] | None = None,
    file_signatures: Iterable[str | Path] = (),
    home: Path | None = None,
    workspace: Path | None = None,
    app_bundle_id: str | None = None,
) -> ProbeResult:
    """Convenience wrapper that accepts string paths and expands ``~``."""
    return detect_product(
        product,
        profile,
        binary=binaries,
        version_command=version_command,
        file_signature=file_signatures,
        home=home,
        workspace=workspace,
        app_bundle_id=app_bundle_id,
    )
