#!/usr/bin/env python3
"""Fetch an arXiv paper and convert it to Markdown."""

from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import sys
import tarfile
import textwrap
import urllib.error
import urllib.parse
import zipfile
from dataclasses import asdict
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from arxiv_api import (  # noqa: E402
    ARXIV_ABS_URL,
    ARXIV_EPRINT_URL,
    ARXIV_HTML_URL,
    ARXIV_PDF_URL,
    PaperMetadata,
    fetch_metadata,
    normalize_identifier,
    request_bytes,
    request_text,
    safe_dir_name,
)

MAX_ARCHIVE_MEMBERS = 5000
MAX_ACCEPTED_TEX_FILES = 200
MAX_TEX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_TEX_BYTES = 25 * 1024 * 1024


def decode_bytes(payload: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return payload.decode("utf-8", errors="replace")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class HTMLToMarkdownParser(HTMLParser):
    SKIP_TAGS = {"script", "style", "svg", "noscript", "nav", "footer", "header", "form", "button"}

    def __init__(self, capture_tag: str | None = None) -> None:
        super().__init__(convert_charrefs=True)
        self.capture_tag = capture_tag
        self.capture_depth = 0
        self.in_capture = capture_tag is None
        self.skip_depth = 0
        self.parts: list[str] = []
        self.list_stack: list[dict[str, int | str]] = []
        self.preformatted = False
        self.link_stack: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = dict(attrs)

        if self.capture_tag and tag == self.capture_tag:
            self.capture_depth += 1
            self.in_capture = True

        if not self.in_capture:
            return

        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            self.parts.append(f"\n\n{'#' * level} ")
        elif tag in {"p", "section", "article", "main"}:
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "blockquote":
            self.parts.append("\n\n> ")
        elif tag == "ul":
            self.list_stack.append({"type": "ul", "counter": 0})
            self.parts.append("\n")
        elif tag == "ol":
            self.list_stack.append({"type": "ol", "counter": 0})
            self.parts.append("\n")
        elif tag == "li":
            indent = "  " * max(len(self.list_stack) - 1, 0)
            if self.list_stack and self.list_stack[-1]["type"] == "ol":
                self.list_stack[-1]["counter"] = int(self.list_stack[-1]["counter"]) + 1
                bullet = f"{self.list_stack[-1]['counter']}. "
            else:
                bullet = "- "
            self.parts.append(f"\n{indent}{bullet}")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self.preformatted:
            self.parts.append("`")
        elif tag == "pre":
            self.preformatted = True
            self.parts.append("\n\n```text\n")
        elif tag == "a":
            self.link_stack.append(attributes.get("href"))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if self.skip_depth and tag in self.SKIP_TAGS:
            self.skip_depth -= 1
            return

        if not self.in_capture or self.skip_depth:
            if self.capture_tag and tag == self.capture_tag and self.capture_depth:
                self.capture_depth -= 1
                if self.capture_depth == 0:
                    self.in_capture = False
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "section"}:
            self.parts.append("\n\n")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self.preformatted:
            self.parts.append("`")
        elif tag == "pre":
            self.preformatted = False
            self.parts.append("\n```\n")
        elif tag == "a":
            href = self.link_stack.pop() if self.link_stack else None
            if href:
                self.parts.append(f" ({href})")
        elif tag in {"ul", "ol"} and self.list_stack:
            self.list_stack.pop()
            self.parts.append("\n")

        if self.capture_tag and tag == self.capture_tag and self.capture_depth:
            self.capture_depth -= 1
            if self.capture_depth == 0:
                self.in_capture = False

    def handle_data(self, data: str) -> None:
        if not self.in_capture or self.skip_depth:
            return

        if self.preformatted:
            self.parts.append(data)
            return

        collapsed = re.sub(r"\s+", " ", data)
        if not collapsed.strip():
            if self.parts and not self.parts[-1].endswith((" ", "\n")):
                self.parts.append(" ")
            return

        self.parts.append(collapsed)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"\n +", "\n", text)
        return text.strip()


def html_to_markdown(html_text: str) -> str:
    lowered = html_text.lower()
    capture_tag = None
    if "<article" in lowered:
        capture_tag = "article"
    elif "<main" in lowered:
        capture_tag = "main"

    parser = HTMLToMarkdownParser(capture_tag=capture_tag)
    parser.feed(html_text)
    parser.close()
    return parser.markdown()


def content_looks_complete(markdown_text: str) -> bool:
    word_count = len(re.findall(r"\b\w+\b", markdown_text))
    heading_count = len(re.findall(r"^\s{0,3}#{1,6}\s", markdown_text, flags=re.MULTILINE))
    return word_count >= 250 or (word_count >= 150 and heading_count >= 3)


