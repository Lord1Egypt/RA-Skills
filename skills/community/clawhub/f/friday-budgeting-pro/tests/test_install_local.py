"""tests/test_install_local.py — Smoke tests for the local-install path (issue #95).

Validates that the manifest is correctly wired for `clawhub install ./` so a
local clone installs identically to a registry install.  Does NOT actually
run `clawhub install` (too heavy for unit tests).
"""

from __future__ import annotations

import json
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# package.json
# ---------------------------------------------------------------------------


def _load_package_json() -> dict:
    path = REPO_ROOT / "package.json"
    with open(path) as f:
        return json.load(f)


def test_package_json_has_openclaw_block():
    """package.json must have an 'openclaw' block so clawhub can find metadata."""
    pkg = _load_package_json()
    assert "openclaw" in pkg, "package.json missing 'openclaw' key"
    assert isinstance(pkg["openclaw"], dict), "'openclaw' must be a dict"


def test_package_json_points_to_skill_md():
    """openclaw.skillFile must point at SKILL.md (exists and non-empty)."""
    pkg = _load_package_json()
    skill_file = pkg["openclaw"].get("skillFile", "")
    assert skill_file, "openclaw.skillFile must be non-empty"
    skill_path = REPO_ROOT / skill_file
    assert skill_path.exists(), f"skillFile '{skill_file}' does not exist at repo root"


def test_package_json_has_slug():
    """slug field needed for clawhub to identify the package."""
    pkg = _load_package_json()
    assert "slug" in pkg and pkg["slug"].strip(), "package.json must have a non-empty 'slug'"


# ---------------------------------------------------------------------------
# SKILL.md — install hooks
# ---------------------------------------------------------------------------


def _read_skill_md() -> str:
    return (REPO_ROOT / "SKILL.md").read_text()


def test_skill_md_exists():
    assert (REPO_ROOT / "SKILL.md").exists(), "SKILL.md must exist at repo root"


def test_skill_md_has_pip_hook():
    """SKILL.md metadata must declare a pip install hook."""
    content = _read_skill_md()
    assert (
        "pip3 install" in content or "pip install" in content
    ), "SKILL.md missing pip install hook"


def test_skill_md_has_db_init_hook():
    """SKILL.md metadata must declare a db-init hook."""
    content = _read_skill_md()
    assert "db-init" in content or "init_db" in content, "SKILL.md missing db-init hook"


def test_skill_md_has_launchd_hook():
    """SKILL.md metadata must declare a launchd/installer hook."""
    content = _read_skill_md()
    assert (
        "server.installer" in content or "launchd" in content
    ), "SKILL.md missing launchd/installer hook"


def test_skill_md_install_hooks_count():
    """SKILL.md must declare all three install hooks: pip, db-init, launchd."""
    content = _read_skill_md()
    # Each hook has an "id" field
    ids = re.findall(r'"id":\s*"([^"]+)"', content)
    required = {"pip", "db-init", "launchd"}
    missing = required - set(ids)
    assert not missing, f"SKILL.md missing install hook id(s): {missing}"


# ---------------------------------------------------------------------------
# server/installer.py — exists and is referenced by SKILL.md
# ---------------------------------------------------------------------------


def test_installer_py_exists():
    assert (REPO_ROOT / "server" / "installer.py").exists(), "server/installer.py must exist"


def test_installer_py_referenced_in_skill_md():
    """SKILL.md launchd hook must call server.installer so clawhub runs it."""
    content = _read_skill_md()
    assert "server.installer" in content, "SKILL.md launchd hook must reference 'server.installer'"


# ---------------------------------------------------------------------------
# README — local install docs
# ---------------------------------------------------------------------------


def test_readme_documents_local_install():
    """README must document the local-clone install path."""
    readme = (REPO_ROOT / "README.md").read_text()
    assert (
        "clawhub install ./" in readme or "clawhub install /" in readme
    ), "README must document `clawhub install ./` (local clone) flow"


def test_readme_documents_registry_install():
    """README must document the registry install path."""
    readme = (REPO_ROOT / "README.md").read_text()
    assert (
        "clawhub install friday-budgeting-pro" in readme
    ), "README must document `clawhub install friday-budgeting-pro` (registry) flow"
