#!/usr/bin/env python3
"""
Tests for the ClawHub skill manifest (SKILL.md frontmatter).

The skill is published to ClawHub as @and3rn3t/apple-photos-cleaner, and the
registry reads its metadata straight out of the SKILL.md frontmatter. Before
these guards existed the version lived in three places that had all drifted
apart: the registry was on 1.0.1, pyproject.toml said 1.0.0, and SKILL.md
declared no version at all.

Schema reference: https://docs.openclaw.ai/clawhub/skill-format
"""

import json
import re
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "SKILL.md"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

# ClawHub documents these as the OS restriction vocabulary. Node's own
# `process.platform` spelling ("darwin") is used for *package* targets, not for
# skill manifests — the two vocabularies are not interchangeable.
KNOWN_OS_VALUES = {"macos", "linux", "windows"}


def parse_frontmatter(markdown: str) -> dict:
    """Extract the leading `---` delimited YAML block as a flat dict.

    Deliberately hand-rolled rather than using PyYAML: this skill ships
    stdlib-only, and the frontmatter is flat `key: value` pairs.
    """
    if not markdown.startswith("---\n"):
        raise ValueError("SKILL.md must open with a '---' frontmatter delimiter")

    _, _, rest = markdown.partition("---\n")
    block, delimiter, _ = rest.partition("\n---\n")
    if not delimiter:
        raise ValueError("SKILL.md frontmatter is not closed with '---'")

    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith((" ", "\t")):  # continuation of the previous value
            continue
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return fields


def read_pyproject_version() -> str:
    """Read `version` from the [project] table without needing tomllib (3.11+)."""
    text = PYPROJECT_PATH.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise AssertionError("pyproject.toml has no version field")
    return match.group(1)


@pytest.fixture(scope="module")
def frontmatter() -> dict:
    return parse_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def openclaw_metadata(frontmatter: dict) -> dict:
    raw = frontmatter.get("metadata")
    assert raw, "frontmatter must carry a metadata block"
    parsed = json.loads(raw)
    assert "openclaw" in parsed, "metadata must contain an 'openclaw' key"
    return parsed["openclaw"]


class TestSkillFrontmatter:
    """Schema conformance for the fields ClawHub actually reads."""

    def test_name_matches_directory_and_slug_rules(self, frontmatter: dict) -> None:
        name = frontmatter.get("name")
        assert name == REPO_ROOT.name, "skill name should match the parent directory"
        assert SLUG_PATTERN.match(name), f"{name!r} is not a valid ClawHub slug"

    def test_description_is_present_and_substantial(self, frontmatter: dict) -> None:
        # The registry surfaces this verbatim as the search/UI summary.
        description = frontmatter.get("description", "")
        assert len(description) > 100, "description is the published summary; keep it informative"

    def test_version_is_semver(self, frontmatter: dict) -> None:
        version = frontmatter.get("version")
        assert version, "SKILL.md must declare a version — ClawHub publishes per-version"
        assert SEMVER_PATTERN.match(version), f"{version!r} is not semver"

    def test_version_matches_pyproject(self, frontmatter: dict) -> None:
        assert frontmatter["version"] == read_pyproject_version(), (
            "SKILL.md and pyproject.toml versions have drifted; "
            "the publish workflow uses SKILL.md as the source of truth"
        )

    def test_no_license_override(self, frontmatter: dict) -> None:
        # ClawHub fixes every published skill at MIT-0 and does not support
        # per-skill overrides; a `license:` key here is a conflicting term.
        # The repository's own LICENSE file is unaffected by this.
        assert "license" not in frontmatter, "ClawHub forbids a license field in SKILL.md frontmatter"


