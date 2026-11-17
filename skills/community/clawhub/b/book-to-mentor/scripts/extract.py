#!/usr/bin/env python3
"""Extract book text with explicit fidelity, failure, and size metadata.

Usage: extract.py <path...> --mode <technical|text> [--workdir DIR]
Exit status: 0 = success, 1 = no usable sources, 2 = partial success.
Token counts are conservative heuristics for planning, never billing counts.
"""
import argparse
import codecs
import glob
import json
import math
import posixpath
import re
import sys
import tempfile
import unicodedata
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

SUPPORTED = {".pdf", ".epub", ".docx", ".txt", ".md", ".markdown", ".html", ".htm", ".rtf"}
TOKEN_ESTIMATION = {
    "method": "conservative_cjk_utf8_heuristic_v1",
    "is_estimate": True,
    "description": "2 tokens per CJK character plus ceil(other UTF-8 bytes / 3); for chunk planning, not model billing or a guaranteed upper bound.",
}
_CJK = re.compile(r"[\u2e80-\u9fff\uac00-\ud7af\uf900-\ufaff\U00020000-\U000323af]")
_WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _try_import(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False


def report_check():
    deps = {
        "docling": "pip install docling (technical PDF layout extraction)",
        "pypdf": "pip install pypdf",
        "pdfminer.high_level": "pip install pdfminer.six",
        "striprtf": "pip install striprtf",
    }
    print("=== 提取器可用性 ===")
    print("[OK] stdlib: TXT / Markdown / HTML / EPUB (OPF spine) / DOCX (paragraphs + tables)")
    for mod, install in deps.items():
        ok = _try_import(mod)
        print(f"{'[OK]' if ok else '[--]'} {mod:24} {'' if ok else install}")


def estimate_tokens(text):
    cjk = len(_CJK.findall(text))
    other = _CJK.sub("", text)
    return cjk * 2 + math.ceil(len(other.encode("utf-8")) / 3)


def _has_content(text):
    return any(not ch.isspace() and not unicodedata.category(ch).startswith("C") for ch in text)


def _decode(data, warnings, declared=False):
    # A BOM or a document declaration is evidence; never guess a legacy encoding.
    encoding = "utf-8"
    if data.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        encoding = "utf-32"
    elif data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        encoding = "utf-16"
    elif data.startswith(codecs.BOM_UTF8):
        encoding = "utf-8-sig"
    elif declared:
        header = data[:4096].decode("ascii", errors="ignore")
        match = re.search(r"<\?xml[^>]*encoding\s*=\s*['\"]([^'\"]+)", header, re.I)
        if not match:
            match = re.search(r"<meta\b[^>]*charset\s*=\s*['\"]?([\w.-]+)", header, re.I)
        if match:
            encoding = match.group(1)
    try:
        text = data.decode(encoding, errors="strict")
    except (UnicodeError, LookupError) as exc:
        raise ValueError(f"Cannot decode text as {encoding}; convert to UTF-8 or supply a correct BOM/HTML encoding declaration: {exc}") from exc
    if "\x00" in text:
        raise ValueError("NUL characters found: input may be binary or use an undeclared encoding; convert to UTF-8")
    if encoding.lower().replace("_", "-") not in ("utf-8", "utf-8-sig"):
        warnings.append(f"Decoded declared/BOM encoding {encoding}; output is UTF-8.")
    if "\ufffd" in text:
        warnings.append("Source already contains Unicode replacement characters; review source fidelity.")
    return text


class _HTMLText(HTMLParser):
    BLOCKS = {"address", "article", "aside", "blockquote", "br", "dd", "div", "dl", "dt", "figcaption", "figure", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre", "section", "table", "tr", "ul"}
    HIDDEN = {"script", "style", "head", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = []

    def handle_starttag(self, tag, attrs):
        if tag in self.HIDDEN:
            self.hidden.append(tag)
        if not self.hidden:
            if tag in self.BLOCKS:
                self.parts.append("\n")
            elif tag in {"td", "th"}:
                self.parts.append("\t")

    def handle_endtag(self, tag):
        if self.hidden:
            if tag in self.hidden:
                self.hidden = self.hidden[:self.hidden.index(tag)]
            return
        if tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def _html_text(raw):
    parser = _HTMLText()
    parser.feed(raw)
    parser.close()
    return re.sub(r"\n[\t ]*\n(?:[\t ]*\n)*", "\n\n", "".join(parser.parts)).strip()


def _archive_path(base, href):
    link = urlsplit(href)
    if link.scheme or link.netloc:
        raise ValueError(f"External EPUB resource is not supported: {href}")
    name = posixpath.normpath(posixpath.join(base, unquote(link.path)))
    if name.startswith("/") or name == ".." or name.startswith("../"):
        raise ValueError(f"Unsafe EPUB archive path: {href}")
    return name


def _epub_result(path):
    warnings = []
    parts = []
    with zipfile.ZipFile(path) as archive:
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        roots = [e for e in container.iter() if e.tag.rsplit("}", 1)[-1] == "rootfile"]
        if not roots or not roots[0].get("full-path"):
            raise ValueError("EPUB container has no package document")
        package_name = _archive_path("", roots[0].get("full-path"))
        package = ET.fromstring(archive.read(package_name))
        manifest = {}
        spine = None
        for element in package:
            local = element.tag.rsplit("}", 1)[-1]
            if local == "manifest":
                manifest = {item.get("id"): item for item in element}
            elif local == "spine":
                spine = element
        if spine is None or not list(spine):
            raise ValueError("EPUB has no usable OPF spine; refusing to guess chapter order from filenames")
        for reference in spine:
            if reference.tag.rsplit("}", 1)[-1] != "itemref":
                continue
            item_id = reference.get("idref")
            item = manifest.get(item_id)
            if item is None or not item.get("href"):
                raise ValueError(f"EPUB spine references missing manifest item: {item_id}")
            if reference.get("linear", "yes").lower() == "no":
                warnings.append(f"Excluded non-linear supplementary spine item: {item_id}")
                continue
            media = item.get("media-type", "")
            if media not in {"application/xhtml+xml", "text/html"}:
                raise ValueError(f"EPUB spine item {item_id} has unsupported media type {media!r}; review manually")
            name = _archive_path(posixpath.dirname(package_name), item.get("href"))
            raw = _decode(archive.read(name), warnings, declared=True)
            text = _html_text(raw)
            if not _has_content(text):
                warnings.append(f"EPUB spine item contains no extractable text: {name}; inspect images or scans.")
            parts.append(text)
    warnings.append("EPUB extracts text in primary OPF spine order; images, equations rendered as images, and visual layout require source review.")
    return {"text": "\n\n".join(parts), "extractor": "stdlib.epub_spine", "warnings": warnings, "pages": None}


def _docx_result(path):
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find(_WORD_NS + "body")
    if body is None:
        raise ValueError("DOCX has no document body")

    def paragraph(node):
        parts = []
        for child in node.iter():
            if child.tag == _WORD_NS + "t":
                parts.append(child.text or "")
            elif child.tag == _WORD_NS + "tab":
                parts.append("\t")
            elif child.tag in {_WORD_NS + "br", _WORD_NS + "cr"}:
                parts.append("\n")
        return "".join(parts)

    def blocks(node):
        parts = []
        for child in node:
            if child.tag == _WORD_NS + "p":
                parts.append(paragraph(child))
            elif child.tag == _WORD_NS + "tbl":
                for row in child.findall(_WORD_NS + "tr"):
                    parts.append("\t".join(" / ".join(blocks(cell)) for cell in row.findall(_WORD_NS + "tc")))
            elif child.tag in {_WORD_NS + "sdt", _WORD_NS + "sdtContent", _WORD_NS + "customXml", _WORD_NS + "ins"}:
                parts.extend(blocks(child))
        return parts

    warnings = ["DOCX preserves body paragraph/table order; headers, footers, footnotes, drawings, equations, and visual pagination are not extracted. Review the original for those elements."]
    return {"text": "\n".join(blocks(body)), "extractor": "stdlib.docx_ooxml", "warnings": warnings, "pages": None}


def _pdf_result(path, technical):
    warnings = []
    if technical:
        if _try_import("docling"):
            try:
                from docling.document_converter import DocumentConverter
                result = DocumentConverter().convert(str(path))
                text = result.document.export_to_markdown()
                if not _has_content(text):
                    raise ValueError("docling produced no usable text")
                pages = getattr(result.document, "pages", None)
                return {"text": text, "extractor": "docling", "warnings": warnings, "pages": len(pages) if pages else None}
            except Exception as exc:
                warnings.append(f"Technical extraction degraded: docling failed ({exc}); using plain PDF text. Check reading order, formulas, tables, and code.")
        else:
            warnings.append("Technical extraction degraded: docling is unavailable; using plain PDF text. Check reading order, formulas, tables, and code.")
    if _try_import("pypdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            texts = [page.extract_text() or "" for page in reader.pages]
            if not _has_content("\n".join(texts)):
                raise ValueError("PDF contains no extractable text; OCR may be required")
            empty_pages = [i + 1 for i, text in enumerate(texts) if not _has_content(text)]
            if empty_pages:
                warnings.append(f"PDF pages without extractable text: {empty_pages}; inspect for scans or missing content.")
            warnings.append("PDF text extraction does not guarantee visual reading order or formula/table fidelity.")
            return {"text": "\n".join(texts), "extractor": "pypdf", "warnings": warnings, "pages": len(reader.pages)}
        except Exception as exc:
            warnings.append(f"pypdf extraction failed: {exc}")
    if _try_import("pdfminer.high_level"):
        from pdfminer.high_level import extract_text
        from pdfminer.pdfpage import PDFPage
        text = extract_text(str(path))
        with path.open("rb") as source:
            pages = sum(1 for _ in PDFPage.get_pages(source))
        warnings.append("PDF text extraction does not guarantee visual reading order or formula/table fidelity.")
        return {"text": text, "extractor": "pdfminer.six", "warnings": warnings, "pages": pages}
    detail = "; ".join(warnings)
    raise RuntimeError(f"PDF needs a working pypdf or pdfminer.six extractor (pip install pypdf). {detail}")


def _rtf_result(path):
    if not _try_import("striprtf"):
        raise RuntimeError("RTF requires striprtf (pip install striprtf); refusing lossy regex extraction")
    from striprtf.striprtf import rtf_to_text
    data = path.read_bytes()
    match = re.search(rb"\\ansicpg(\d+)", data[:4096])
    encoding = "cp" + match.group(1).decode("ascii") if match else "cp1252"
    try:
        raw = data.decode(encoding, errors="strict")
        text = rtf_to_text(raw, encoding=encoding, errors="strict")
        # RTF represents non-BMP characters as UTF-16 surrogate pairs.
        text = text.encode("utf-16", errors="surrogatepass").decode("utf-16", errors="strict")
    except (UnicodeError, LookupError) as exc:
        raise ValueError(f"RTF decoding failed using {encoding}: {exc}") from exc
    return {"text": text, "extractor": "striprtf", "warnings": ["RTF extracts text only; inspect embedded objects and layout in the original."], "pages": None}


def _text_result(path, html=False):
    warnings = []
    text = _decode(Path(path).read_bytes(), warnings, declared=html)
    return {"text": _html_text(text) if html else text, "extractor": "stdlib.html_parser" if html else "stdlib.text", "warnings": warnings, "pages": None}


def _validate_result(result):
    if not _has_content(result["text"]):
        raise ValueError("No usable text extracted (empty/whitespace-only content or scanned pages); inspect the source or run OCR")
    if "\x00" in result["text"]:
        raise ValueError("Extracted text contains NUL characters; review source encoding")
    return result


def extract_result(path, technical=False):
    path = Path(path)
    ext = path.suffix.lower()
    if ext not in SUPPORTED:
        raise ValueError(f"不支持格式: {ext or '(none)'}")
    if ext == ".pdf":
        result = _pdf_result(path, technical)
    elif ext == ".epub":
        result = _epub_result(path)
    elif ext == ".docx":
        result = _docx_result(path)
    elif ext == ".rtf":
        result = _rtf_result(path)
    else:
        result = _text_result(path, html=ext in {".html", ".htm"})
    return _validate_result(result)


# Preserve the public text-returning helpers used by existing callers.
def extract_txt(path):
    return _validate_result(_text_result(path))["text"]


def extract_html(path):
    return _validate_result(_text_result(path, html=True))["text"]


def extract_pdf(path, technical=False):
    return _validate_result(_pdf_result(Path(path), technical))["text"]


def extract_epub(path):
    return _validate_result(_epub_result(Path(path)))["text"]


def extract_docx(path):
    return _validate_result(_docx_result(Path(path)))["text"]


def extract_rtf(path):
    return _validate_result(_rtf_result(Path(path)))["text"]


def extract(path, technical=False):
    return extract_result(path, technical)["text"]


def _within(path, directory):
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def _collect_files(inputs, workdir):
    files, problems = set(), []
    output_file = workdir / "full_text.txt"
    for value in inputs:
        path = Path(value).expanduser()
        explicit = path.exists()
        matches = [path] if explicit else [Path(item) for item in glob.glob(str(path), recursive=True)]
        if not matches:
            problems.append((str(path), "Input path or glob matched no files"))
            continue
        before = len(files)
        found_supported = False
        for match in matches:
            if match.is_file():
                resolved = match.resolve()
                if not explicit and _within(resolved, workdir):
                    continue
                if resolved == output_file:
                    problems.append((str(match), "Refusing to ingest this run's generated full_text.txt"))
                else:
                    files.add(resolved)
                    found_supported = True
            elif match.is_dir():
                directory = match.resolve()
                for candidate in directory.rglob("*"):
                    if not candidate.is_file() or candidate.suffix.lower() not in SUPPORTED:
                        continue
                    resolved = candidate.resolve()
                    if resolved == output_file or (directory != workdir and _within(resolved, workdir)):
                        continue
                    files.add(resolved)
                    found_supported = True
        if not found_supported and len(files) == before and (not explicit or any(match.is_dir() for match in matches)):
            problems.append((str(path), "Input contains no supported source files outside the output directory"))
    return sorted(files), problems


def _failed_source(path, error):
    return {"source_file": str(path), "format": Path(path).suffix.lower(), "status": "failed", "extractor": None, "warnings": [], "errors": [str(error)], "error": str(error), "characters": 0, "words": 0, "tokens": 0, "token_estimation": TOKEN_ESTIMATION, "pages": None}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="文件/目录/glob")
    ap.add_argument("--mode", choices=["technical", "text"], default="text")
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        report_check()
        return 0
    if not args.paths:
        ap.error("至少需要一个文件/目录/glob")
    workdir = Path(args.workdir).expanduser().resolve() if args.workdir else Path(tempfile.mkdtemp(prefix="book_mentor_work-")).resolve()
    reserved = {workdir / "full_text.txt", workdir / "metadata.json"}
    for value in args.paths:
        source = Path(value).expanduser()
        if source.is_file() and source.resolve() in reserved:
            print(f"[failed] Input collides with a reserved output file: {source}; choose a separate --workdir", file=sys.stderr)
            return 1
    if any(path.is_symlink() for path in reserved):
        print("[failed] Output files must not be symbolic links; choose a separate --workdir", file=sys.stderr)
        return 1
    if any(path.exists() for path in reserved):
        try:
            previous = json.loads((workdir / "metadata.json").read_text(encoding="utf-8"))
            owned = previous.get("schema_version") == 2 and previous.get("workdir") == str(workdir)
        except (OSError, ValueError, AttributeError):
            owned = False
        if not owned:
            print("[failed] Existing full_text.txt/metadata.json are not confirmed outputs of this extractor; choose an empty --workdir", file=sys.stderr)
            return 1
    workdir.mkdir(parents=True, exist_ok=True)
    files, problems = _collect_files(args.paths, workdir)
    sources = [_failed_source(path, error) for path, error in problems]
    full = []
    for path in files:
        try:
            result = extract_result(path, args.mode == "technical")
            text = result["text"]
            words = len(re.findall(r"\S+", text))
            tokens = estimate_tokens(text)
            sources.append({"source_file": str(path), "format": path.suffix.lower(), "status": "success", "extractor": result["extractor"], "warnings": result["warnings"], "errors": [], "characters": len(text), "words": words, "tokens": tokens, "token_estimation": TOKEN_ESTIMATION, "pages": result["pages"]})
            full.append(f"===== SOURCE: {json.dumps(str(path), ensure_ascii=False)} =====\n{text}")
            print(f"[ok] {path} ({len(text)} characters; ~{tokens} heuristic tokens)")
            for warning in result["warnings"]:
                print(f"[warn] {path}: {warning}", file=sys.stderr)
        except Exception as exc:
            sources.append(_failed_source(path, exc))
    successful = [source for source in sources if source["status"] == "success"]
    failed = [source for source in sources if source["status"] == "failed"]
    for source in failed:
        print(f"[failed] {source['source_file']}: {source['error']}", file=sys.stderr)
    status = "partial" if successful and failed else "success" if successful else "failed"
    known_pages = sum(source["pages"] for source in successful if source["pages"] is not None)
    meta = {
        "schema_version": 2,
        "workdir": str(workdir),
        "mode": args.mode,
        "status": status,
        "sources": sources,
        "successful_sources": len(successful),
        "failed_sources": len(failed),
        "failures": [{"source_file": source["source_file"], "error": source["error"]} for source in failed],
        "total_characters": sum(source["characters"] for source in successful),
        "total_words": sum(source["words"] for source in successful),
        "total_tokens": sum(source["tokens"] for source in successful),
        "token_estimation": TOKEN_ESTIMATION,
        "pages": known_pages if successful and all(source["pages"] is not None for source in successful) else None,
        "known_pages": known_pages,
        "warnings": [f"{source['source_file']}: {warning}" for source in sources for warning in source["warnings"]],
        "errors": [f"{source['source_file']}: {source['error']}" for source in failed],
    }
    # Remove stale output after failure; metadata is always emitted for diagnosis.
    text_path = workdir / "full_text.txt"
    if successful:
        text_path.write_text("\n\n".join(full), encoding="utf-8")
    elif text_path.exists():
        text_path.unlink()
    (workdir / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Workdir -> {workdir}\nText   -> {workdir / 'full_text.txt'}\nMeta   -> {workdir / 'metadata.json'}")
    return 2 if status == "partial" else 0 if status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
