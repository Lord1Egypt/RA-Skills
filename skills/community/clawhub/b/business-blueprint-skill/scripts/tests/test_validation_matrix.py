from __future__ import annotations

import json
from pathlib import Path

from business_blueprint.validation_matrix import (
    DEFAULT_TEMPLATE_PROFILES,
    build_template_validation_matrix,
)


def test_template_validation_matrix_exports_one_medium_blueprint_per_template(
    tmp_path: Path,
) -> None:
    summary = build_template_validation_matrix(output_dir=tmp_path, render_png=False)

    summary_path = tmp_path / "template-validation-summary.json"
    assert summary_path.exists()
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert payload == summary
    assert payload["entryCount"] == len(DEFAULT_TEMPLATE_PROFILES)

    industries = {entry["industry"] for entry in payload["entries"]}
    assert industries == set(DEFAULT_TEMPLATE_PROFILES)

    for entry in payload["entries"]:
        assert entry["complexity"] == "medium"
        assert entry["templateId"] == entry["industry"]
        assert entry["templateName"] == DEFAULT_TEMPLATE_PROFILES[entry["industry"]]["templateName"]
        assert entry["validation"]["errorCount"] == 0
        assert entry["validation"]["capabilityCount"] >= 4 or entry["blueprintType"] == "domain-knowledge"
        assert entry["validation"]["relationCount"] >= 6

        blueprint_path = Path(entry["blueprintPath"])
        svg_path = Path(entry["svgPath"])
        html_path = Path(entry["htmlPath"])

        assert blueprint_path.exists()
        assert svg_path.exists()
        assert html_path.exists()

        blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))
        assert blueprint["meta"]["industry"] == entry["industry"]
        assert blueprint["meta"]["templateId"] == entry["industry"]
        assert blueprint["meta"]["templateName"] == entry["templateName"]

        html = html_path.read_text(encoding="utf-8")
        assert "Schema v1.0" in html
        assert f"Template: {entry['templateName']}" in html
        assert "Skill v" not in html
        assert "Business Blueprint v" not in html

        svg = svg_path.read_text(encoding="utf-8")
        assert f"visual-profile: {entry['visualProfile']}" in svg
        assert entry["pngStatus"] == "disabled"
