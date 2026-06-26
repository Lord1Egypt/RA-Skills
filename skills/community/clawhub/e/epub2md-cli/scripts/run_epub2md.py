#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_WORKSPACE_ROOT = Path("/home/admin1/.agents/skills/epub2md-cli-workspace")
VALID_MODES = {"split", "merge", "both", "inspect"}
VALID_INSPECT_ACTIONS = {"info", "structure", "sections", "unzip"}


@dataclass(frozen=True)
class WorkspacePaths:
    book_name: str
    book_dir: Path
    inputs_dir: Path
    outputs_dir: Path
    input_epub: Path
    split_dir: Path
    merge_dir: Path
    inspect_dir: Path


def build_workspace_paths(epub_path: Path, workspace_root: Path = DEFAULT_WORKSPACE_ROOT) -> WorkspacePaths:
    book_name = epub_path.stem
    book_dir = workspace_root / book_name
    inputs_dir = book_dir / "inputs"
    outputs_dir = book_dir / "outputs"
    return WorkspacePaths(
        book_name=book_name,
        book_dir=book_dir,
        inputs_dir=inputs_dir,
        outputs_dir=outputs_dir,
        input_epub=inputs_dir / epub_path.name,
        split_dir=outputs_dir / "split",
        merge_dir=outputs_dir / "merge",
        inspect_dir=outputs_dir / "inspect",
    )


def default_merge_name(epub_path: Path) -> str:
    return f"{epub_path.stem}-merged.md"


def normalize_inspect_actions(actions: list[str] | None) -> list[str]:
    if not actions:
        return ["info", "structure"]

    normalized: list[str] = []
    for action in actions:
        if action not in VALID_INSPECT_ACTIONS:
            raise ValueError(f"Unsupported inspect action: {action}")
        if action not in normalized:
            normalized.append(action)
    return normalized


def build_epub_command(
    epub_path: Path,
    mode: str,
    merge_name: str | None = None,
    autocorrect: bool = False,
    localize: bool = False,
) -> list[str]:
    if mode not in {"split", "merge"}:
        raise ValueError(f"Unsupported mode: {mode}")

    command = ["epub2md"]
    if autocorrect:
        command.append("--autocorrect")
    if localize:
        command.append("--localize")
    if mode == "merge":
        command.append(f"--merge={merge_name or default_merge_name(epub_path)}")
    command.append(str(epub_path))
    return command


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_clean_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_input_epub(source_epub: Path, paths: WorkspacePaths) -> Path:
    ensure_directory(paths.inputs_dir)
    shutil.copy2(source_epub, paths.input_epub)
    ensure_directory(paths.outputs_dir)
    return paths.input_epub


def require_epub2md() -> None:
    if shutil.which("epub2md") is None:
        raise RuntimeError("epub2md is not installed or not available on PATH")


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )


def copy_tree(source: Path, destination: Path) -> None:
    ensure_clean_directory(destination)
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)


def stage_epub(input_epub: Path, temp_dir: Path) -> Path:
    staged_epub = temp_dir / input_epub.name
    shutil.copy2(input_epub, staged_epub)
    return staged_epub


def run_split(input_epub: Path, paths: WorkspacePaths, autocorrect: bool, localize: bool) -> Path:
    with tempfile.TemporaryDirectory(dir=paths.book_dir, prefix=".tmp-split-") as temp_root:
        temp_dir = Path(temp_root)
        staged_epub = stage_epub(input_epub, temp_dir)
        command = build_epub_command(staged_epub, mode="split", autocorrect=autocorrect, localize=localize)
        run_command(command, cwd=temp_dir)
        copy_tree(temp_dir / paths.book_name, paths.split_dir)
    return paths.split_dir


