#!/usr/bin/env python3
"""
Safe validation script for epub-read.

By default this script runs a lightweight smoke test:
1. Parse one EPUB into a temporary output directory.
2. Verify the key JSON files exist.
3. Generate an overview plan.

Use --full only when you explicitly want chunking and state-management checks.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run smoke/full checks for epub-read.")
    parser.add_argument("--epub", required=True, help="Path to a test EPUB file")
    parser.add_argument(
        "--output-dir",
        default=str(Path(tempfile.gettempdir()) / "epub-read-test-output"),
        help="Output directory for generated artifacts",
    )
    parser.add_argument("--full", action="store_true", help="Run chunking and session-state checks too")
    parser.add_argument("--keep-output", action="store_true", help="Keep output directory after the test")
    return parser.parse_args()


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_book_dir(output_dir: Path) -> Path:
    book_dirs = [path for path in output_dir.iterdir() if path.is_dir()]
    if len(book_dirs) != 1:
        raise RuntimeError(f"Expected exactly one parsed book directory in {output_dir}, got {len(book_dirs)}")
    return book_dirs[0]


def assert_parse_outputs(book_dir: Path) -> None:
    required_files = [
        "metadata.json",
        "toc.json",
        "book.json",
        "manifest.json",
        "reading_index.json",
        "complex_content.json",
        "session_state.json",
    ]
    for filename in required_files:
        if not (book_dir / filename).exists():
            raise RuntimeError(f"Missing required file: {book_dir / filename}")

    manifest = load_json(book_dir / "manifest.json")
    for field in [
        "total_words",
        "total_images",
        "total_tables",
        "total_xhtml_files",
        "estimated_reading_time_minutes",
        "detected_complex_content",
    ]:
        if field not in manifest:
            raise RuntimeError(f"manifest.json is missing field: {field}")


def assert_chunk_outputs(book_dir: Path) -> None:
    manifest = load_json(book_dir / "manifest.json")
    if int(manifest.get("chunk_count", 0)) <= 0:
        raise RuntimeError("chunk_book.py did not create any chunks")

    first_chunk = book_dir / "chunks" / "chunk-0001.md"
    if not first_chunk.exists():
        raise RuntimeError("Expected first chunk file to exist")

    chunk_text = first_chunk.read_text(encoding="utf-8")
    for field in [
        "chapter_index",
        "chunk_in_chapter",
        "chapter_chunk_index",
        "total_chunks_in_chapter",
        "word_count",
        "has_images",
        "has_tables",
    ]:
        if field not in chunk_text:
            raise RuntimeError(f"Chunk frontmatter is missing field: {field}")

    reading_index = load_json(book_dir / "reading_index.json")
    first_chapter = reading_index.get("chapters", [{}])[0]
    for field in ["chunk_start", "chunk_end", "chunk_count"]:
        if field not in first_chapter:
            raise RuntimeError(f"reading_index.json is missing field: {field}")


def main() -> int:
    args = parse_args()

    skill_dir = Path(__file__).resolve().parent
    epub_path = Path(args.epub).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not epub_path.exists():
        raise SystemExit(f"EPUB does not exist: {epub_path}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    python_executable = sys.executable

    try:
        parse_result = run_command(
            [python_executable, "parse_epub.py", str(epub_path), "--output-dir", str(output_dir)],
            cwd=skill_dir,
        )
        parse_summary = json.loads(parse_result.stdout)
        if parse_summary.get("status") != "ok":
            raise RuntimeError("parse_epub.py did not return status=ok")

        book_dir = find_book_dir(output_dir)
        assert_parse_outputs(book_dir)

        overview_result = run_command(
            [python_executable, "task_router.py", str(book_dir), "--mode", "overview"],
            cwd=skill_dir,
        )
        overview_plan = json.loads(overview_result.stdout)
        if overview_plan.get("mode") != "overview":
            raise RuntimeError("Overview plan was not generated correctly")

        if args.full:
            run_command(
                [python_executable, "chunk_book.py", str(book_dir), "--mode", "balanced"],
                cwd=skill_dir,
            )
            assert_chunk_outputs(book_dir)

            run_command(
                [python_executable, "task_router.py", str(book_dir), "--mode", "full_read", "--start-chunk", "1"],
                cwd=skill_dir,
            )
            run_command(
                [python_executable, "update_session_state.py", str(book_dir), "set", "--mode", "full_read", "--chapter", "ch001", "--chunk", "1", "--action", "read_chunk"],
                cwd=skill_dir,
            )
            state_result = run_command(
                [python_executable, "update_session_state.py", str(book_dir), "get"],
                cwd=skill_dir,
            )
            state = json.loads(state_result.stdout)
            if state.get("current_mode") != "full_read":
                raise RuntimeError("session_state.json was not updated correctly")

        print(
            json.dumps(
                {
                    "status": "ok",
                    "mode": "full" if args.full else "smoke",
                    "output_dir": str(output_dir),
                    "book_dir": str(book_dir),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    finally:
        if output_dir.exists() and not args.keep_output:
            shutil.rmtree(output_dir)


if __name__ == "__main__":
    raise SystemExit(main())
