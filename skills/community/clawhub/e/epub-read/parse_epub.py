from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from utils import (
    HTML_TYPES,
    ensure_dir,
    extract_markdown_from_html,
    is_probably_noise_page,
    normalize_whitespace,
    read_zip_text,
    resolve_href,
    slugify,
    write_json,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse an EPUB into structured markdown and JSON artifacts.",
    )
    parser.add_argument("epub_path", help="Path to a single .epub file")
    parser.add_argument(
        "--output-dir",
        default=".epub_read_output",
        help="Root directory for parser outputs",
    )
    parser.add_argument(
        "--book-id",
        default=None,
        help="Optional explicit book identifier",
    )
    return parser.parse_args()


def parse_container(archive: zipfile.ZipFile) -> str:
    container_xml = read_zip_text(archive, "META-INF/container.xml")
    root = ET.fromstring(container_xml)

    for rootfile in root.findall(".//{*}rootfile"):
        full_path = rootfile.attrib.get("full-path")
        if full_path:
            return full_path

    raise ValueError("Could not locate OPF path from META-INF/container.xml")


def parse_opf(opf_text: str) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    root = ET.fromstring(opf_text)

    metadata_node = root.find(".//{*}metadata")
    manifest_node = root.find(".//{*}manifest")
    spine_node = root.find(".//{*}spine")

    if metadata_node is None or manifest_node is None or spine_node is None:
        raise ValueError("OPF is missing metadata, manifest, or spine")

    titles = [
        normalize_whitespace(node.text or "")
        for node in metadata_node.findall(".//{http://purl.org/dc/elements/1.1/}title")
        if normalize_whitespace(node.text or "")
    ]
    creators = [
        normalize_whitespace(node.text or "")
        for node in metadata_node.findall(".//{http://purl.org/dc/elements/1.1/}creator")
        if normalize_whitespace(node.text or "")
    ]
    languages = [
        normalize_whitespace(node.text or "")
        for node in metadata_node.findall(".//{http://purl.org/dc/elements/1.1/}language")
        if normalize_whitespace(node.text or "")
    ]

    identifiers: list[dict[str, str]] = []
    for node in metadata_node.findall(".//{http://purl.org/dc/elements/1.1/}identifier"):
        value = normalize_whitespace(node.text or "")
        if value:
            identifiers.append(
                {
                    "id": node.attrib.get("id", ""),
                    "value": value,
                }
            )

    description = ""
    description_node = metadata_node.find(".//{http://purl.org/dc/elements/1.1/}description")
    if description_node is not None:
        description = normalize_whitespace(description_node.text or "")

    publisher = ""
    publisher_node = metadata_node.find(".//{http://purl.org/dc/elements/1.1/}publisher")
    if publisher_node is not None:
        publisher = normalize_whitespace(publisher_node.text or "")

    published_date = ""
    date_node = metadata_node.find(".//{http://purl.org/dc/elements/1.1/}date")
    if date_node is not None:
        published_date = normalize_whitespace(date_node.text or "")

    manifest: list[dict[str, Any]] = []
    for item in manifest_node.findall("./{*}item"):
        manifest.append(
            {
                "id": item.attrib.get("id", ""),
                "href": item.attrib.get("href", ""),
                "media_type": item.attrib.get("media-type", ""),
                "properties": item.attrib.get("properties", ""),
            }
        )

    spine = [
        itemref.attrib.get("idref", "")
        for itemref in spine_node.findall("./{*}itemref")
        if itemref.attrib.get("idref", "")
    ]

    metadata = {
        "title": titles[0] if titles else "Untitled",
        "titles": titles,
        "author": ", ".join(creators) if creators else "Unknown",
        "authors": creators,
        "language": languages[0] if languages else "",
        "languages": languages,
        "identifier": identifiers[0]["value"] if identifiers else "",
        "identifiers": identifiers,
        "publisher": publisher,
        "published_date": published_date,
        "description": description,
    }

    return metadata, manifest, spine


def _nav_is_toc(nav_tag: Any) -> bool:
    for _, value in nav_tag.attrs.items():
        rendered = " ".join(value) if isinstance(value, list) else str(value)
        if "toc" in rendered.lower():
            return True
    return False


