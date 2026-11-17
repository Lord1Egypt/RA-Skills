#!/usr/bin/env python3
"""Scaffold fiction projects and check required file structure only."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


FILES = (
    "README.md",
    "story-bible.md",
    "world.md",
    "characters/index.md",
    "outline/volume-01.md",
    "outline/timeline.md",
    "chapters/001-title.md",
)


def init_project(out: Path, title: str) -> Path:
    if not title.strip():
        raise ValueError("needs_clarification: 作品名不能为空")
    for rel in FILES:
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        text = f"# {title}\n\n待填写。\n" if rel in ("README.md", "story-bible.md", "world.md") else "# 待填写\n\n"
        try:
            with path.open("x", encoding="utf-8") as stream:
                stream.write(text)
        except FileExistsError:
            # O_EXCL protects concurrent creates and existing (including broken symlink) paths.
            pass
    return out


def check_project(root: Path) -> dict:
    """Check required paths and whether required files contain text; never inspect prose consistency."""
    missing = []
    invalid = []
    empty = []
    for rel in FILES:
        path = root / rel
        if not path.exists():
            missing.append(rel)
        elif not path.is_file():
            invalid.append(rel)
        else:
            try:
                if not path.read_text(encoding="utf-8").strip():
                    empty.append(rel)
            except (OSError, UnicodeError):
                invalid.append(rel)

    chapter_dir = root / "chapters"
    chapters = sorted(chapter_dir.glob("*.md")) if chapter_dir.is_dir() else []
    needs_review = bool(missing or invalid or empty)
    return {
        "check_type": "project_structure",
        "structure_status": "needs_review" if needs_review else "complete",
        "missing": missing,
        "empty": empty,
        "invalid": invalid,
        "chapter_count": len(chapters),
        "message": "目录结构或必需文件内容不完整，请按列表补齐。" if needs_review else "必需文件均存在且非空；正文连续性尚未检查。",
    }


def run_self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="fiction-crafter-") as temp:
        root = Path(temp) / "novel"
        init_project(root, "测试作品")
        initialized = check_project(root)
        assert initialized["structure_status"] == "complete", initialized
        assert initialized["chapter_count"] == 1, initialized

        # Deliberately contradictory prose remains structurally complete: this is not semantic QA.
        (root / "story-bible.md").write_text("主角不能离开车站。\n", encoding="utf-8")
        (root / "chapters/001-title.md").write_text("主角离开了车站。\n", encoding="utf-8")
        assert check_project(root)["structure_status"] == "complete"

        chapter = root / "chapters/001-title.md"
        chapter.write_text("既有章节内容\n", encoding="utf-8")
        init_project(root, "覆盖测试")
        assert chapter.read_text(encoding="utf-8") == "既有章节内容\n"

        # Simulate another writer creating a file after our parent directory setup,
        # immediately before this process attempts its exclusive create.
        raced_root = Path(temp) / "race-novel"
        raced_file = raced_root / "chapters/001-title.md"
        original_open = Path.open

        def create_before_exclusive_open(path, mode="r", *args, **kwargs):
            if path == raced_file and mode == "x":
                with original_open(path, "w", encoding="utf-8") as stream:
                    stream.write("并发写入的正文\n")
            return original_open(path, mode, *args, **kwargs)

        with patch.object(Path, "open", create_before_exclusive_open):
            init_project(raced_root, "竞态测试")
        assert raced_file.read_text(encoding="utf-8") == "并发写入的正文\n"

        link_root = Path(temp) / "linked-novel"
        link_root.mkdir()
        broken_link = link_root / "world.md"
        link_target = Path(temp) / "must-not-be-created.md"
        broken_link.symlink_to(link_target)
        init_project(link_root, "断链测试")
        assert broken_link.is_symlink()
        assert not link_target.exists()

        (root / "world.md").write_text("  \n", encoding="utf-8")
        (root / "outline/timeline.md").unlink()
        incomplete = check_project(root)
        assert incomplete["structure_status"] == "needs_review", incomplete
        assert incomplete["missing"] == ["outline/timeline.md"], incomplete
        assert incomplete["empty"] == ["world.md"], incomplete

        nested_file = root / "characters/index.md"
        nested_file.unlink()
        nested_file.mkdir()
        invalid = check_project(root)
        assert invalid["invalid"] == ["characters/index.md"], invalid

        cli = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "check", "--input", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert cli.returncode == 1, cli
        assert json.loads(cli.stdout)["check_type"] == "project_structure", cli.stdout

        absent = check_project(Path(temp) / "absent")
        assert absent["structure_status"] == "needs_review", absent
        assert absent["missing"] == list(FILES), absent

    print("self-test: PASS (scaffold, non-overwrite, missing/empty structure checks)")


def main() -> int:
    parser = argparse.ArgumentParser(description="小说项目脚手架和目录结构检查（不分析正文连续性）")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("self-test")
    init_parser = sub.add_parser("init")
    init_parser.add_argument("--output", required=True)
    init_parser.add_argument("--title", required=True)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--input", required=True)
    args = parser.parse_args()

    try:
        if args.cmd == "self-test":
            run_self_test()
            return 0
        if args.cmd == "init":
            print(f"initialized {init_project(Path(args.output), args.title)}")
            return 0
        result = check_project(Path(args.input))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["structure_status"] == "needs_review" else 0
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
