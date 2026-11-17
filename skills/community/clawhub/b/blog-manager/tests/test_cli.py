"""Tests for the CLI entry point, capability-list, and formatter output."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import pytest

from blog_manager import capability
from blog_manager.formatter import format_output


class TestCapabilityList:
    def test_returns_exactly_27_commands(self):
        data, kind = capability.list_commands()
        assert kind == "capability_list"
        assert data["total"] == 27
        assert len(data["commands"]) == 27

    def test_no_version_field(self):
        """v1.0.0: capability-list output must NOT contain a version field."""
        data, _ = capability.list_commands()
        assert "version" not in data
        assert "skill" not in data

    def test_each_command_has_required_fields(self):
        data, _ = capability.list_commands()
        for cmd in data["commands"]:
            assert "module" in cmd
            assert "name" in cmd
            assert "description" in cmd

    def test_module_distribution_matches_spec(self):
        data, _ = capability.list_commands()
        modules = {}
        for cmd in data["commands"]:
            modules[cmd["module"]] = modules.get(cmd["module"], 0) + 1
        assert modules == {
            "articles": 7,
            "labels": 2,
            "users": 2,
            "comments": 3,
            "messages": 4,
            "moods": 3,
            "uploads": 4,
            "health": 1,
            "meta": 1,
        }

    def test_capability_list_command_is_present(self):
        data, _ = capability.list_commands()
        names = [c["name"] for c in data["commands"]]
        assert "capability-list" in names

    def test_26_api_operations_plus_1_meta(self):
        data, _ = capability.list_commands()
        meta_count = sum(1 for c in data["commands"] if c["module"] == "meta")
        api_count = sum(1 for c in data["commands"] if c["module"] != "meta")
        assert meta_count == 1
        assert api_count == 26

    def test_all_command_names_are_kebab_case(self):
        data, _ = capability.list_commands()
        for cmd in data["commands"]:
            name = cmd["name"]
            assert " " not in name
            assert name == name.lower()


class TestCLIParsing:
    def _parse(self, argv):
        from main import build_parser

        parser = build_parser()
        return parser.parse_args(argv)

    def test_capability_list(self):
        ns = self._parse(["capability-list"])
        assert ns.command == "capability-list"

    def test_list_articles(self):
        ns = self._parse(["list-articles", "--page", "2", "--size", "5",
                          "--lid", "3", "--keyword", "py"])
        assert ns.command == "list-articles"
        assert ns.page == 2
        assert ns.size == 5
        assert ns.lid == 3
        assert ns.keyword == "py"

    def test_create_article(self):
        ns = self._parse(["create-article", "--title", "T", "--content", "C"])
        assert ns.command == "create-article"
        assert ns.title == "T"
        assert ns.content == "C"

    def test_get_article(self):
        ns = self._parse(["get-article", "--id", "42"])
        assert ns.command == "get-article"
        assert ns.article_id == 42

    def test_update_article(self):
        ns = self._parse(["update-article", "--id", "1", "--heat", "99"])
        assert ns.command == "update-article"
        assert ns.article_id == 1
        assert ns.heat == 99

    def test_delete_article_soft(self):
        ns = self._parse(["delete-article", "--id", "1"])
        assert ns.soft == "true"

    def test_delete_article_hard(self):
        ns = self._parse(["delete-article", "--id", "1", "--soft", "false"])
        assert ns.soft == "false"

    def test_restore_article(self):
        ns = self._parse(["restore-article", "--id", "1"])
        assert ns.article_id == 1

    def test_top_articles(self):
        ns = self._parse(["top-articles", "--limit", "3"])
        assert ns.limit == 3

    def test_list_labels(self):
        ns = self._parse(["list-labels"])
        assert ns.command == "list-labels"

    def test_create_label(self):
        ns = self._parse(["create-label", "--lname", "tech"])
        assert ns.lname == "tech"

    def test_list_users(self):
        ns = self._parse(["list-users"])
        assert ns.command == "list-users"

    def test_create_user(self):
        ns = self._parse(["create-user", "--uname", "alice"])
        assert ns.uname == "alice"

    def test_create_comment(self):
        ns = self._parse(["create-comment", "--uid", "1", "--aid", "2",
                          "--content", "c"])
        assert ns.uid == 1
        assert ns.aid == 2

    def test_list_comments(self):
        ns = self._parse(["list-comments", "--aid", "5"])
        assert ns.aid == 5

    def test_delete_comment(self):
        ns = self._parse(["delete-comment", "--id", "9"])
        assert ns.comment_id == 9

    def test_list_messages(self):
        ns = self._parse(["list-messages"])
        assert ns.command == "list-messages"

    def test_create_message(self):
        ns = self._parse(["create-message", "--uid", "1", "--content", "hello"])
        assert ns.uid == 1

    def test_reply_message(self):
        ns = self._parse(["reply-message", "--uid", "1", "--mid", "2",
                          "--content", "r"])
        assert ns.mid == 2

    def test_delete_message(self):
        ns = self._parse(["delete-message", "--id", "7"])
        assert ns.message_id == 7

    def test_list_moods(self):
        ns = self._parse(["list-moods"])
        assert ns.command == "list-moods"

    def test_create_mood(self):
        ns = self._parse(["create-mood", "--content", "心情不错"])
        assert ns.content == "心情不错"

    def test_delete_mood(self):
        ns = self._parse(["delete-mood", "--id", "4"])
        assert ns.mood_id == 4

    def test_upload_file(self):
        ns = self._parse(["upload-file", "--file", "/path/to/file.png"])
        assert ns.file_path == "/path/to/file.png"

    def test_upload_files(self):
        ns = self._parse(["upload-files", "--files", "a.txt", "b.txt"])
        assert ns.file_paths == ["a.txt", "b.txt"]

    def test_list_uploads(self):
        ns = self._parse(["list-uploads"])
        assert ns.command == "list-uploads"

    def test_delete_upload(self):
        ns = self._parse(["delete-upload", "--filename", "abc.png"])
        assert ns.filename == "abc.png"

    def test_health_check(self):
        ns = self._parse(["health-check"])
        assert ns.command == "health-check"


class TestFormatterOutput:
    def test_output_contains_json_and_markdown(self):
        out = format_output({"code": 200, "data": []},
                            kind="articles_list", title="Test")
        assert "### JSON" in out
        assert "```json" in out
        assert "### Markdown" in out

    def test_json_is_valid(self):
        out = format_output({"code": 200, "data": {"id": 1}}, kind="id_response")
        json_block = re.search(r"```json\n(.+?)\n```", out, re.DOTALL).group(1)
        parsed = json.loads(json_block)
        assert parsed["data"]["id"] == 1

    def test_capability_list_render_has_27_rows(self):
        data, kind = capability.list_commands()
        out = format_output(data, kind=kind, title="capability-list")
        assert "27" in out
        assert "| `" in out

    def test_capability_list_render_no_version(self):
        """v1.0.0: rendered output must not contain a version tag."""
        data, kind = capability.list_commands()
        out = format_output(data, kind=kind, title="capability-list")
        assert "v1.0.0" not in out
        assert "v2.0.0" not in out

    def test_health_render(self):
        out = format_output(
            {"status": "ok", "service": "blog-api", "version": "1.0.0"},
            kind="health",
        )
        assert "✅" in out
        assert "blog-api" in out


class TestNoHardcodedURL:
    """The API address must never appear in source code or docs."""

    def _source_files(self):
        base = os.path.join(os.path.dirname(__file__), "..", "blog_manager")
        for fname in os.listdir(base):
            if fname.endswith(".py"):
                yield os.path.join(base, fname)
        yield os.path.join(os.path.dirname(__file__), "..", "main.py")

    def test_no_hardcoded_ip_in_source(self):
        for fpath in self._source_files():
            with open(fpath) as fh:
                content = fh.read()
            assert "123.249.19.227" not in content, f"IP found in {fpath}"
            assert "18080" not in content, f"Port found in {fpath}"

    def test_no_hardcoded_ip_in_docs(self):
        base = os.path.join(os.path.dirname(__file__), "..")
        for fname in ("SKILL.md", "README.md"):
            fpath = os.path.join(base, fname)
            with open(fpath) as fh:
                content = fh.read()
            assert "123.249.19.227" not in content, f"IP found in {fpath}"


class TestCLISubprocess:
    def test_capability_list_via_subprocess(self):
        base_dir = os.path.join(os.path.dirname(__file__), "..")
        env = dict(os.environ, BLOG_MANAGER_BASE_URL="http://test:1234")
        result = subprocess.run(
            [sys.executable, "main.py", "capability-list"],
            capture_output=True, text=True, cwd=base_dir,
            env=env, timeout=15,
        )
        assert result.returncode == 0
        assert "27" in result.stdout

    def test_missing_env_var_exits_2(self):
        base_dir = os.path.join(os.path.dirname(__file__), "..")
        env = dict(os.environ)
        env.pop("BLOG_MANAGER_BASE_URL", None)
        result = subprocess.run(
            [sys.executable, "main.py", "health-check"],
            capture_output=True, text=True, cwd=base_dir,
            env=env, timeout=15,
        )
        assert result.returncode == 2
        assert "BLOG_MANAGER_BASE_URL" in result.stderr


class TestNoV2Residue:
    """v1.0.0 must not contain any v2.0.0 code residue."""

    def test_no_version_field_in_capability(self):
        data, _ = capability.list_commands()
        assert "version" not in data

    def test_no_test_vars_base_url_fallback_in_client(self):
        """client.py must not read from test-vars.json."""
        client_path = os.path.join(
            os.path.dirname(__file__), "..", "blog_manager", "client.py"
        )
        with open(client_path) as fh:
            content = fh.read()
        assert "test-vars" not in content
        assert "_read_test_vars" not in content
        assert "_TEST_VARS_PATH" not in content

    def test_no_base_url_in_test_vars_json(self):
        tv_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "test-vars.json"
        )
        with open(tv_path) as fh:
            data = json.load(fh)
        assert "base_url" not in data

    def test_init_version_is_1_0_0(self):
        from blog_manager import __version__

        assert __version__ == "1.0.0"

    def test_skill_md_version_is_1_0_0(self):
        skill_path = os.path.join(os.path.dirname(__file__), "..", "SKILL.md")
        with open(skill_path) as fh:
            content = fh.read()
        assert "version: 1.0.0" in content
        assert "2.0.0" not in content


LIVE_URL = os.environ.get("BLOG_MANAGER_BASE_URL", "")
IS_LIVE = LIVE_URL.startswith("http://") and "test" not in LIVE_URL


@pytest.mark.skipif(
    not IS_LIVE, reason="BLOG_MANAGER_BASE_URL does not point to a live server"
)
class TestIntegration:
    """Smoke tests against the real Blog System API."""

    def test_health(self):
        from blog_manager.client import BlogClient
        from blog_manager.health import health_check

        client = BlogClient()
        data, _ = health_check(client)
        assert data["status"] == "ok"

    def test_articles_list(self):
        from blog_manager.client import BlogClient
        from blog_manager.articles import list_articles

        client = BlogClient()
        data, _ = list_articles(client, page=1, size=1)
        assert data["code"] == 200
        assert "data" in data

    def test_labels_list(self):
        from blog_manager.client import BlogClient
        from blog_manager.labels import list_labels

        client = BlogClient()
        data, _ = list_labels(client)
        assert data["code"] == 200

    def test_full_capability_list(self):
        data, _ = capability.list_commands()
        assert data["total"] == 27
