#!/usr/bin/env python3
"""
Extract text-based question blocks from scraped 9702 PDFs.

The output keeps enough metadata to pair question papers with mark schemes later:
  {
    "source": "9702_s25_qp_42.pdf",
    "paper": "9702_s25_qp_42",
    "question_id": "3",
    "text": "...",
    "paper_type": "qp",
    "paper_no": "4",
    "variant": "42",
    "markscheme_pdf": "9702_s25_ms_42.pdf"
  }
"""

import json
import re
from pathlib import Path
from typing import Optional

import pdfplumber
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FILE_RE = re.compile(
    r"^(?P<subject>\d{4})_(?P<season>[smwn])(?P<year>\d{2})_(?P<kind>[a-z]{2})_(?P<variant>\d{2})\.pdf$",
    re.IGNORECASE,
)
TEXT_BASED_PAPERS = {"2", "4", "5"}


def load_manifest(raw_dir: Path) -> list[dict]:
    manifest_path = raw_dir / "manifest.json"
    if not manifest_path.exists():
        return []
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("items", [])


def parse_file_meta(filename: str) -> Optional[dict]:
    match = FILE_RE.match(filename)
    if not match:
        return None
    groups = match.groupdict()
    paper_no = groups["variant"][0]
    return {
        "subject": groups["subject"],
        "season_code": groups["season"],
        "year_short": groups["year"],
        "paper_type": groups["kind"].lower(),
        "variant": groups["variant"],
        "paper_no": paper_no,
    }


def is_text_based_question_paper(filename: str) -> bool:
    meta = parse_file_meta(filename)
    if not meta:
        return False
    return meta["paper_type"] == "qp" and meta["paper_no"] in TEXT_BASED_PAPERS


def matching_markscheme(filename: str, available_files: set[str]) -> Optional[str]:
    meta = parse_file_meta(filename)
    if not meta:
        return None
    ms_name = (
        f"{meta['subject']}_{meta['season_code']}{meta['year_short']}_"
        f"ms_{meta['variant']}.pdf"
    )
    return ms_name if ms_name in available_files else None


def normalise_pdf_text(text: str) -> str:
    text = text.replace("\x0c", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"© UCLES \d{4}", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"BLANK PAGE", " ", text, flags=re.IGNORECASE)
    return text.strip()


def extract_question_blocks(text: str) -> list[tuple[str, str]]:
    """
    Return top-level question blocks as [(question_number, text), ...].
    """
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    starts = []
    for idx, line in enumerate(lines):
        if re.match(r"^(?:Question\s+)?\d{1,2}\b", line) and not re.match(r"^\d+\s+mark", line, re.I):
            starts.append((idx, re.match(r"^(?:Question\s+)?(\d{1,2})\b", line).group(1)))

    if not starts:
        return []

    blocks = []
    for pos, (start_idx, question_no) in enumerate(starts):
        end_idx = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        chunk = " ".join(lines[start_idx:end_idx]).strip()
        chunk = re.sub(r"\s+", " ", chunk)
        if len(chunk) >= 80:
            blocks.append((question_no, chunk[:4000]))
    return blocks


def extract_from_pdf(pdf_path: Path, available_files: set[str]) -> list[dict]:
    questions = []
    if not is_text_based_question_paper(pdf_path.name):
        return questions

    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
    except Exception as exc:
        print(f"[WARN] PDF error {pdf_path.name}: {exc}")
        return questions

    text = normalise_pdf_text("\n".join(pages))
    blocks = extract_question_blocks(text)

    meta = parse_file_meta(pdf_path.name) or {}
    ms_name = matching_markscheme(pdf_path.name, available_files)

    for question_id, block in blocks:
        if re.match(r"^(?:9702|page\s+\d+)", block, re.I):
            continue
        questions.append(
            {
                "source": pdf_path.name,
                "paper": pdf_path.stem,
                "question_id": question_id,
                "text": block,
                "marks": None,
                "paper_type": meta.get("paper_type"),
                "paper_no": meta.get("paper_no"),
                "variant": meta.get("variant"),
                "markscheme_pdf": ms_name,
            }
        )
    return questions


def main():
    raw_dir = PROJECT_ROOT / "data" / "raw"
    out_path = PROJECT_ROOT / "data" / "questions.jsonl"
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(raw_dir)
    pdfs = []
    for item in manifest:
        local_path = item.get("local_path")
        if local_path:
            pdfs.append(Path(local_path))

    if not pdfs:
        pdfs = list(raw_dir.glob("*.pdf"))

    available_files = {path.name for path in pdfs}
    all_questions = []
    for pdf_path in tqdm(sorted(pdfs), desc="PDF"):
        all_questions.extend(extract_from_pdf(pdf_path, available_files))

    with open(out_path, "w", encoding="utf-8") as f:
        for question in all_questions:
            f.write(json.dumps(question, ensure_ascii=False) + "\n")
    print(f"Wrote {len(all_questions)} questions to {out_path}")


if __name__ == "__main__":
    main()
