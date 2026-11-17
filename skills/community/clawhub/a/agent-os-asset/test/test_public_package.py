"""Release-contract tests for the public Agent OS Asset suite."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]
CHILD_SKILLS = ("agent-readable-doc", "kb-review", "second-brain")
FORBIDDEN_NAMES = {
    ".DS_Store",
    "PROGRESS.md",
    "decision.log",
}


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"missing frontmatter: {path}"
    return match.group(1)


def test_nested_suite_layout() -> None:
    assert (REPO_ROOT / "SKILL.md").is_file()
    for name in CHILD_SKILLS:
        assert (REPO_ROOT / "skills" / name / "SKILL.md").is_file()


def test_release_metadata_uses_one_suite_version() -> None:
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["version"] == "0.2.0"
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert pyproject["project"]["version"] == "0.2.0"

    skill_files = [REPO_ROOT / "SKILL.md"] + [
        REPO_ROOT / "skills" / name / "SKILL.md" for name in CHILD_SKILLS
    ]
    for skill_file in skill_files:
        frontmatter = _frontmatter(skill_file)
        assert 'version: "0.2.0"' in frontmatter
        assert "user-invocable:" not in frontmatter


def test_main_skill_declares_bundled_children() -> None:
    skill_text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    for name in CHILD_SKILLS:
        assert f"skills/{name}/SKILL.md" in skill_text


def test_first_party_release_license_is_consistent_and_keeps_third_party_terms() -> None:
    expected = "Apache-2.0 OR MIT-0"
    package = json.loads((REPO_ROOT / "package.json").read_text())
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    assert package["license"] == expected
    assert pyproject["project"]["license"] == expected
    for skill_file in [REPO_ROOT / "SKILL.md"] + [
        REPO_ROOT / "skills" / name / "SKILL.md" for name in CHILD_SKILLS
    ]:
        assert f"license: {expected}" in _frontmatter(skill_file)
    license_text = (REPO_ROOT / "LICENSE").read_text()
    assert expected in license_text
    assert "MIT No Attribution" in license_text
    assert "Apache License" in license_text
    assert "THIRD_PARTY_NOTICES.md" in license_text
    assert (REPO_ROOT / "THIRD_PARTY_NOTICES.md").is_file()


def test_suite_is_described_as_agent_runtime_neutral() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for runtime in ("Codex", "Claude Code", "OpenClaw", "Hermes", "WorkBuddy"):
        assert runtime in readme
    assert "-a codex" not in readme


def test_public_recommendation_is_compelling_and_truthful() -> None:
    skill_text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    interface = (REPO_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert "Turn forgotten files into AI-ready assets" in interface
    assert "将吃灰文件变成 AI 资产" in interface
    assert "personal second brain" in skill_text
    assert "个人第二大脑" in skill_text
    assert "digital knowledge twin" in readme
    assert "数字知识分身" in readme
    for overclaim in ("one-click", "一键", "fully automatic", "全自动"):
        assert overclaim not in skill_text
        assert overclaim not in readme


def test_release_contains_required_repository_files() -> None:
    for name in ("README.md", "AGENTS.md", "LICENSE", ".gitignore"):
        assert (REPO_ROOT / name).is_file(), name


def test_release_tree_excludes_private_and_generated_artifacts() -> None:
    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        assert path.name not in FORBIDDEN_NAMES, str(path)
        assert not path.name.startswith("SKILL.md.bak."), str(path)

    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "__pycache__/" in gitignore
    assert ".pytest_cache/" in gitignore


def test_release_text_has_no_absolute_user_home_paths() -> None:
    findings: list[str] = []
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for value in result.stdout.splitlines():
        path = REPO_ROOT / value
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "test" not in path.parts and re.search(r"/" + r"Users/[A-Za-z0-9._-]+", text):
            findings.append(str(path.relative_to(REPO_ROOT)))
    assert not findings, findings


def test_main_runtime_resolves_nested_companion_skills() -> None:
    pipeline = (REPO_ROOT / "scripts" / "asset_pipeline.py").read_text(
        encoding="utf-8"
    )
    adapter = (REPO_ROOT / "scripts" / "mixed_folder_adapter.py").read_text(
        encoding="utf-8"
    )
    assert 'SKILL_ROOT / "skills" / "second-brain"' in pipeline
    assert 'SKILL_ROOT / "skills" / "agent-readable-doc"' in adapter


def test_local_server_has_no_wildcard_cors_and_defaults_to_read_only() -> None:
    server = (REPO_ROOT / "scripts" / "review_workbench_server.py").read_text(
        encoding="utf-8"
    )
    assert 'Access-Control-Allow-Origin", "*"' not in server
    assert 'parser.add_argument("--enable-write"' in server
    assert 'parser.add_argument("--enable-apply"' in server
