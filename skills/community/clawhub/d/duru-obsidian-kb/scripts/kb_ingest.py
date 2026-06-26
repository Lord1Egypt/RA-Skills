#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from kb_env import (
    OPENCLAW_WORKSPACE,
    PROMPT_SHIELD_SCRIPT,
    KB_VENV_PYTHON,
    USER_AGENT,
    MIN_CONTENT_LENGTH,
    MAX_PREVIEW_LENGTH,
    MAX_SEGMENTS,
)
from urllib.parse import urlparse
from urllib.request import Request, urlopen

WORKSPACE = OPENCLAW_WORKSPACE
PSL_SCRIPT = PROMPT_SHIELD_SCRIPT
VENDOR_ROOT = WORKSPACE / "skills/vendor-anthropic"
PDF_SKILL_DIR = VENDOR_ROOT / "pdf"
XLSX_SKILL_DIR = VENDOR_ROOT / "xlsx"


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(path: Path, manifest):
    manifest["updated_at"] = now_iso()
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80] or "item"


def unique_slug(source: str) -> str:
    base = slugify(source)
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:8]
    return f"{base}-{digest}"


def infer_type(source: str, explicit: Optional[str]):
    if explicit:
        return explicit
    lower = source.lower()
    if source.startswith("http://") or source.startswith("https://"):
        host = urlparse(source).netloc.lower()
        if "github.com" in host:
            return "repo"
        if lower.endswith(".pdf") or "arxiv" in host:
            return "paper"
        return "article"
    if lower.endswith((".pdf",)):
        return "paper"
    if lower.endswith((".xlsx", ".xlsm", ".csv", ".tsv")):
        return "spreadsheet"
    return "file"


def raw_subdir(source_type: str):
    return {
        "article": "raw/articles",
        "paper": "raw/papers",
        "repo": "raw/repos",
        "spreadsheet": "raw/files",
        "file": "raw/files",
    }.get(source_type, "raw/files")


def title_from_source(source: str):
    if source.startswith("http://") or source.startswith("https://"):
        parsed = urlparse(source)
        tail = parsed.path.rstrip("/").split("/")[-1] or parsed.netloc
        return tail.replace("-", " ").replace("_", " ").strip() or source
    return Path(source).stem or Path(source).name


