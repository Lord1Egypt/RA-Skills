"""Tests for Confluence Publish Skill."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import ConfluencePublishSkill, handler, normalize_base_url, parse_page_document, read_env_file


class TestHelpers(unittest.TestCase):
    def test_normalize_base_url_from_domain(self):
        self.assertEqual(
            normalize_base_url("exampletenant"),
            "https://exampletenant.atlassian.net/wiki",
        )

    def test_normalize_base_url_from_full_url(self):
        self.assertEqual(
            normalize_base_url("https://exampletenant.atlassian.net"),
            "https://exampletenant.atlassian.net/wiki",
        )

    def test_normalize_base_url_rejects_non_atlassian_host(self):
        with self.assertRaises(ValueError):
            normalize_base_url("https://evil.example.com/wiki")

    def test_normalize_base_url_rejects_http(self):
        with self.assertRaises(ValueError):
            normalize_base_url("http://exampletenant.atlassian.net/wiki")

    def test_parse_page_document_with_metadata_block(self):
        raw = """<!-- {\"space_key\":\"ABC\",\"page_title\":\"Demo\"} -->\n<h1>Hello</h1>"""
        metadata, body = parse_page_document(raw)
        self.assertEqual(metadata["space_key"], "ABC")
        self.assertEqual(metadata["page_title"], "Demo")
        self.assertIn("<h1>Hello</h1>", body)

    def test_read_env_file_supports_colon_and_equals(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write("EMAIL:test@example.com\nDOMAIN=exampletenant\nAPI_TOKEN='abc'\n")
            path = tmp.name
        try:
            env = read_env_file(path)
            self.assertEqual(env["EMAIL"], "test@example.com")
            self.assertEqual(env["DOMAIN"], "exampletenant")
            self.assertEqual(env["API_TOKEN"], "abc")
        finally:
            os.remove(path)


class TestConfluencePublishSkill(unittest.TestCase):
    def setUp(self):
        self.skill = ConfluencePublishSkill()
        self.base_config = {
            "credentials": {
                "EMAIL": "user@example.com",
                "DOMAIN": "exampletenant",
                "API_TOKEN": "token",
            }
        }

    @patch("main.ConfluenceClient.upsert_page")
    def test_publish_page_from_metadata_comment(self, mock_upsert):
        mock_upsert.return_value = (
            "created",
            {"id": "123", "title": "Demo", "_links": {"webui": "/spaces/ABC/pages/123"}},
        )
        input_doc = """<!-- {"space_key":"ABC","page_title":"Demo"} -->\n<h1>Body</h1>"""
        result = self.skill.publish_page(input_doc, self.base_config)
        self.assertEqual(result["operation"], "created")
        self.assertEqual(result["page_id"], "123")
        self.assertIn("/wiki/spaces/ABC/pages/123", result["url"])

    @patch("main.ConfluenceClient.test_connection")
    def test_test_connection(self, mock_test_connection):
        mock_test_connection.return_value = {"displayName": "User", "accountId": "1", "type": "known"}
        result = self.skill.test_connection("", self.base_config)
        self.assertEqual(result["displayName"], "User")
        self.assertEqual(result["base_url"], "https://exampletenant.atlassian.net/wiki")

    @patch("main.ConfluenceClient.upsert_page")
    def test_publish_page_with_config_override(self, mock_upsert):
        mock_upsert.return_value = ("updated", {"id": "2", "title": "FromConfig", "_links": {}})
        result = self.skill.publish_page(
            "<p>Body</p>",
            {
                **self.base_config,
                "space_key": "SPACE",
                "page_title": "FromConfig",
                "body_html": "<h1>Configured</h1>",
            },
        )
        self.assertEqual(result["operation"], "updated")
        self.assertEqual(result["space_key"], "SPACE")

    def test_publish_page_missing_metadata(self):
        with self.assertRaises(ValueError):
            self.skill.publish_page("<h1>Body</h1>", self.base_config)

    def test_missing_credentials(self):
        with self.assertRaises(ValueError):
            self.skill.test_connection("", {"credentials": {"EMAIL": "x"}})

    def test_env_file_outside_workspace_is_rejected(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write("EMAIL=user@example.com\nDOMAIN=exampletenant\nAPI_TOKEN=abc\n")
            outside_path = tmp.name
        try:
            with self.assertRaises(ValueError):
                self.skill.test_connection(
                    "",
                    {
                        "env_file": outside_path,
                        "credentials": {},
                    },
                )
        finally:
            os.remove(outside_path)

    def test_page_path_outside_workspace_is_rejected(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write('<!-- {"space_key":"A","page_title":"T"} --><h1>Body</h1>')
            outside_path = tmp.name
        try:
            with self.assertRaises(ValueError):
                self.skill.publish_page(
                    "",
                    {
                        **self.base_config,
                        "page_path": outside_path,
                    },
                )
        finally:
            os.remove(outside_path)

    def test_page_path_inside_workspace_is_allowed(self):
        temp_path = Path("tmp_confluence_page_test.html")
        temp_path.write_text(
            '<!-- {"space_key":"A","page_title":"T"} --><h1>Body</h1>',
            encoding="utf-8",
        )
        try:
            with patch("main.ConfluenceClient.upsert_page") as mock_upsert:
                mock_upsert.return_value = ("created", {"id": "1", "title": "T", "_links": {}})
                result = self.skill.publish_page(
                    "",
                    {
                        **self.base_config,
                        "page_path": str(temp_path),
                    },
                )
                self.assertEqual(result["operation"], "created")
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_base_url_override_rejects_non_atlassian(self):
        with self.assertRaises(ValueError):
            self.skill.test_connection(
                "",
                {
                    **self.base_config,
                    "base_url": "https://evil.example.com/wiki",
                },
            )


class TestHandler(unittest.TestCase):
    @patch("main.ConfluenceClient.upsert_page")
    def test_handler_success(self, mock_upsert):
        mock_upsert.return_value = ("created", {"id": "1", "title": "T", "_links": {}})
        result = handler(
            {
                "action": "publish_page",
                "input": '<!-- {"space_key":"A","page_title":"T"} --><p>x</p>',
                "config": {
                    "credentials": {
                        "EMAIL": "user@example.com",
                        "DOMAIN": "exampletenant",
                        "API_TOKEN": "token",
                    }
                },
            }
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["action"], "publish_page")

    def test_handler_unknown_action(self):
        result = handler({"action": "unknown", "input": "", "config": {}})
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