class TestOpenClawMetadata:
    """The `metadata.openclaw` block that gates installation."""

    def test_metadata_is_valid_json(self, openclaw_metadata: dict) -> None:
        assert isinstance(openclaw_metadata, dict)

    def test_os_values_are_known(self, openclaw_metadata: dict) -> None:
        declared = set(openclaw_metadata.get("os", []))
        assert declared, "this skill is macOS-only; declare it so ClawHub can gate installs"
        unknown = declared - KNOWN_OS_VALUES
        assert not unknown, f"unrecognised os value(s): {sorted(unknown)}"

    def test_declares_the_binaries_it_shells_out_to(self, openclaw_metadata: dict) -> None:
        """Every binary the scripts exec must be declared, not just the interpreter.

        ClawHub's security review flags "undeclared capability" when a skill
        shells out to something its manifest never mentions. `osascript` is the
        one that matters here: it is how the two mutating commands reach
        Photos.app, so it is a capability, not an implementation detail.
        """
        bins = set(openclaw_metadata.get("requires", {}).get("bins", []))
        assert "python3" in bins, "every script is run via python3"

        executed: set[str] = set()
        for script in (REPO_ROOT / "scripts").glob("*.py"):
            source = script.read_text(encoding="utf-8")
            executed.update(re.findall(r'subprocess\.\w+\(\s*\[\s*["\']([\w.-]+)["\']', source))

        assert not (executed - bins), f"binaries executed but undeclared: {sorted(executed - bins)}"

    def test_env_var_usage_matches_the_manifest(self, openclaw_metadata: dict) -> None:
        """ClawHub's security review flags env vars used in code but undeclared."""
        requires = openclaw_metadata.get("requires", {})
        declared = set(requires.get("env", []))
        declared.update(entry["name"] for entry in openclaw_metadata.get("envVars", []))

        used: set[str] = set()
        for script in (REPO_ROOT / "scripts").glob("*.py"):
            source = script.read_text(encoding="utf-8")
            used.update(re.findall(r'os\.environ(?:\.get)?[\[(]\s*["\']([A-Za-z_][A-Za-z0-9_]*)', source))
            used.update(re.findall(r'os\.getenv\(\s*["\']([A-Za-z_][A-Za-z0-9_]*)', source))

        assert not (used - declared), f"env vars read by scripts but undeclared: {sorted(used - declared)}"


class TestChangelog:
    """Merging a version bump publishes it, so its CHANGELOG entry must be final.

    The PR that bumps SKILL.md *is* the release: clawhub-publish.yml ships it
    the moment it lands on main. An entry still reading "Unreleased" would
    publish with an unfinished changelog, so CI fails until it is dated.
    """

    def test_current_version_has_a_dated_entry(self, frontmatter: dict) -> None:
        version = frontmatter["version"]
        changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
        heading = re.search(rf"^## \[{re.escape(version)}\] - (.+)$", changelog, re.MULTILINE)
        assert heading, f"CHANGELOG.md has no '## [{version}] - YYYY-MM-DD' entry for the version in SKILL.md"

        stamp = heading.group(1).strip()
        try:
            date.fromisoformat(stamp)
        except ValueError:
            raise AssertionError(
                f"CHANGELOG.md entry for {version} is dated {stamp!r}; set it to the release (merge) date as "
                "YYYY-MM-DD before merging, since merging publishes to ClawHub (see RELEASING.md)"
            ) from None

    def test_current_version_has_a_compare_link(self, frontmatter: dict) -> None:
        version = frontmatter["version"]
        changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
        assert re.search(rf"^\[{re.escape(version)}\]: https://", changelog, re.MULTILINE), (
            f"CHANGELOG.md needs a '[{version}]: https://...' compare link at the bottom"
        )


class TestProgressiveDisclosure:
    """SKILL.md is loaded on every trigger, so it stays a router (ROADMAP T1.23); detail lives in references/."""

    MAX_LINES = 250
    SCRIPTS = sorted(p.stem for p in (REPO_ROOT / "scripts").glob("[a-z]*.py"))

    def test_skill_md_stays_small(self) -> None:
        lines = SKILL_PATH.read_text(encoding="utf-8").count("\n")
        assert lines <= self.MAX_LINES, f"SKILL.md is {lines} lines; move detail to references/commands/"

    @pytest.mark.parametrize("script", SCRIPTS)
    def test_every_command_has_a_linked_reference(self, script: str) -> None:
        reference = REPO_ROOT / "references" / "commands" / f"{script}.md"
        assert reference.is_file(), f"missing {reference.relative_to(REPO_ROOT)}"
        assert f"](references/commands/{script}.md)" in SKILL_PATH.read_text(encoding="utf-8")
        assert f"scripts/{script}.py" in reference.read_text(encoding="utf-8")

    def test_no_orphan_references(self) -> None:
        documented = {p.stem for p in (REPO_ROOT / "references" / "commands").glob("*.md")}
        assert documented == set(self.SCRIPTS)

    def test_relative_links_resolve(self) -> None:
        docs = [SKILL_PATH, *sorted((REPO_ROOT / "references").rglob("*.md"))]
        broken = [
            f"{doc.relative_to(REPO_ROOT)}: {target}"
            for doc in docs
            for target in re.findall(r"\]\(([^)#:]+\.md)(?:#[^)]*)?\)", doc.read_text(encoding="utf-8"))
            if not (doc.parent / target).resolve().is_file()
        ]
        assert not broken, broken
