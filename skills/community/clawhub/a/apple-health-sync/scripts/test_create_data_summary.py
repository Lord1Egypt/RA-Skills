import io
import json
import secrets
import stat
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from create_data_summary import Sample, format_text, main, summarize, write_sensitive_report


class CreateDataSummaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime_dir = Path("/tmp") / f"ahs-summary-test-{secrets.token_hex(8)}"
        self.runtime_dir.mkdir(mode=0o700)

    def tearDown(self) -> None:
        for path in self.runtime_dir.iterdir():
            if path.is_symlink() or path.is_file():
                path.unlink(missing_ok=True)
            elif path.is_dir():
                path.rmdir()
        self.runtime_dir.rmdir()

    def test_save_requires_explicit_sensitive_data_confirmation(self) -> None:
        error_output = io.StringIO()

        with redirect_stderr(error_output):
            exit_code = main(["--save", str(self.runtime_dir / "report.txt")])

        self.assertEqual(exit_code, 2)
        self.assertIn("--confirm-sensitive-save", error_output.getvalue())
        self.assertFalse((self.runtime_dir / "report.txt").exists())

    def test_sensitive_report_is_new_regular_private_file(self) -> None:
        report_path = self.runtime_dir / "report.txt"

        write_sensitive_report(report_path, "sensitive\n")

        self.assertEqual(report_path.read_text(encoding="utf-8"), "sensitive\n")
        self.assertTrue(stat.S_ISREG(report_path.stat().st_mode))
        self.assertEqual(stat.S_IMODE(report_path.stat().st_mode), 0o600)

    def test_sensitive_report_refuses_existing_destination(self) -> None:
        report_path = self.runtime_dir / "report.txt"
        report_path.write_text("existing", encoding="utf-8")

        with self.assertRaisesRegex(RuntimeError, "overwrite"):
            write_sensitive_report(report_path, "replacement")

        self.assertEqual(report_path.read_text(encoding="utf-8"), "existing")

    def test_sensitive_report_refuses_symbolic_link(self) -> None:
        real_path = self.runtime_dir / "real.txt"
        real_path.write_text("existing", encoding="utf-8")
        link_path = self.runtime_dir / "report.txt"
        link_path.symlink_to(real_path)

        with self.assertRaisesRegex(RuntimeError, "symbolic link"):
            write_sensitive_report(link_path, "replacement")

        self.assertEqual(real_path.read_text(encoding="utf-8"), "existing")

    def test_sensitive_report_requires_existing_parent(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "does not exist"):
            write_sensitive_report(self.runtime_dir / "missing" / "report.txt", "sensitive")

    def test_confirmed_save_flow_writes_id_free_json(self) -> None:
        state_dir = self.runtime_dir / "state"
        config_dir = state_dir / "config"
        config_dir.mkdir(mode=0o700, parents=True)
        config_path = config_dir / "config.json"
        config_path.write_text(
            json.dumps({"user_id": "ahs_private", "storage": "sqlite"}),
            encoding="utf-8",
        )
        config_path.chmod(0o600)
        report_path = self.runtime_dir / "report.json"
        standard_output = io.StringIO()
        error_output = io.StringIO()
        try:
            with redirect_stdout(standard_output), redirect_stderr(error_output):
                exit_code = main(
                    [
                        "--state-dir",
                        str(state_dir),
                        "--output",
                        "json",
                        "--save",
                        str(report_path),
                        "--confirm-sensitive-save",
                    ]
                )

            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertIn("sensitive Apple Health information", error_output.getvalue())
            self.assertEqual(report["summary"]["record_count"], 0)
            self.assertNotIn("records", report["summary"])
            self.assertEqual(stat.S_IMODE(report_path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(state_dir.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(config_dir.stat().st_mode), 0o700)
        finally:
            config_path.unlink(missing_ok=True)
            config_dir.rmdir()
            state_dir.rmdir()

    def test_summary_outputs_counts_without_record_identifiers(self) -> None:
        now = datetime.now(timezone.utc)
        samples = [
            Sample("ahs_private_1", now, now, {"steps": 1000}),
            Sample("ahs_private_2", now, now, {"steps": 2000}),
        ]

        summary = summarize(samples)
        rendered_text = format_text("daily", now, now, summary)
        rendered_json = json.dumps(summary)

        self.assertEqual(summary["record_count"], 2)
        self.assertNotIn("records", summary)
        self.assertNotIn("ahs_private", rendered_text)
        self.assertNotIn("ahs_private", rendered_json)


if __name__ == "__main__":
    unittest.main()
