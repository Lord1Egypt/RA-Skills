"""Tests for package.json ClawHub metadata.

NOTE: As of commit b46888 the install convention moved from package.json
install hooks into SKILL.md's `metadata.openclaw.install` block (the canonical
location per the OpenClaw skill spec). package.json now only carries the
high-level package identity (name, version, description, keywords, repo,
slug, homepage) plus a pointer to SKILL.md via `openclaw.skillFile`.
"""

import json
import os

# Fields that must be present in package.json itself.
# Install hooks live in SKILL.md → metadata.openclaw.install (see SKILL.md tests).
REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "keywords",
    "repository",
    "slug",
    "openclaw",
]


def load_package_json():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(repo_root, "package.json")
    with open(path) as f:
        return json.load(f)


def test_package_json_exists():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(repo_root, "package.json")
    assert os.path.isfile(path), "package.json must exist at repo root"


def test_required_fields_present():
    pkg = load_package_json()
    for field in REQUIRED_FIELDS:
        assert field in pkg, f"package.json missing required field: {field}"


def test_required_fields_non_empty():
    pkg = load_package_json()
    for field in REQUIRED_FIELDS:
        value = pkg.get(field)
        assert value is not None, f"Field '{field}' must not be None"
        if isinstance(value, str):
            assert value.strip() != "", f"Field '{field}' must not be empty string"
        elif isinstance(value, list):
            assert len(value) > 0, f"Field '{field}' must not be empty list"
        elif isinstance(value, dict):
            assert len(value) > 0, f"Field '{field}' must not be empty dict"


def test_name():
    pkg = load_package_json()
    assert pkg["name"] == "friday-budgeting-pro"


def test_version_format():
    pkg = load_package_json()
    parts = pkg["version"].split(".")
    assert len(parts) == 3, "version must follow semver (x.y.z)"
    for part in parts:
        assert part.isdigit(), f"version component '{part}' must be numeric"


def test_keywords_are_list_of_strings():
    pkg = load_package_json()
    kws = pkg["keywords"]
    assert isinstance(kws, list)
    for kw in kws:
        assert isinstance(kw, str) and kw.strip(), f"keyword must be non-empty string: {kw!r}"


def test_repository_has_url():
    pkg = load_package_json()
    repo = pkg["repository"]
    assert isinstance(repo, dict), "repository must be an object"
    assert "url" in repo and repo["url"].strip(), "repository.url must be a non-empty string"


def test_slug():
    pkg = load_package_json()
    assert isinstance(pkg["slug"], str) and pkg["slug"].strip(), "slug must be a non-empty string"


def test_openclaw_pointer_to_skill_file():
    """package.json points at SKILL.md, which holds the canonical install convention."""
    pkg = load_package_json()
    openclaw = pkg["openclaw"]
    assert isinstance(openclaw, dict), "openclaw must be an object"
    assert "skillFile" in openclaw, "openclaw.skillFile must point at the skill markdown"
    assert openclaw["skillFile"].strip(), "openclaw.skillFile must not be empty"
