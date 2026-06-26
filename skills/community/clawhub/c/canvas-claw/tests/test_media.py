from pathlib import Path

from canvas_claw.media import classify_media_input


def test_classify_local_path(tmp_path: Path) -> None:
    path = tmp_path / "frame.png"
    path.write_bytes(b"fake")
    result = classify_media_input(str(path))
    assert result.kind == "file"
    assert result.path == path
