import contextlib
import importlib.util
import io
import urllib.error
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "esa_acme_issue.py"
SPEC = importlib.util.spec_from_file_location("esa_acme_issue", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def build_acme_output(challenges):
    blocks = []
    for fqdn, token in challenges:
        blocks.append(f"Domain: '{fqdn}'\nTXT value: '{token}'")
    return "\n\n".join(blocks)


class FlowTests(unittest.TestCase):
    def setUp(self):
        MODULE._REGION = None

    def test_esa_req_retries_connection_reset_then_succeeds(self):
        calls = {"count": 0}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"ok": true}'

        def fake_urlopen(req, timeout=60):
            calls["count"] += 1
            if calls["count"] == 1:
                raise urllib.error.URLError("[Errno 104] Connection reset by peer")
            return FakeResponse()

        with patch.object(MODULE.urllib.request, "urlopen", side_effect=fake_urlopen), \
             patch.object(MODULE.time, "sleep"):
            result = MODULE.esa_req({"ak": "ak", "sk": "sk"}, "ListSites", "GET", region="cn-hangzhou")

        self.assertEqual(result, {"ok": True})
        self.assertEqual(calls["count"], 2)

    def test_main_success_runs_full_dns_and_install_flow(self):
        created = []
        deleted = []
        challenge_output = build_acme_output(
            [
                ("_acme-challenge.example.com", "token-one"),
                ("_acme-challenge.example.com", "token-two"),
            ]
        )

        def fake_run(cmd, timeout=MODULE.DEFAULT_CMD_TIMEOUT):
            if "--issue" in cmd:
                self.assertEqual(
                    cmd,
                    [
                        "/mock/acme.sh",
                        "--issue",
                        "--dns",
                        "-d",
                        "example.com",
                        "-d",
                        "*.example.com",
                        "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
                        "--keylength",
                        "ec-256",
                    ],
                )
                return 0, challenge_output
            if "--renew" in cmd:
                self.assertIn("example.com", cmd)
                return 0, "renew ok"
            if "--install-cert" in cmd:
                self.assertEqual(
                    cmd,
                    [
                        "/mock/acme.sh",
                        "--install-cert",
                        "-d",
                        "example.com",
                        "--ecc",
                        "--fullchain-file",
                        "/etc/nginx/ssl/example.com.crt",
                        "--key-file",
                        "/etc/nginx/ssl/example.com.key",
                        "--reloadcmd",
                        "systemctl reload nginx",
                    ],
                )
                return 0, "install ok"
            self.fail(f"unexpected command: {cmd}")

        def fake_esa_req(client, action, method="POST", region=None, **params):
            if action == "CreateRecord":
                record_id = f"api-record-{len(created) + 1}"
                created.append((params["RecordName"], params["Data"], record_id))
                return {"RecordId": record_id}
            if action == "DeleteRecord":
                deleted.append(params["RecordId"])
                return {"RequestId": "cleanup-ok"}
            self.fail(f"unexpected ESA action: {action}")

        def fake_wait_visible(client, site_id, fqdn, token, timeout=120):
            return True, f"confirmed-{token}"

        stdout = io.StringIO()
        with patch.object(MODULE, "ensure_python_deps"), \
             patch.object(MODULE, "find_acme_sh", return_value="/mock/acme.sh"), \
             patch.object(MODULE, "print_security_reminders"), \
             patch.object(MODULE, "ensure_parent_dirs"), \
             patch.object(MODULE, "make_acs_client", side_effect=["probe-client", "active-client"]) as make_client_mock, \
             patch.object(MODULE, "auto_detect_region", return_value=("cn-hangzhou", "site-1", "example.com")), \
             patch.object(MODULE, "run", side_effect=fake_run) as run_mock, \
             patch.object(MODULE, "esa_req", side_effect=fake_esa_req), \
             patch.object(MODULE, "wait_record_visible_in_esa", side_effect=fake_wait_visible), \
             patch.object(MODULE, "wait_dns_record", return_value=(True, "visible")) as wait_dns_mock, \
             patch("sys.argv", ["esa_acme_issue.py", "-d", "example.com", "-d", "*.example.com", "--ak", "ak", "--sk", "sk", "--sts-token", "sts", "--install-cert"]), \
             contextlib.redirect_stdout(stdout):
            MODULE.main()

        self.assertEqual(len(created), 2)
        self.assertEqual(
            deleted,
            ["confirmed-token-one", "confirmed-token-two"],
        )
        self.assertEqual(run_mock.call_count, 3)
        self.assertEqual(wait_dns_mock.call_count, 2)
        self.assertTrue(all(call.kwargs["sts_token"] == "sts" for call in make_client_mock.call_args_list))
        self.assertIn("[OK] installed to /etc/nginx/ssl/example.com.crt, /etc/nginx/ssl/example.com.key", stdout.getvalue())

    def test_main_cleans_up_txt_records_when_renew_fails(self):
        deleted = []
        challenge_output = build_acme_output(
            [
                ("_acme-challenge.test.example.com", "token-one"),
            ]
        )

        def fake_run(cmd, timeout=MODULE.DEFAULT_CMD_TIMEOUT):
            if "--issue" in cmd:
                return 0, challenge_output
            if "--renew" in cmd:
                return 1, "renew failed"
            self.fail(f"unexpected command: {cmd}")

        def fake_esa_req(client, action, method="POST", region=None, **params):
            if action == "CreateRecord":
                return {"RecordId": "api-record-1"}
            if action == "DeleteRecord":
                deleted.append(params["RecordId"])
                return {"RequestId": "cleanup-ok"}
            self.fail(f"unexpected ESA action: {action}")

        stdout = io.StringIO()
        with patch.object(MODULE, "ensure_python_deps"), \
             patch.object(MODULE, "find_acme_sh", return_value="/mock/acme.sh"), \
             patch.object(MODULE, "print_security_reminders"), \
             patch.object(MODULE, "make_acs_client", side_effect=["probe-client", "active-client"]), \
             patch.object(MODULE, "auto_detect_region", return_value=("cn-hangzhou", "site-1", "example.com")), \
             patch.object(MODULE, "run", side_effect=fake_run), \
             patch.object(MODULE, "esa_req", side_effect=fake_esa_req), \
             patch.object(MODULE, "wait_record_visible_in_esa", return_value=(True, "confirmed-token-one")), \
             patch.object(MODULE, "wait_dns_record", return_value=(True, "visible")), \
             patch("sys.argv", ["esa_acme_issue.py", "-d", "test.example.com", "--ak", "ak", "--sk", "sk"]), \
             contextlib.redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as cm:
                MODULE.main()

        self.assertEqual(cm.exception.code, 5)
        self.assertEqual(deleted, ["confirmed-token-one"])
        self.assertIn("[ERR] renew/sign failed", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
