from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from utils import dump_frontmatter, ensure_dir, load_json, normalize_whitespace, write_json, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chunk parsed EPUB chapter content into markdown reading chunks.",
    )
    parser.add_argument(
        "book_dir",
        help="Path to a parsed book output directory that contains book.json and manifest.json",
    )
    parser.add_argument(
        "--target-chars",
        type=int,
        default=3500,
        help="Preferred chunk size in characters",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=5000,
        help="Maximum chunk size in characters",
    )
    parser.add_argument(
        "--overlap-chars",
        type=int,
        default=300,
        help="Approximate overlap between adjacent chunks",
    )
    parser.add_argument(
        "--mode",
        choices=["balanced", "chapter-strict", "extract-friendly"],
        default="balanced",
        help="Chunking mode: balanced (default), chapter-strict, extract-friendly",
    )
    return parser.parse_args()


def split_long_paragraph(text: str, max_chars: int) -> list[str]:
    clean = text.strip()
    if len(clean) <= max_chars:
        return [clean]

    sentences = re.split(r"(?<=[。！？.!?])\s+", clean)
    if len(sentences) == 1:
        return [clean[index:index + max_chars].strip() for index in range(0, len(clean), max_chars)]

    parts: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        candidate = f"{current} {sentence}".strip() if current else sentence
        if current and len(candidate) > max_chars:
            parts.append(current)
            current = sentence
            continue

        if len(sentence) > max_chars:
            if current:
                parts.append(current)
                current = ""
            parts.extend(
                chunk.strip()
                for chunk in [sentence[index:index + max_chars] for index in range(0, len(sentence), max_chars)]
                if chunk.strip()
            )
            continue

        current = candidate

    if current:
        parts.append(current)

    return parts or [clean]


def prepare_paragraphs(content: str, max_chars: int) -> list[dict[str, Any]]:
    raw_paragraphs = [
        normalize_whitespace(paragraph)
        for paragraph in re.split(r"\n\s*\n", content)
        if normalize_whitespace(paragraph)
    ]

    paragraphs: list[str] = []
    for paragraph in raw_paragraphs:
        paragraphs.extend(split_long_paragraph(paragraph, max_chars))

    records: list[dict[str, Any]] = []
    cursor = 0
    for index, paragraph in enumerate(paragraphs):
        start = cursor
        end = start + len(paragraph)
        records.append(
            {
                "index": index,
                "text": paragraph,
                "start": start,
                "end": end,
            }
        )
        cursor = end + 2
    return records


def chunk_paragraphs(
    paragraphs: list[dict[str, Any]],
    target_chars: int,
    max_chars: int,
    overlap_chars: int,
) -> list[dict[str, Any]]:
    if not paragraphs:
        return []

    chunks: list[dict[str, Any]] = []
    index = 0
    min_fill = max(1, min(target_chars, int(target_chars * 0.6)))

    while index < len(paragraphs):
        start_index = index
        selected: list[dict[str, Any]] = []
        current_length = 0

        while index < len(paragraphs):
            paragraph = paragraphs[index]
            addition = len(paragraph["text"]) + (2 if selected else 0)
            candidate_length = current_length + addition

            if selected and candidate_length > max_chars:
                break

            if selected and candidate_length > target_chars and current_length >= min_fill:
                break

            selected.append(paragraph)
            current_length = candidate_length
            index += 1

        if not selected:
            selected.append(paragraphs[index])
            current_length = len(paragraphs[index]["text"])
            index += 1

        end_index = selected[-1]["index"]
        chunks.append(
            {
                "text": "\n\n".join(item["text"] for item in selected),
                "char_start": selected[0]["start"],
                "char_end": selected[-1]["end"],
                "start_index": start_index,
                "end_index": end_index,
            }
        )

        if index >= len(paragraphs) or overlap_chars <= 0:
            continue

        overlap_start = index
        overlap_length = 0
        probe = end_index

        while probe >= start_index:
            addition = len(paragraphs[probe]["text"]) + (2 if overlap_length else 0)
            if overlap_length and overlap_length + addition > overlap_chars:
                break
            overlap_length += addition
            overlap_start = probe
            probe -= 1

        if overlap_start <= start_index and end_index > start_index:
            overlap_start = start_index + 1

        if overlap_start < index:
            index = overlap_start

    return chunks


def resolve_book_dir(input_path: Path) -> Path:
    if input_path.is_file():
        return input_path.parent
    return input_path


