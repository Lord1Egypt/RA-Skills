import json
import os
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from email_crm import connect, initialize  # noqa: E402


class EmailCrmCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.temp.name) / "crm.sqlite")

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, script, *args, expected=0, stdin=None):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / script), "--db", self.db, *args],
            input=stdin,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout)

    def fetchone(self, query, params=()):
        with sqlite3.connect(self.db) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(query, params).fetchone()

    def test_readiness_and_suppression_are_normalized_and_idempotent(self):
        self.assertEqual(self.invoke("init_email_crm.py")["schema_version"], 1)
        contact = self.invoke(
            "upsert_contact.py", "--email-stdin", "--source", "manual-review", stdin=" Alice@Example.COM \n"
        )
        self.assertEqual(contact, {"ok": True, "contact_id": 1})
        self.assertTrue(
            self.invoke("check_email_readiness.py", "--email-stdin", stdin="alice@example.com\n")["ready"]
        )
        first = self.invoke(
            "suppress_email.py", "--email-stdin", "--reason", "unsubscribe", stdin="ALICE@example.com\n"
        )
        second = self.invoke(
            "suppress_email.py", "--email-stdin", "--reason", "complaint", stdin="alice@example.com\n"
        )
        self.assertEqual(first["reason"], "unsubscribe")
        self.assertEqual(second["reason"], "unsubscribe")
        result = self.invoke(
            "check_email_readiness.py", "--email-stdin", expected=1, stdin=" alice@example.com \n"
        )
        self.assertFalse(result["ready"])
        self.assertEqual(set(result["reasons"]), {"contact_do_not_contact", "email_suppressed"})

    def test_suppression_before_contact_synchronizes_do_not_contact(self):
        self.invoke("suppress_email.py", "--email-stdin", "--reason", "manual_dnc", stdin="later@example.com\n")
        self.invoke(
            "upsert_contact.py", "--email-stdin", "--source", "manual-review", stdin="LATER@example.com\n"
        )
        row = self.fetchone(
            "SELECT email, email_normalized, do_not_contact FROM contacts WHERE email_normalized = ?",
            ("later@example.com",),
        )
        self.assertEqual(tuple(row), ("later@example.com", "later@example.com", 1))
        readiness = self.invoke("check_email_readiness.py", "--email", "later@example.com", expected=1)
        self.assertEqual(set(readiness["reasons"]), {"contact_do_not_contact", "email_suppressed"})

    def test_upsert_normalizes_storage_and_updates_source(self):
        first = self.invoke("upsert_contact.py", "--email", "Person@Example.COM", "--source", "first")
        second = self.invoke("upsert_contact.py", "--email", "person@example.com", "--source", "second")
        self.assertEqual(first["contact_id"], second["contact_id"])
        row = self.fetchone("SELECT email, email_normalized, source FROM contacts")
        self.assertEqual(tuple(row), ("person@example.com", "person@example.com", "second"))

    def test_unsupported_schema_is_rejected_without_mutation_or_ddl(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("CREATE TABLE schema_meta (singleton INTEGER PRIMARY KEY, schema_version INTEGER, updated_at TEXT)")
            conn.execute("INSERT INTO schema_meta VALUES (1, 999, 'future')")
            conn.execute("CREATE TABLE future_data (value TEXT)")
            conn.execute("INSERT INTO future_data VALUES ('preserve-me')")
        before = Path(self.db).read_bytes()
        before_files = sorted(path.name for path in Path(self.temp.name).iterdir())

        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "init_email_crm.py"), "--db", self.db],
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("database schema is newer than this skill", result.stderr)
        self.assertEqual(Path(self.db).read_bytes(), before)
        self.assertEqual(sorted(path.name for path in Path(self.temp.name).iterdir()), before_files)
        with sqlite3.connect(self.db) as conn:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            self.assertEqual(tables, {"schema_meta", "future_data"})
            self.assertEqual(conn.execute("SELECT value FROM future_data").fetchone()[0], "preserve-me")

    def test_older_schema_is_rejected_without_mutation(self):
        with sqlite3.connect(self.db) as conn:
            conn.execute("CREATE TABLE schema_meta (singleton INTEGER PRIMARY KEY, schema_version INTEGER, updated_at TEXT)")
            conn.execute("INSERT INTO schema_meta VALUES (1, 0, 'legacy')")
        before = Path(self.db).read_bytes()

        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "init_email_crm.py"), "--db", self.db],
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no migration is available", result.stderr)
        self.assertEqual(Path(self.db).read_bytes(), before)

    def test_database_and_live_sidecars_are_owner_only(self):
        old_umask = os.umask(0)
        try:
            conn = connect(self.db)
            initialize(conn)
            conn.execute("INSERT INTO contacts (email, email_normalized, source, created_at, updated_at) "
                         "VALUES ('mode@example.com', 'mode@example.com', 'test', 'now', 'now')")
            for path in (Path(self.db), Path(f"{self.db}-wal"), Path(f"{self.db}-shm")):
                self.assertTrue(path.exists(), str(path))
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600, str(path))
        finally:
            if "conn" in locals():
                conn.close()
            os.umask(old_umask)

    def test_default_database_is_per_user_and_independent_of_cwd(self):
        data_home = Path(self.temp.name) / "private-data"
        env = os.environ.copy()
        env.pop("EMAIL_CRM_DB", None)
        env["XDG_DATA_HOME"] = str(data_home)
        working_a = Path(self.temp.name) / "a"
        working_b = Path(self.temp.name) / "b"
        working_a.mkdir()
        working_b.mkdir()
        outputs = []
        for cwd in (working_a, working_b):
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_email_crm.py")],
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(json.loads(result.stdout)["db"])
        expected = data_home / "openclaw-email-crm" / "email_crm.sqlite"
        self.assertEqual(outputs, [str(expected), str(expected)])
        self.assertTrue(expected.exists())
        self.assertFalse((working_a / "data").exists())
        self.assertFalse((working_b / "data").exists())

        empty_xdg_env = env.copy()
        empty_xdg_env["XDG_DATA_HOME"] = ""
        empty_xdg_env["HOME"] = str(Path(self.temp.name) / "home")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "init_email_crm.py")],
            cwd=working_a,
            env=empty_xdg_env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        home_default = Path(empty_xdg_env["HOME"]) / ".local" / "share" / "openclaw-email-crm" / "email_crm.sqlite"
        self.assertEqual(json.loads(result.stdout)["db"], str(home_default))
        self.assertTrue(home_default.exists())

    def test_event_requires_real_contact(self):
        self.invoke("init_email_crm.py")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "log_email_event.py"), "--db", self.db, "--contact-id", "99", "--event-type", "sent"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_event_metadata_is_validated_and_canonicalized(self):
        contact_id = self.invoke("upsert_contact.py", "--email", "event@example.com", "--source", "test")["contact_id"]
        event = self.invoke(
            "log_email_event.py", "--contact-id", str(contact_id), "--event-type", "queued",
            "--metadata-json", '{"z": 1, "a": true}',
        )
        self.assertEqual(event["event_type"], "queued")
        self.assertEqual(self.fetchone("SELECT metadata_json FROM email_events")[0], '{"a":true,"z":1}')
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "log_email_event.py"), "--db", self.db,
             "--contact-id", str(contact_id), "--event-type", "sent", "--metadata-json", "{"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_invalid_email_fails_closed_from_stdin(self):
        self.invoke("init_email_crm.py")
        result = self.invoke("check_email_readiness.py", "--email-stdin", expected=1, stdin="not-an-email\n")
        self.assertEqual(result["reasons"], ["invalid_email"])


if __name__ == "__main__":
    unittest.main()
