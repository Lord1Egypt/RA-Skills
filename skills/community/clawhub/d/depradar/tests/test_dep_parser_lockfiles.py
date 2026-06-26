"""Tests for lock file parsing in lib/dep_parser.py."""

import json
import sys
import textwrap
from pathlib import Path

import pytest

from lib.dep_parser import (
    parse_package_lock_json,
    parse_yarn_lock,
    parse_pnpm_lock,
)


class TestParsePackageLockJson:
    def test_v2_format(self, tmp_path):
        lock = {
            "lockfileVersion": 2,
            "packages": {
                "": {},
                "node_modules/stripe": {"version": "8.1.2"},
                "node_modules/openai": {"version": "1.35.0"},
                "node_modules/chalk": {"version": "5.3.1"},
            },
        }
        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        result = parse_package_lock_json(str(lock_path))
        assert result.get("stripe") == "8.1.2"
        assert result.get("openai") == "1.35.0"
        assert result.get("chalk") == "5.3.1"

    def test_v3_format(self, tmp_path):
        lock = {
            "lockfileVersion": 3,
            "packages": {
                "node_modules/express": {"version": "4.19.2"},
            },
        }
        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        result = parse_package_lock_json(str(lock_path))
        assert result.get("express") == "4.19.2"

    def test_skips_empty_key(self, tmp_path):
        lock = {
            "lockfileVersion": 2,
            "packages": {
                "": {"version": "1.0.0"},
                "node_modules/stripe": {"version": "8.0.0"},
            },
        }
        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        result = parse_package_lock_json(str(lock_path))
        assert "" not in result
        assert "stripe" in result

    def test_scoped_package(self, tmp_path):
        lock = {
            "lockfileVersion": 2,
            "packages": {
                "node_modules/@company/mylib": {"version": "2.0.0"},
            },
        }
        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        result = parse_package_lock_json(str(lock_path))
        assert result.get("@company/mylib") == "2.0.0"

    def test_missing_version_field_skipped(self, tmp_path):
        """Packages without a version field are skipped (no version to report)."""
        lock = {
            "lockfileVersion": 2,
            "packages": {
                "node_modules/stripe": {},          # no version field
                "node_modules/chalk": {"version": "5.0.0"},
            },
        }
        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        result = parse_package_lock_json(str(lock_path))
        # stripe has no version → skipped
        assert "stripe" not in result
        # chalk has a version → present
        assert result.get("chalk") == "5.0.0"

    def test_empty_packages(self, tmp_path):
        lock = {"lockfileVersion": 2, "packages": {}}
        lock_path = tmp_path / "package-lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        result = parse_package_lock_json(str(lock_path))
        assert result == {}


class TestParseYarnLock:
    def test_basic_v1(self, tmp_path):
        content = textwrap.dedent("""\
            # yarn lockfile v1

            stripe@^7.0.0:
              version "7.5.0"
              resolved "https://registry.yarnpkg.com/stripe/-/stripe-7.5.0.tgz"

            openai@^0.28.0, openai@^0.27.0:
              version "0.28.1"
              resolved "https://registry.yarnpkg.com/openai/-/openai-0.28.1.tgz"
        """)
        lock_path = tmp_path / "yarn.lock"
        lock_path.write_text(content, encoding="utf-8")
        result = parse_yarn_lock(str(lock_path))
        assert result.get("stripe") == "7.5.0"
        assert result.get("openai") == "0.28.1"

    def test_multiple_version_specs_same_package(self, tmp_path):
        content = textwrap.dedent("""\
            lodash@^4.0.0, lodash@^4.17.0:
              version "4.17.21"
              resolved "https://example.com"
        """)
        lock_path = tmp_path / "yarn.lock"
        lock_path.write_text(content, encoding="utf-8")
        result = parse_yarn_lock(str(lock_path))
        assert result.get("lodash") == "4.17.21"

    def test_empty_file(self, tmp_path):
        lock_path = tmp_path / "yarn.lock"
        lock_path.write_text("# yarn lockfile v1\n", encoding="utf-8")
        result = parse_yarn_lock(str(lock_path))
        assert result == {}


class TestParsePnpmLock:
    def test_v6_format(self, tmp_path):
        content = textwrap.dedent("""\
            lockfileVersion: '6.0'

            packages:

              /stripe@8.0.0:
                resolution: {integrity: sha512-abc}
                dev: false

              /chalk@5.3.0:
                resolution: {integrity: sha512-def}
        """)
        lock_path = tmp_path / "pnpm-lock.yaml"
        lock_path.write_text(content, encoding="utf-8")
        result = parse_pnpm_lock(str(lock_path))
        assert result.get("stripe") == "8.0.0"
        assert result.get("chalk") == "5.3.0"

    def test_v5_format(self, tmp_path):
        content = textwrap.dedent("""\
            lockfileVersion: 5

            packages:

              /express/4.18.2:
                resolution: {integrity: sha512-ghi}
        """)
        lock_path = tmp_path / "pnpm-lock.yaml"
        lock_path.write_text(content, encoding="utf-8")
        result = parse_pnpm_lock(str(lock_path))
        assert result.get("express") == "4.18.2"

    def test_empty_packages(self, tmp_path):
        content = "lockfileVersion: '6.0'\n\npackages:\n"
        lock_path = tmp_path / "pnpm-lock.yaml"
        lock_path.write_text(content, encoding="utf-8")
        result = parse_pnpm_lock(str(lock_path))
        assert result == {}
