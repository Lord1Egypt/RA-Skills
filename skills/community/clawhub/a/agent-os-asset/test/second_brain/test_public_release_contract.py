from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "second-brain"
SCRIPTS = SKILL_ROOT / "scripts"
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ENGLISH = re.compile(r"[A-Za-z]{2,}")


def load_module(filename: str, name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_skill_frontmatter_uses_public_release_metadata() -> None:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]

    assert "user-invocable" not in frontmatter
    assert "metadata:" in frontmatter
    assert 'version: "0.2.0"' in frontmatter


def test_release_metadata_and_skill_policy_are_bilingual_v010() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    version = json.loads((SKILL_ROOT / "references" / "version.json").read_text(encoding="utf-8"))
    openai_metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert version["version"] == "0.2.0"
    assert "English is normative" in skill_text
    assert "ZH-CN" in skill_text
    assert "Second Brain / 第二大脑" in openai_metadata


def test_scoped_publication_has_no_unpaired_chinese_literals() -> None:
    failures: list[str] = []
    suffixes = {".md", ".py", ".yaml", ".yml", ".json"}
    for path in sorted(SKILL_ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        previous_nonblank = ""
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            previous = previous_nonblank.strip()
            paired = (
                ("bilingual-compat:" in line and ENGLISH.search(line))
                or ("bilingual-compat:" in previous and ENGLISH.search(previous))
                or (stripped.startswith("ZH-CN:") and previous.startswith("EN:") and ENGLISH.search(previous))
                or (
                    " / " in line
                    and (english := ENGLISH.search(line))
                    and (chinese := HAN.search(line))
                    and english.start() < line.find(" / ") < chinese.start()
                )
            )
            if HAN.search(line) and not paired:
                failures.append(f"{path.relative_to(SKILL_ROOT)}:{number}: {stripped}")
            if stripped:
                previous_nonblank = line
    assert not failures, "Unpaired Chinese publication text:\n" + "\n".join(failures)


def test_generated_reports_and_summary_prompts_are_bilingual(tmp_path: Path) -> None:
    build_index = load_module("build_index.py", "second_brain_build_bilingual_test")
    retrieval_quality = load_module("retrieval_quality.py", "second_brain_quality_bilingual_test")

    prompts = build_index.summary_prompt_variants("Sample", "Title: Sample\n\nContent:\nA durable decision.")
    assert prompts
    assert all("English is normative" in prompt for prompt in prompts)
    assert all("EN:" in prompt and "ZH-CN:" in prompt for prompt in prompts)

    summary = build_index.BuildSummary(
        total_documents=1,
        indexed_documents=1,
        reused_documents=0,
        removed_documents=0,
        excluded_pii_documents=0,
    )
    build_index.write_generated_references(tmp_path, tmp_path / "vault", [], [], summary, "agent-readable")
    generated = (tmp_path / "index-summary.md").read_text(encoding="utf-8")
    assert "# Second Brain Index Summary / 第二大脑索引摘要" in generated
    assert "Generated at / 生成时间" in generated

    report = retrieval_quality.render_markdown(
        {
            "summary": {
                "strict_top1": 1,
                "strict_total": 1,
                "strict_top1_rate": 1.0,
                "strict_top1_passed": True,
                "embedding_recommended": False,
                "semantic_rerank_statuses": [],
            },
            "results": [],
        }
    )
    assert "# SecondBrain Retrieval Quality Report / 第二大脑检索质量报告" in report
    assert "## Summary / 摘要" in report


def test_cli_help_exposes_english_normative_bilingual_copy() -> None:
    for script in (
        "asset_index_registry.py",
        "build_index.py",
        "query_index.py",
        "retrieval_quality.py",
        "routine_update.py",
        "validate_privacy.py",
    ):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / script), "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "English is normative" in result.stdout, script
        assert "ZH-CN" in result.stdout, script


def test_release_tree_excludes_generated_state_and_personal_paths() -> None:
    assert not (SKILL_ROOT / "references" / "generated").exists()
    assert not (SKILL_ROOT / "references" / "generated-report").exists()
    assert not any(SKILL_ROOT.rglob("__pycache__"))
    assert not any(SKILL_ROOT.rglob("*.pyc"))

    forbidden = (
        "/" + "Users" + "/" + "lee",
        "Library/Mobile Documents",
        ".openclaw/workspace",
        "Obsidian Vault",
    )
    for path in SKILL_ROOT.rglob("*"):
        if not path.is_file() or path.suffix == ".pyc":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        assert not any(marker in text for marker in forbidden), path