def fetch_html_markdown(paper_id: str, timeout: float) -> str | None:
    try:
        html_text = request_text(ARXIV_HTML_URL.format(paper_id=urllib.parse.quote(paper_id)), timeout)
    except urllib.error.HTTPError as error:
        if error.code in {403, 404}:
            return None
        raise

    markdown_text = html_to_markdown(html_text)
    if not content_looks_complete(markdown_text):
        return None
    return markdown_text


def validate_archive_member_name(name: str) -> str:
    normalized = name.replace("\\", "/").strip()
    if not normalized:
        raise RuntimeError("archive member name cannot be empty")
    if normalized.startswith("/"):
        raise RuntimeError(f"unsafe archive member path: {name}")
    if re.match(r"^[A-Za-z]:", normalized):
        raise RuntimeError(f"unsafe archive member path: {name}")

    parts = PurePosixPath(normalized).parts
    if any(part == ".." for part in parts):
        raise RuntimeError(f"unsafe archive member path: {name}")

    return normalized


def validate_member_count(count: int) -> None:
    if count > MAX_ARCHIVE_MEMBERS:
        raise RuntimeError(f"archive contains too many members (limit: {MAX_ARCHIVE_MEMBERS})")


def validate_tex_file_size(size: int, name: str) -> None:
    if size > MAX_TEX_FILE_BYTES:
        raise RuntimeError(f"archive member {name} exceeds the per-file size limit ({MAX_TEX_FILE_BYTES} bytes)")


def update_total_tex_bytes(current_total: int, added_size: int) -> int:
    new_total = current_total + added_size
    if new_total > MAX_TOTAL_TEX_BYTES:
        raise RuntimeError(f"archive exceeds the total TeX size limit ({MAX_TOTAL_TEX_BYTES} bytes)")
    return new_total


def validate_tex_file_count(current_count: int) -> None:
    if current_count >= MAX_ACCEPTED_TEX_FILES:
        raise RuntimeError(f"archive contains too many TeX files (limit: {MAX_ACCEPTED_TEX_FILES})")


def read_gzip_payload(payload: bytes, max_bytes: int) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(payload)) as handle:
        expanded = handle.read(max_bytes + 1)
    if len(expanded) > max_bytes:
        raise RuntimeError(f"gzip payload exceeds the size limit ({max_bytes} bytes)")
    return expanded


def decode_single_tex_payload(payload: bytes, name: str) -> dict[str, str]:
    validate_tex_file_size(len(payload), name)
    update_total_tex_bytes(0, len(payload))
    validate_archive_member_name(name)
    return {name: decode_bytes(payload)}


def unpack_source_files(payload: bytes) -> dict[str, str]:
    source_files = extract_archive_files(payload)
    if source_files:
        return source_files

    try:
        expanded = read_gzip_payload(payload, MAX_TOTAL_TEX_BYTES)
    except OSError:
        expanded = None

    if expanded is not None:
        source_files = extract_archive_files(expanded)
        if source_files:
            return source_files
        return decode_single_tex_payload(expanded, "source.tex")

    return decode_single_tex_payload(payload, "source.tex")


def extract_archive_files(payload: bytes) -> dict[str, str]:
    buffer = io.BytesIO(payload)
    output: dict[str, str] = {}
    inspected_members = 0
    total_tex_bytes = 0

    if zipfile.is_zipfile(buffer):
        buffer.seek(0)
        with zipfile.ZipFile(buffer) as archive:
            for info in archive.infolist():
                inspected_members += 1
                validate_member_count(inspected_members)
                if info.is_dir() or not info.filename.lower().endswith(".tex"):
                    continue

                validate_tex_file_count(len(output))
                normalized_name = validate_archive_member_name(info.filename)
                validate_tex_file_size(info.file_size, normalized_name)
                total_tex_bytes = update_total_tex_bytes(total_tex_bytes, info.file_size)
                output[normalized_name] = decode_bytes(archive.read(info))
        return output

    for mode in ("r:*", "r:gz", "r:bz2", "r:xz"):
        buffer.seek(0)
        try:
            with tarfile.open(fileobj=buffer, mode=mode) as archive:
                for member in archive:
                    inspected_members += 1
                    validate_member_count(inspected_members)
                    if not member.isfile() or not member.name.lower().endswith(".tex"):
                        continue

                    validate_tex_file_count(len(output))
                    normalized_name = validate_archive_member_name(member.name)
                    validate_tex_file_size(member.size, normalized_name)
                    file_handle = archive.extractfile(member)
                    if file_handle is None:
                        continue
                    payload_bytes = file_handle.read(MAX_TEX_FILE_BYTES + 1)
                    validate_tex_file_size(len(payload_bytes), normalized_name)
                    total_tex_bytes = update_total_tex_bytes(total_tex_bytes, len(payload_bytes))
                    output[normalized_name] = decode_bytes(payload_bytes)
                if output:
                    return output
        except tarfile.TarError:
            continue

    return output


