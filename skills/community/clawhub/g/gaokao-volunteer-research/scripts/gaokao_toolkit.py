#!/usr/bin/env python3
"""Deterministic helper tools for gaokao-volunteer-research."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "data" / "official-source-index.json"
FORBIDDEN_PHRASES = ["保证录取", "预测录取概率", "内部数据", "代填志愿"]
REQUIRED_PACKAGE_FILES = [
    "sources.md",
    "data-check.md",
    "candidate-matrix.md",
    "family-brief.md",
    "risk-notes.md",
]


def dump(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def load_index(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_province(index: dict, province: str | None) -> list[dict]:
    rows = index.get("province_sources", [])
    if not province:
        return rows
    return [row for row in rows if province in row.get("province", "") or province in row.get("authority_name", "")]


def http_check(url: str, timeout: int) -> dict:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "gaokao-volunteer-research/0.3"})
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {
                "url": url,
                "ok": 200 <= resp.status < 400,
                "status": resp.status,
                "content_type": resp.headers.get("content-type", ""),
                "elapsed_ms": int((time.time() - started) * 1000),
            }
    except Exception as exc:  # noqa: BLE001 - CLI should report external failures without crashing.
        return {
            "url": url,
            "ok": False,
            "error": type(exc).__name__,
            "message": str(exc),
            "elapsed_ms": int((time.time() - started) * 1000),
        }


def slugify(text: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "-", text.strip())
    safe = re.sub(r"-+", "-", safe).strip("-._")
    return safe or "source"


def infer_extension(url: str, content_type: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix
    if suffix and len(suffix) <= 8:
        return suffix
    if "pdf" in content_type:
        return ".pdf"
    if "html" in content_type:
        return ".html"
    if "json" in content_type:
        return ".json"
    if "csv" in content_type:
        return ".csv"
    return mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".bin"


def fetch_snapshot(args: argparse.Namespace) -> None:
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(args.url, headers={"User-Agent": "gaokao-volunteer-research/0.3"})
    with urllib.request.urlopen(req, timeout=args.timeout) as resp:
        body = resp.read()
        content_type = resp.headers.get("content-type", "")
        final_url = resp.geturl()
        status = resp.status

    sha = hashlib.sha256(body).hexdigest()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    name = slugify(args.source_name or urllib.parse.urlparse(final_url).netloc)
    ext = infer_extension(final_url, content_type)
    raw_path = out_dir / f"{stamp}-{name}{ext}"
    raw_path.write_bytes(body)

    meta = {
        "source_name": args.source_name,
        "source_type": args.source_type,
        "province": args.province,
        "year": args.year,
        "category": args.category,
        "note": args.note,
        "url": args.url,
        "final_url": final_url,
        "status": status,
        "content_type": content_type,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sha256": sha,
        "bytes": len(body),
        "raw_path": str(raw_path),
    }
    meta_path = raw_path.with_suffix(raw_path.suffix + ".meta.json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    dump({"ok": True, "raw_path": str(raw_path), "meta_path": str(meta_path), "sha256": sha})


def strip_tags(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def parse_markdown_table(text: str) -> list[dict]:
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return []
    rows = []
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def parse_html_tables(text: str) -> list[dict]:
    table_match = re.search(r"<table[\s\S]*?</table>", text, flags=re.I)
    if not table_match:
        return []
    row_html = re.findall(r"<tr[\s\S]*?</tr>", table_match.group(0), flags=re.I)
    matrix = []
    for row in row_html:
        cells = re.findall(r"<t[hd][^>]*>([\s\S]*?)</t[hd]>", row, flags=re.I)
        if cells:
            matrix.append([strip_tags(cell) for cell in cells])
    if len(matrix) < 2:
        return []
    header = matrix[0]
    return [dict(zip(header, row)) for row in matrix[1:] if len(row) == len(header)]


def parse_delimited(path: Path) -> list[dict]:
    sample = path.read_text(encoding="utf-8-sig").splitlines()
    if not sample:
        return []
    dialect = csv.Sniffer().sniff("\n".join(sample[:5]), delimiters=",\t")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, dialect=dialect))


HEADER_ALIASES = {
    "score": ["分数", "成绩", "投档分", "原始分"],
    "rank": ["位次", "排名", "累计位次", "最低位次", "最低排名"],
    "segment_count": ["本段人数", "同分人数", "人数"],
    "cumulative_count": ["累计人数", "累计"],
    "batch": ["批次", "类别", "录取批次", "批次/类别"],
    "cutoff_score": ["分数线", "控制线", "批次线", "本科线", "专科线"],
    "category": ["科类", "选科", "科类/选科", "类别"],
}


def normalize_row(row: dict) -> dict:
    normalized = {"raw": row}
    for key, aliases in HEADER_ALIASES.items():
        for alias in aliases:
            if alias in row and str(row[alias]).strip():
                normalized[key] = str(row[alias]).strip()
                break
    return normalized


def parse_table(args: argparse.Namespace) -> None:
    path = Path(args.input)
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        rows = parse_delimited(path)
    elif suffix in {".html", ".htm"}:
        rows = parse_html_tables(text)
    else:
        rows = parse_markdown_table(text) or parse_html_tables(text)

    normalized = [normalize_row(row) for row in rows]
    result = {
        "ok": bool(rows),
        "kind": args.kind,
        "province": args.province,
        "year": args.year,
        "category": args.category,
        "source": args.source,
        "input": str(path),
        "row_count": len(rows),
        "rows": normalized,
        "warnings": [] if rows else ["No parseable table rows found."],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    dump({"ok": result["ok"], "out": str(out), "row_count": len(rows)})


def read_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def validate_package(args: argparse.Namespace) -> None:
    root = Path(args.dir)
    errors: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED_PACKAGE_FILES:
        if not (root / name).exists():
            errors.append(f"missing required file: {name}")

    combined = "\n".join(read_if_exists(root / name) for name in REQUIRED_PACKAGE_FILES)
    if not re.search(r"https?://", combined):
        errors.append("no source URL found in package")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in combined:
            errors.append(f"forbidden phrase found: {phrase}")

    if args.province and args.province not in combined:
        warnings.append(f"province not found in package text: {args.province}")
    if args.year and str(args.year) not in combined:
        warnings.append(f"year not found in package text: {args.year}")
    if args.category and args.category not in combined:
        warnings.append(f"category not found in package text: {args.category}")

    if "需核验" in combined and "核验" not in read_if_exists(root / "risk-notes.md"):
        warnings.append("package mentions 需核验 but risk-notes.md does not appear to document verification steps")

    dump({"ok": not errors, "errors": errors, "warnings": warnings})
    if errors:
        raise SystemExit(1)


def run_regression(args: argparse.Namespace) -> None:
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    errors: list[str] = []
    for phrase in cases.get("required_skill_phrases", []):
        if phrase not in skill:
            errors.append(f"missing required skill phrase: {phrase}")
    for case in cases.get("cases", []):
        prompt = case.get("prompt", "")
        if not prompt:
            errors.append(f"case {case.get('id')} has empty prompt")
        if not case.get("expected_behavior"):
            errors.append(f"case {case.get('id')} has empty expected_behavior")
    dump({"ok": not errors, "case_count": len(cases.get("cases", [])), "errors": errors})
    if errors:
        raise SystemExit(1)


def cmd_index(args: argparse.Namespace) -> None:
    index = load_index(Path(args.index))
    if args.index_command == "list":
        dump({"national_sources": index.get("national_sources", []), "province_sources": index.get("province_sources", [])})
    elif args.index_command == "lookup":
        matches = find_province(index, args.province)
        dump({"ok": bool(matches), "matches": matches})
        if not matches:
            raise SystemExit(1)
    elif args.index_command == "verify":
        rows = find_province(index, args.province)
        urls: list[dict] = []
        if not args.province:
            urls.extend({"label": row["name"], "url": row["url"]} for row in index.get("national_sources", []))
        urls.extend({"label": row["authority_name"], "url": row["home_url"]} for row in rows)
        results = [{"label": item["label"], **http_check(item["url"], args.timeout)} for item in urls]
        dump({"ok": all(item.get("ok") for item in results), "results": results})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    index = sub.add_parser("index", help="Use official source index")
    index.add_argument("--index", default=str(DEFAULT_INDEX))
    index_sub = index.add_subparsers(dest="index_command", required=True)
    index_sub.add_parser("list")
    lookup = index_sub.add_parser("lookup")
    lookup.add_argument("--province", required=True)
    verify = index_sub.add_parser("verify")
    verify.add_argument("--province")
    verify.add_argument("--timeout", type=int, default=10)
    index.set_defaults(func=cmd_index)

    snapshot = sub.add_parser("snapshot", help="Fetch and save a source snapshot")
    snapshot.add_argument("--url", required=True)
    snapshot.add_argument("--out", required=True)
    snapshot.add_argument("--source-name", required=True)
    snapshot.add_argument("--source-type", required=True, choices=["policy", "score_table", "cutoff_table", "charter", "exam", "school", "major", "other"])
    snapshot.add_argument("--province")
    snapshot.add_argument("--year", type=int)
    snapshot.add_argument("--category")
    snapshot.add_argument("--note")
    snapshot.add_argument("--timeout", type=int, default=20)
    snapshot.set_defaults(func=fetch_snapshot)

    parse = sub.add_parser("parse-table", help="Parse score/rank or cutoff table")
    parse.add_argument("--input", required=True)
    parse.add_argument("--out", required=True)
    parse.add_argument("--kind", required=True, choices=["score", "cutoff", "admission"])
    parse.add_argument("--province", required=True)
    parse.add_argument("--year", type=int, required=True)
    parse.add_argument("--category", required=True)
    parse.add_argument("--source")
    parse.set_defaults(func=parse_table)

    validate = sub.add_parser("validate-package", help="Validate a gaokao research package")
    validate.add_argument("--dir", required=True)
    validate.add_argument("--province")
    validate.add_argument("--year", type=int)
    validate.add_argument("--category")
    validate.set_defaults(func=validate_package)

    regression = sub.add_parser("regression", help="Run static regression case checks")
    regression.add_argument("--cases", default=str(ROOT / "tests" / "regression-cases.json"))
    regression.set_defaults(func=run_regression)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
