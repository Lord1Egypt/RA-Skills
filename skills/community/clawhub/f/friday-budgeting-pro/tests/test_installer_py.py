"""tests/test_installer_py.py — Unit tests for server/installer.py.

All filesystem writes and subprocess calls are mocked — no real
~/Library/LaunchAgents/ or launchctl interaction occurs.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import server.installer as installer

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _patch_paths(tmp_path: Path):
    """Return context managers that redirect plist + config paths to tmp_path."""
    plist_target = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    config_target = tmp_path / ".openclaw" / "config.json"

    plist_cm = patch.object(installer, "_plist_path", return_value=plist_target)
    config_cm = patch.object(installer, "_openclaw_config_path", return_value=config_target)
    return plist_cm, config_cm


# ---------------------------------------------------------------------------
# install() — plist content
# ---------------------------------------------------------------------------


def test_install_writes_plist(tmp_path: Path) -> None:
    """install() must create the plist file with correct content."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    plist_path = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    assert plist_path.exists(), "plist was not written"
    content = plist_path.read_text()
    assert "<true/>" in content, "plist missing <true/> (KeepAlive or RunAtLoad)"
    assert "KeepAlive" in content
    assert "RunAtLoad" in content
    assert "server.daemon" in content, "ProgramArguments must reference server.daemon"
    assert str(tmp_path) in content, "WorkingDirectory must be the install_dir"
    assert installer.LABEL in content


def test_install_plist_keep_alive(tmp_path: Path) -> None:
    """KeepAlive key must be <true/>."""
    import xml.etree.ElementTree as ET

    plist_cm, config_cm = _patch_paths(tmp_path)
    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    plist_path = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    tree = ET.parse(str(plist_path))
    root = tree.getroot()
    d = root.find("dict")
    assert d is not None
    keys = [el.text for el in d.findall("key")]
    assert "KeepAlive" in keys
    ka_idx = list(d).index(d.findall("key")[keys.index("KeepAlive")])
    assert list(d)[ka_idx + 1].tag == "true"


def test_install_plist_run_at_load(tmp_path: Path) -> None:
    """RunAtLoad key must be <true/>."""
    import xml.etree.ElementTree as ET

    plist_cm, config_cm = _patch_paths(tmp_path)
    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    plist_path = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    tree = ET.parse(str(plist_path))
    root = tree.getroot()
    d = root.find("dict")
    assert d is not None
    keys = [el.text for el in d.findall("key")]
    assert "RunAtLoad" in keys
    ral_idx = list(d).index(d.findall("key")[keys.index("RunAtLoad")])
    assert list(d)[ral_idx + 1].tag == "true"


def test_install_plist_program_arguments(tmp_path: Path) -> None:
    """ProgramArguments must include sys.executable and server.daemon."""
    import xml.etree.ElementTree as ET

    plist_cm, config_cm = _patch_paths(tmp_path)
    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    plist_path = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    tree = ET.parse(str(plist_path))
    root = tree.getroot()
    d = root.find("dict")
    assert d is not None
    keys = [el.text for el in d.findall("key")]
    pa_idx = list(d).index(d.findall("key")[keys.index("ProgramArguments")])
    args_el = list(d)[pa_idx + 1]
    args = [el.text for el in args_el.findall("string")]
    assert sys.executable in args, "sys.executable must be the first ProgramArguments entry"
    assert "server.daemon" in args


# ---------------------------------------------------------------------------
# install() — launchctl bootstrap
# ---------------------------------------------------------------------------


