import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "cad_pdf_vec.py"
VENV = Path(os.environ.get("PDF_INSPECTOR_VENV", str(Path.home() / ".codex" / "skills" / "pdf-inspector" / ".venv" / "bin" / "python")))


class CadPdfVecTest(unittest.TestCase):
    def _make_text_pdf(self, workdir: Path) -> Path:
        txt = workdir / "sample.txt"
        txt.write_text("一层平面图\nC30 混凝土\n消火栓 2531\n", encoding="utf-8")
        pdf = workdir / "sample.pdf"
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(workdir), str(txt)],
            check=True, capture_output=True, timeout=120,
        )
        return pdf

    def test_extract_native_text_coords(self):
        if not VENV.is_file():
            self.skipTest("pdf-inspector venv not found")
        with tempfile.TemporaryDirectory(prefix="cad-vec-test-") as tmp:
            workdir = Path(tmp)
            pdf = self._make_text_pdf(workdir)
            out = workdir / "vec.json"
            proc = subprocess.run(
                [str(VENV), str(SCRIPT), str(pdf), "--json", str(out)],
                capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "cad-file-reader/pdf-vector-text-coords/v1")
            self.assertGreaterEqual(payload["count"], 1)
            for item in payload["items"]:
                self.assertEqual(item["page"], 1)
                self.assertIsInstance(item["x"], (int, float))
                self.assertIsInstance(item["y"], (int, float))
            self.assertIn("boundary", payload)
            self.assertTrue("final_quantity=false" in payload["boundary"])


if __name__ == "__main__":
    unittest.main()
