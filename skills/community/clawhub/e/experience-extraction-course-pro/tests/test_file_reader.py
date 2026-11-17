import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "file_reader.py"


class FileReaderTests(unittest.TestCase):
    def test_file_reader_prints_unicode_under_legacy_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.md"
            source.write_text("中文资料\n⚠️ 风险提示\n🟢 可直接复用", encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "cp936"

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--file_path", str(source)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
            output = result.stdout.decode("utf-8", errors="replace")
            self.assertIn("中文资料", output)
            self.assertIn("风险提示", output)
            self.assertIn("可直接复用", output)

    def test_long_text_is_not_truncated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "long.md"
            content = "课程资料" * 5000
            source.write_text(content, encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--file_path", str(source)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.rstrip("\r\n"), content)

    def test_help_and_errors_are_chinese(self) -> None:
        help_result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("提取课程资料中的可读文本", help_result.stdout)
        self.assertNotIn("max_pages", help_result.stdout)
        self.assertNotIn("max_chars", help_result.stdout)

        missing_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--file_path",
                str(ROOT / "不存在的资料.md"),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertNotEqual(missing_result.returncode, 0)
        self.assertIn("文件不存在", missing_result.stderr)

if __name__ == "__main__":
    unittest.main()
