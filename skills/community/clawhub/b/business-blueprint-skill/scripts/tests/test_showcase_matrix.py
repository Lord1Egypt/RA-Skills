from __future__ import annotations

import json
from pathlib import Path

from business_blueprint.showcase_matrix import build_showcase_matrix


def test_showcase_matrix_writes_summary_and_profiled_svgs(tmp_path: Path) -> None:
    summary = build_showcase_matrix(
        output_dir=tmp_path,
        industries=["common", "retail"],
        visual_profiles=["executive-clean", "dark-ops"],
        theme="dark",
        render_png=False,
    )

    summary_path = tmp_path / "showcase-summary.json"
    assert summary_path.exists()
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert payload == summary
    assert len(payload["entries"]) == 4

    for entry in payload["entries"]:
        svg_path = Path(entry["svgPath"])
        assert svg_path.exists()
        svg = svg_path.read_text(encoding="utf-8")
        assert f"visual-profile: {entry['visualProfile']}" in svg
        assert entry["industry"] in {"common", "retail"}
        assert entry["pngStatus"] == "disabled"