def parse_nav_toc(
    archive: zipfile.ZipFile,
    opf_path: str,
    manifest_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    from bs4 import BeautifulSoup

    nav_item = None
    for item in manifest_items:
        if "nav" in item.get("properties", "").split():
            nav_item = item
            break

    if nav_item is None:
        for item in manifest_items:
            href = item.get("href", "").lower()
            if href.endswith("nav.xhtml") or href.endswith("nav.html"):
                nav_item = item
                break

    if nav_item is None:
        return []

    nav_path = resolve_href(opf_path, nav_item["href"])
    soup = BeautifulSoup(read_zip_text(archive, nav_path), "lxml")
    toc_root = None

    for nav in soup.find_all("nav"):
        if _nav_is_toc(nav):
            toc_root = nav
            break

    if toc_root is None:
        toc_root = soup.find("nav")

    if toc_root is None:
        return []

    toc_entries: list[dict[str, Any]] = []
    seen: set[str] = set()

    for anchor in toc_root.find_all("a"):
        href = anchor.get("href", "")
        title = normalize_whitespace(anchor.get_text(" ", strip=True))
        if not href or not title:
            continue

        resolved = resolve_href(nav_path, href)
        if resolved in seen:
            continue
        seen.add(resolved)

        level = max(1, len(anchor.find_parents(["ol", "ul"])))
        toc_entries.append(
            {
                "title": title,
                "href": resolved,
                "level": level,
                "source": "nav",
            }
        )

    return toc_entries


def parse_ncx_toc(
    archive: zipfile.ZipFile,
    opf_path: str,
    manifest_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ncx_item = None
    for item in manifest_items:
        if item.get("media_type") == "application/x-dtbncx+xml":
            ncx_item = item
            break
        if item.get("href", "").lower().endswith(".ncx"):
            ncx_item = item

    if ncx_item is None:
        return []

    ncx_path = resolve_href(opf_path, ncx_item["href"])
    root = ET.fromstring(read_zip_text(archive, ncx_path))

    entries: list[dict[str, Any]] = []

    def walk(nav_point: ET.Element, level: int) -> None:
        label_node = nav_point.find("./{*}navLabel/{*}text")
        content_node = nav_point.find("./{*}content")

        title = normalize_whitespace(label_node.text or "") if label_node is not None else ""
        src = content_node.attrib.get("src", "") if content_node is not None else ""
        if title and src:
            entries.append(
                {
                    "title": title,
                    "href": resolve_href(ncx_path, src),
                    "level": level,
                    "source": "ncx",
                }
            )

        for child in nav_point.findall("./{*}navPoint"):
            walk(child, level + 1)

    nav_map = root.find(".//{*}navMap")
    if nav_map is not None:
        for top_level in nav_map.findall("./{*}navPoint"):
            walk(top_level, 1)

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in entries:
        if entry["href"] in seen:
            continue
        seen.add(entry["href"])
        deduped.append(entry)
    return deduped


def build_toc_lookup(toc_entries: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for entry in toc_entries:
        href = entry.get("href", "")
        title = entry.get("title", "")
        if href and title:
            lookup[href] = title
    return lookup


def chapter_markdown(title: str, body: str) -> str:
    body = body.strip()
    if body:
        return f"# {title}\n\n{body}\n"
    return f"# {title}\n"


def is_html_manifest_item(item: dict[str, Any]) -> bool:
    href = item.get("href", "").lower()
    media_type = item.get("media_type", "")
    return media_type in HTML_TYPES or href.endswith(".xhtml") or href.endswith(".html") or href.endswith(".htm")


def detect_complex_content(
    manifest_items: list[dict[str, Any]],
    chapters: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Detect image-heavy or resource-heavy chapters that may need special handling.
    """
    has_images = False
    has_svg = False
    has_tables = False
    image_heavy_sections: list[dict[str, Any]] = []
    low_text_resource_sections: list[dict[str, Any]] = []

    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}
    image_items = []

    for item in manifest_items:
        href = item.get("href", "")
        media_type = item.get("media_type", "")
        if any(href.lower().endswith(ext) for ext in image_extensions) or "image" in media_type:
            image_items.append(item)
            has_images = True
        if href.lower().endswith(".svg") or media_type == "image/svg+xml":
            has_svg = True

    for chapter in chapters:
        image_count = int(chapter.get("image_count", 0))
        table_count = int(chapter.get("table_count", 0))
        char_count = int(chapter.get("char_count", 0))
        resource_count = image_count + table_count

        if table_count > 0:
            has_tables = True

        if image_count >= 10:
            image_heavy_sections.append(
                {
                    "chapter_id": chapter["chapter_id"],
                    "chapter_title": chapter["chapter_title"],
                    "image_count": image_count,
                }
            )

        if resource_count > 0 and char_count < 800:
            low_text_resource_sections.append(
                {
                    "chapter_id": chapter["chapter_id"],
                    "chapter_title": chapter["chapter_title"],
                    "char_count": char_count,
                    "image_count": image_count,
                    "table_count": table_count,
                }
            )

    needs_manual_review = bool(
        has_svg
        or image_heavy_sections
        or low_text_resource_sections
        or (has_images and sum(int(ch.get("image_count", 0)) for ch in chapters) > 20)
    )

    summary_parts: list[str] = []
    if has_images:
        summary_parts.append(f"包含图片资源 {len(image_items)} 个")
    if has_svg:
        summary_parts.append("包含 SVG 矢量图")
    if has_tables:
        summary_parts.append("包含表格")
    if image_heavy_sections:
        summary_parts.append(f"有 {len(image_heavy_sections)} 个图片密集型章节")
    if low_text_resource_sections:
        summary_parts.append(f"有 {len(low_text_resource_sections)} 个低文本高资源章节")

    summary = "；".join(summary_parts) if summary_parts else "无显著复杂内容"

    return {
        "has_images": has_images,
        "has_svg": has_svg,
        "has_tables": has_tables,
        "image_heavy_sections": image_heavy_sections,
        "low_text_resource_sections": low_text_resource_sections,
        "needs_manual_review": needs_manual_review,
        "summary": summary,
    }


def build_parse_guidance(summary: dict[str, Any]) -> str:
    lines = [
        "EPUB 已解析完成。当前可执行以下任务类型：",
        "",
        "A. 快速概览：查看目录、结构、元数据与主题",
        "B. 指定章节读取：按章节、目录项或 chunk 范围读取",
        "C. 全文阅读：按分块连续精读整本书",
        "D. 定向抽取：抽取关键词、概念、金句、例子、行动项等",
        "E. 图像与复杂内容辅助：查看图片、表格与复杂排版情况",
        "F. 批量处理：对多个 EPUB 文件批量解析或抽取",
        "",
        "当前书籍信息：",
        f"- 书名：{summary['title']}",
        f"- 作者：{summary['author']}",
        f"- 章节数：{summary['chapter_count']}",
        f"- chunk 数：{summary['chunk_count']}",
        f"- 图片数：{summary['image_count']}",
        f"- 表格数：{summary['table_count']}",
        f"- 输出目录：{summary['output_dir']}",
    ]
    return "\n".join(lines)


def build_initial_session_state() -> dict[str, Any]:
    return {
        "current_mode": None,
        "current_chapter_id": None,
        "current_chunk": None,
        "last_action": None,
        "last_query": None,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "reading_history": [],
    }


def parse_book(epub_path: Path, output_root: Path, explicit_book_id: str | None) -> dict[str, Any]:
    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    if epub_path.suffix.lower() != ".epub":
        raise ValueError(f"Input file is not an .epub file: {epub_path}")

    with zipfile.ZipFile(epub_path, "r") as archive:
        opf_path = parse_container(archive)
        metadata, manifest_items, spine = parse_opf(read_zip_text(archive, opf_path))

        manifest_by_id = {item["id"]: item for item in manifest_items}
        toc_entries = parse_nav_toc(archive, opf_path, manifest_items)
        toc_source = "nav"

        if not toc_entries:
            toc_entries = parse_ncx_toc(archive, opf_path, manifest_items)
            toc_source = "ncx"

        toc_lookup = build_toc_lookup(toc_entries)

        book_id = slugify(
            explicit_book_id or metadata["identifier"] or metadata["title"],
            fallback="book",
        )

        book_dir = ensure_dir(output_root / book_id)
        chapters_dir = ensure_dir(book_dir / "chapters")
        ensure_dir(book_dir / "chunks")

        chapters: list[dict[str, Any]] = []
        skipped_pages: list[dict[str, Any]] = []

        total_words = 0
        total_chars = 0
        total_paragraphs = 0
        total_headings = 0
        total_images = 0
        total_tables = 0
        total_xhtml_files = sum(1 for item in manifest_items if is_html_manifest_item(item))

        chapter_number = 1
        for spine_index, idref in enumerate(spine, start=1):
            item = manifest_by_id.get(idref)
            if not item or not is_html_manifest_item(item):
                continue

            resolved_path = resolve_href(opf_path, item["href"])
            extracted = extract_markdown_from_html(read_zip_text(archive, resolved_path))
            body_markdown = extracted["markdown"].strip()
            stats = extracted["stats"]

            title = (
                toc_lookup.get(resolved_path)
                or extracted["title"]
                or f"Chapter {chapter_number}"
            )

            if is_probably_noise_page(
                title=title,
                text=body_markdown,
                href=item["href"],
                stats=stats,
            ):
                skipped_pages.append(
                    {
                        "spine_index": spine_index,
                        "href": item["href"],
                        "resolved_path": resolved_path,
                        "title": title,
                    }
                )
                continue

            chapter_id = f"ch{chapter_number:03d}-{slugify(title, fallback='chapter')}"
            chapter_file = chapters_dir / f"{chapter_id}.md"
            rendered_markdown = chapter_markdown(title, body_markdown)
            write_text(chapter_file, rendered_markdown)

            total_words += stats.get("word_count", len(body_markdown.split()))
            total_chars += stats.get("total_chars", len(body_markdown))
            total_paragraphs += stats.get("paragraph_count", 0)
            total_headings += stats.get("heading_count", 0)
            total_images += stats.get("image_count", 0)
            total_tables += stats.get("table_count", 0)

            source_files = [resolved_path]
            chapters.append(
                {
                    "index": chapter_number,
                    "spine_index": spine_index,
                    "chapter_id": chapter_id,
                    "chapter_title": title,
                    "source_path": resolved_path,
                    "source_files": source_files,
                    "manifest_id": item["id"],
                    "chapter_file": str(chapter_file.resolve()),
                    "char_count": stats.get("total_chars", len(body_markdown)),
                    "word_count": stats.get("word_count", len(body_markdown.split())),
                    "paragraph_count": stats.get("paragraph_count", 0),
                    "heading_count": stats.get("heading_count", 0),
                    "image_count": stats.get("image_count", 0),
                    "table_count": stats.get("table_count", 0),
                    "content_markdown": body_markdown,
                }
            )
            chapter_number += 1

        if not toc_entries:
            toc_entries = [
                {
                    "title": chapter["chapter_title"],
                    "href": chapter["source_path"],
                    "level": 1,
                    "source": "spine_fallback",
                }
                for chapter in chapters
            ]
            toc_source = "spine_fallback"

        book_markdown = "\n\n".join(
            chapter_markdown(chapter["chapter_title"], chapter["content_markdown"]).strip()
            for chapter in chapters
        ).strip()
        if book_markdown:
            book_markdown += "\n"

        complex_content = detect_complex_content(manifest_items, chapters)
        estimated_reading_time = max(1, (total_words + 249) // 250)

        metadata_payload = {
            "book_id": book_id,
            "title": metadata["title"],
            "author": metadata["author"],
            "authors": metadata["authors"],
            "language": metadata["language"],
            "languages": metadata["languages"],
            "identifier": metadata["identifier"],
            "identifiers": metadata["identifiers"],
            "publisher": metadata["publisher"],
            "published_date": metadata["published_date"],
            "description": metadata["description"],
            "source_epub": str(epub_path.resolve()),
            "opf_path": opf_path,
            "total_words": total_words,
            "total_chars": total_chars,
            "total_paragraphs": total_paragraphs,
            "total_headings": total_headings,
            "total_images": total_images,
            "total_tables": total_tables,
            "total_xhtml_files": total_xhtml_files,
            "estimated_reading_time_minutes": estimated_reading_time,
            "detected_complex_content": complex_content,
        }

        toc_payload = {
            "book_id": book_id,
            "source": toc_source,
            "entries": toc_entries,
        }

        book_payload = {
            "book_id": book_id,
            "title": metadata["title"],
            "author": metadata["author"],
            "source_epub": str(epub_path.resolve()),
            "opf_path": opf_path,
            "chapters": chapters,
        }

        manifest_payload = {
            "book_id": book_id,
            "title": metadata["title"],
            "author": metadata["author"],
            "source_epub": str(epub_path.resolve()),
            "output_dir": str(book_dir.resolve()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "chapter_count": len(chapters),
            "chunk_count": 0,
            "toc_source": toc_source,
            "skipped_pages": skipped_pages,
            "chunking": {
                "status": "not_started",
                "parameters": None,
                "generated_at": None,
            },
            "files": {
                "metadata_json": "metadata.json",
                "toc_json": "toc.json",
                "book_json": "book.json",
                "book_md": "book.md",
                "manifest_json": "manifest.json",
                "complex_content_json": "complex_content.json",
                "reading_index_json": "reading_index.json",
                "session_state_json": "session_state.json",
                "chapters_dir": "chapters",
                "chapter_files": [
                    f"chapters/{Path(chapter['chapter_file']).name}"
                    for chapter in chapters
                ],
                "chunks_dir": "chunks",
                "chunk_files": [],
            },
            "total_words": total_words,
            "total_chars": total_chars,
            "total_paragraphs": total_paragraphs,
            "total_headings": total_headings,
            "total_images": total_images,
            "total_tables": total_tables,
            "total_xhtml_files": total_xhtml_files,
            "estimated_reading_time_minutes": estimated_reading_time,
            "detected_complex_content": complex_content,
        }

        complex_content_payload = {
            "book_id": book_id,
            "title": metadata["title"],
            "author": metadata["author"],
            "source_epub": str(epub_path.resolve()),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            **complex_content,
        }

        reading_index = {
            "book_id": book_id,
            "title": metadata["title"],
            "chapters": [
                {
                    "chapter_id": chapter["chapter_id"],
                    "chapter_title": chapter["chapter_title"],
                    "word_count": chapter["word_count"],
                    "char_count": chapter["char_count"],
                    "paragraph_count": chapter["paragraph_count"],
                    "heading_count": chapter["heading_count"],
                    "image_count": chapter["image_count"],
                    "table_count": chapter["table_count"],
                    "has_images": chapter["image_count"] > 0,
                    "has_tables": chapter["table_count"] > 0,
                    "chunk_start": None,
                    "chunk_end": None,
                    "chunk_count": 0,
                    "source_files": chapter["source_files"],
                }
                for chapter in chapters
            ],
            "total_words": total_words,
            "total_images": total_images,
            "total_tables": total_tables,
            "total_xhtml_files": total_xhtml_files,
        }

        session_state = build_initial_session_state()

        write_json(book_dir / "metadata.json", metadata_payload)
        write_json(book_dir / "toc.json", toc_payload)
        write_json(book_dir / "book.json", book_payload)
        write_text(book_dir / "book.md", book_markdown)
        write_json(book_dir / "manifest.json", manifest_payload)
        write_json(book_dir / "complex_content.json", complex_content_payload)
        write_json(book_dir / "reading_index.json", reading_index)
        write_json(book_dir / "session_state.json", session_state)

        return {
            "metadata": metadata_payload,
            "toc": toc_payload,
            "book": book_payload,
            "manifest": manifest_payload,
            "complex_content": complex_content_payload,
            "reading_index": reading_index,
            "session_state": session_state,
        }


def main() -> int:
    args = parse_args()
    epub_path = Path(args.epub_path).expanduser().resolve()
    output_root = Path(args.output_dir).expanduser().resolve()

    try:
        result = parse_book(epub_path, output_root, args.book_id)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except zipfile.BadZipFile:
        print("Error: Input file is not a valid EPUB/ZIP archive", file=sys.stderr)
        return 1
    except ET.ParseError as exc:
        print(f"Error: XML parsing failed: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"Error: Required EPUB member is missing: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    summary = {
        "status": "ok",
        "book_id": result["metadata"]["book_id"],
        "title": result["metadata"]["title"],
        "author": result["metadata"]["author"],
        "chapter_count": result["manifest"]["chapter_count"],
        "chunk_count": result["manifest"]["chunk_count"],
        "image_count": result["manifest"]["total_images"],
        "table_count": result["manifest"]["total_tables"],
        "total_xhtml_files": result["manifest"]["total_xhtml_files"],
        "output_dir": result["manifest"]["output_dir"],
    }
    summary["guidance"] = build_parse_guidance(summary)
    summary["available_modes"] = [
        "overview",
        "targeted_read",
        "full_read",
        "extract",
        "complex_content",
        "batch",
    ]

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
