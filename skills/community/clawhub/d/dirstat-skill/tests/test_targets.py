from pathlib import Path

import sys

import pytest

from dirstat_skill.targets import ScanTarget, normalize_targets


@pytest.mark.skipif(sys.platform != "win32", reason="windows-native engine requires a Windows host")
def test_normalize_targets_keeps_multiple_explicit_paths() -> None:
    targets = normalize_targets(
        requested_paths=["C:\\", "D:\\models", "F:\\"],
        auto_discover=False,
        platform_name="windows",
    )

    assert targets == [
        ScanTarget(raw_path="C:\\", resolved_path=Path("C:/"), platform_name="windows"),
        ScanTarget(raw_path="D:\\models", resolved_path=Path("D:/models"), platform_name="windows"),
        ScanTarget(raw_path="F:\\", resolved_path=Path("F:/"), platform_name="windows"),
    ]


def test_normalize_targets_rejects_empty_request_when_auto_discover_disabled() -> None:
    with pytest.raises(ValueError, match="No scan targets were provided"):
        normalize_targets(requested_paths=[], auto_discover=False, platform_name="windows")