def choose_main_tex(source_files: dict[str, str]) -> str:
    if not source_files:
        raise RuntimeError("no TeX files found in arXiv source package")

    best_name = ""
    best_score = -1
    for name, text in source_files.items():
        score = len(text)
        if "\\begin{document}" in text:
            score += 100000
        score += text.count("\\section") * 1000
        score += text.count("\\subsection") * 500
        if "\\title{" in text:
            score += 2000
        if score > best_score:
            best_name = name
            best_score = score
    return best_name


def resolve_inputs(text: str, source_files: dict[str, str], depth: int = 0) -> str:
    if depth > 2:
        return text

    lookup: dict[str, str] = {}
    for name, content in source_files.items():
        normalized = Path(name).as_posix()
        candidates = {normalized, Path(normalized).name}
        if normalized.endswith(".tex"):
            candidates.add(normalized[:-4])
            candidates.add(Path(normalized).stem)
        for candidate in candidates:
            lookup.setdefault(candidate, content)

    pattern = re.compile(r"\\(?:input|include)\{([^}]+)\}")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1).strip().replace("\\", "/")
        options = [key, f"{key}.tex", Path(key).name, f"{Path(key).name}.tex"]
        for option in options:
            if option in lookup:
                return "\n\n" + resolve_inputs(lookup[option], source_files, depth + 1) + "\n\n"
        return ""

    return pattern.sub(replace, text)


def strip_comments(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        cleaned_lines.append(re.sub(r"(?<!\\)%.*", "", line))
    return "\n".join(cleaned_lines)


def convert_math_environment(match: re.Match[str]) -> str:
    body = match.group(1).strip()
    if not body:
        return ""
    return f"\n\n```math\n{body}\n```\n\n"


def latex_to_markdown(latex_text: str) -> str:
    text = strip_comments(latex_text)

    if "\\begin{document}" in text:
        text = text.split("\\begin{document}", 1)[1]
    if "\\end{document}" in text:
        text = text.split("\\end{document}", 1)[0]

    text = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", "", text, flags=re.DOTALL)
    text = re.sub(
        r"\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}(.*?)\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}",
        convert_math_environment,
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r"\\\[(.*?)\\\]", convert_math_environment, text, flags=re.DOTALL)
    text = re.sub(r"\$\$(.*?)\$\$", convert_math_environment, text, flags=re.DOTALL)

    replacements = [
        (r"\\part\*?\{([^{}]+)\}", r"\n\n# \1\n\n"),
        (r"\\chapter\*?\{([^{}]+)\}", r"\n\n# \1\n\n"),
        (r"\\section\*?\{([^{}]+)\}", r"\n\n## \1\n\n"),
        (r"\\subsection\*?\{([^{}]+)\}", r"\n\n### \1\n\n"),
        (r"\\subsubsection\*?\{([^{}]+)\}", r"\n\n#### \1\n\n"),
        (r"\\paragraph\*?\{([^{}]+)\}", r"\n\n**\1.** "),
        (r"\\href\{([^{}]+)\}\{([^{}]+)\}", r"[\2](\1)"),
        (r"\\url\{([^{}]+)\}", r"<\1>"),
        (r"\\(?:emph|textit|textsl)\{([^{}]+)\}", r"*\1*"),
        (r"\\(?:textbf|bfseries)\{([^{}]+)\}", r"**\1**"),
        (r"\\(?:texttt|verb)\{([^{}]+)\}", r"`\1`"),
        (r"\\item\b", r"\n- "),
        (r"\\\\", "\n"),
        (r"~", " "),
    ]

    for _ in range(3):
        previous = text
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)
        if text == previous:
            break

    text = re.sub(r"\\begin\{(?:itemize|enumerate|description)\}", "", text)
    text = re.sub(r"\\end\{(?:itemize|enumerate|description)\}", "", text)
    text = re.sub(r"\\begin\{thebibliography\}", "\n\n## References\n\n", text)
    text = re.sub(r"\\end\{thebibliography\}", "", text)
    text = re.sub(r"\\(?:cite|citet|citep|eqref|autoref|ref|pageref)\{[^{}]*\}", "[ref]", text)
    text = re.sub(r"\\(?:label|footnote|thanks|index|bibliography|bibliographystyle)\{[^{}]*\}", "", text)
    text = re.sub(r"\\[A-Za-z@]+(?:\*?)?(?:\[[^\]]*\])?", "", text)
    text = text.replace("{", "").replace("}", "")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?m)^- +", "- ", text)
    text = re.sub(r"\n +", "\n", text)
    return text.strip()


