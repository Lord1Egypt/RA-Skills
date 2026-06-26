import json
from pathlib import Path

from canvas_claw.output import write_metadata


def test_write_metadata(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    metadata_path = write_metadata(
        output_dir=output_dir,
        payload={"task_id": "123", "status": "succeeded"},
    )
    assert metadata_path.exists()
    data = json.loads(metadata_path.read_text())
    assert data["task_id"] == "123"