def fetch_url(source: str) -> str:
    request = Request(source, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def download_binary(source: str) -> bytes:
    request = Request(source, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return response.read()


def extract_title(html: str, fallback: str) -> str:
    og = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if og:
        return og.group(1).strip() or fallback
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not match:
        return fallback
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return title or fallback


def strip_blocks(html: str, tag: str) -> str:
    pattern = rf"<{tag}\b[^<]*(?:(?!</{tag}>)<[^<]*)*</{tag}>"
    return re.sub(pattern, " ", html, flags=re.IGNORECASE | re.DOTALL)


def extract_main_html(html: str) -> str:
    candidates = [
        r"<(article|main)[^>]*>(.*?)</\1>",
        r"<div[^>]+class=[\"'][^\"']*(post-content|entry-content|article-content|content|markdown-body|post|entry|article)[^\"']*[\"'][^>]*>(.*?)</div>",
        r"<section[^>]+class=[\"'][^\"']*(content|article|post)[^\"']*[\"'][^>]*>(.*?)</section>",
    ]
    best = html
    best_len = 0
    for pattern in candidates:
        for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
            candidate = match.group(match.lastindex)
            length = len(candidate)
            if length > best_len:
                best = candidate
                best_len = length
    return best


def html_to_markdown(html: str) -> str:
    html = strip_blocks(html, "script")
    html = strip_blocks(html, "style")
    html = strip_blocks(html, "svg")
    html = re.sub(r"<(nav|footer|header|aside|noscript)[^>]*>.*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.DOTALL)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</p>", "\n\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<p[^>]*>", "", html, flags=re.IGNORECASE)
    for level in [1, 2, 3, 4]:
        html = re.sub(rf"<h{level}[^>]*>(.*?)</h{level}>", rf"{'#' * level} \1\n\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<pre[^>]*>(.*?)</pre>", r"```\n\1\n```\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<a [^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", r"[\2](\1)", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"</?(article|main|section|div|span|body|html)[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"&lt;", "<", html)
    html = re.sub(r"&gt;", ">", html)
    lines = [re.sub(r"\s+", " ", line).strip() for line in html.splitlines()]
    return "\n\n".join(line for line in lines if line).strip()


def split_segments(markdown: str):
    chunks = re.split(r"\n\s*\n", markdown)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def link_density(segment: str) -> float:
    if not segment:
        return 0.0
    links = len(re.findall(r"\[[^\]]*\]\([^\)]+\)", segment))
    words = max(1, len(re.findall(r"\w+", segment)))
    return links / words


def segment_noise_score(segment: str) -> int:
    score = 0
    lower = segment.lower()
    if len(segment) < 40:
        score += 2
    if re.search(r"^(home|about|contact|login|signup|privacy|terms|bio|featured talks)$", lower):
        score += 4
    if lower.count("[") >= 3 and lower.count("](") >= 3:
        score += 2
    if link_density(segment) > 0.12:
        score += 3
    if re.search(r"cookie|subscribe|newsletter|copyright|all rights reserved", lower):
        score += 3
    if re.search(r"share on|follow us|twitter|facebook|linkedin|instagram", lower):
        score += 2
    if re.search(r"menu|navigation|sidebar|table of contents", lower):
        score += 2
    return score


def clean_markdown(markdown: str):
    segments = split_segments(markdown)
    kept = []
    suspicious = []
    for segment in segments:
        score = segment_noise_score(segment)
        if score >= 5:
            suspicious.append({"reason": "noise", "text": segment[:500]})
        else:
            kept.append(segment)
    cleaned = "\n\n".join(kept).strip()
    return cleaned, suspicious


def run_prompt_shield(text: str):
    if not PSL_SCRIPT.exists():
        return {"available": False, "action": "allow", "severity": "SAFE", "reasons": ["psl script missing"], "degraded": False}
    proc = subprocess.run(["bash", str(PSL_SCRIPT)], input=text, text=True, capture_output=True, check=False)
    output = (proc.stdout or proc.stderr or "").strip()
    if not output:
        return {"available": True, "action": "warn", "severity": "UNKNOWN", "reasons": ["empty PSL output"], "degraded": True}
    try:
        data = json.loads(output.splitlines()[-1])
        reasons = data.get("reasons", [])
        degraded = "rate_limit_exceeded" in reasons
        if degraded:
            filtered = [reason for reason in reasons if reason != "rate_limit_exceeded"]
            data["reasons"] = filtered or ["rate_limit_exceeded"]
            if data.get("severity") == "CRITICAL":
                data["severity"] = "UNKNOWN"
            if data.get("action") == "block":
                data["action"] = "warn"
        data["degraded"] = degraded
        data["available"] = True
        return data
    except Exception:
        return {"available": True, "action": "warn", "severity": "UNKNOWN", "reasons": [output[:300]], "degraded": True}


def detect_suspicious_segments(cleaned_markdown: str):
    segments = split_segments(cleaned_markdown)
    flagged = []
    for segment in segments:
        if len(flagged) >= MAX_SEGMENTS:
            break
        reasons = []
        score = segment_noise_score(segment)
        lower = segment.lower()
        if score >= 5:
            reasons.append("noise")
        if re.search(r"ignore previous instructions|system prompt|developer message|tool call|jailbreak", lower):
            reasons.append("prompt-like")
        if re.search(r"order of the unicorn|unicorn magic|cryptic scar|destiny", lower):
            reasons.append("fantasy/anomalous")
        if link_density(segment) > 0.12:
            reasons.append("link-heavy")
        if reasons:
            flagged.append({
                "text": segment[:500],
                "severity": "MEDIUM" if "prompt-like" in reasons else "LOW",
                "action": "warn",
                "reasons": reasons,
            })
    return flagged


def read_text_file(path: Optional[Path]) -> str:
    if not path:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def vendor_status():
    return {
        "pdf_skill_present": PDF_SKILL_DIR.exists(),
        "xlsx_skill_present": XLSX_SKILL_DIR.exists(),
        "python_pandas": import_check("pandas"),
        "python_openpyxl": import_check("openpyxl"),
        "python_pypdf": import_check("pypdf") or import_check("PyPDF2"),
        "python_pdfplumber": import_check("pdfplumber"),
    }


def kb_python() -> str:
    return str(KB_VENV_PYTHON) if KB_VENV_PYTHON.exists() else "python3"


def import_check(module_name: str) -> bool:
    proc = subprocess.run([kb_python(), "-c", f"import importlib.util; print(importlib.util.find_spec('{module_name}') is not None)"], capture_output=True, text=True, check=False)
    return proc.stdout.strip() == "True"


def render_article_markdown(title: str, slug: str, source: str, tags, status: str, extraction: str, psl_result, suspicious_segments, cleaned_markdown: str):
    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"slug: {slug}",
        "source_type: article",
        f"source_url: {source}",
        f"ingested_at: {now_iso()}",
        f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
        f"status: {status}",
        f"extraction: {extraction}",
        f"prompt_shield_action: {psl_result.get('action', 'allow')}",
        f"prompt_shield_severity: {psl_result.get('severity', 'SAFE')}",
        "---",
        "",
        f"# {title}",
        "",
        "## Source",
        "",
        source,
        "",
    ]
    if suspicious_segments:
        lines.extend(["## Suspicious segments", ""])
        for item in suspicious_segments[:MAX_SEGMENTS]:
            lines.append(f"- reason/action={item.get('reason', item.get('action', 'flag'))} severity={item.get('severity', 'n/a')}: {item.get('text', '')}")
        lines.append("")
    lines.extend(["## Extracted body", "", cleaned_markdown, ""])
    return "\n".join(lines)


def ingest_article(root: Path, rel_dir: Path, slug: str, source: str, title: str, tags, notes: str):
    raw_rel_path = str((rel_dir / f"{slug}.md").as_posix())
    raw_abs_path = root / raw_rel_path
    status = "stub"
    extraction = "stub"
    body_preview = ""
    suspicious_segments = []
    psl_result = {"available": PSL_SCRIPT.exists(), "action": "allow", "severity": "SAFE", "reasons": []}

    try:
        html = fetch_url(source)
        extracted_title = extract_title(html, title)
        candidate_html = extract_main_html(html)
        markdown = html_to_markdown(candidate_html)
        cleaned_markdown, noise_segments = clean_markdown(markdown)
        suspicious_segments.extend(noise_segments)
        psl_result = run_prompt_shield(cleaned_markdown[:12000])
        suspicious_segments.extend(detect_suspicious_segments(cleaned_markdown))

        if len(cleaned_markdown) < MIN_CONTENT_LENGTH:
            raise ValueError("extracted markdown too short after cleaning")

        title = extracted_title
        body_preview = cleaned_markdown[:MAX_PREVIEW_LENGTH]

        if psl_result.get("action") == "block" or psl_result.get("severity") in {"HIGH", "CRITICAL"}:
            status = "suspicious"
            extraction = "suspicious"
        elif suspicious_segments or psl_result.get("degraded"):
            status = "suspicious"
            extraction = "partial"
        else:
            status = "raw"
            extraction = "full"

        raw_abs_path.write_text(render_article_markdown(title, slug, source, tags, status, extraction, psl_result, suspicious_segments, cleaned_markdown), encoding="utf-8")

        if psl_result.get("reasons"):
            notes = (notes + "\n" if notes else "") + "Prompt Shield: " + "; ".join(psl_result.get("reasons", [])[:5])
        if suspicious_segments:
            notes = (notes + "\n" if notes else "") + f"Suspicious/noisy segments: {len(suspicious_segments)}"
    except Exception as exc:
        raw_abs_path.write_text("\n".join([
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            "source_type: article",
            f"source_url: {source}",
            f"ingested_at: {now_iso()}",
            f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
            "status: stub",
            "extraction: failed",
            "---",
            "",
            f"# {title}",
            "",
            f"Source: {source}",
            "",
            f"Extraction failed or was incomplete: {exc}",
            "",
        ]) + "\n", encoding="utf-8")
        notes = (notes + "\n" if notes else "") + f"Extraction fallback: {exc}"
        extraction = "failed"
        psl_result = {"available": PSL_SCRIPT.exists(), "action": "warn", "severity": "UNKNOWN", "reasons": [str(exc)], "degraded": True}

    return {
        "title": title,
        "raw_path": raw_rel_path,
        "status": status,
        "extraction": extraction,
        "body_preview": body_preview,
        "notes": notes,
        "suspicious_segments": suspicious_segments,
        "prompt_shield": {
            "action": psl_result.get("action", "allow"),
            "severity": psl_result.get("severity", "SAFE"),
            "reasons": psl_result.get("reasons", []),
            "degraded": psl_result.get("degraded", False),
        },
    }


def clone_repo(repo_url: str, repo_dir: Path):
    if repo_dir.exists() and any(repo_dir.iterdir()):
        return "existing"
    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", repo_url, str(repo_dir)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "cloned"


def summarize_repo(repo_dir: Path):
    readme = None
    for candidate in ["README.md", "readme.md", "README.MD"]:
        path = repo_dir / candidate
        if path.exists():
            readme = path
            break
    readme_text = read_text_file(readme)[:5000] if readme else ""
    top_items = sorted([p.name for p in repo_dir.iterdir() if not p.name.startswith(".")])[:30]
    return readme_text, top_items


def ingest_repo(root: Path, rel_dir: Path, slug: str, source: str, title: str, tags, notes: str):
    repo_root = root / rel_dir / slug
    repo_dir = repo_root / "repo"
    summary_path = repo_root / f"{slug}.md"
    repo_status = "stub"
    extraction = "stub"
    clone_state = "skipped"
    readme_text = ""
    top_items = []

    try:
        clone_state = clone_repo(source, repo_dir)
        readme_text, top_items = summarize_repo(repo_dir)
        repo_status = "raw"
        extraction = "repo"
    except Exception as exc:
        notes = (notes + "\n" if notes else "") + f"Repo clone fallback: {exc}"

    summary = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"slug: {slug}",
        "source_type: repo",
        f"source_url: {source}",
        f"ingested_at: {now_iso()}",
        f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
        f"status: {repo_status}",
        f"extraction: {extraction}",
        "---",
        "",
        f"# {title}",
        "",
        f"Repository URL: {source}",
        "",
        f"Clone state: {clone_state}",
        "",
        "## Top-level files",
        "",
    ]
    if top_items:
        summary.extend([f"- {item}" for item in top_items])
    else:
        summary.append("- Repository tree unavailable.")
    summary.extend(["", "## README excerpt", ""])
    summary.append(readme_text if readme_text else "README unavailable.")
    summary.append("")
    summary_path.write_text("\n".join(summary), encoding="utf-8")

    return {
        "title": title,
        "raw_path": str(summary_path.relative_to(root).as_posix()),
        "status": repo_status,
        "extraction": extraction,
        "repo_local_path": str(repo_dir.relative_to(root).as_posix()) if repo_dir.exists() else "",
        "body_preview": readme_text[:1000],
        "notes": notes,
        "suspicious_segments": [],
        "prompt_shield": {"action": "allow", "severity": "SAFE", "reasons": [], "degraded": False},
        "processor": "vendor-anthropic/repo-local",
    }


def normalize_paper_source(source: str) -> str:
    if "arxiv.org/abs/" in source:
        paper_id = source.split("/abs/")[-1].split("?")[0]
        return f"https://arxiv.org/pdf/{paper_id}.pdf"
    return source


def extract_arxiv_metadata(html: str):
    title_match = re.search(r'<meta[^>]+name=["\']citation_title["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    abstract_match = re.search(r'<meta[^>]+name=["\']citation_abstract["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    return {
        "title": title_match.group(1).strip() if title_match else "",
        "abstract": abstract_match.group(1).strip() if abstract_match else "",
    }


def extract_pdf_text(pdf_path: Path) -> str:
    if import_check("pdfplumber"):
        script = """
import pdfplumber, sys
from pathlib import Path
import os
path = Path(sys.argv[1])
parts = []
with pdfplumber.open(path) as pdf:
    for page in pdf.pages[:20]:
        txt = page.extract_text() or ''
        if txt.strip():
            parts.append(txt.strip())
print('\n\n'.join(parts))
"""
        proc = subprocess.run([kb_python(), "-c", script, str(pdf_path)], capture_output=True, text=True, check=False)
        text = (proc.stdout or "").strip()
        if len(text) > 400:
            return text
    if import_check("pypdf"):
        script = """
from pypdf import PdfReader
import sys
reader = PdfReader(sys.argv[1])
parts = []
for page in reader.pages[:20]:
    txt = page.extract_text() or ''
    if txt.strip():
        parts.append(txt.strip())
print('\n\n'.join(parts))
"""
        proc = subprocess.run([kb_python(), "-c", script, str(pdf_path)], capture_output=True, text=True, check=False)
        text = (proc.stdout or "").strip()
        if len(text) > 400:
            return text
    proc = subprocess.run(["strings", str(pdf_path)], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return ""
    lines = [line.strip() for line in proc.stdout.splitlines()]
    kept = [line for line in lines if len(line) > 20 and not re.match(r"^[\W_]+$", line)]
    return "\n".join(kept[:2000]).strip()


def ingest_paper(root: Path, rel_dir: Path, slug: str, source: str, title: str, tags, notes: str):
    paper_url = normalize_paper_source(source)
    paper_dir = root / rel_dir
    pdf_path = paper_dir / f"{slug}.pdf"
    md_path = paper_dir / f"{slug}.md"
    metadata = {"title": "", "abstract": ""}
    prompt_shield = {"action": "allow", "severity": "SAFE", "reasons": [], "degraded": False}
    suspicious_segments = []
    extraction = "stub"
    status = "stub"
    body_preview = ""
    vendor = vendor_status()

    try:
        if "arxiv.org" in source and "/abs/" in source:
            abs_html = fetch_url(source)
            metadata = extract_arxiv_metadata(abs_html)
            if metadata.get("title"):
                title = metadata["title"]
        pdf_bytes = download_binary(paper_url)
        pdf_path.write_bytes(pdf_bytes)

        extracted_text = extract_pdf_text(pdf_path)
        if metadata.get("abstract"):
            extracted_text = f"## Abstract\n\n{metadata['abstract']}\n\n## Extracted text\n\n{extracted_text}" if extracted_text else f"## Abstract\n\n{metadata['abstract']}"
        extracted_text = extracted_text.strip()
        if len(extracted_text) < 400:
            raise ValueError("paper text extraction too short")

        prompt_shield = run_prompt_shield(extracted_text[:12000])
        suspicious_segments = detect_suspicious_segments(extracted_text)
        body_preview = extracted_text[:MAX_PREVIEW_LENGTH]

        if prompt_shield.get("action") == "block" or prompt_shield.get("severity") in {"HIGH", "CRITICAL"}:
            status = "suspicious"
            extraction = "suspicious"
        elif suspicious_segments or prompt_shield.get("degraded"):
            status = "suspicious"
            extraction = "partial"
        else:
            status = "raw"
            extraction = "pdf-text"

        lines = [
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            "source_type: paper",
            f"source_url: {source}",
            f"pdf_url: {paper_url}",
            f"ingested_at: {now_iso()}",
            f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
            f"status: {status}",
            f"extraction: {extraction}",
            f"prompt_shield_action: {prompt_shield.get('action', 'allow')}",
            f"prompt_shield_severity: {prompt_shield.get('severity', 'SAFE')}",
            "---",
            "",
            f"# {title}",
            "",
            f"Source: {source}",
            f"PDF: [[../../{pdf_path.relative_to(root).as_posix()}]]",
            "",
            "## Processor",
            "",
            "- Preferred skill: vendor-anthropic/pdf",
            f"- pypdf available: {vendor['python_pypdf']}",
            f"- pdfplumber available: {vendor['python_pdfplumber']}",
            "- Current fallback: strings-based extraction",
            "",
        ]
        if suspicious_segments:
            lines.extend(["## Suspicious segments", ""])
            for item in suspicious_segments[:MAX_SEGMENTS]:
                lines.append(f"- severity={item.get('severity', 'n/a')} action={item.get('action', 'warn')}: {item.get('text', '')}")
            lines.append("")
        lines.extend(["## Extracted text", "", extracted_text, ""])
        md_path.write_text("\n".join(lines), encoding="utf-8")

        if prompt_shield.get("reasons"):
            notes = (notes + "\n" if notes else "") + "Prompt Shield: " + "; ".join(prompt_shield.get("reasons", [])[:5])
        if suspicious_segments:
            notes = (notes + "\n" if notes else "") + f"Suspicious/noisy segments: {len(suspicious_segments)}"
    except Exception as exc:
        lines = [
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            "source_type: paper",
            f"source_url: {source}",
            f"pdf_url: {paper_url}",
            f"ingested_at: {now_iso()}",
            f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
            "status: stub",
            "extraction: failed",
            "---",
            "",
            f"# {title}",
            "",
            f"Source: {source}",
            "",
            f"Paper extraction failed or was incomplete: {exc}",
            "",
            "## Processor",
            "",
            "- Preferred skill: vendor-anthropic/pdf",
            f"- pypdf available: {vendor['python_pypdf']}",
            f"- pdfplumber available: {vendor['python_pdfplumber']}",
            "- Current fallback: strings-based extraction",
            "",
        ]
        if metadata.get("abstract"):
            lines.extend(["## Abstract", "", metadata["abstract"], ""])
        md_path.write_text("\n".join(lines), encoding="utf-8")
        notes = (notes + "\n" if notes else "") + f"Paper extraction fallback: {exc}"
        prompt_shield = {"action": "warn", "severity": "UNKNOWN", "reasons": [str(exc)], "degraded": True}

    return {
        "title": title,
        "raw_path": str(md_path.relative_to(root).as_posix()),
        "status": status,
        "extraction": extraction,
        "body_preview": body_preview,
        "notes": notes,
        "suspicious_segments": suspicious_segments,
        "prompt_shield": prompt_shield,
        "pdf_local_path": str(pdf_path.relative_to(root).as_posix()) if pdf_path.exists() else "",
        "processor": "vendor-anthropic/pdf",
        "capabilities": vendor,
    }


def preview_delimited_file(path: Path, delimiter: str):
    rows = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            rows.append(row)
            if i >= 9:
                break
    return rows


def ingest_spreadsheet(root: Path, rel_dir: Path, slug: str, source: str, title: str, tags, notes: str):
    src_path = Path(source).expanduser().resolve()
    if not src_path.exists():
        raise SystemExit(f"Local spreadsheet not found: {src_path}")
    dest = root / rel_dir / f"{slug}{src_path.suffix.lower()}"
    shutil.copy2(src_path, dest)
    summary_path = root / rel_dir / f"{slug}.md"
    vendor = vendor_status()

    extraction = "copied"
    status = "raw"
    body_preview = ""
    preview_rows = []
    sheet_names = []
    delimiter = "," if src_path.suffix.lower() == ".csv" else "\t"

    if src_path.suffix.lower() in {".csv", ".tsv"}:
        preview_rows = preview_delimited_file(dest, delimiter)
        body_preview = "\n".join([" | ".join(row[:12]) for row in preview_rows[:5]])[:MAX_PREVIEW_LENGTH]
        extraction = "delimited-preview"
    else:
        if vendor['python_pandas'] and vendor['python_openpyxl']:
            script = """
import json, sys
import pandas as pd
xls = pd.ExcelFile(sys.argv[1])
out = {"sheet_names": xls.sheet_names, "preview_rows": []}
if xls.sheet_names:
    df = pd.read_excel(sys.argv[1], sheet_name=xls.sheet_names[0]).head(5).fillna('')
    out["preview_rows"] = [list(map(str, df.columns.tolist()))] + [list(map(str, row)) for row in df.astype(str).values.tolist()]
print(json.dumps(out, ensure_ascii=False))
"""
            proc = subprocess.run([kb_python(), "-c", script, str(dest)], capture_output=True, text=True, check=False)
            try:
                data = json.loads((proc.stdout or "").strip())
                sheet_names = data.get("sheet_names", [])
                preview_rows = data.get("preview_rows", [])
                body_preview = "\n".join([" | ".join(row[:12]) for row in preview_rows[:5]])[:MAX_PREVIEW_LENGTH]
                extraction = "xlsx-preview"
            except Exception:
                extraction = "spreadsheet-stub"
                notes = (notes + "\n" if notes else "") + "XLSX preview parse failed; file copied and indexed as structured artifact."
        else:
            extraction = "spreadsheet-stub"
            notes = (notes + "\n" if notes else "") + "XLSX preview requires pandas/openpyxl; file copied and indexed as structured artifact."

    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"slug: {slug}",
        "source_type: spreadsheet",
        f"source_path: {str(src_path)}",
        f"ingested_at: {now_iso()}",
        f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
        f"status: {status}",
        f"extraction: {extraction}",
        "---",
        "",
        f"# {title}",
        "",
        f"Local file: [[../../{dest.relative_to(root).as_posix()}]]",
        "",
        "## Processor",
        "",
        "- Preferred skill: vendor-anthropic/xlsx",
        f"- pandas available: {vendor['python_pandas']}",
        f"- openpyxl available: {vendor['python_openpyxl']}",
        "",
    ]
    if sheet_names:
        lines.extend(["## Sheets", ""])
        lines.extend([f"- {name}" for name in sheet_names])
        lines.append("")
    if preview_rows:
        lines.extend(["## Preview rows", ""])
        for row in preview_rows:
            lines.append("- " + " | ".join(row[:12]))
        lines.append("")
    else:
        lines.extend(["## Preview rows", "", "- No tabular preview available with current local dependencies.", ""])
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "title": title,
        "raw_path": str(summary_path.relative_to(root).as_posix()),
        "status": status,
        "extraction": extraction,
        "body_preview": body_preview,
        "notes": notes,
        "suspicious_segments": [],
        "prompt_shield": {"action": "allow", "severity": "SAFE", "reasons": [], "degraded": False},
        "spreadsheet_local_path": str(dest.relative_to(root).as_posix()),
        "processor": "vendor-anthropic/xlsx",
        "capabilities": vendor,
    }


def main():
    parser = argparse.ArgumentParser(description="Register a source into the KB manifest")
    parser.add_argument("--root", required=True)
    parser.add_argument("--source", required=True, help="URL or local file path")
    parser.add_argument("--type", choices=["article", "paper", "repo", "spreadsheet", "file"], default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--tags", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest_path = root / "manifest.json"
    manifest = load_manifest(manifest_path)

    source = args.source.strip()
    source_type = infer_type(source, args.type)
    slug = unique_slug(source)
    title = args.title or title_from_source(source)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    rel_dir = Path(raw_subdir(source_type))
    (root / rel_dir).mkdir(parents=True, exist_ok=True)

    raw_rel_path = None
    status = "stub"
    extraction = "none"
    body_preview = ""
    repo_local_path = ""
    pdf_local_path = ""
    spreadsheet_local_path = ""
    notes = args.notes
    suspicious_segments = []
    prompt_shield = {"action": "allow", "severity": "SAFE", "reasons": [], "degraded": False}
    processor = "native"
    capabilities = None

    if source_type == "article" and source.startswith(("http://", "https://")):
        result = ingest_article(root, rel_dir, slug, source, title, tags, notes)
        title = result["title"]
        raw_rel_path = result["raw_path"]
        status = result["status"]
        extraction = result["extraction"]
        body_preview = result["body_preview"]
        notes = result["notes"]
        suspicious_segments = result["suspicious_segments"]
        prompt_shield = result["prompt_shield"]
    elif source_type == "paper" and source.startswith(("http://", "https://")):
        result = ingest_paper(root, rel_dir, slug, source, title, tags, notes)
        title = result["title"]
        raw_rel_path = result["raw_path"]
        status = result["status"]
        extraction = result["extraction"]
        body_preview = result["body_preview"]
        notes = result["notes"]
        suspicious_segments = result["suspicious_segments"]
        prompt_shield = result["prompt_shield"]
        pdf_local_path = result["pdf_local_path"]
        processor = result["processor"]
        capabilities = result["capabilities"]
    elif source_type == "repo" and source.startswith(("http://", "https://")):
        result = ingest_repo(root, rel_dir, slug, source, title, tags, notes)
        title = result["title"]
        raw_rel_path = result["raw_path"]
        status = result["status"]
        extraction = result["extraction"]
        repo_local_path = result["repo_local_path"]
        body_preview = result["body_preview"]
        notes = result["notes"]
        suspicious_segments = result["suspicious_segments"]
        prompt_shield = result["prompt_shield"]
        processor = result["processor"]
    elif source_type == "spreadsheet":
        result = ingest_spreadsheet(root, rel_dir, slug, source, title, tags, notes)
        title = result["title"]
        raw_rel_path = result["raw_path"]
        status = result["status"]
        extraction = result["extraction"]
        body_preview = result["body_preview"]
        notes = result["notes"]
        suspicious_segments = result["suspicious_segments"]
        prompt_shield = result["prompt_shield"]
        spreadsheet_local_path = result["spreadsheet_local_path"]
        processor = result["processor"]
        capabilities = result["capabilities"]
    elif source.startswith(("http://", "https://")):
        raw_rel_path = str((rel_dir / f"{slug}.md").as_posix())
        (root / raw_rel_path).write_text("\n".join([
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            f"source_type: {source_type}",
            f"source_url: {source}",
            f"ingested_at: {now_iso()}",
            f"tags: [{', '.join(json.dumps(t, ensure_ascii=False) for t in tags)}]",
            "status: stub",
            "extraction: none",
            "---",
            "",
            f"# {title}",
            "",
            f"Source: {source}",
            "",
            "Extraction pending or unsupported in current ingest path.",
            "",
        ]) + "\n", encoding="utf-8")
    else:
        src_path = Path(source).expanduser().resolve()
        if not src_path.exists():
            raise SystemExit(f"Local file not found: {src_path}")
        dest = root / rel_dir / f"{slug}{src_path.suffix}"
        shutil.copy2(src_path, dest)
        raw_rel_path = str(dest.relative_to(root).as_posix())
        status = "raw"
        extraction = "copied"
        if src_path.suffix.lower() in {".md", ".txt"}:
            body_preview = read_text_file(dest)[:1000]

    entry = {
        "id": slug,
        "slug": slug,
        "title": title,
        "source": source,
        "source_type": source_type,
        "raw_path": raw_rel_path,
        "ingested_at": now_iso(),
        "tags": tags,
        "status": status,
        "extraction": extraction,
        "body_preview": body_preview,
        "notes": notes,
        "prompt_shield": prompt_shield,
        "suspicious_segment_count": len(suspicious_segments),
        "processor": processor,
    }
    if suspicious_segments:
        entry["suspicious_segments"] = suspicious_segments[:MAX_SEGMENTS]
    if repo_local_path:
        entry["repo_local_path"] = repo_local_path
    if pdf_local_path:
        entry["pdf_local_path"] = pdf_local_path
    if spreadsheet_local_path:
        entry["spreadsheet_local_path"] = spreadsheet_local_path
    if capabilities:
        entry["capabilities"] = capabilities

    if any(e.get("slug") == slug for e in manifest.get("entries", [])):
        raise SystemExit(f"Duplicate slug exists: {slug}")

    manifest.setdefault("entries", []).append(entry)
    save_manifest(manifest_path, manifest)
    print(json.dumps({"ok": True, "entry": entry}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