def fetch_latex_markdown(paper_id: str, timeout: float) -> str | None:
    try:
        payload = request_bytes(ARXIV_EPRINT_URL.format(paper_id=urllib.parse.quote(paper_id)), timeout)
    except urllib.error.HTTPError as error:
        if error.code in {403, 404}:
            return None
        raise

    source_files = unpack_source_files(payload)
    if not source_files:
        return None

    main_tex = choose_main_tex(source_files)
    combined = resolve_inputs(source_files[main_tex], source_files)
    markdown_text = latex_to_markdown(combined)
    if not markdown_text:
        return None
    return markdown_text


def assemble_markdown(metadata: PaperMetadata, body: str, source_kind: str) -> str:
    lines = [
        f"# {metadata.title}",
        "",
        f"- arXiv ID: `{metadata.paper_id}`",
        f"- Abstract page: {ARXIV_ABS_URL.format(paper_id=metadata.paper_id)}",
        f"- PDF: {ARXIV_PDF_URL.format(paper_id=metadata.paper_id)}",
        f"- Authors: {', '.join(metadata.authors) if metadata.authors else 'Unknown'}",
        f"- Categories: {', '.join(metadata.categories) if metadata.categories else 'Unknown'}",
        f"- Published: {metadata.published or 'Unknown'}",
        f"- Updated: {metadata.updated or 'Unknown'}",
        f"- Extracted from: {source_kind}",
        "",
        "## Abstract",
        "",
        metadata.abstract or "No abstract returned by the arXiv API.",
    ]

    if body.strip():
        lines.extend(["", "## Full Text", "", body.strip()])
    elif source_kind == "abstract-only":
        lines.extend(
            [
                "",
                "## Full Text",
                "",
                "_The converter could not obtain arXiv HTML or source files. Only the abstract is available._",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def build_output_paths(output_dir: Path) -> dict[str, Path]:
    return {
        "paper_pdf": output_dir / "paper.pdf",
        "paper_md": output_dir / "paper.md",
        "metadata_json": output_dir / "metadata.json",
    }


def fetch_pdf_bytes(paper_id: str, timeout: float) -> bytes:
    pdf_url = ARXIV_PDF_URL.format(paper_id=urllib.parse.quote(paper_id))
    return request_bytes(pdf_url, timeout)


def fetch_paper_to_directory(
    paper_id: str,
    output_dir: Path,
    timeout: float = 30.0,
    extra_metadata: dict[str, str] | None = None,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = build_output_paths(output_dir)

    metadata = fetch_metadata(paper_id, timeout)
    output_paths["paper_pdf"].write_bytes(fetch_pdf_bytes(paper_id, timeout))

    body = fetch_html_markdown(paper_id, timeout)
    source_kind = "arXiv HTML"

    if body is None:
        body = fetch_latex_markdown(paper_id, timeout)
        source_kind = "arXiv source"

    if body is None:
        body = ""
        source_kind = "abstract-only"

    paper_markdown = assemble_markdown(metadata, body, source_kind)
    output_paths["paper_md"].write_text(paper_markdown, encoding="utf-8")

    metadata_payload = {
        **asdict(metadata),
        "abstract_url": ARXIV_ABS_URL.format(paper_id=paper_id),
        "pdf_url": ARXIV_PDF_URL.format(paper_id=paper_id),
        "source_kind": source_kind,
        "paper_pdf": str(output_paths["paper_pdf"]),
        "paper_md": str(output_paths["paper_md"]),
    }
    if extra_metadata:
        metadata_payload.update(extra_metadata)
    output_paths["metadata_json"].write_text(
        json.dumps(metadata_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "paper_id": paper_id,
        "output_dir": str(output_dir),
        "paper_pdf": str(output_paths["paper_pdf"]),
        "paper_md": str(output_paths["paper_md"]),
        "metadata_json": str(output_paths["metadata_json"]),
        "source_kind": source_kind,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch an arXiv paper, convert it to Markdown, and save metadata alongside it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              python arxiv_to_md.py 1706.03762
              python arxiv_to_md.py https://arxiv.org/abs/2401.00001 --output-dir ./artifacts/arxiv/2401.00001
            """
        ),
    )
    parser.add_argument("paper", help="arXiv identifier or URL")
    parser.add_argument("--output-dir", type=Path, help="directory for paper.md and metadata.json")
    parser.add_argument("--timeout", type=float, default=30.0, help="network timeout in seconds")
    args = parser.parse_args(argv)

    try:
        paper_id = normalize_identifier(args.paper)
        output_dir = args.output_dir or Path.cwd() / "artifacts" / "arxiv" / safe_dir_name(paper_id)
        result = fetch_paper_to_directory(paper_id, output_dir, timeout=args.timeout)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as error:  # pragma: no cover - surfaced in CLI output
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
