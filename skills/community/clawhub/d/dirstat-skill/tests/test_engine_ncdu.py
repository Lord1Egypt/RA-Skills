from pathlib import Path

from dirstat_skill.engine_ncdu import build_ncdu_export_command, detect_ncdu
from dirstat_skill.raw_export import load_raw_export


def test_detect_ncdu_returns_none_when_binary_missing() -> None:
    assert detect_ncdu(path_entries=[]) is None


def test_build_ncdu_export_command_uses_json_export_and_one_filesystem(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "export.json"

    command = build_ncdu_export_command(
        binary="ncdu",
        target=Path("/"),
        output_path=output_path,
        one_file_system=True,
        exclude_patterns=[".cache", "node_modules"],
    )

    assert command[:4] == ["ncdu", "-o", output_path.as_posix(), "-x"]
    assert "--exclude" in command
    assert command[-1] == "/"


def test_load_raw_export_wraps_ncdu_payload() -> None:
    payload = load_raw_export(Path("tests/fixtures/ncdu_minimal_export.json"))

    assert payload["engine"] == "ncdu"
    assert isinstance(payload["payload"], list)

