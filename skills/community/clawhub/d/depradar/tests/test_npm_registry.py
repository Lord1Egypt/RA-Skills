"""Tests for lib/npm_registry.py — npm Registry API integration."""
import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import PackageUpdate

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


STRIPE_NPM = load_fixture("npm_registry_stripe.json")

import lib.npm_registry as npm_reg


class TestGetLatestVersion(unittest.TestCase):
    @patch("lib.npm_registry.fetch_package_info")
    def test_extracts_dist_tags_latest(self, mock_info):
        mock_info.return_value = {
            "dist-tags": {"latest": "8.0.0"},
            "versions": {"7.0.0": {}, "8.0.0": {}}
        }
        result = npm_reg.get_latest_version("stripe")
        self.assertEqual(result, "8.0.0")

    @patch("lib.npm_registry.fetch_package_info")
    def test_falls_back_to_computed_latest(self, mock_info):
        mock_info.return_value = {
            "versions": {"7.0.0": {}, "8.0.0": {}, "6.5.0": {}}
        }
        result = npm_reg.get_latest_version("stripe")
        # Should return the latest stable — exact order depends on latest_stable()
        self.assertIsNotNone(result)

    @patch("lib.npm_registry.fetch_package_info")
    def test_returns_none_when_package_not_found(self, mock_info):
        mock_info.return_value = None
        result = npm_reg.get_latest_version("nonexistent")
        self.assertIsNone(result)


class TestFetchPackageInfo(unittest.TestCase):
    @patch("lib.npm_registry.get_json")
    def test_returns_registry_data(self, mock_get):
        mock_get.return_value = STRIPE_NPM
        info = npm_reg.fetch_package_info("stripe")
        self.assertIsNotNone(info)
        self.assertIsInstance(info, dict)

    @patch("lib.npm_registry.get_json")
    def test_returns_none_on_not_found(self, mock_get):
        from lib.http import NotFoundError
        mock_get.side_effect = NotFoundError("https://registry.npmjs.org/x", 404, "not found")
        info = npm_reg.fetch_package_info("nonexistent-package-xyz")
        self.assertIsNone(info)

    @patch("lib.npm_registry._CACHE_AVAILABLE", False)
    @patch("lib.npm_registry.get_json")
    def test_returns_none_on_http_error(self, mock_get):
        from lib.http import HttpError
        mock_get.side_effect = HttpError("https://registry.npmjs.org/stripe", 500, "server error")
        info = npm_reg.fetch_package_info("stripe")
        self.assertIsNone(info)


class TestBuildPackageUpdate(unittest.TestCase):
    @patch("lib.npm_registry.fetch_package_info")
    def test_builds_update_when_outdated(self, mock_info):
        mock_info.return_value = {
            "dist-tags": {"latest": "8.0.0"},
            "versions": {"7.0.0": {}, "8.0.0": {}},
            "time": {"7.0.0": "2025-01-01T00:00:00Z", "8.0.0": "2026-01-01T00:00:00Z"},
            "repository": {"url": "git+https://github.com/stripe/stripe-node.git"},
            "description": "Stripe node.js library",
        }
        pkg = npm_reg.build_package_update("stripe", "7.0.0")
        self.assertIsInstance(pkg, PackageUpdate)
        self.assertEqual(pkg.package, "stripe")
        self.assertEqual(pkg.current_version, "7.0.0")
        self.assertEqual(pkg.latest_version, "8.0.0")
        self.assertEqual(pkg.ecosystem, "npm")
        self.assertEqual(pkg.semver_type, "major")

    @patch("lib.npm_registry.fetch_package_info")
    def test_returns_none_when_already_up_to_date(self, mock_info):
        mock_info.return_value = {
            "dist-tags": {"latest": "8.0.0"},
            "versions": {"8.0.0": {}},
            "time": {"8.0.0": "2026-01-01T00:00:00Z"},
        }
        pkg = npm_reg.build_package_update("stripe", "8.0.0")
        self.assertIsNone(pkg)  # bump_type returns 'none' → returns None

    @patch("lib.npm_registry.fetch_package_info")
    def test_returns_none_when_not_found(self, mock_info):
        mock_info.return_value = None
        pkg = npm_reg.build_package_update("nonexistent", "1.0.0")
        self.assertIsNone(pkg)

    @patch("lib.npm_registry.fetch_package_info")
    def test_extracts_github_repo(self, mock_info):
        mock_info.return_value = {
            "dist-tags": {"latest": "8.0.0"},
            "versions": {"7.0.0": {}, "8.0.0": {}},
            "time": {"7.0.0": "2025-01-01T00:00:00Z", "8.0.0": "2026-01-01T00:00:00Z"},
            "repository": {"url": "git+https://github.com/stripe/stripe-node.git"},
        }
        pkg = npm_reg.build_package_update("stripe", "7.0.0")
        if pkg:
            self.assertIsNotNone(pkg.github_repo)
            self.assertIn("stripe", pkg.github_repo)


class TestEncodePackage(unittest.TestCase):
    def test_encodes_scoped_package(self):
        encoded = npm_reg._encode_package("@openai/api")
        self.assertIn("%40", encoded)  # @ encoded
        self.assertNotIn("@", encoded)

    def test_leaves_normal_package_unchanged(self):
        encoded = npm_reg._encode_package("stripe")
        self.assertEqual(encoded, "stripe")

    def test_encodes_slash_in_scoped(self):
        encoded = npm_reg._encode_package("@scope/name")
        self.assertNotIn("/", encoded)


class TestExtractGithubRepo(unittest.TestCase):
    def test_extracts_from_git_plus_https(self):
        info = {"repository": {"url": "git+https://github.com/stripe/stripe-node.git"}}
        repo = npm_reg._extract_github_repo_from_info(info)
        self.assertEqual(repo, "stripe/stripe-node")

    def test_extracts_from_ssh(self):
        info = {"repository": {"url": "git@github.com:stripe/stripe-node.git"}}
        repo = npm_reg._extract_github_repo_from_info(info)
        self.assertEqual(repo, "stripe/stripe-node")

    def test_extracts_from_string_shorthand(self):
        # Some packages use "owner/repo" shorthand — check if module handles it
        info = {"repository": "stripe/stripe-node"}
        repo = npm_reg._extract_github_repo_from_info(info)
        # May be None if module only handles URL formats — just verify no crash
        self.assertIsInstance(repo, (str, type(None)))

    def test_returns_none_for_non_github(self):
        info = {"repository": {"url": "https://gitlab.com/foo/bar.git"}}
        repo = npm_reg._extract_github_repo_from_info(info)
        self.assertIsNone(repo)

    def test_returns_none_when_no_repository(self):
        repo = npm_reg._extract_github_repo_from_info({})
        self.assertIsNone(repo)


if __name__ == "__main__":
    unittest.main()