def test_install_calls_launchctl_bootstrap(tmp_path: Path) -> None:
    """install() must call launchctl bootstrap with the right args."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    with plist_cm, config_cm, patch("subprocess.run") as mock_run:
        installer.install(install_dir=tmp_path)

    plist_path = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    expected_cmd = ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(plist_path)]
    mock_run.assert_called_once_with(expected_cmd, check=False)


# ---------------------------------------------------------------------------
# install() — OpenClaw config
# ---------------------------------------------------------------------------


def test_install_creates_config_when_missing(tmp_path: Path) -> None:
    """install() must create ~/.openclaw/config.json with mcpServers if absent."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    config_path = tmp_path / ".openclaw" / "config.json"
    assert not config_path.exists()

    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    assert config_path.exists(), "config.json was not created"
    data = json.loads(config_path.read_text())
    assert "mcp" in data
    assert "friday-budgeting-pro" in data["mcp"]["servers"]
    entry = data["mcp"]["servers"]["friday-budgeting-pro"]
    assert entry["command"] == sys.executable
    assert "-m" in entry["args"]
    assert "server.main" in entry["args"]
    assert "cwd" in entry


def test_install_adds_to_existing_config_without_clobbering(tmp_path: Path) -> None:
    """install() must add the entry without removing other mcpServers keys."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    config_path = tmp_path / ".openclaw" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    existing = {
        "mcp": {
            "servers": {
                "other-server": {"command": "node", "args": ["index.js"]},
            }
        },
        "someOtherKey": "preserved",
    }
    config_path.write_text(json.dumps(existing))

    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    data = json.loads(config_path.read_text())
    assert "friday-budgeting-pro" in data["mcp"]["servers"]
    assert "other-server" in data["mcp"]["servers"], "pre-existing entry was clobbered"
    assert data["someOtherKey"] == "preserved", "non-mcpServers key was clobbered"


def test_install_adds_when_no_mcp_servers_key(tmp_path: Path) -> None:
    """install() must create mcpServers if config.json exists but lacks the key."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    config_path = tmp_path / ".openclaw" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps({"someOtherKey": 42}))

    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)

    data = json.loads(config_path.read_text())
    assert "mcp" in data
    assert "friday-budgeting-pro" in data["mcp"]["servers"]
    assert data["someOtherKey"] == 42


# ---------------------------------------------------------------------------
# uninstall()
# ---------------------------------------------------------------------------


def test_uninstall_calls_launchctl_bootout(tmp_path: Path) -> None:
    """uninstall() must call launchctl bootout with the right service path."""
    plist_cm, _ = _patch_paths(tmp_path)
    with plist_cm, patch("subprocess.run") as mock_run:
        installer.uninstall()

    expected_cmd = ["launchctl", "bootout", f"gui/{os.getuid()}/{installer.LABEL}"]
    mock_run.assert_called_once_with(expected_cmd, check=False)


def test_uninstall_removes_plist(tmp_path: Path) -> None:
    """uninstall() must delete the plist if it exists."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    plist_path = tmp_path / "Library" / "LaunchAgents" / installer.PLIST_NAME
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    plist_path.write_text("<plist/>")

    with plist_cm, patch("subprocess.run"):
        installer.uninstall()

    assert not plist_path.exists(), "plist was not removed by uninstall()"


def test_uninstall_no_error_when_plist_missing(tmp_path: Path) -> None:
    """uninstall() must not raise if the plist doesn't exist."""
    plist_cm, _ = _patch_paths(tmp_path)
    with plist_cm, patch("subprocess.run"):
        installer.uninstall()  # must not raise


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_install_is_idempotent(tmp_path: Path) -> None:
    """Calling install() twice must not duplicate or corrupt the config."""
    plist_cm, config_cm = _patch_paths(tmp_path)
    with plist_cm, config_cm, patch("subprocess.run"):
        installer.install(install_dir=tmp_path)
        installer.install(install_dir=tmp_path)

    config_path = tmp_path / ".openclaw" / "config.json"
    data = json.loads(config_path.read_text())
    assert isinstance(
        data["mcp"]["servers"]["friday-budgeting-pro"], dict
    ), "Re-running install() corrupted the mcpServers entry"
    # Ensure there's exactly one top-level "mcp" key (no duplication).
    raw = config_path.read_text()
    assert raw.count('"mcp"') == 1, "mcpServers key duplicated"
    assert raw.count('"friday-budgeting-pro"') == 1, "friday-budgeting-pro entry duplicated"
