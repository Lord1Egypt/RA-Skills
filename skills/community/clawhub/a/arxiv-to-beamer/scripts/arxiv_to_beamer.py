#!/usr/bin/env python3
"""Download arxiv source, ask an OpenRouter model for a Beamer presentation,
and pack the result into an Overleaf-uploadable zip.

If arxiv has no TeX source (PDF-only), fall back to MinerU's PDF -> Markdown
API and feed the parsed markdown to the model instead.

Env:
    OPENROUTER_API_KEY (required)
    MINERU_API_TOKEN   (optional; required for PDF-only fallback)
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ARXIV_ID_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf|e-print)/)?"
    r"(?P<id>(?:\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7}))"
    r"(?P<v>v\d+)?",
    re.IGNORECASE,
)

USER_AGENT = "Mozilla/5.0 (compatible; arxiv-beamer-skill/1.0; +https://arxiv.org)"

DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"
DEFAULT_MAX_CHARS = 200_000

MINERU_API_BASE = "https://mineru.net/api/v4"
MINERU_DEFAULT_TIMEOUT = 900  # seconds to wait for parsing
MINERU_POLL_INTERVAL = 8


def parse_arxiv_id(raw: str) -> str:
    raw = raw.strip().rstrip("/")
    raw = re.sub(r"\.pdf$", "", raw, flags=re.IGNORECASE)
    m = ARXIV_ID_RE.search(raw)
    if not m:
        raise SystemExit(f"ERROR: could not parse arxiv id from: {raw}")
    return m.group("id") + (m.group("v") or "")


def http_get(url: str, timeout: int = 60) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def download_source(arxiv_id: str, work_dir: Path) -> Path | None:
    """Return the directory of extracted TeX source, or None if PDF-only."""
    src_dir = work_dir / "source"
    src_dir.mkdir(parents=True, exist_ok=True)
    archive = work_dir / "archive.bin"

    url = f"https://arxiv.org/e-print/{arxiv_id}"
    print(f"GET {url}", file=sys.stderr)
    try:
        data, _ = http_get(url, timeout=120)
    except urllib.error.HTTPError as e:
        print(f"HTTP error from arxiv: {e.code} {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        raise SystemExit(f"ERROR: network failure contacting arxiv: {e.reason}")

    if data.startswith(b"%PDF"):
        return None

    archive.write_bytes(data)

    extracted = False
    try:
        with tarfile.open(archive, "r:*") as tf:
            tf.extractall(src_dir)
            extracted = True
    except tarfile.ReadError:
        pass

    if not extracted:
        try:
            with gzip.open(archive, "rb") as gf:
                content = gf.read()
            if b"\\documentclass" in content or b"\\begin{document}" in content:
                (src_dir / "main.tex").write_bytes(content)
                extracted = True
        except OSError:
            pass

    if not extracted:
        # Maybe a raw .tex
        if b"\\documentclass" in data or b"\\begin{document}" in data:
            (src_dir / "main.tex").write_bytes(data)
            extracted = True

    if not extracted:
        return None

    if not list(src_dir.rglob("*.tex")):
        return None
    return src_dir


def parse_pdf_with_mineru(
    arxiv_id: str,
    work_dir: Path,
    token: str,
    timeout: int = MINERU_DEFAULT_TIMEOUT,
) -> tuple[str, Path] | None:
    """Submit the arxiv PDF URL to MinerU and return (markdown_text, extracted_dir).

    Returns None on any failure. The returned markdown is concatenated from
    every .md file in the result archive, each prefixed with a FILE marker.
    """
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    submit_body = json.dumps(
        {
            "url": pdf_url,
            "is_ocr": False,
            "enable_formula": True,
            "enable_table": True,
            "language": "en",
            "model_version": "v2",
        }
    ).encode("utf-8")

    submit_req = urllib.request.Request(
        f"{MINERU_API_BASE}/extract/task",
        data=submit_body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(submit_req, timeout=60) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        print(f"MinerU submit HTTP {e.code}: {detail}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"MinerU network error: {e.reason}", file=sys.stderr)
        return None

    if payload.get("code") not in (0, "0", 200):
        print(f"MinerU submit rejected: {payload}", file=sys.stderr)
        return None

    task_id = (payload.get("data") or {}).get("task_id")
    if not task_id:
        print(f"MinerU response missing task_id: {payload}", file=sys.stderr)
        return None
    print(f"    submitted MinerU task {task_id}; polling ...", file=sys.stderr)

    deadline = time.time() + timeout
    zip_url: str | None = None
    last_state = ""
    while time.time() < deadline:
        poll_req = urllib.request.Request(
            f"{MINERU_API_BASE}/extract/task/{task_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(poll_req, timeout=60) as r:
                poll_payload = json.loads(r.read())
        except urllib.error.HTTPError as e:
            print(f"MinerU poll HTTP {e.code}; retrying ...", file=sys.stderr)
            time.sleep(MINERU_POLL_INTERVAL)
            continue
        except urllib.error.URLError as e:
            print(f"MinerU poll network error: {e.reason}; retrying ...", file=sys.stderr)
            time.sleep(MINERU_POLL_INTERVAL)
            continue

        data = poll_payload.get("data") or {}
        state = str(data.get("state", "")).lower()
        if state != last_state:
            print(f"    MinerU state: {state or '(unknown)'}", file=sys.stderr)
            last_state = state
        if state == "done":
            zip_url = data.get("full_zip_url") or data.get("zip_url")
            break
        if state in {"failed", "fail", "error"}:
            err = data.get("err_msg") or poll_payload
            print(f"MinerU task failed: {err}", file=sys.stderr)
            return None
        time.sleep(MINERU_POLL_INTERVAL)

    if not zip_url:
        print(f"MinerU task did not finish within {timeout}s", file=sys.stderr)
        return None

    print(f"    downloading MinerU result archive ...", file=sys.stderr)
    try:
        zip_bytes, _ = http_get(zip_url, timeout=180)
    except urllib.error.URLError as e:
        print(f"MinerU result download failed: {e}", file=sys.stderr)
        return None

    extract_dir = work_dir / "mineru_out"
    extract_dir.mkdir(parents=True, exist_ok=True)
    zip_path = work_dir / "mineru.zip"
    zip_path.write_bytes(zip_bytes)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)
    except zipfile.BadZipFile:
        print("MinerU result is not a valid zip", file=sys.stderr)
        return None

    md_files = sorted(extract_dir.rglob("*.md"))
    if not md_files:
        print("MinerU result contains no markdown", file=sys.stderr)
        return None

    parts: list[str] = []
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = md.relative_to(extract_dir)
        parts.append(f"\n\n===== FILE: {rel} =====\n{text}\n")
    return "".join(parts), extract_dir


def _file_priority(p: Path) -> tuple[int, str]:
    name = p.name.lower()
    if name in {"main.tex", "paper.tex", "manuscript.tex", "ms.tex", "root.tex"}:
        return (0, name)
    if "main" in name or "paper" in name:
        return (1, name)
    return (2, name)


def collect_source(src_dir: Path, max_chars: int) -> str:
    tex_files = sorted(src_dir.rglob("*.tex"), key=_file_priority)
    bib_files = sorted(src_dir.rglob("*.bib"))
    parts: list[str] = []
    total = 0
    for f in tex_files + bib_files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = f.relative_to(src_dir)
        header = f"\n\n===== FILE: {rel} =====\n"
        chunk = header + text + "\n"
        if total + len(chunk) > max_chars:
            remaining = max_chars - total
            if remaining > len(header) + 200:
                parts.append(chunk[:remaining] + "\n[... truncated ...]\n")
            break
        parts.append(chunk)
        total += len(chunk)
    return "".join(parts)


def call_openrouter(prompt: str, model: str, api_key: str) -> str:
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an academic presentation assistant. "
                        "Given a paper's LaTeX source, produce a complete, "
                        "compilable Beamer presentation that introduces the work."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dirtycomputer/beamer",
            "X-Title": "arxiv-to-beamer skill",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise SystemExit(f"OpenRouter HTTP {e.code}: {detail}")
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise SystemExit(f"Unexpected OpenRouter response: {payload}")


FILE_BLOCK_RE = re.compile(
    r"={3,}\s*FILE:\s*(?P<name>[^\n=]+?)\s*={3,}\s*\n(?P<body>.*?)(?=\n={3,}\s*FILE:|\Z)",
    re.DOTALL,
)
FENCED_NAMED_RE = re.compile(
    r"```(?:latex|tex|bibtex|bib)?\s*(?:filename=|file=|:)?\s*"
    r"(?P<name>[\w./\-]+\.(?:tex|bib|sty|cls|bst))\s*\n"
    r"(?P<body>.*?)```",
    re.DOTALL | re.IGNORECASE,
)
FENCED_PLAIN_RE = re.compile(
    r"```(?:latex|tex)?\s*\n(?P<body>.*?)```",
    re.DOTALL | re.IGNORECASE,
)


def parse_files_from_response(text: str) -> dict[str, str]:
    files: dict[str, str] = {}

    for m in FILE_BLOCK_RE.finditer(text):
        name = m.group("name").strip().strip("`'\"")
        body = m.group("body").strip("\n")
        # Strip optional fenced code wrappers inside the block.
        inner = re.match(
            r"```[\w]*\s*\n(?P<b>.*?)```\s*\Z", body, re.DOTALL
        )
        if inner:
            body = inner.group("b").strip("\n")
        files[name] = body + "\n"
    if files:
        return files

    for m in FENCED_NAMED_RE.finditer(text):
        files[m.group("name").strip()] = m.group("body").strip("\n") + "\n"
    if files:
        return files

    m = FENCED_PLAIN_RE.search(text)
    if m:
        return {"main.tex": m.group("body").strip("\n") + "\n"}

    return {"main.tex": text.strip() + "\n"}


def make_overleaf_zip(files: dict[str, str], zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            safe = name.replace("\\", "/").lstrip("/")
            if ".." in Path(safe).parts:
                continue
            zf.writestr(safe, content)


def build_prompt(
    arxiv_id: str, language: str, source_text: str, source_kind: str = "latex"
) -> str:
    if source_kind == "markdown":
        source_label = (
            "由 MinerU 从 PDF 解析出的 Markdown 内容（公式与表格已尽量保留，"
            "可能含有少量 OCR 噪声，请理解性地阅读）"
        )
        section_banner = "ARXIV PDF MARKDOWN"
    else:
        source_label = "LaTeX 源文件内容"
        section_banner = "ARXIV SOURCE"
    return (
        f"以下是 arxiv 论文 {arxiv_id} 的{source_label}，"
        f"帮我做一个 beamer 来介绍一下这个研究工作。\n\n"
        f"要求：\n"
        f"1. 使用 {language} 撰写所有 slides 内容。\n"
        f"2. 文档结构包含：标题页、目录(\\tableofcontents)、研究背景与动机、"
        f"   相关工作、方法/模型、实验设置与结果、讨论与结论、致谢/Q&A。\n"
        f"3. 选择简洁现代的 beamer theme（如 metropolis 或 Madrid）。\n"
        f"4. 若使用中文，请用 \\documentclass{{ctexbeamer}} 或加载 ctex/xeCJK，"
        f"   并在注释中提示使用 XeLaTeX 编译。\n"
        f"5. 输出必须是完整、可直接编译的 LaTeX 项目。\n"
        f"6. 输出格式（重要）：每个文件用如下分隔标记包裹，便于自动解析；"
        f"   不要再额外用 markdown 代码块包裹文件内容：\n"
        f"   ===== FILE: main.tex =====\n"
        f"   <文件内容>\n"
        f"   ===== FILE: references.bib =====\n"
        f"   <文件内容>\n"
        f"7. 至少要输出 main.tex；如果引用了文献，再附带 references.bib。\n\n"
        f"================ {section_banner} BEGIN ================\n"
        f"{source_text}\n"
        f"================ {section_banner} END ================\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("arxiv", help="arxiv id (e.g. 2603.19835) or full URL")
    ap.add_argument("--output", "-o", default=None, help="output zip path")
    ap.add_argument("--model", "-m", default=DEFAULT_MODEL, help="OpenRouter model id")
    ap.add_argument("--language", "-l", default="中文", help="slide language hint")
    ap.add_argument("--keep-source", action="store_true",
                    help="also copy the extracted arxiv source / MinerU output "
                         "next to the zip")
    ap.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS,
                    help="max chars of source to send to the model")
    ap.add_argument("--mineru-timeout", type=int, default=MINERU_DEFAULT_TIMEOUT,
                    help="seconds to wait for MinerU PDF parsing (PDF-only fallback)")
    ap.add_argument("--no-mineru-fallback", action="store_true",
                    help="do not fall back to MinerU when arxiv has no TeX source")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY env var is not set.", file=sys.stderr)
        return 1

    arxiv_id = parse_arxiv_id(args.arxiv)
    safe_id = arxiv_id.replace("/", "_")
    out_zip = Path(args.output or f"{safe_id}-beamer.zip").resolve()

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        print(f"==> Fetching arxiv source for {arxiv_id} ...")
        src_dir = download_source(arxiv_id, work)

        source_text: str
        source_kind: str
        if src_dir is not None:
            n_tex = sum(1 for _ in src_dir.rglob("*.tex"))
            n_bib = sum(1 for _ in src_dir.rglob("*.bib"))
            print(f"    found {n_tex} .tex file(s), {n_bib} .bib file(s)")
            if args.keep_source:
                keep_dir = out_zip.parent / f"{safe_id}-source"
                if keep_dir.exists():
                    shutil.rmtree(keep_dir)
                shutil.copytree(src_dir, keep_dir)
                print(f"    copied source -> {keep_dir}")
            print(f"==> Building prompt from LaTeX source (cap {args.max_chars} chars) ...")
            source_text = collect_source(src_dir, args.max_chars)
            source_kind = "latex"
        else:
            print("    no TeX source on arxiv (PDF-only or withdrawn).")
            if args.no_mineru_fallback:
                print("ERROR: --no-mineru-fallback set; aborting.", file=sys.stderr)
                return 2
            mineru_token = os.environ.get("MINERU_API_TOKEN")
            if not mineru_token:
                print("ERROR: arxiv has no TeX source and MINERU_API_TOKEN is "
                      "not set; cannot fall back to PDF parsing.", file=sys.stderr)
                return 2
            print(f"==> Falling back to MinerU PDF parsing for {arxiv_id} ...")
            result = parse_pdf_with_mineru(
                arxiv_id, work, mineru_token, timeout=args.mineru_timeout
            )
            if result is None:
                print("ERROR: MinerU PDF parsing failed.", file=sys.stderr)
                return 2
            md_text, mineru_dir = result
            md_count = sum(1 for _ in mineru_dir.rglob("*.md"))
            print(f"    MinerU returned {md_count} markdown file(s), "
                  f"{len(md_text)} chars total")
            if args.keep_source:
                keep_dir = out_zip.parent / f"{safe_id}-mineru"
                if keep_dir.exists():
                    shutil.rmtree(keep_dir)
                shutil.copytree(mineru_dir, keep_dir)
                print(f"    copied MinerU output -> {keep_dir}")
            if len(md_text) > args.max_chars:
                md_text = md_text[: args.max_chars] + "\n[... truncated ...]\n"
            print(f"==> Building prompt from MinerU markdown (cap {args.max_chars} chars) ...")
            source_text = md_text
            source_kind = "markdown"

        prompt = build_prompt(arxiv_id, args.language, source_text, source_kind)

        print(f"==> Calling OpenRouter (model={args.model}) ...")
        response = call_openrouter(prompt, args.model, api_key)

        files = parse_files_from_response(response)
        print(f"==> Parsed {len(files)} file(s) from model response: "
              f"{', '.join(files)}")

        make_overleaf_zip(files, out_zip)

    print(f"==> Done.")
    print(f"    Overleaf project: {out_zip}")
    print(f"    Upload via Overleaf -> New Project -> Upload Project.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
