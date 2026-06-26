from __future__ import annotations

import json
from pathlib import Path

import pytest

from engram_server.lint import lint_engram
from engram_server.server import main


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _create_valid_pack(root: Path, name: str = "demo") -> Path:
    pack = root / name
    _write(
        pack / "meta.json",
        json.dumps({"name": name, "description": "desc"}, ensure_ascii=False, indent=2),
    )
    _write(pack / "role.md", "# role\n")
    _write(
        pack / "knowledge" / "_index.md",
        "## 知识索引\n- `knowledge/topic.md` - 主题\n",
    )
    _write(pack / "knowledge" / "topic.md", "# topic\n")
    _write(
        pack / "examples" / "_index.md",
        "## 案例索引\n- `examples/case.md` - 案例\n",
    )
    _write(
        pack / "examples" / "case.md",
        "---\nuses:\n  - knowledge/topic.md\n---\n\n正文\n",
    )
    return pack


def test_lint_ok_pack_has_no_messages(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path)
    messages = lint_engram(pack)
    assert messages == []


def test_lint_detects_missing_index_reference(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path)
    _write(
        pack / "knowledge" / "_index.md",
        "## 知识索引\n- `knowledge/missing.md` - 丢失\n",
    )

    messages = lint_engram(pack)
    assert any(
        m.level == "error" and "索引引用文件不存在" in m.message for m in messages
    )


def test_lint_detects_orphan_file_warning(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path)
    _write(pack / "knowledge" / "orphan.md", "# orphan\n")

    messages = lint_engram(pack)
    assert any(
        m.level == "warning"
        and m.file_path == "knowledge/orphan.md"
        and "孤儿文件" in m.message
        for m in messages
    )


def test_lint_detects_invalid_meta_json(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path)
    _write(pack / "meta.json", "{broken json")

    messages = lint_engram(pack)
    assert any(
        m.level == "error" and "meta.json 不是合法 JSON" in m.message for m in messages
    )


def test_lint_detects_empty_knowledge_file_warning(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path)
    _write(pack / "knowledge" / "topic.md", "")

    messages = lint_engram(pack)
    assert any(
        m.level == "warning"
        and m.file_path == "knowledge/topic.md"
        and "0 字节" in m.message
        for m in messages
    )


def test_lint_detects_extends_parent_missing(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path, "child")
    _write(
        pack / "meta.json",
        json.dumps(
            {"name": "child", "description": "desc", "extends": "missing-parent"},
            ensure_ascii=False,
            indent=2,
        ),
    )

    messages = lint_engram(pack)
    assert any(
        m.level == "error" and "extends 引用的父 Engram 不存在" in m.message
        for m in messages
    )


def test_lint_accepts_extends_parent_exists(tmp_path: Path) -> None:
    _create_valid_pack(tmp_path, "parent")
    child = _create_valid_pack(tmp_path, "child")
    _write(
        child / "meta.json",
        json.dumps(
            {"name": "child", "description": "desc", "extends": "parent"},
            ensure_ascii=False,
            indent=2,
        ),
    )

    messages = lint_engram(child)
    assert not any("extends" in m.message and m.level == "error" for m in messages)


def test_lint_checks_recursive_nested_indexes(tmp_path: Path) -> None:
    pack = _create_valid_pack(tmp_path)
    _write(
        pack / "knowledge" / "_index.md",
        "## 知识索引\n"
        "- `knowledge/topic.md` - 根知识\n"
        "  → 详见 knowledge/sub/_index.md\n",
    )
    _write(
        pack / "knowledge" / "sub" / "_index.md",
        "## 子索引\n- `knowledge/sub/deep.md` - 深层知识\n",
    )
    _write(pack / "knowledge" / "sub" / "deep.md", "# deep\n")

    assert lint_engram(pack) == []

    (pack / "knowledge" / "sub" / "deep.md").unlink()
    messages = lint_engram(pack)
    assert any(
        m.level == "error" and "索引引用文件不存在" in m.message for m in messages
    )


def test_cli_lint_exit_code_and_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _create_valid_pack(tmp_path, "ok-pack")
    broken = _create_valid_pack(tmp_path, "broken-pack")
    (broken / "role.md").unlink()

    with pytest.raises(SystemExit) as exc:
        main(["lint", "--packs-dir", str(tmp_path)])
    assert exc.value.code == 1

    out = capsys.readouterr().out
    assert "ok-pack: 0 errors, 0 warnings" in out
    assert "broken-pack: 1 errors, 0 warnings" in out