def run_inspect(input_epub: Path, paths: WorkspacePaths, actions: list[str] | None) -> Path:
    ensure_clean_directory(paths.inspect_dir)
    effective_actions = normalize_inspect_actions(actions)
    output_files = {
        "info": "info.txt",
        "structure": "structure.txt",
        "sections": "sections.txt",
    }

    for action in effective_actions:
        if action == "unzip":
            command = ["epub2md", "--unzip", str(input_epub)]
            run_command(command, cwd=paths.inspect_dir)
            unzipped_dir = paths.inspect_dir / paths.book_name
            if unzipped_dir.exists():
                target_dir = paths.inspect_dir / "unzipped"
                ensure_clean_directory(target_dir)
                for child in unzipped_dir.iterdir():
                    target = target_dir / child.name
                    if child.is_dir():
                        shutil.copytree(child, target)
                    else:
                        shutil.copy2(child, target)
                shutil.rmtree(unzipped_dir)
            continue

        command = ["epub2md", f"--{action}", str(input_epub)]
        result = run_command(command, cwd=paths.inspect_dir)
        (paths.inspect_dir / output_files[action]).write_text(result.stdout, encoding="utf-8")

    return paths.inspect_dir


def run_merge(input_epub: Path, paths: WorkspacePaths, merge_name: str | None, autocorrect: bool, localize: bool) -> Path:
    with tempfile.TemporaryDirectory(dir=paths.book_dir, prefix=".tmp-merge-") as temp_root:
        temp_dir = Path(temp_root)
        staged_epub = stage_epub(input_epub, temp_dir)
        effective_merge_name = merge_name or default_merge_name(staged_epub)
        command = build_epub_command(
            staged_epub,
            mode="merge",
            merge_name=effective_merge_name,
            autocorrect=autocorrect,
            localize=localize,
        )
        run_command(command, cwd=temp_dir)
        copy_tree(temp_dir / paths.book_name, paths.merge_dir)
    return paths.merge_dir / effective_merge_name


def execute(
    epub_path: Path,
    mode: str,
    workspace_root: Path = DEFAULT_WORKSPACE_ROOT,
    merge_name: str | None = None,
    autocorrect: bool = False,
    localize: bool = False,
    inspect_actions: list[str] | None = None,
) -> WorkspacePaths:
    if mode not in VALID_MODES:
        raise ValueError(f"Unsupported mode: {mode}")
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    require_epub2md()
    paths = build_workspace_paths(epub_path, workspace_root)
    ensure_directory(paths.book_dir)
    input_epub = copy_input_epub(epub_path, paths)

    if mode in {"split", "both"}:
        run_split(input_epub, paths, autocorrect=autocorrect, localize=localize)
    if mode in {"merge", "both"}:
        run_merge(input_epub, paths, merge_name=merge_name, autocorrect=autocorrect, localize=localize)
    if mode == "inspect":
        run_inspect(input_epub, paths, actions=inspect_actions)

    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run epub2md into a stable workspace layout.")
    parser.add_argument("--input", required=True, help="Absolute or relative path to the source EPUB file")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), required=True, help="split, merge, or both")
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT), help="Root directory for epub2md workspace output")
    parser.add_argument("--merge-name", help="Custom merged markdown filename for merge mode")
    parser.add_argument("--autocorrect", action="store_true", help="Enable epub2md autocorrect mode")
    parser.add_argument("--localize", action="store_true", help="Download remote images when present")
    parser.add_argument(
        "--inspect-actions",
        nargs="+",
        choices=sorted(VALID_INSPECT_ACTIONS),
        help="Inspect actions to run in inspect mode. Defaults to: info structure",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = execute(
        epub_path=Path(args.input).expanduser().resolve(),
        mode=args.mode,
        workspace_root=Path(args.workspace_root).expanduser().resolve(),
        merge_name=args.merge_name,
        autocorrect=args.autocorrect,
        localize=args.localize,
        inspect_actions=args.inspect_actions,
    )
    print(f"book_dir={paths.book_dir}")
    print(f"input_epub={paths.input_epub}")
    print(f"split_dir={paths.split_dir}")
    print(f"merge_dir={paths.merge_dir}")
    print(f"inspect_dir={paths.inspect_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
