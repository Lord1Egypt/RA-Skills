from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "expert_distiller.py"


class StandaloneScoreTest(unittest.TestCase):
    def run_cli(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def test_score_reads_artifact_and_writes_real_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "forum"
            project = Path(tmp) / "project"
            project.mkdir()
            (project / ".git").mkdir()
            paper = project / "paper.md"
            paper.write_text(
                """# Artifact

## Abstract
We analyze 540 paired records with intervals and p-value reporting.

## Introduction
This bounded study asks whether a controlled semantic specification helps.

## Related Work And Positioning
Prior work covers controlled language, DSLs, LLM code evaluation, and artifacts.

## Study Design
The paired comparison uses tasks, models, modes, and repeats.

## Results
| Model | Mode | N | Direct Python | CSL | Delta |
|---|---|---:|---:|---:|---:|
| `m1` | `think` | 30 | 33.3% | 63.3% | +30.0pp |
Wilson interval and exact paired discordance are reported.

## Discussion
The effect is conditional and not universal.

## Claim Ledger
Semantic correctness is rejected as a current claim.

## Limitations
Compile success does not prove semantic correctness.

## Artifact Availability
clean_research_assets/MANIFEST.csv and pytest checks are provided.

## References
Reference list.

## Conclusion
The artifact answers the structural-checkability question.
""",
                encoding="utf-8",
            )
            (project / "clean_research_assets").mkdir()
            (project / "clean_research_assets" / "MANIFEST.csv").write_text("source,dest\n", encoding="utf-8")

            self.run_cli("init", "--root", str(root), "--domain", "CSL Research", "--topic", "CSL paper review")
            for expert in ("controlled-natural-language", "statistical-analysis", "reproducibility-governance"):
                self.run_cli("candidate", "--root", str(root), "--domain", "CSL Research", "--name", expert)
                self.run_cli(
                    "source",
                    "--root",
                    str(root),
                    "--expert-id",
                    expert,
                    "--tier",
                    "A",
                    "--title",
                    "A source",
                    "--url",
                    "https://example.com/a",
                )
                self.run_cli(
                    "source",
                    "--root",
                    str(root),
                    "--expert-id",
                    expert,
                    "--tier",
                    "B",
                    "--title",
                    "B source",
                    "--url",
                    "https://example.com/b",
                )
                self.run_cli("audit", "--root", str(root), "--expert-id", expert)
                self.run_cli("profile", "--root", str(root), "--domain", "CSL Research", "--expert-id", expert, "--name", expert)
            self.run_cli("council", "create", "--root", str(root), "--domain", "CSL Research", "--name", "CSL Council")

            result = self.run_cli("score", "--root", str(root), "--domain", "CSL Research", "--artifact", str(paper))
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "standalone-real-score")
            self.assertGreater(payload["total"], 0)
            self.assertGreater(payload["score"]["breadth"], 0)
            self.assertTrue(payload["axes"][0]["expert_votes"])
            self.assertNotIn("No artifact evaluated yet", json.dumps(payload))

            reports = list((root / "scoring_reports").glob("*.json"))
            self.assertEqual(len(reports), 1)
            state = json.loads((root / "pipeline_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["last_score"]["total"], payload["total"])


if __name__ == "__main__":
    unittest.main()

