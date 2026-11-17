from pathlib import Path

import pytest

from dirstat_skill.engine_windows import _scan_path, build_windows_export


def test_build_windows_export_writes_raw_json(tmp_path: Path) -> None:
    source_root = tmp_path / "scan-root"
    source_root.mkdir()
    (source_root / "cache.bin").write_bytes(b"x" * 8)
    (source_root / "nested").mkdir()
    (source_root / "nested" / "weights.gguf").write_bytes(b"y" * 16)

    export_path = tmp_path / "windows-export.json"
    result = build_windows_export(target=source_root, output_path=export_path)

    assert result.engine_name == "windows-native"
    assert export_path.exists()
    assert '"path"' in export_path.read_text(encoding="utf-8")


def test_build_windows_export_rejects_missing_root(tmp_path: Path) -> None:
    export_path = tmp_path / "windows-export.json"

    with pytest.raises(FileNotFoundError):
        build_windows_export(target=tmp_path / "missing-root", output_path=export_path)


def test_scan_path_skips_windows_junctions(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "scan-root"
    root.mkdir()
    junction_path = root / "loop-junction"

    class FakeDirEntry:
        name = "loop-junction"
        path = str(junction_path)

        def is_dir(self, follow_symlinks: bool = False) -> bool:
            return True

        def is_junction(self) -> bool:
            return True

    class FakeScandir:
        def __init__(self, entries: list[FakeDirEntry]) -> None:
            self._entries = entries

        def __enter__(self) -> list[FakeDirEntry]:
            return self._entries

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

    def fake_scandir(path: Path) -> FakeScandir:
        if Path(path) == root:
            return FakeScandir([FakeDirEntry()])
        raise RuntimeError("junction recursion should have been skipped")

    monkeypatch.setattr("dirstat_skill.engine_windows.os.scandir", fake_scandir)

    nodes, total_size = _scan_path(root=root, swallow_root_errors=False)

    assert nodes == []
    assert total_size == 0

