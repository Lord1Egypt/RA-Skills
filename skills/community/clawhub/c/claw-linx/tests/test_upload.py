import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote, unquote

HELPER = Path(__file__).resolve().parents[1] / "scripts/upload.py"


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        curl = shutil.which("curl")
        if not curl:
            self.skipTest("curl required")
        (self.bin / "curl").symlink_to(curl)
        self.source = self.root / "hello # world.txt"
        self.source.write_bytes(b"Linx upload smoke\n")
        self.requests = []
        self.status = 200
        self.bad_checksum = False
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_PUT(self):
                if self.headers.get("Transfer-Encoding") == "chunked":
                    parts = []
                    while True:
                        size = int(self.rfile.readline().strip(), 16)
                        if not size:
                            self.rfile.readline()
                            break
                        parts.append(self.rfile.read(size))
                        self.rfile.read(2)
                    body = b"".join(parts)
                else:
                    body = self.rfile.read(int(self.headers["Content-Length"]))
                owner.requests.append((self.path, self.headers, body))
                name = quote(unquote(self.path.rsplit("/", 1)[-1]), safe="")
                result = {"url": owner.base + name, "direct_url": owner.base + "selif/" + name,
                          "delete_key": "private-delete-key", "sha256sum": "bad" if owner.bad_checksum else hashlib.sha256(body).hexdigest()}
                if owner.status != 200:
                    result = {"error": "upload rejected"}
                data = json.dumps(result).encode()
                self.send_response(owner.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = f"http://127.0.0.1:{server.server_port}/prefix/"
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("LINX_")}
        self.env.update(PATH=str(self.bin), HOME=str(self.root), XDG_CONFIG_HOME=str(self.root / "config"),
                        XDG_STATE_HOME=str(self.root / "state"), LINX_URL=self.base, LINX_API_KEY="environment-key")
        self.log = self.root / "state/openclaw-linx/uploads.json"

    def run_upload(self, *options):
        return subprocess.run([sys.executable, str(HELPER), *options, "--", str(self.source)],
                              env=self.env, capture_output=True, text=True, timeout=20)

    def install_client(self):
        client = os.environ.get("LINX_TEST_CLIENT")
        if not client:
            self.skipTest("set LINX_TEST_CLIENT to test real binary")
        (self.bin / "linx-client").symlink_to(Path(client).resolve())

    def test_curl_bytes_headers_encoded_name_and_private_log(self):
        result = self.run_upload("--expiry", "600", "--randomize", "--direct")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), self.base + "selif/" + quote(self.source.name, safe=""))
        path, headers, body = self.requests[0]
        self.assertEqual(path, "/prefix/upload/hello%20%23%20world.txt")
        self.assertEqual(body, self.source.read_bytes())
        self.assertEqual(headers["Linx-Api-Key"], "environment-key")
        self.assertEqual(headers["Linx-Expiry"], "600")
        self.assertEqual(headers["Linx-Randomize"], "yes")
        self.assertEqual(json.loads(self.log.read_text()), {self.base + quote(self.source.name, safe=""): "private-delete-key"})
        self.assertEqual(self.log.stat().st_mode & 0o777, 0o600)
        self.assertNotIn("private-delete-key", result.stdout + result.stderr)

    def test_config_environment_precedence_and_key_clearing(self):
        config = self.root / "client.json"
        custom_log = self.root / "custom.json"
        config.write_text(json.dumps({"siteurl": "http://127.0.0.1:1/", "apikey": "config-key", "logfile": str(custom_log)}))
        self.env.update(LINX_CONFIG=str(config), LINX_API_KEY="")
        result = self.run_upload("--name", "renamed.txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requests[0][0], "/prefix/upload/renamed.txt")
        self.assertIsNone(self.requests[0][1].get("Linx-Api-Key"))
        self.assertIn(self.base + "renamed.txt", json.loads(custom_log.read_text()))

    def test_explicit_missing_config_fails_before_upload(self):
        self.env["LINX_CONFIG"] = str(self.root / "missing")
        result = self.run_upload()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.requests, [])

    def test_http_error_does_not_retry_or_log_success(self):
        self.status = 403
        result = self.run_upload()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HTTP 403", result.stderr)
        self.assertEqual(len(self.requests), 1)
        self.assertFalse(self.log.exists())

    def test_checksum_failure_preserves_delete_key(self):
        self.bad_checksum = True
        result = self.run_upload()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksum mismatch", result.stderr)
        self.assertEqual(json.loads(self.log.read_text())[self.base + quote(self.source.name, safe="")], "private-delete-key")
        self.assertEqual(result.stdout, "")

    def test_real_client_preferred_and_config_only(self):
        self.install_client()
        # Curl absent: successful upload proves binary use, not mocked forwarding.
        (self.bin / "curl").unlink()
        config = self.root / "client.json"
        config.write_text(json.dumps({"siteurl": self.base, "apikey": "config-key", "logfile": str(self.log)}))
        self.env["LINX_CONFIG"] = str(config)
        del self.env["LINX_URL"]
        del self.env["LINX_API_KEY"]
        result = self.run_upload("--name", "report.txt", "--expiry", "90", "--randomize", "--direct")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), self.base + "selif/report.txt")
        self.assertEqual(self.requests[0][2], self.source.read_bytes())
        self.assertEqual(self.requests[0][1]["Linx-Api-Key"], "config-key")
        self.assertEqual(self.requests[0][1]["Linx-Expiry"], "90")
        self.assertEqual(self.requests[0][1]["Linx-Randomize"], "yes")
        self.assertEqual(json.loads(self.log.read_text())[self.base + "report.txt"], "private-delete-key")

    def test_real_client_zero_exit_error_never_falls_back(self):
        self.install_client()
        self.status = 409
        result = self.run_upload("--name", "conflict.txt")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No fallback attempted", result.stderr)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