def test_runtime_defaults_are_portable_and_outside_skill_tree(tmp_path: Path) -> None:
    runtime_paths = load_module("runtime_paths.py", "second_brain_runtime_paths_test")
    env = {"XDG_STATE_HOME": str(tmp_path / "state")}

    paths = runtime_paths.resolve_paths(environ=env, home=tmp_path / "home")

    assert paths.vault == tmp_path / "home" / "Documents" / "SecondBrain"
    assert paths.state_dir == tmp_path / "state" / "second-brain"
    assert paths.index_dir == paths.state_dir / "index"
    assert paths.log_path == paths.state_dir / "logs" / "routine-update.log"
    assert paths.lock_path == paths.state_dir / "locks" / "routine-update.lock"
    assert SKILL_ROOT not in paths.index_dir.parents


def test_runtime_paths_honor_cli_environment_configuration(tmp_path: Path) -> None:
    runtime_paths = load_module("runtime_paths.py", "second_brain_runtime_paths_env_test")
    env = {
        "SECOND_BRAIN_VAULT": str(tmp_path / "vault"),
        "SECOND_BRAIN_STATE_DIR": str(tmp_path / "runtime"),
        "SECOND_BRAIN_REPORT_VAULT": str(tmp_path / "reports"),
        "SECOND_BRAIN_REPORT_INDEX": str(tmp_path / "report-index" / "documents.jsonl"),
        "SECOND_BRAIN_ASSET_REGISTRY": str(tmp_path / "registry.json"),
    }

    paths = runtime_paths.resolve_paths(environ=env, home=tmp_path / "home")

    assert paths.vault == tmp_path / "vault"
    assert paths.state_dir == tmp_path / "runtime"
    assert paths.report_vault == tmp_path / "reports"
    assert paths.report_index == tmp_path / "report-index" / "documents.jsonl"
    assert paths.asset_registry == tmp_path / "registry.json"


def test_summary_remote_configuration_is_explicit_and_https_only(monkeypatch) -> None:
    build_index = load_module("build_index.py", "second_brain_build_index_release_test")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "general-key-must-not-be-consumed")
    monkeypatch.delenv("SECOND_BRAIN_SUMMARY_ENABLED", raising=False)

    disabled = build_index.summary_remote_status()
    assert disabled["available"] is False
    assert disabled["reason"] == "explicit_opt_in_required"

    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_ENABLED", "1")
    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_API_KEY", "specific-key")
    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_MODEL", "summary-model")
    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_BASE_URL", "http://example.invalid/v1")
    insecure = build_index.summary_remote_status()
    assert insecure["available"] is False
    assert insecure["reason"] == "https_required"

    monkeypatch.setenv("SECOND_BRAIN_SUMMARY_BASE_URL", "https://example.invalid/v1")
    enabled = build_index.summary_remote_status()
    assert enabled["available"] is True
    assert enabled["model"] == "summary-model"
    assert "api_key" not in enabled


def test_script_defaults_use_external_runtime_state() -> None:
    runtime_paths = load_module("runtime_paths.py", "second_brain_runtime_defaults_test")
    build_index = load_module("build_index.py", "second_brain_build_defaults_test")
    registry = load_module("asset_index_registry.py", "second_brain_registry_defaults_test")
    routine = load_module("routine_update.py", "second_brain_routine_defaults_test")

    state_dir = runtime_paths.DEFAULT_PATHS.state_dir
    assert build_index.DEFAULT_OUT == runtime_paths.DEFAULT_PATHS.index_dir
    assert registry.DEFAULT_REGISTRY_PATH == runtime_paths.DEFAULT_PATHS.asset_registry
    assert routine.DEFAULT_OUT == runtime_paths.DEFAULT_PATHS.index_dir
    assert routine.DEFAULT_LOG == runtime_paths.DEFAULT_PATHS.log_path
    assert routine.DEFAULT_LOCK == runtime_paths.DEFAULT_PATHS.lock_path
    assert SKILL_ROOT not in state_dir.parents