def read_inputs(book_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest_path = book_dir / "manifest.json"
    book_path = book_dir / "book.json"
    metadata_path = book_dir / "metadata.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.json not found in {book_dir}")
    if not book_path.exists():
        raise FileNotFoundError(f"book.json not found in {book_dir}")
    if not metadata_path.exists():
        raise FileNotFoundError(f"metadata.json not found in {book_dir}")

    return load_json(manifest_path), load_json(book_path), load_json(metadata_path)


def update_reading_index(book_dir: Path, book: dict[str, Any], all_chunks: list[dict[str, Any]]) -> None:
    reading_index_path = book_dir / "reading_index.json"
    if reading_index_path.exists():
        reading_index = load_json(reading_index_path)
    else:
        reading_index = {
            "book_id": book.get("book_id", ""),
            "title": book.get("title", ""),
            "chapters": [],
        }

    chunk_ranges: dict[str, dict[str, Any]] = {}
    for chunk in all_chunks:
        chapter_id = chunk["chapter_id"]
        entry = chunk_ranges.setdefault(
            chapter_id,
            {
                "chunk_start": chunk["chunk_index"],
                "chunk_end": chunk["chunk_index"],
                "chunk_count": 0,
            },
        )
        entry["chunk_end"] = chunk["chunk_index"]
        entry["chunk_count"] += 1

    chapters_by_id = {
        chapter.get("chapter_id", ""): chapter
        for chapter in book.get("chapters", [])
    }
    updated_chapters: list[dict[str, Any]] = []

    for chapter in reading_index.get("chapters", []):
        chapter_id = chapter.get("chapter_id", "")
        source = chapters_by_id.get(chapter_id, {})
        chunk_info = chunk_ranges.get(
            chapter_id,
            {"chunk_start": None, "chunk_end": None, "chunk_count": 0},
        )
        chapter.update(
            {
                "has_images": bool(source.get("image_count", chapter.get("image_count", 0))),
                "has_tables": bool(source.get("table_count", chapter.get("table_count", 0))),
                "chunk_start": chunk_info["chunk_start"],
                "chunk_end": chunk_info["chunk_end"],
                "chunk_count": chunk_info["chunk_count"],
            }
        )
        updated_chapters.append(chapter)

    if not updated_chapters:
        for chapter in book.get("chapters", []):
            chapter_id = chapter.get("chapter_id", "")
            chunk_info = chunk_ranges.get(
                chapter_id,
                {"chunk_start": None, "chunk_end": None, "chunk_count": 0},
            )
            updated_chapters.append(
                {
                    "chapter_id": chapter_id,
                    "chapter_title": chapter.get("chapter_title", ""),
                    "word_count": chapter.get("word_count", 0),
                    "char_count": chapter.get("char_count", 0),
                    "paragraph_count": chapter.get("paragraph_count", 0),
                    "heading_count": chapter.get("heading_count", 0),
                    "image_count": chapter.get("image_count", 0),
                    "table_count": chapter.get("table_count", 0),
                    "has_images": bool(chapter.get("image_count", 0)),
                    "has_tables": bool(chapter.get("table_count", 0)),
                    "chunk_start": chunk_info["chunk_start"],
                    "chunk_end": chunk_info["chunk_end"],
                    "chunk_count": chunk_info["chunk_count"],
                    "source_files": chapter.get("source_files", []),
                }
            )

    reading_index["chapters"] = updated_chapters
    write_json(reading_index_path, reading_index)


