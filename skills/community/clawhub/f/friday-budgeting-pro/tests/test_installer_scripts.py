"""tests/test_installer_scripts.py — Static checks for ClawHub installer scripts.

These tests perform file-system and content checks only.  They do NOT invoke
launchctl, run install.sh, or modify the real system.  Manual E2E testing is
required to verify the actual install/uninstall flow.
"""

from __future__ import annotations

import os
import stat
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
INSTALL_SH = SCRIPTS_DIR / "install.sh"
UNINSTALL_SH = SCRIPTS_DIR / "uninstall.sh"
PLIST_TEMPLATE = SCRIPTS_DIR / "launchd-template.plist"


def _is_executable(path: Path) -> bool:
    """Return True if the owner-execute bit is set on *path*."""
    return bool(os.stat(path).st_mode & stat.S_IXUSR)


# ---------------------------------------------------------------------------
# install.sh
# ---------------------------------------------------------------------------


def test_install_sh_exists() -> None:
    assert INSTALL_SH.exists(), f"{INSTALL_SH} not found"


def test_install_sh_is_executable() -> None:
    assert _is_executable(INSTALL_SH), f"{INSTALL_SH} is not executable"


# ---------------------------------------------------------------------------
# uninstall.sh
# ---------------------------------------------------------------------------


def test_uninstall_sh_exists() -> None:
    assert UNINSTALL_SH.exists(), f"{UNINSTALL_SH} not found"


def test_uninstall_sh_is_executable() -> None:
    assert _is_executable(UNINSTALL_SH), f"{UNINSTALL_SH} is not executable"


# ---------------------------------------------------------------------------
# launchd-template.plist
# ---------------------------------------------------------------------------


def test_plist_template_is_valid_xml() -> None:
    """xml.etree.ElementTree.parse must succeed without raising."""
    ET.parse(str(PLIST_TEMPLATE))  # raises ParseError on malformed XML


def test_plist_template_contains_home_placeholder() -> None:
    content = PLIST_TEMPLATE.read_text()
    assert "@HOME@" in content, "Template missing @HOME@ placeholder"


def test_plist_template_contains_python_placeholder() -> None:
    content = PLIST_TEMPLATE.read_text()
    assert "@PYTHON@" in content, "Template missing @PYTHON@ placeholder"


def test_plist_template_label() -> None:
    """The plist <dict> must contain the correct Label string."""
    tree = ET.parse(str(PLIST_TEMPLATE))
    root = tree.getroot()
    # plist > dict > key/string pairs
    d = root.find("dict")
    assert d is not None, "Root <plist> must contain a <dict>"
    keys = [el.text for el in d.findall("key")]
    assert "Label" in keys, "Template missing <key>Label</key>"
    label_idx = list(d).index(d.findall("key")[keys.index("Label")])
    label_value = list(d)[label_idx + 1]
    assert (
        label_value.text == "ai.openclaw.friday-budgeting-pro"
    ), f"Unexpected label value: {label_value.text!r}"


def test_plist_template_keep_alive_true() -> None:
    tree = ET.parse(str(PLIST_TEMPLATE))
    root = tree.getroot()
    d = root.find("dict")
    assert d is not None
    keys = [el.text for el in d.findall("key")]
    assert "KeepAlive" in keys, "Template missing <key>KeepAlive</key>"
    ka_idx = list(d).index(d.findall("key")[keys.index("KeepAlive")])
    ka_value = list(d)[ka_idx + 1]
    assert ka_value.tag == "true", f"KeepAlive should be <true/>, got <{ka_value.tag}/>"


def test_plist_template_run_at_load_true() -> None:
    tree = ET.parse(str(PLIST_TEMPLATE))
    root = tree.getroot()
    d = root.find("dict")
    assert d is not None
    keys = [el.text for el in d.findall("key")]
    assert "RunAtLoad" in keys, "Template missing <key>RunAtLoad</key>"
    ral_idx = list(d).index(d.findall("key")[keys.index("RunAtLoad")])
    ral_value = list(d)[ral_idx + 1]
    assert ral_value.tag == "true", f"RunAtLoad should be <true/>, got <{ral_value.tag}/>"
