#!/usr/bin/env python3
"""Tests for clawallex.py credential helpers, API client, and setup command."""

import argparse
import base64
import contextlib
import hashlib
import hmac
import io
import json
import os
import tempfile
import unittest

# Override module-level paths for testing (must happen before functions are called)
_tmpdir = tempfile.mkdtemp()

import clawallex as cw

cw.CREDENTIALS_DIR = _tmpdir
cw.CREDENTIALS_FILE = os.path.join(_tmpdir, "credentials.json")
cw.CLIENT_IDS_FILE = os.path.join(_tmpdir, "client_ids.json")


class TestCredentials(unittest.TestCase):

    def setUp(self):
        for f in [cw.CREDENTIALS_FILE, cw.CLIENT_IDS_FILE]:
            if os.path.exists(f):
                os.remove(f)

    def test_load_credentials_missing_file(self):
        result = cw.load_credentials()
        self.assertIsNone(result)

    def test_save_and_load_credentials(self):
        creds = {"apiKey": "ak_test", "apiSecret": "as_test", "baseUrl": "https://test.example.com"}
        cw.save_credentials(creds)
        loaded = cw.load_credentials()
        self.assertEqual(loaded["apiKey"], "ak_test")
        self.assertEqual(loaded["apiSecret"], "as_test")
        self.assertEqual(loaded["baseUrl"], "https://test.example.com")
        mode = os.stat(cw.CREDENTIALS_FILE).st_mode & 0o777
        self.assertEqual(mode, 0o600)

    def test_load_credentials_missing_keys(self):
        with open(cw.CREDENTIALS_FILE, "w") as f:
            json.dump({"apiKey": "ak_test"}, f)
        result = cw.load_credentials()
        self.assertIsNone(result)

    def test_save_and_resolve_client_id(self):
        cw.save_client_id("https://test.example.com", "test-client-id-123")
        cid = cw.resolve_client_id("https://test.example.com")
        self.assertEqual(cid, "test-client-id-123")

    def test_resolve_client_id_missing(self):
        cid = cw.resolve_client_id("https://nonexistent.example.com")
        self.assertIsNone(cid)

    def test_normalize_base_url(self):
        self.assertEqual(cw.normalize_base_url("https://API.Example.COM"), "https://api.example.com")
        self.assertEqual(cw.normalize_base_url("https://api.example.com:443"), "https://api.example.com")
        self.assertEqual(cw.normalize_base_url("http://api.example.com:8080"), "http://api.example.com:8080")


class TestOutputHelpers(unittest.TestCase):

    def test_output_success(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.output_success({"balance": "100"}, "Wallet OK")
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["balance"], "100")
        self.assertEqual(data["_hint"], "Wallet OK")

    def test_output_success_no_hint(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.output_success({"status": "ok"})
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertNotIn("_hint", data)

    def test_output_error(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.output_error("Something went wrong")
        self.assertEqual(code, 1)
        data = json.loads(buf.getvalue())
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "Something went wrong")


class TestClawalexClient(unittest.TestCase):

    def test_sign_get_request(self):
        client = cw.ClawalexClient("ak_test", "as_test", "https://api.test.com", "cid-" + "x" * 32)
        headers = client._sign("GET", "/api/v1/payment/wallets/detail", "")
        self.assertEqual(headers["X-API-Key"], "ak_test")
        self.assertEqual(headers["X-Client-Id"], "cid-" + "x" * 32)
        self.assertIn("X-Timestamp", headers)
        self.assertIn("X-Signature", headers)
        self.assertEqual(headers["Content-Type"], "application/json")
        base64.b64decode(headers["X-Signature"])

    def test_sign_post_request(self):
        client = cw.ClawalexClient("ak_test", "as_test", "https://api.test.com", "cid-" + "x" * 32)
        body = '{"amount": "50.0000"}'
        headers = client._sign("POST", "/api/v1/payment/card-orders", body)
        ts = headers["X-Timestamp"]
        body_hash = hashlib.sha256(body.encode()).hexdigest()
        canonical = f"POST\n/api/v1/payment/card-orders\n{ts}\n{body_hash}"
        expected_sig = base64.b64encode(
            hmac.new("as_test".encode(), canonical.encode(), hashlib.sha256).digest()
        ).decode()
        self.assertEqual(headers["X-Signature"], expected_sig)

    def test_build_url_get_with_query(self):
        client = cw.ClawalexClient("ak_test", "as_test", "https://api.test.com", "cid-" + "x" * 32)
        url = client._build_url("/payment/cards", {"page": 1, "page_size": 20})
        self.assertIn("/api/v1/payment/cards", url)
        self.assertIn("page=1", url)
        self.assertIn("page_size=20", url)

    def test_build_url_skips_empty_params(self):
        client = cw.ClawalexClient("ak_test", "as_test", "https://api.test.com", "cid-" + "x" * 32)
        url = client._build_url("/payment/cards", {"page": 1, "card_id": ""})
        self.assertIn("page=1", url)
        self.assertNotIn("card_id", url)


class TestCmdSetup(unittest.TestCase):

    def setUp(self):
        for f in [cw.CREDENTIALS_FILE, cw.CLIENT_IDS_FILE]:
            if os.path.exists(f):
                os.remove(f)

    def test_setup_status_not_configured(self):
        args = argparse.Namespace(action="status")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.cmd_setup(args)
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["data"]["status"], "not_configured")

    def test_setup_status_configured(self):
        cw.save_credentials({"apiKey": "ak_test_1234", "apiSecret": "as_test", "baseUrl": "https://test.com"})
        args = argparse.Namespace(action="status")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.cmd_setup(args)
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["data"]["status"], "configured")
        self.assertIn("...", data["data"]["api_key"])

    def test_setup_register(self):
        args = argparse.Namespace(action="register")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.cmd_setup(args)
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertIn("sign_up_url", data["data"])

    def test_setup_connect_missing_args(self):
        args = argparse.Namespace(action="connect", api_key=None, api_secret=None, base_url="https://api.test.com")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cw.cmd_setup(args)
        self.assertEqual(code, 1)
        data = json.loads(buf.getvalue())
        self.assertIn("required", data["error"].lower())


if __name__ == "__main__":
    unittest.main()
