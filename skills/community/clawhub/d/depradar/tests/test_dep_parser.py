"""Tests for scripts/lib/dep_parser.py"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from dep_parser import (
    detect_ecosystem,
    parse_cargo_toml,
    parse_go_mod,
    parse_package_json,
    parse_pyproject_toml,
    parse_requirements_txt,
)

_FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "package_json_samples"


class TestDetectEcosystem(unittest.TestCase):

    def test_package_json(self):
        self.assertEqual(detect_ecosystem("package.json"), "npm")
        self.assertEqual(detect_ecosystem("/path/to/package.json"), "npm")

    def test_requirements_txt(self):
        self.assertEqual(detect_ecosystem("requirements.txt"), "pypi")

    def test_pyproject_toml(self):
        self.assertEqual(detect_ecosystem("pyproject.toml"), "pypi")

    def test_pipfile(self):
        self.assertEqual(detect_ecosystem("Pipfile"), "pypi")

    def test_go_mod(self):
        self.assertEqual(detect_ecosystem("go.mod"), "go")

    def test_cargo_toml(self):
        self.assertEqual(detect_ecosystem("Cargo.toml"), "cargo")

    def test_gemfile(self):
        self.assertEqual(detect_ecosystem("Gemfile"), "gem")

    def test_pom_xml(self):
        self.assertEqual(detect_ecosystem("pom.xml"), "maven")

    def test_unknown_file(self):
        self.assertEqual(detect_ecosystem("composer.json"), "unknown")
        self.assertEqual(detect_ecosystem("Makefile"), "unknown")


class TestParsePackageJson(unittest.TestCase):

    def setUp(self):
        self.fixture_path = str(_FIXTURES_DIR / "node_sample.json")

    def test_parses_stripe_dependency(self):
        deps = parse_package_json(self.fixture_path)
        self.assertIn("stripe", deps)
        dep = deps["stripe"]
        self.assertEqual(dep.name, "stripe")
        self.assertEqual(dep.ecosystem, "npm")
        self.assertIn("7.0.0", dep.version_spec)
        self.assertEqual(dep.version, "7.0.0")
        self.assertFalse(dep.is_dev)

    def test_parses_openai_dependency(self):
        deps = parse_package_json(self.fixture_path)
        self.assertIn("openai", deps)
        dep = deps["openai"]
        self.assertIn("0.28.0", dep.version_spec)

    def test_parses_axios(self):
        deps = parse_package_json(self.fixture_path)
        self.assertIn("axios", deps)

    def test_parses_express(self):
        deps = parse_package_json(self.fixture_path)
        self.assertIn("express", deps)

    def test_parses_lodash(self):
        deps = parse_package_json(self.fixture_path)
        self.assertIn("lodash", deps)

    def test_parses_dotenv(self):
        deps = parse_package_json(self.fixture_path)
        self.assertIn("dotenv", deps)

    def test_excludes_dev_deps_by_default(self):
        deps = parse_package_json(self.fixture_path, include_dev=False)
        # typescript is in devDependencies, should be excluded
        self.assertNotIn("typescript", deps)

    def test_includes_dev_deps_when_requested(self):
        deps = parse_package_json(self.fixture_path, include_dev=True)
        self.assertIn("typescript", deps)
        self.assertTrue(deps["typescript"].is_dev)

    def test_source_file_is_package_json(self):
        deps = parse_package_json(self.fixture_path)
        for dep in deps.values():
            self.assertEqual(dep.source_file, "node_sample.json")

    def test_inline_package_json(self):
        import json
        import tempfile
        data = {
            "name": "test-pkg",
            "dependencies": {
                "express": "^4.18.0",
                "lodash": "4.17.21",
            },
            "devDependencies": {
                "jest": "^29.0.0",
            },
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            tmp_path = f.name
        try:
            deps = parse_package_json(tmp_path)
            self.assertIn("express", deps)
            self.assertIn("lodash", deps)
            self.assertNotIn("jest", deps)
        finally:
            os.unlink(tmp_path)


class TestParseRequirementsTxt(unittest.TestCase):

    def setUp(self):
        self.fixture_path = str(_FIXTURES_DIR / "python_requirements.txt")

    def test_parses_openai_pinned(self):
        deps = parse_requirements_txt(self.fixture_path)
        self.assertIn("openai", deps)
        dep = deps["openai"]
        self.assertEqual(dep.version, "0.28.0")
        self.assertEqual(dep.ecosystem, "pypi")

    def test_parses_stripe_pinned(self):
        deps = parse_requirements_txt(self.fixture_path)
        self.assertIn("stripe", deps)
        self.assertEqual(deps["stripe"].version, "7.0.0")

    def test_parses_requests_range(self):
        deps = parse_requirements_txt(self.fixture_path)
        self.assertIn("requests", deps)

    def test_parses_fastapi(self):
        deps = parse_requirements_txt(self.fixture_path)
        self.assertIn("fastapi", deps)

    def test_parses_sqlalchemy_with_upper_bound(self):
        deps = parse_requirements_txt(self.fixture_path)
        self.assertIn("sqlalchemy", deps)

    def test_parses_uvicorn_with_extras(self):
        deps = parse_requirements_txt(self.fixture_path)
        self.assertIn("uvicorn", deps)

    def test_source_file_is_requirements(self):
        deps = parse_requirements_txt(self.fixture_path)
        for dep in deps.values():
            self.assertEqual(dep.source_file, "python_requirements.txt")

    def test_inline_requirements(self):
        content = (
            "# Comment\n"
            "requests==2.28.1\n"
            "flask>=2.0.0\n"
            "-r other.txt\n"
            "pytest>=7.0.0  # dev dep\n"
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, prefix="requirements"
        ) as f:
            f.write(content)
            tmp_path = f.name
        try:
            deps = parse_requirements_txt(tmp_path)
            self.assertIn("requests", deps)
            self.assertEqual(deps["requests"].version, "2.28.1")
            self.assertIn("flask", deps)
            self.assertIn("pytest", deps)
        finally:
            os.unlink(tmp_path)

    def test_skips_comments_and_options(self):
        content = "# this is a comment\n-r requirements-dev.txt\nflask==2.0.0\n"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, prefix="requirements"
        ) as f:
            f.write(content)
            tmp_path = f.name
        try:
            deps = parse_requirements_txt(tmp_path)
            self.assertNotIn("#", str(deps.keys()))
            self.assertIn("flask", deps)
        finally:
            os.unlink(tmp_path)


class TestParsePyprojectToml(unittest.TestCase):

    def setUp(self):
        self.fixture_path = str(_FIXTURES_DIR / "pyproject_toml_sample.toml")

    def test_parses_openai(self):
        deps = parse_pyproject_toml(self.fixture_path)
        self.assertIn("openai", deps)

    def test_parses_stripe(self):
        deps = parse_pyproject_toml(self.fixture_path)
        self.assertIn("stripe", deps)

    def test_parses_fastapi(self):
        deps = parse_pyproject_toml(self.fixture_path)
        self.assertIn("fastapi", deps)

    def test_parses_sqlalchemy(self):
        deps = parse_pyproject_toml(self.fixture_path)
        self.assertIn("sqlalchemy", deps)

    def test_ecosystem_is_pypi(self):
        deps = parse_pyproject_toml(self.fixture_path)
        for dep in deps.values():
            self.assertEqual(dep.ecosystem, "pypi")

    def test_inline_pyproject(self):
        content = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-app"
version = "1.0.0"
dependencies = [
    "requests>=2.28.0",
    "flask>=2.3.0",
    "pydantic>=2.0.0",
]
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, prefix="pyproject"
        ) as f:
            f.write(content)
            tmp_path = f.name
        try:
            deps = parse_pyproject_toml(tmp_path)
            self.assertIn("requests", deps)
            self.assertIn("flask", deps)
            self.assertIn("pydantic", deps)
        finally:
            os.unlink(tmp_path)


class TestParseGoMod(unittest.TestCase):

    _GO_MOD_CONTENT = """\