def write_chunks(
    book_dir: Path,
    manifest: dict[str, Any],
    book: dict[str, Any],
    metadata: dict[str, Any],
    target_chars: int,
    max_chars: int,
    overlap_chars: int,
    mode: str = "balanced",
) -> dict[str, Any]:
    chunks_dir = ensure_dir(book_dir / "chunks")
    all_chunks: list[dict[str, Any]] = []
    chunk_files: list[str] = []

    if mode == "extract-friendly":
        target_chars = min(target_chars, 2000)
        max_chars = min(max_chars, 3000)
        overlap_chars = max(overlap_chars, 500)

    global_index = 1
    chapters = book.get("chapters", [])

    for chapter in chapters:
        chapter_id = chapter.get("chapter_id", "")
        chapter_title = chapter.get("chapter_title", "")
        content_markdown = chapter.get("content_markdown", "")
        chapter_index = chapter.get("index", 0)
        chapter_has_images = chapter.get("image_count", 0) > 0
        chapter_has_tables = chapter.get("table_count", 0) > 0

        paragraphs = prepare_paragraphs(content_markdown, max_chars=max_chars)
        chapter_chunks = chunk_paragraphs(
            paragraphs=paragraphs,
            target_chars=target_chars,
            max_chars=max_chars,
            overlap_chars=overlap_chars,
        )

        total_chunks_in_chapter = len(chapter_chunks)

        for chunk_in_chapter, chunk in enumerate(chapter_chunks, start=1):
            filename = f"chunk-{global_index:04d}.md"
            relative_path = f"chunks/{filename}"
            chunk_word_count = len(chunk["text"].split())

            chunk_record = {
                "book_id": metadata.get("book_id", ""),
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "chapter_id": chapter_id,
                "chapter_title": chapter_title,
                "chunk_index": global_index,
                "chunk_in_chapter": chunk_in_chapter,
                "chapter_chunk_index": chunk_in_chapter,
                "chapter_index": chapter_index,
                "total_chunks_in_chapter": total_chunks_in_chapter,
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
                "previous_chunk": "",
                "next_chunk": "",
                "file": relative_path,
                "word_count": chunk_word_count,
                "has_images": chapter_has_images,
                "has_tables": chapter_has_tables,
                "content": chunk["text"],
            }
            all_chunks.append(chunk_record)
            chunk_files.append(relative_path)
            global_index += 1

    for index, chunk in enumerate(all_chunks):
        chunk["previous_chunk"] = all_chunks[index - 1]["file"] if index > 0 else ""
        chunk["next_chunk"] = all_chunks[index + 1]["file"] if index + 1 < len(all_chunks) else ""

        content = dump_frontmatter(
            {
                "book_id": chunk["book_id"],
                "title": chunk["title"],
                "author": chunk["author"],
                "chapter_id": chunk["chapter_id"],
                "chapter_title": chunk["chapter_title"],
                "chunk_index": chunk["chunk_index"],
                "chapter_index": chunk["chapter_index"],
                "chunk_in_chapter": chunk["chunk_in_chapter"],
                "chapter_chunk_index": chunk["chapter_chunk_index"],
                "total_chunks_in_chapter": chunk["total_chunks_in_chapter"],
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
                "previous_chunk": chunk["previous_chunk"],
                "next_chunk": chunk["next_chunk"],
                "word_count": chunk["word_count"],
                "has_images": chunk["has_images"],
                "has_tables": chunk["has_tables"],
            },
            chunk["content"],
        )
        write_text(book_dir / chunk["file"], content)

    manifest["chunk_count"] = len(all_chunks)
    manifest["chunking"] = {
        "status": "complete",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "target_chars": target_chars,
            "max_chars": max_chars,
            "overlap_chars": overlap_chars,
            "mode": mode,
        },
    }
    manifest.setdefault("files", {})
    manifest["files"]["chunks_dir"] = "chunks"
    manifest["files"]["chunk_files"] = chunk_files
    manifest["chunks"] = [
        {
            "chunk_index": chunk["chunk_index"],
            "chapter_id": chunk["chapter_id"],
            "chapter_title": chunk["chapter_title"],
            "chapter_index": chunk["chapter_index"],
            "chunk_in_chapter": chunk["chunk_in_chapter"],
            "chapter_chunk_index": chunk["chapter_chunk_index"],
            "total_chunks_in_chapter": chunk["total_chunks_in_chapter"],
            "char_start": chunk["char_start"],
            "char_end": chunk["char_end"],
            "file": chunk["file"],
            "previous_chunk": chunk["previous_chunk"],
            "next_chunk": chunk["next_chunk"],
            "word_count": chunk["word_count"],
            "has_images": chunk["has_images"],
            "has_tables": chunk["has_tables"],
        }
        for chunk in all_chunks
    ]

    write_json(book_dir / "manifest.json", manifest)
    update_reading_index(book_dir, book, all_chunks)

    return {
        "book_id": metadata.get("book_id", ""),
        "title": metadata.get("title", ""),
        "author": metadata.get("author", ""),
        "chapter_count": manifest.get("chapter_count", 0),
        "chunk_count": manifest.get("chunk_count", 0),
        "output_dir": str(book_dir.resolve()),
    }


def main() -> int:
    args = parse_args()

    if args.target_chars <= 0 or args.max_chars <= 0 or args.overlap_chars < 0:
        print("Error: chunk size arguments must be positive, and overlap must be >= 0", file=sys.stderr)
        return 1

    if args.target_chars > args.max_chars:
        print("Error: --target-chars cannot be greater than --max-chars", file=sys.stderr)
        return 1

    book_dir = resolve_book_dir(Path(args.book_dir).expanduser().resolve())

    try:
        manifest, book, metadata = read_inputs(book_dir)
        summary = write_chunks(
            book_dir=book_dir,
            manifest=manifest,
            book=book,
            metadata=metadata,
            target_chars=args.target_chars,
            max_chars=args.max_chars,
            overlap_chars=args.overlap_chars,
            mode=args.mode,
        )
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": "ok", **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
