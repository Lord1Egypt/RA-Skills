#!/usr/bin/env python3
"""Extract mixed source documents for agent-readable Markdown conversion."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import html.parser
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
from typing import Iterator
from urllib.parse import unquote, urlsplit
import zipfile
from xml.etree import ElementTree


GENERATED_SUFFIXES = {".agent.md"}
SKIP_DIR_NAMES = {"extracted", "Archived", ".git", ".obsidian", "__pycache__"}
PII_TAG_PATTERN = re.compile(r"(^|\s|[,\[\]-])PII($|\s|[,\]\-])", re.IGNORECASE)
ARCHIVED_TAG_PATTERN = re.compile(r"(^|\s|[,\[\]-])archived($|\s|[,\]\-])", re.IGNORECASE)
PRIVACY_FILENAME_PATTERNS = [
    re.compile(r"(^|[-_\s])about[-_\s]?me($|[-_\s.])", re.IGNORECASE),
    # bilingual-compat: Legacy Chinese privacy filename meaning "about me."
    re.compile(r"关于我"),
    # bilingual-compat: Legacy Chinese privacy filename meaning "personal profile."
    re.compile(r"个人简介"),
    # bilingual-compat: Legacy Chinese privacy filename meaning "self introduction."
    re.compile(r"自我介绍"),
]

TEXT_EXTENSIONS = {
    ".txt",
    ".text",
    ".md",
    ".markdown",
    ".rst",
    ".csv",
    ".tsv",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".log",
}
SHELL_EXTENSIONS = {".sh", ".bash", ".zsh", ".fish", ".ksh", ".csh"}
HTML_EXTENSIONS = {".html", ".htm"}
DOCX_EXTENSIONS = {".docx"}
DOC_EXTENSIONS = {".doc"}
PPTX_EXTENSIONS = {".pptx"}
PPT_EXTENSIONS = {".ppt"}
PDF_EXTENSIONS = {".pdf"}
DEFAULT_IMAGE_WIDTH = 560
MAX_ARCHIVE_MEMBERS = 4096
MAX_ARCHIVE_MEMBER_BYTES = 128 * 1024 * 1024
MAX_ARCHIVE_TOTAL_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_ARCHIVE_COMPRESSION_RATIO = 200
MIN_COMPRESSION_RATIO_CHECK_BYTES = 1_000_000
MAX_XML_BYTES = 32 * 1024 * 1024
MAX_XML_NODES = 250_000
UNSAFE_XML_DECLARATION = re.compile(br"<!\s*(?:DOCTYPE|ENTITY)\b", re.IGNORECASE)


class ExtractionError(RuntimeError):
    """Raised when a required extraction step cannot complete safely."""


class BodyHTMLParser(html.parser.HTMLParser):
    """Small HTML-to-Markdown-ish parser for headings, lists, code, and text."""

    def __init__(self, allowed_images: set[str] | None = None) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.stack: list[str] = []
        self.link_href: str | None = None
        self.allowed_images = allowed_images

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        self.stack.append(tag)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            self.parts.append("\n" + "#" * level + " ")
        elif tag in {"p", "div", "section", "article", "tr"}:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "br":
            self.parts.append("\n")
        elif tag in {"pre", "code"} and "pre" not in self.stack[:-1]:
            self.parts.append("`")
        elif tag == "a":
            self.link_href = attrs_dict.get("href")
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src and (self.allowed_images is None or src in self.allowed_images):
                self.parts.append(f"\n![{alt}|{DEFAULT_IMAGE_WIDTH}]({src})\n")



    def handle_endtag(self, tag: str) -> None:
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "section", "article", "ul", "ol", "tr"}:
            self.parts.append("\n")
        elif tag in {"pre", "code"} and tag in self.stack:
            self.parts.append("`")
        elif tag == "a":
            self.link_href = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index] == tag:
                del self.stack[index]
                break

    def handle_data(self, data: str) -> None:
        text = re.sub(r"\s+", " ", data).strip()
        if not text:
            return
        if self.link_href:
            self.parts.append(f"[{text}]({self.link_href})")
        else:
            self.parts.append(text + " ")

    def markdown(self) -> str:
        raw = "".join(self.parts)
        return normalize_blank_lines(raw)


def normalize_blank_lines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n" if text.strip() else ""


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = value.strip("-._")
    return value or "source"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def run_command(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require_tool(name: str, install_hint: str) -> None:
    if shutil.which(name) is None:
        raise ExtractionError(f"Missing required tool `{name}`. {install_hint} / 缺少必需工具 `{name}`；请安装后重试。")


def collect_sources(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if any(part in SKIP_DIR_NAMES for part in child.parts):
                    continue
                if any(child.name.endswith(suffix) for suffix in GENERATED_SUFFIXES):
                    continue
                if child.is_file() and not child.name.startswith("."):
                    if should_skip_for_archived(child):
                        continue
                    files.append(child)
        elif path.is_file():
            if not should_skip_for_archived(path):
                files.append(path)
        else:
            raise ExtractionError(f"Input path does not exist: {path}. / 输入路径不存在：{path}。")
    return files


def read_frontmatter_only(path: Path, max_bytes: int = 65536) -> str:
    """Read only YAML frontmatter lines, stopping before document body."""
    with path.open("rb") as handle:
        first = handle.readline()
        if first not in {b"---\n", b"---\r\n"}:
            return ""
        chunks = [first]
        total = len(first)
        while total < max_bytes:
            line = handle.readline()
            if not line:
                break
            chunks.append(line)
            total += len(line)
            if line in {b"---\n", b"---\r\n"}:
                break
    text = b"".join(chunks).decode("utf-8", errors="replace")
    end = text.find("\n---", 4)
    if end == -1:
        return text[4:]
    return text[4:end]


def has_pii_tag_in_frontmatter(path: Path) -> bool:
    return has_tag_pattern_in_frontmatter(path, PII_TAG_PATTERN)


def has_archived_tag_in_frontmatter(path: Path) -> bool:
    return has_tag_pattern_in_frontmatter(path, ARCHIVED_TAG_PATTERN)


def has_tag_pattern_in_frontmatter(path: Path, pattern: re.Pattern[str]) -> bool:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return False
    frontmatter = read_frontmatter_only(path)
    if not frontmatter:
        return False
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower().startswith("tags:"):
            if pattern.search(line):
                return True
            cursor = index + 1
            while cursor < len(lines):
                next_line = lines[cursor]
                if not next_line.startswith((" ", "\t", "-")):
                    break
                if pattern.search(next_line):
                    return True
                cursor += 1
    return False


def should_skip_for_pii(source: Path) -> bool:
    if PII_TAG_PATTERN.search(source.name):
        return True
    if any(pattern.search(source.stem) for pattern in PRIVACY_FILENAME_PATTERNS):
        return True
    return has_pii_tag_in_frontmatter(source)


def should_skip_for_archived(source: Path) -> bool:
    return has_archived_tag_in_frontmatter(source)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_text_lossy(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def copy_asset(source: Path, target_dir: Path) -> str:
    target_dir.mkdir(parents=True, exist_ok=True)
    target = unique_path(target_dir / source.name)
    shutil.copy2(source, target)
    return str(target)


def extract_text_file(source: Path, normalized_dir: Path) -> dict:
    text = read_text_lossy(source)
    ext = source.suffix.lower()
    if ext in SHELL_EXTENSIONS:
        header = f"# Shell Script / Shell 脚本: {source.name}\n\n"
        if not text.startswith("#!"):
            header += "> Warning: no shebang was found in this script. / 警告：此脚本未发现 shebang。\n\n"
        text = header + "```sh\n" + text.rstrip() + "\n```\n"
    output = unique_path(normalized_dir / f"{slugify(source.stem)}.md")
    write_text(output, normalize_blank_lines(text))
    return {
        "status": "ok",
        "method": "direct_text",
        "normalized": str(output),
        "assets": [],
        "warnings": [],
    }


def safe_html_image(source: Path, reference: str) -> Path | None:
    """HTML references are data, never permission to read arbitrary local files."""
    try:
        parsed = urlsplit(html.unescape(reference))
        if parsed.scheme or parsed.netloc:
            return None
        relative = Path(unquote(parsed.path))
        if (relative.is_absolute() or not parsed.path or "\\" in parsed.path
                or any(part.startswith(".") for part in relative.parts)):
            return None
        boundary = source.parent.resolve()
        image = (boundary / relative).resolve(strict=True)
        resolved = image.relative_to(boundary)
        if any(part.startswith(".") for part in resolved.parts):
            return None
        # bilingual-compat: Chinese names for resumes, pay, banking, personal records, reviews, promotions, and transfers.
        sensitive = re.compile(r"secret|token|credential|password|payroll|salary|bank|resume|personnel|private|简历|薪资|工资|银行|个人|绩效|晋升|转账", re.I)
        if sensitive.search(relative.as_posix()) or sensitive.search(resolved.as_posix()):
            return None
        if any(PII_TAG_PATTERN.search(part) for part in (*relative.parts, *resolved.parts)):
            return None
        if image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"}:
            return None
        if should_skip_for_pii(image):
            return None
        info = image.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > 16 * 1024 * 1024:
            return None
        return image
    except (OSError, ValueError, RuntimeError):
        return None


def extract_html(source: Path, normalized_dir: Path, assets_dir: Path) -> dict:
    text = read_text_lossy(source)
    assets: list[str] = []
    allowed_images: set[str] = set()
    warnings: list[str] = []
    total_bytes = 0
    for match in re.finditer(r"<img\b[^>]*\bsrc=['\"]([^'\"]+)['\"]", text, flags=re.IGNORECASE):
        src = html.unescape(match.group(1))
        image_path = safe_html_image(source, src)
        if image_path is None or len(assets) >= 256:
            if not warnings:
                warnings.append("Skipped unapproved or oversized HTML image references / 已跳过未获准或超限的 HTML 图片引用")
            continue
        total_bytes += image_path.stat().st_size
        if total_bytes > 64 * 1024 * 1024:
            if not warnings:
                warnings.append("Skipped unapproved or oversized HTML image references / 已跳过未获准或超限的 HTML 图片引用")
            continue
        assets.append(copy_asset(image_path, assets_dir / slugify(source.stem) / "images"))
        allowed_images.add(src)
    parser = BodyHTMLParser(allowed_images=allowed_images)
    parser.feed(text)
    output = unique_path(normalized_dir / f"{slugify(source.stem)}.md")
    write_text(output, parser.markdown())

    return {
        "status": "ok",
        "method": "html_parser",
        "normalized": str(output),
        "assets": assets,
        "warnings": warnings,
    }


def xml_text(element: ElementTree.Element) -> str:
    pieces: list[str] = []
    for node in element.iter():
        if node.tag.endswith("}t") and node.text:
            pieces.append(node.text)
        elif node.tag.endswith("}tab"):
            pieces.append("\t")
        elif node.tag.endswith("}br"):
            pieces.append("\n")
    return "".join(pieces)


def normalized_archive_name(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or normalized.startswith("/")
        or re.match(r"^[A-Za-z]:", normalized)
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ExtractionError(f"Rejected unsafe archive member path: {name}. / 已拒绝不安全的归档成员路径：{name}。")
    return path


def validate_office_archive(archive: zipfile.ZipFile, source: Path) -> None:
    infos = archive.infolist()
    if len(infos) > MAX_ARCHIVE_MEMBERS:
        raise ExtractionError(
            f"Office archive has too many members ({len(infos)} > {MAX_ARCHIVE_MEMBERS}): {source}. / Office 归档成员过多：{source}。"
        )

    total_size = 0
    normalized_names: set[str] = set()
    for info in infos:
        normalized = normalized_archive_name(info.filename).as_posix()
        if normalized in normalized_names:
            raise ExtractionError(f"Office archive contains a duplicate member path: {info.filename}. / Office 归档包含重复成员路径：{info.filename}。")
        normalized_names.add(normalized)
        if info.flag_bits & 0x1:
            raise ExtractionError(f"Encrypted archive members are not supported: {info.filename}. / 不支持加密归档成员：{info.filename}。")
        mode = (info.external_attr >> 16) & 0o170000
        if mode == stat.S_IFLNK:
            raise ExtractionError(f"Archive symlink members are not supported: {info.filename}. / 不支持归档中的符号链接成员：{info.filename}。")
        if info.file_size > MAX_ARCHIVE_MEMBER_BYTES:
            raise ExtractionError(
                f"Office archive member exceeds the size limit ({info.file_size} bytes): {info.filename}. / Office 归档成员超过大小限制：{info.filename}。"
            )
        total_size += info.file_size
        if total_size > MAX_ARCHIVE_TOTAL_UNCOMPRESSED_BYTES:
            raise ExtractionError(
                "Office archive exceeds the total uncompressed size limit "
                f"({total_size} bytes): {source}. / Office 归档超过解压后总大小限制：{source}。"
            )
        if info.file_size >= MIN_COMPRESSION_RATIO_CHECK_BYTES:
            ratio = info.file_size / max(info.compress_size, 1)
            if ratio > MAX_ARCHIVE_COMPRESSION_RATIO:
                raise ExtractionError(
                    f"Office archive member exceeds the compression ratio limit ({ratio:.1f}): {info.filename}. / Office 归档成员超过压缩比限制：{info.filename}。"
                )


@contextmanager
def open_office_archive(source: Path) -> Iterator[zipfile.ZipFile]:
    try:
        with zipfile.ZipFile(source) as archive:
            validate_office_archive(archive, source)
            yield archive
    except (zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise ExtractionError(f"Invalid Office archive: {source}. / 无效的 Office 归档：{source}。") from exc


def read_archive_member(
    archive: zipfile.ZipFile,
    name: str,
    *,
    max_bytes: int = MAX_ARCHIVE_MEMBER_BYTES,
) -> bytes:
    try:
        info = archive.getinfo(name)
    except KeyError as exc:
        raise ExtractionError(f"Office archive is missing required member: {name}. / Office 归档缺少必需成员：{name}。") from exc
    if info.file_size > max_bytes:
        raise ExtractionError(f"Archive member exceeds the read limit ({info.file_size} bytes): {name}. / 归档成员超过读取限制：{name}。")
    with archive.open(info) as handle:
        data = handle.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ExtractionError(f"Archive member exceeds the read limit while expanding: {name}. / 归档成员展开时超过读取限制：{name}。")
    return data


def copy_archive_member(archive: zipfile.ZipFile, info: zipfile.ZipInfo, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    try:
        with archive.open(info) as source_handle, target.open("xb") as target_handle:
            while chunk := source_handle.read(1024 * 1024):
                written += len(chunk)
                if written > MAX_ARCHIVE_MEMBER_BYTES:
                    raise ExtractionError(f"Archive member exceeds the extraction limit: {info.filename}. / 归档成员超过抽取限制：{info.filename}。")
                target_handle.write(chunk)
    except Exception:
        target.unlink(missing_ok=True)
        raise


def parse_safe_xml(data: bytes, source: Path, member_name: str) -> ElementTree.Element:
    if len(data) > MAX_XML_BYTES:
        raise ExtractionError(f"XML member exceeds the size limit: {source}!{member_name}. / XML 成员超过大小限制：{source}!{member_name}。")
    if UNSAFE_XML_DECLARATION.search(data):
        raise ExtractionError(f"XML DTD or entity declarations are not allowed: {source}!{member_name}. / 不允许 XML DTD 或 entity 声明：{source}!{member_name}。")
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise ExtractionError(f"Invalid XML in Office archive: {source}!{member_name}. / Office 归档中的 XML 无效：{source}!{member_name}。") from exc
    node_count = sum(1 for _ in root.iter())
    if node_count > MAX_XML_NODES:
        raise ExtractionError(
            f"XML member exceeds the node limit ({node_count} > {MAX_XML_NODES}): {source}!{member_name}. / XML 成员超过节点数量限制：{source}!{member_name}。"
        )
    return root


def extract_docx(source: Path, normalized_dir: Path, assets_dir: Path) -> dict:
    output = unique_path(normalized_dir / f"{slugify(source.stem)}.md")
    media_dir = assets_dir / slugify(source.stem) / "images"
    paragraphs: list[str] = [f"# {source.stem}\n"]
    assets: list[str] = []
    warnings: list[str] = []

    with open_office_archive(source) as archive:
        for info in archive.infolist():
            name = normalized_archive_name(info.filename).as_posix()
            if name.startswith("word/media/") and not info.is_dir():
                target = unique_path(media_dir / PurePosixPath(name).name)
                copy_archive_member(archive, info, target)
                assets.append(str(target))

        document_xml = read_archive_member(archive, "word/document.xml", max_bytes=MAX_XML_BYTES)

    root = parse_safe_xml(document_xml, source, "word/document.xml")
    for paragraph in root.iter():
        if paragraph.tag.endswith("}p"):
            text = xml_text(paragraph).strip()
            if text:
                paragraphs.append(text)
        elif paragraph.tag.endswith("}tbl"):
            rows = []
            for row in paragraph.iter():
                if row.tag.endswith("}tr"):
                    cells = []
                    for cell in row.iter():
                        if cell.tag.endswith("}tc"):
                            cells.append(xml_text(cell).strip().replace("\n", " "))
                    if cells:
                        rows.append(cells)
            if rows:
                paragraphs.append(markdown_table(rows))

    if assets:
        paragraphs.append("\n## Extracted Images / 已抽取图片\n")
        paragraphs.extend(f"- `{asset}`" for asset in assets)

    write_text(output, normalize_blank_lines("\n\n".join(paragraphs)))
    return {
        "status": "ok",
        "method": "docx_zip_xml",
        "normalized": str(output),
        "assets": assets,
        "warnings": warnings,
    }


def markdown_table(rows: list[list[str]]) -> str:
    width = max(len(row) for row in rows)
    padded = [row + [""] * (width - len(row)) for row in rows]
    header = padded[0]
    separator = ["---"] * width
    body = padded[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


def extract_pptx(source: Path, normalized_dir: Path, assets_dir: Path) -> dict:
    output = unique_path(normalized_dir / f"{slugify(source.stem)}.md")
    media_dir = assets_dir / slugify(source.stem) / "images"
    assets: list[str] = []
    slides: list[tuple[int, str]] = []

    with open_office_archive(source) as archive:
        for info in archive.infolist():
            name = normalized_archive_name(info.filename).as_posix()
            if name.startswith("ppt/media/") and not info.is_dir():
                target = unique_path(media_dir / PurePosixPath(name).name)
                copy_archive_member(archive, info, target)
                assets.append(str(target))

        slide_names = sorted(
            [
                normalized_archive_name(info.filename).as_posix()
                for info in archive.infolist()
                if re.match(
                    r"ppt/slides/slide\d+\.xml$",
                    normalized_archive_name(info.filename).as_posix(),
                )
            ],
            key=lambda item: int(re.search(r"slide(\d+)\.xml", item).group(1)),  # type: ignore[union-attr]
        )
        for name in slide_names:
            slide_num = int(re.search(r"slide(\d+)\.xml", name).group(1))  # type: ignore[union-attr]
            slide_xml = read_archive_member(archive, name, max_bytes=MAX_XML_BYTES)
            root = parse_safe_xml(slide_xml, source, name)
            text = normalize_blank_lines(xml_text(root))
            slides.append((slide_num, text.strip()))

    parts = [f"# {source.stem}\n"]
    for slide_num, text in slides:
        parts.append(f"## Slide / 幻灯片 {slide_num}\n\n{text or '> No extractable text. / 没有可抽取文本。'}")
    if assets:
        parts.append("\n## Extracted Images / 已抽取图片\n")
        parts.extend(f"- `{asset}`" for asset in assets)

    write_text(output, normalize_blank_lines("\n\n".join(parts)))
    return {
        "status": "ok",
        "method": "pptx_zip_xml",
        "normalized": str(output),
        "assets": assets,
        "warnings": [],
    }


def convert_legacy_office(source: Path, normalized_dir: Path, assets_dir: Path) -> dict:
    require_tool("soffice", "Install LibreOffice, then retry legacy Office conversion. / 请安装 LibreOffice 后重试旧版 Office 转换。")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        result = run_command(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "docx" if source.suffix.lower() in DOC_EXTENSIONS else "pptx",
                "--outdir",
                str(tmp_path),
                str(source),
            ]
        )
        if result.returncode != 0:
            raise ExtractionError(f"LibreOffice conversion failed for {source}: {result.stderr.strip()} / LibreOffice 转换失败：{source}。")
        converted = next(tmp_path.glob("*.docx" if source.suffix.lower() in DOC_EXTENSIONS else "*.pptx"), None)
        if converted is None:
            raise ExtractionError(f"LibreOffice did not produce a converted file for {source}. / LibreOffice 未生成转换文件：{source}。")
        if converted.suffix.lower() == ".docx":
            return extract_docx(converted, normalized_dir, assets_dir)
        return extract_pptx(converted, normalized_dir, assets_dir)


def available_tesseract_languages() -> set[str]:
    result = run_command(["tesseract", "--list-langs"])
    if result.returncode != 0:
        raise ExtractionError(f"Unable to list Tesseract languages: {result.stderr.strip()} / 无法列出 Tesseract 语言包。")
    lines = result.stdout.splitlines()
    return {line.strip() for line in lines[1:] if line.strip()}


def require_ocr_languages(language: str) -> None:
    required = {part for part in language.split("+") if part}
    available = available_tesseract_languages()
    missing = sorted(required - available)
    if missing:
        raise ExtractionError(
            "Missing Tesseract language pack(s) / 缺少 Tesseract 语言包: "
            + ", ".join(missing)
            + ". Install them or pass --ocr-lang with installed languages. / 请安装这些语言包，或通过 --ocr-lang 指定已安装语言。"
        )


def extract_pdf(source: Path, normalized_dir: Path, assets_dir: Path, ocr_lang: str, dpi: int) -> dict:
    require_tool("gs", "Install Ghostscript to render PDF pages for OCR. / 请安装 Ghostscript 以渲染 PDF 页面供 OCR 使用。")
    require_tool("tesseract", "Install Tesseract and the required language packs. / 请安装 Tesseract 及所需语言包。")
    require_ocr_languages(ocr_lang)

    source_slug = slugify(source.stem)
    output = unique_path(normalized_dir / f"{source_slug}.md")
    page_dir = assets_dir / source_slug / "pages"
    ocr_dir = assets_dir / source_slug / "ocr"
    page_dir.mkdir(parents=True, exist_ok=True)
    ocr_dir.mkdir(parents=True, exist_ok=True)

    embedded_text = ""
    warnings: list[str] = []
    if shutil.which("pdftotext"):
        with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
            result = run_command(["pdftotext", "-layout", str(source), tmp.name])
            if result.returncode == 0:
                embedded_text = Path(tmp.name).read_text(encoding="utf-8", errors="replace")
            else:
                warnings.append(f"pdftotext failed: {result.stderr.strip()} / pdftotext 执行失败。")
    else:
        warnings.append("pdftotext was not found; embedded PDF text was not extracted. / 未找到 pdftotext；未抽取 PDF 内嵌文本。")

    render_pattern = str(page_dir / "page-%04d.png")
    render_result = run_command(
        [
            "gs",
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=png16m",
            f"-r{dpi}",
            f"-sOutputFile={render_pattern}",
            str(source),
        ]
    )
    if render_result.returncode != 0:
        raise ExtractionError(f"Ghostscript rendering failed for {source}: {render_result.stderr.strip()} / Ghostscript 渲染失败：{source}。")

    page_images = sorted(page_dir.glob("page-*.png"))
    if not page_images:
        raise ExtractionError(f"Ghostscript produced no page images for {source}. / Ghostscript 未生成页面图片：{source}。")

    ocr_sections: list[str] = []
    assets = [str(path) for path in page_images]
    for page_image in page_images:
        page_match = re.search(r"page-(\d+)\.png$", page_image.name)
        page_num = int(page_match.group(1)) if page_match else len(ocr_sections) + 1
        out_base = ocr_dir / page_image.stem
        result = run_command(["tesseract", str(page_image), str(out_base), "-l", ocr_lang])
        ocr_text_path = out_base.with_suffix(".txt")
        if result.returncode != 0 or not ocr_text_path.exists():
            warnings.append(f"OCR failed for {page_image.name}: {result.stderr.strip()} / OCR 失败：{page_image.name}。")
            continue
        ocr_text = normalize_blank_lines(ocr_text_path.read_text(encoding="utf-8", errors="replace"))
        assets.append(str(ocr_text_path))
        ocr_sections.append(
            f"## OCR Page / OCR 页面 {page_num}\n\n"
            f"{ocr_text if ocr_text.strip() else '> No OCR text detected. / 未检测到 OCR 文本。'}"
        )

    parts = [f"# {source.stem}\n"]
    if embedded_text.strip():
        parts.append("## Embedded Text / 内嵌文本\n\n" + normalize_blank_lines(embedded_text))
    parts.append("## OCR Text / OCR 文本\n\n" + "\n\n".join(ocr_sections))
    write_text(output, normalize_blank_lines("\n\n".join(parts)))

    return {
        "status": "ok",
        "method": "pdf_embedded_text_gs_tesseract",
        "normalized": str(output),
        "assets": assets,
        "warnings": warnings,
    }


def extract_one(source: Path, normalized_dir: Path, assets_dir: Path, ocr_lang: str, dpi: int) -> dict:
    ext = source.suffix.lower()
    if ext in TEXT_EXTENSIONS or ext in SHELL_EXTENSIONS:
        return extract_text_file(source, normalized_dir)
    if ext in HTML_EXTENSIONS:
        return extract_html(source, normalized_dir, assets_dir)
    if ext in DOCX_EXTENSIONS:
        return extract_docx(source, normalized_dir, assets_dir)
    if ext in DOC_EXTENSIONS or ext in PPT_EXTENSIONS:
        return convert_legacy_office(source, normalized_dir, assets_dir)
    if ext in PPTX_EXTENSIONS:
        return extract_pptx(source, normalized_dir, assets_dir)
    if ext in PDF_EXTENSIONS:
        return extract_pdf(source, normalized_dir, assets_dir, ocr_lang, dpi)
    raise ExtractionError(f"Unsupported file type `{ext}` for {source}. / 不支持 {source} 的文件类型 `{ext}`。")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract mixed documents into normalized text, assets, a manifest, and warnings. / 将混合文档抽取为规范化文本、资产、manifest 和警告。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("inputs", nargs="+", help="Input files or directories. / 输入文件或目录。")
    parser.add_argument("-o", "--output", default="extracted", help="Extraction output directory. / 抽取输出目录。")
    parser.add_argument("--ocr-lang", default="chi_sim+eng", help="Tesseract OCR language expression. / Tesseract OCR 语言表达式。")
    parser.add_argument("--pdf-dpi", type=int, default=200, help="Ghostscript render DPI for PDF OCR. / PDF OCR 的 Ghostscript 渲染 DPI。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output).resolve()
    normalized_dir = output_dir / "normalized"
    assets_dir = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "ocr_lang": args.ocr_lang,
        "pdf_dpi": args.pdf_dpi,
        "sources": [],
    }
    all_warnings: list[str] = []

    try:
        sources = collect_sources([Path(item).expanduser().resolve() for item in args.inputs])
    except ExtractionError as exc:
        print(f"ERROR / 错误: {exc}", file=sys.stderr)
        return 2

    hard_failure = False
    for source in sources:
        entry = {"source": str(source)}
        if should_skip_for_pii(source):
            message = "Skipped because the source filename or frontmatter tags mark it as PII. / 因源文件名或 frontmatter 标签标记为 PII，已跳过。"
            entry.update(
                {
                    "status": "skipped_pii",
                    "method": "pii_guard",
                    "normalized": None,
                    "assets": [],
                    "warnings": [message],
                }
            )
            all_warnings.append(f"- {source}: {message}")
            manifest["sources"].append(entry)  # type: ignore[index]
            continue
        try:
            result = extract_one(source, normalized_dir, assets_dir, args.ocr_lang, args.pdf_dpi)
            entry.update(result)
            for warning in result.get("warnings", []):
                all_warnings.append(f"- {source}: {warning}")
        except ExtractionError as exc:
            hard_failure = True
            message = str(exc)
            entry.update({"status": "error", "method": None, "normalized": None, "assets": [], "warnings": [message]})
            all_warnings.append(f"- {source}: {message}")
        manifest["sources"].append(entry)  # type: ignore[index]

    write_text(output_dir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    warnings_text = "# Extraction Warnings / 抽取警告\n\n"
    warnings_text += "\n".join(all_warnings) if all_warnings else "No warnings. / 无警告。\n"
    write_text(output_dir / "warnings.md", warnings_text + "\n")

    if hard_failure:
        print(
            textwrap.dedent(
                f"""\
                Extraction completed with errors. / 抽取完成，但存在错误。
                See / 查看: {output_dir / "manifest.json"}
                See / 查看: {output_dir / "warnings.md"}
                """
            ).strip(),
            file=sys.stderr,
        )
        return 1

    print(f"Extraction complete: {output_dir} / 抽取完成：{output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
