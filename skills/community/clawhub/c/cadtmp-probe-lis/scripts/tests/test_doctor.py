import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCTOR = ROOT / "scripts" / "doctor.py"
ALLOWED_STATUSES = {"可用", "需外部转换", "需OCR引擎", "不可用"}


class CadDoctorTest(unittest.TestCase):
    def _run(self, tmp: Path, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(DOCTOR), *extra],
            capture_output=True, text=True, timeout=60, cwd=str(tmp),
        )

    def test_json_report_schema_and_files(self):
        with tempfile.TemporaryDirectory(prefix="cad-doctor-") as tmpd:
            tmp = Path(tmpd)
            proc = self._run(tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(proc.stdout.strip())
            json_path = tmp / "doctor-report.json"
            self.assertTrue(json_path.exists())
            report = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(report["tool"], "cad-file-reader-doctor")
            self.assertEqual(report["schema"], "cad-file-reader/doctor-v1")
            caps = report["tier0"]["capabilities"]
            for key in ("dxf", "dwg", "pdf_vector", "pdf_raster_ocr", "measure", "qto_linkage"):
                self.assertIn(key, caps)
                self.assertIn(caps[key]["status"], ALLOWED_STATUSES,
                              f"{key} 状态必须是可用/需外部转换/需OCR引擎/不可用")
            self.assertIn("tier1", report)
            self.assertIn("fixes", report["tier1"])
            self.assertIn("tier2", report)
            self.assertIn("dwg_conversion_backends", report["tier2"])
            self.assertIn("next_steps", report["tier2"])
            md_path = tmp / "doctor-report.md"
            self.assertTrue(md_path.exists())
            md = md_path.read_text(encoding="utf-8")
            self.assertIn("档 0", md)
            self.assertIn("档 2", md)

    def test_json_only_does_not_write(self):
        with tempfile.TemporaryDirectory(prefix="cad-doctor-") as tmpd:
            tmp = Path(tmpd)
            proc = self._run(tmp, "--json-only")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            self.assertEqual(report["tool"], "cad-file-reader-doctor")
            self.assertFalse((tmp / "doctor-report.json").exists())
            self.assertFalse((tmp / "doctor-report.md").exists())

    def test_no_write_keeps_dir_clean(self):
        with tempfile.TemporaryDirectory(prefix="cad-doctor-") as tmpd:
            tmp = Path(tmpd)
            proc = self._run(tmp, "--no-write")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse((tmp / "doctor-report.json").exists())
            self.assertFalse((tmp / "doctor-report.md").exists())
            self.assertIn("档 0", proc.stdout)

    def test_md_only(self):
        with tempfile.TemporaryDirectory(prefix="cad-doctor-") as tmpd:
            tmp = Path(tmpd)
            proc = self._run(tmp, "--md-only")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("cad-file-reader 环境体检报告", proc.stdout)
            self.assertIn("## 档 0", proc.stdout)
            self.assertIn("| 能力 |", proc.stdout)


if __name__ == "__main__":
    unittest.main()
