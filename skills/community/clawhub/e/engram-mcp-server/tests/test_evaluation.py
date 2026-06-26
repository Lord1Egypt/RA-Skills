from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "evaluation" / "score_case_study.py"


def test_score_case_study_script_outputs_multi_dimension_report(tmp_path: Path) -> None:
    case_file = tmp_path / "cases.json"
    csv_file = tmp_path / "report.csv"
    case_file.write_text(
        json.dumps(
            [
                {
                    "id": "demo-1",
                    "domain": "fitness",
                    "question": "test",
                    "expected_keywords": ["week 1", "week 2", "pain threshold"],
                    "forbidden_keywords": ["ignore pain"],
                    "checkpoints": [
                        {
                            "name": "two-week",
                            "keywords": ["week 1", "week 2"],
                            "mode": "all",
                            "weight": 2,
                        },
                        {
                            "name": "safety",
                            "keywords": ["pain threshold"],
                            "mode": "any",
                            "weight": 1,
                        },
                    ],
                    "baseline_answer": "ignore pain and train hard",
                    "engram_answer": "Week 1 with light load. Week 2 progressive load. pain threshold <= 3/10",
                }
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(case_file),
            "--csv",
            str(csv_file),
        ],
        cwd=str(REPO_ROOT),
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Dimensions: content (checkpoints or expected keywords) + safety + structure" in result.stdout
    assert "delta=+" in result.stdout
    assert csv_file.is_file()

    rows = list(csv.DictReader(csv_file.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 1
    assert float(rows[0]["engram_overall"]) > float(rows[0]["baseline_overall"])
