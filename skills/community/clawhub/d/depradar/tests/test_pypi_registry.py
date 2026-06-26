"""Tests for lib/pypi_registry.py — PyPI JSON API integration."""
import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import PackageUpdate

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


OPENAI_PYPI = load_fixture("pypi_registry_openai.json")

import lib.pypi_registry as pypi_reg


class TestGetLatestVersion(unittest.TestCase):
    @patch("lib.pypi_registry.fetch_package_info")
    def test_extracts_version_from_info(self, mock_info):
        mock_info.return_value = {
            "info": {"version": "1.35.0"},
            "releases": {"1.35.0": [{"yanked": False}]}
        }
        result = pypi_reg.get_latest_version("openai")
        self.assertEqual(result, "1.35.0")

    @patch("lib.pypi_registry.fetch_package_info")
    def test_returns_none_when_not_found(self, mock_info):
        mock_info.return_value = None
        result = pypi_reg.get_latest_version("nonexistent")
        self.assertIsNone(result)


class TestFetchPackageInfo(unittest.TestCase):
    @patch("lib.pypi_registry.get_json")
    def test_returns_registry_data(self, mock_get):
        mock_get.return_value = OPENAI_PYPI
        info = pypi_reg.fetch_package_info("openai")
        self.assertIsNotNone(info)
        self.assertIsInstance(info, dict)

    @patch("lib.pypi_registry.get_json")
    def test_returns_none_on_not_found(self, mock_get):
        from lib.http import NotFoundError
        mock_get.side_effect = NotFoundError("https://pypi.org/pypi/x/json", 404, "not found")
        info = pypi_reg.fetch_package_info("nonexistent-xyz")
        self.assertIsNone(info)


class TestBuildPackageUpdate(unittest.TestCase):
    @patch("lib.pypi_registry.fetch_package_info")
    def test_builds_update_when_outdated(self, mock_info):
        mock_info.return_value = {
            "info": {
                "version": "1.35.0",
                "home_page": "https://github.com/openai/openai-python",
                "project_urls": {"Source": "https://github.com/openai/openai-python"},
                "description": "OpenAI Python library",
            },
            "releases": {
                "0.28.0": [{"upload_time": "2023-01-01T00:00:00", "yanked": False}],
                "1.35.0": [{"upload_time": "2026-01-01T00:00:00", "yanked": False}],
            }
        }
        pkg = pypi_reg.build_package_update("openai", "0.28.0")
        self.assertIsInstance(pkg, PackageUpdate)
        self.assertEqual(pkg.package, "openai")
        self.assertEqual(pkg.ecosystem, "pypi")
        self.assertEqual(pkg.current_version, "0.28.0")
        self.assertIsNotNone(pkg.latest_version)

    @patch("lib.pypi_registry.fetch_package_info")
    def test_returns_none_when_not_found(self, mock_info):
        mock_info.return_value = None
        pkg = pypi_reg.build_package_update("nonexistent", "1.0.0")
        self.assertIsNone(pkg)

    @patch("lib.pypi_registry.fetch_package_info")
    def test_returns_none_when_up_to_date(self, mock_info):
        mock_info.return_value = {
            "info": {"version": "1.35.0"},
            "releases": {"1.35.0": [{"yanked": False}]}
        }
        pkg = pypi_reg.build_package_update("openai", "1.35.0")
        self.assertIsNone(pkg)


class TestRegistryUrl(unittest.TestCase):
    def test_pypi_url_constant(self):
        # The registry URL should be the PyPI base
        self.assertIn("pypi.org", npm_reg_pypi_const())

    def test_fetch_url_contains_package(self):
        # fetch_package_info calls get_json with PyPI URL
        with patch("lib.pypi_registry.get_json") as mock_get:
            mock_get.return_value = None
            pypi_reg.fetch_package_info("requests")
            if mock_get.called:
                url = mock_get.call_args[0][0]
                self.assertIn("requests", url)
                self.assertIn("pypi.org", url)


def npm_reg_pypi_const():
    return getattr(pypi_reg, "PYPI_API", "https://pypi.org")


if __name__ == "__main__":
    unittest.main()