module github.com/example/myapp

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/stretchr/testify v1.8.4 // indirect
    golang.org/x/crypto v0.17.0
)

require github.com/joho/godotenv v1.5.1
"""

    def test_parses_block_requires(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".mod", delete=False, prefix="go"
        ) as f:
            f.write(self._GO_MOD_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_go_mod(tmp_path)
            self.assertIn("github.com/gin-gonic/gin", deps)
            gin = deps["github.com/gin-gonic/gin"]
            self.assertEqual(gin.version, "1.9.1")
            self.assertEqual(gin.ecosystem, "go")
        finally:
            os.unlink(tmp_path)

    def test_parses_single_line_require(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".mod", delete=False, prefix="go"
        ) as f:
            f.write(self._GO_MOD_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_go_mod(tmp_path)
            self.assertIn("github.com/joho/godotenv", deps)
            self.assertEqual(deps["github.com/joho/godotenv"].version, "1.5.1")
        finally:
            os.unlink(tmp_path)

    def test_parses_indirect_dep(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".mod", delete=False, prefix="go"
        ) as f:
            f.write(self._GO_MOD_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_go_mod(tmp_path)
            # testify is marked // indirect but should still be included
            self.assertIn("github.com/stretchr/testify", deps)
        finally:
            os.unlink(tmp_path)

    def test_all_deps_are_go_ecosystem(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".mod", delete=False, prefix="go"
        ) as f:
            f.write(self._GO_MOD_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_go_mod(tmp_path)
            for dep in deps.values():
                self.assertEqual(dep.ecosystem, "go")
        finally:
            os.unlink(tmp_path)


class TestParseCargoToml(unittest.TestCase):

    _CARGO_CONTENT = """\
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.35", features = ["full"] }
reqwest = "0.11"
anyhow = "1.0"

[dev-dependencies]
criterion = "0.5"
mockall = "0.12"
"""

    def test_parses_serde(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, prefix="Cargo"
        ) as f:
            f.write(self._CARGO_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_cargo_toml(tmp_path)
            self.assertIn("serde", deps)
            serde = deps["serde"]
            self.assertEqual(serde.version, "1.0.0")
            self.assertEqual(serde.ecosystem, "cargo")
            self.assertFalse(serde.is_dev)
        finally:
            os.unlink(tmp_path)

    def test_parses_tokio(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, prefix="Cargo"
        ) as f:
            f.write(self._CARGO_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_cargo_toml(tmp_path)
            self.assertIn("tokio", deps)
        finally:
            os.unlink(tmp_path)

    def test_parses_plain_version_string(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, prefix="Cargo"
        ) as f:
            f.write(self._CARGO_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_cargo_toml(tmp_path)
            self.assertIn("reqwest", deps)
            self.assertEqual(deps["reqwest"].version, "0.11.0")
        finally:
            os.unlink(tmp_path)

    def test_dev_deps_marked_is_dev(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, prefix="Cargo"
        ) as f:
            f.write(self._CARGO_CONTENT)
            tmp_path = f.name
        try:
            deps = parse_cargo_toml(tmp_path)
            self.assertIn("criterion", deps)
            self.assertTrue(deps["criterion"].is_dev)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
