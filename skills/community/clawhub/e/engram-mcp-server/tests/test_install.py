from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from engram_server.server import init_engram_pack, install_engram_from_source


REPO_ROOT = Path(__file__).resolve().parents[1]


def _init_git_repo(repo_dir: Path, with_meta: bool = True) -> None:
    repo_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.name", "test"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    if with_meta:
        (repo_dir / "meta.json").write_text(
            json.dumps(
                {
                    "name": repo_dir.name,
                    "description": "测试安装包",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    else:
        (repo_dir / "README.md").write_text("no meta", encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"], cwd=repo_dir, check=True, capture_output=True
    )


def test_install_engram_success(tmp_path: Path) -> None:
    source_repo = tmp_path / "source-pack"
    packs_dir = tmp_path / "packs"
    _init_git_repo(source_repo, with_meta=True)

    result = install_engram_from_source(str(source_repo), packs_dir)

    assert result["ok"] is True
    assert "安装成功" in result["message"]
    assert (packs_dir / "source-pack" / "meta.json").is_file()


def test_install_engram_rolls_back_when_meta_missing(tmp_path: Path) -> None:
    source_repo = tmp_path / "bad-pack"
    packs_dir = tmp_path / "packs"
    _init_git_repo(source_repo, with_meta=False)

    result = install_engram_from_source(str(source_repo), packs_dir)

    assert result["ok"] is False
    assert "缺少 meta.json" in result["message"]
    assert not (packs_dir / "bad-pack").exists()


def test_cli_list_command(tmp_path: Path) -> None:
    packs_dir = tmp_path / "packs"
    pack = packs_dir / "demo"
    pack.mkdir(parents=True)
    (pack / "meta.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "description": "演示包",
                "knowledge_count": 2,
                "examples_count": 1,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "engram_server.server",
            "list",
            "--packs-dir",
            str(packs_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "- demo: 演示包 (knowledge=2, examples=1)" in completed.stdout


def test_init_engram_pack_success(tmp_path: Path) -> None:
    packs_dir = tmp_path / "packs"

    result = init_engram_pack("my-expert", packs_dir)

    assert result["ok"] is True
    target = packs_dir / "my-expert"
    assert (target / "meta.json").is_file()
    assert (target / "role.md").is_file()
    assert (target / "knowledge/_index.md").is_file()
    assert (target / "examples/写好案例.md").is_file()
    assert (target / "examples/说明样本.md").is_file()
    meta = json.loads((target / "meta.json").read_text(encoding="utf-8"))
    assert meta["name"] == "my-expert"


def test_cli_init_command(tmp_path: Path) -> None:
    packs_dir = tmp_path / "packs"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "engram_server.server",
            "init",
            "cli-pack",
            "--packs-dir",
            str(packs_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "初始化成功" in completed.stdout
    assert (packs_dir / "cli-pack" / "meta.json").is_file()


def test_init_engram_pack_nested_creates_grouped_indexes(tmp_path: Path) -> None:
    packs_dir = tmp_path / "packs"

    result = init_engram_pack("nested-pack", packs_dir, nested=True)

    assert result["ok"] is True
    target = packs_dir / "nested-pack"
    assert (target / "knowledge" / "_index.md").is_file()
    assert (target / "knowledge" / "分组示例" / "_index.md").is_file()
    assert (target / "knowledge" / "分组示例" / "示例知识.md").is_file()

    top_index = (target / "knowledge" / "_index.md").read_text(encoding="utf-8")
    assert "→ 详见 knowledge/分组示例/_index.md" in top_index
