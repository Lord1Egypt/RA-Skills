#!/usr/bin/env python3
"""Run a two-direction paper reading and research-gap workflow.

The script is intentionally self-contained so the skill can be reused outside
the original project. It uses an OpenAI-compatible chat completion API.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import random
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Paper:
    paper_id: str
    direction_key: str
    direction_name: str
    pdf_path: Path
    text_path: Path
    title_hint: str


def safe_slug(text: str, max_len: int = 96) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_")
    return slug[:max_len] or "paper"


def read_config(args: argparse.Namespace) -> dict[str, str]:
    if args.env_file:
        load_env_file(Path(args.env_file))
    if args.env_prefix:
        prefix = args.env_prefix.upper().rstrip("_")
        config = {
            "api_key": os.environ.get(f"{prefix}_API_KEY", ""),
            "base_url": os.environ.get(f"{prefix}_BASE_URL", ""),
            "model": os.environ.get(f"{prefix}_MODEL", ""),
        }
    else:
        path = Path(args.config)
        if not path.exists():
            raise SystemExit(f"Config file not found: {path}")
        config = json.loads(path.read_text(encoding="utf-8"))
    missing = [key for key in ("api_key", "base_url", "model") if not config.get(key)]
    if missing:
        raise SystemExit(f"Missing API config fields: {', '.join(missing)}")
    return config


def load_env_file(path: Path) -> None:
    """Load KEY=VALUE lines without printing or persisting secrets."""
    if not path.exists():
        raise SystemExit(f"Env file not found: {path}")
    for raw in path.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def chat_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/v1"):
        return base + "/chat/completions"
    return base + "/v1/chat/completions"


def call_chat(
    config: dict[str, str],
    messages: list[dict[str, str]],
    max_tokens: int,
    temperature: float = 0.2,
    retries: int = 5,
    timeout: int = 180,
) -> str:
    payload = {
        "model": config["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    data = json.dumps(payload).encode("utf-8")
    url = chat_url(config["base_url"])
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
            ConnectionResetError,
            OSError,
            http.client.HTTPException,
            KeyError,
            json.JSONDecodeError,
        ) as exc:
            if attempt == retries - 1:
                raise RuntimeError(f"LLM call failed after {retries} attempts: {exc}") from exc
            time.sleep(min(30, 2 ** attempt) + random.random())
    raise RuntimeError("unreachable")


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        return result.stdout
    except Exception as exc:
        raise RuntimeError(f"Could not extract text from {pdf_path}. Install pypdf or pdftotext. Last error: {exc}") from exc


def collect_papers(pdf_dir: Path, direction_key: str, direction_name: str, out_dir: Path, limit: int = 0, recursive: bool = False) -> list[Paper]:
    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(pdf_dir.glob(pattern))
    if limit:
        pdfs = pdfs[:limit]
    text_root = out_dir / "extracted_texts" / direction_key
    text_root.mkdir(parents=True, exist_ok=True)
    papers: list[Paper] = []
    for index, pdf in enumerate(pdfs, 1):
        paper_id = f"{index:03d}_{safe_slug(pdf.stem, 48)}"
        text_path = text_root / f"{paper_id}.txt"
        if not text_path.exists() or text_path.stat().st_size < 200:
            text = extract_pdf_text(pdf)
            text_path.write_text(text, encoding="utf-8")
        papers.append(Paper(paper_id, direction_key, direction_name, pdf, text_path, pdf.stem))
    return papers


def trim_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head = text[: int(max_chars * 0.65)]
    tail = text[-int(max_chars * 0.35) :]
    return head + "\n\n[... middle omitted for length ...]\n\n" + tail


def write_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def note_structure_errors(note: str) -> list[str]:
    errors: list[str] = []
    for index in range(1, 10):
        if not re.search(rf"^##\s+{index}\.", note, flags=re.M):
            errors.append(f"missing section {index}")
    section_9 = re.search(r"^##\s+9\.", note, flags=re.M)
    if section_9:
        tail = note[section_9.end() :].strip()
        if len(tail) < 250:
            errors.append("section 9 too short or likely truncated")
    return errors


def done_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("status") == "ok":
            ids.add(str(row.get("paper_id")))
    return ids


def review_passed_ids(out_dir: Path, direction_key: str) -> set[str]:
    """Return paper ids whose latest review record is passing."""
    review_dir = out_dir / "reviews"
    if not review_dir.exists():
        return set()
    latest: dict[str, dict[str, Any]] = {}
    for path in sorted(review_dir.glob(f"{direction_key}_batch_*.jsonl")):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            paper_id = str(row.get("paper_id", ""))
            review = row.get("review", {})
            if paper_id and isinstance(review, dict):
                latest[paper_id] = review
    return {paper_id for paper_id, review in latest.items() if review.get("pass") is True}


def next_review_batch_index(out_dir: Path, direction_key: str) -> int:
    review_dir = out_dir / "reviews"
    if not review_dir.exists():
        return 0
    highest = 0
    pattern = re.compile(rf"^{re.escape(direction_key)}_batch_(\d+)(?:_retry)?\.jsonl$")
    for path in review_dir.glob(f"{direction_key}_batch_*.jsonl"):
        match = pattern.match(path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest


def note_prompt(paper: Paper, direction_a: str, direction_b: str, text: str, retry_reason: str = "") -> list[dict[str, str]]:
    retry = f"\nPrevious reviewer feedback to fix:\n{retry_reason}\n" if retry_reason else ""
    return [
        {
            "role": "system",
            "content": "You are a senior researcher writing critical literature notes for research-gap discovery. Use your own words, avoid boilerplate, and ground claims in the supplied paper text.",
        },
        {
            "role": "user",
            "content": f"""
We are comparing two research directions:
- Direction A: {direction_a}
- Direction B: {direction_b}

Current paper:
- Direction: {paper.direction_name}
- File: {paper.pdf_path.name}

{retry}

Write a Chinese Markdown paper note. It must follow this structure:

# [Inferred paper title]

## 1. Basic Information
- File
- Direction
- Paper type
- Whether it strictly belongs to this direction
- Main task
- Data / benchmark
- Confidence: high / medium / low

## 2. Background And Motivation
Explain the paper-specific motivation. Do not write generic claims like "privacy is important".

## 3. Core Challenge
What exactly fails in previous methods? Why is it nontrivial?

## 4. Method: Step-By-Step Mechanism
Describe the workflow concretely enough that a reader can reconstruct the algorithm.
If it is FL/distributed: client state, server state, upload, download, aggregation/routing, local training, inference.
If it is skill discovery/evolution: trajectory/data source, skill representation, generator, verifier, optimizer/editor, retrieval/dependency, evolution phase, inference/use phase.

## 5. Why The Method Could Work
Explain the mechanism, not just component names.

## 6. Experiments And Evidence
Separate strong evidence from narrow setting evidence.

## 7. Assumptions And Failure Modes
List stated assumptions, hidden assumptions, author limitations, and inferred non-working scenarios.

## 8. Implications For The Cross-Direction Research Agenda
Start with one explicit category: directly transferable / indirect inspiration / warning-counterexample / mostly irrelevant.
Then give concrete, paper-specific implications for comparing {direction_a} and {direction_b}. Avoid reusable boilerplate.

## 9. Open Questions To Verify
List testable uncertainties and validation experiments.

Paper text:
{text}
""",
        },
    ]


def review_prompt(note: str, recent_notes: list[str]) -> list[dict[str, str]]:
    previous = "\n\n--- previous note excerpt ---\n\n".join(recent_notes[-6:])
    return [
        {"role": "system", "content": "You are a strict research-note reviewer. Return JSON only."},
        {
            "role": "user",
            "content": f"""
Review the candidate note for quality. Return JSON only:
{{
  "pass": true,
  "score": 9,
  "failure_reasons": [],
  "rewrite_instructions": [],
  "duplicate_implication": false,
  "needs_pdf_recheck": false,
  "evidence": "short explanation"
}}

Fail if:
- the note is mostly copied/paraphrased without understanding
- the note appears truncated or any required section is incomplete
- "why important" is generic
- the method is not reconstructable
- implications are boilerplate or duplicate previous notes
- assumptions and failure modes are missing
- author evidence, inference, and uncertain hypotheses are mixed
- relationship to the two-direction agenda is not explicit
- rewrite_instructions would be non-empty; if you need any rewrite, set pass to false

Previous note excerpts for duplicate-implication checking:
{previous}

Candidate note:
{note}
""",
        },
    ]


def clean_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.S)
    return json.loads(cleaned)


def write_note_file(out_dir: Path, paper: Paper, note: str) -> Path:
    notes_dir = out_dir / "notes" / paper.direction_key
    notes_dir.mkdir(parents=True, exist_ok=True)
    path = notes_dir / f"{paper.paper_id}.md"
    path.write_text(note, encoding="utf-8")
    return path


def process_direction(
    config: dict[str, str],
    papers: list[Paper],
    out_dir: Path,
    direction_a: str,
    direction_b: str,
    args: argparse.Namespace,
) -> None:
    raw_path = out_dir / "raw" / f"{papers[0].direction_key}_notes.jsonl" if papers else out_dir / "raw" / "empty.jsonl"
    completed = done_ids(raw_path) if args.resume else set()
    passed_reviews = review_passed_ids(out_dir, papers[0].direction_key) if papers and args.resume else set()
    batch: list[tuple[Paper, str, Path]] = []
    reviewed_notes: list[str] = []
    batch_index = next_review_batch_index(out_dir, papers[0].direction_key) if papers else 0
    for paper in papers:
        if paper.paper_id in completed:
            note_path = out_dir / "notes" / paper.direction_key / f"{paper.paper_id}.md"
            if note_path.exists():
                note = note_path.read_text(encoding="utf-8", errors="ignore")
                structure_errors = note_structure_errors(note)
                if paper.paper_id in passed_reviews and not structure_errors:
                    reviewed_notes.append(note[:3000])
                else:
                    batch.append((paper, note, note_path))
                    reason = "; ".join(structure_errors) if structure_errors else "latest review not passing"
                    print(f"queued review {paper.direction_key} {paper.paper_id} {paper.pdf_path.name} ({reason})")
                if len(batch) == args.batch_size:
                    batch_index += 1
                    reviewed_notes.extend(review_batch(config, batch, reviewed_notes, out_dir, args, batch_index))
                    reviewed_notes = reviewed_notes[-8:]
                    batch = []
                continue
        text = trim_text(paper.text_path.read_text(encoding="utf-8", errors="ignore"), args.max_chars)
        try:
            note = call_chat(
                config,
                note_prompt(paper, direction_a, direction_b, text),
                max_tokens=args.max_tokens,
                retries=args.api_retries,
                timeout=args.api_timeout,
            )
            note_path = write_note_file(out_dir, paper, note)
            write_jsonl(raw_path, {"paper_id": paper.paper_id, "pdf": str(paper.pdf_path), "status": "ok", "note_path": str(note_path)})
            batch.append((paper, note, note_path))
            print(f"ok note {paper.direction_key} {paper.paper_id} {paper.pdf_path.name}")
        except Exception as exc:
            write_jsonl(raw_path, {"paper_id": paper.paper_id, "pdf": str(paper.pdf_path), "status": "failed", "error": str(exc)})
            print(f"failed note {paper.direction_key} {paper.paper_id}: {exc}")

        if len(batch) == args.batch_size:
            batch_index += 1
            reviewed_notes.extend(review_batch(config, batch, reviewed_notes, out_dir, args, batch_index))
            reviewed_notes = reviewed_notes[-8:]
            batch = []
    if batch:
        batch_index += 1
        reviewed_notes.extend(review_batch(config, batch, reviewed_notes, out_dir, args, batch_index))


def review_batch(
    config: dict[str, str],
    batch: list[tuple[Paper, str, Path]],
    recent_notes: list[str],
    out_dir: Path,
    args: argparse.Namespace,
    batch_index: int,
) -> list[str]:
    direction_key = batch[0][0].direction_key
    review_dir = out_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    passes = 0
    failures: list[dict[str, Any]] = []
    review_path = review_dir / f"{direction_key}_batch_{batch_index:03d}.jsonl"
    for paper, note, note_path in batch:
        try:
            review = clean_json(
                call_chat(
                    config,
                    review_prompt(note, recent_notes),
                    max_tokens=1200,
                    retries=args.api_retries,
                    timeout=args.api_timeout,
                )
            )
        except Exception as exc:
            review = {"pass": False, "score": 0, "failure_reasons": [f"review failed: {exc}"], "rewrite_instructions": ["Rewrite with the full schema and more specific mechanisms."]}
        structure_errors = note_structure_errors(note)
        if structure_errors:
            review["pass"] = False
            review.setdefault("failure_reasons", []).append(f"deterministic structure check failed: {structure_errors}")
            review.setdefault("rewrite_instructions", []).append("Regenerate the complete note with all nine required sections; Section 9 must contain concrete testable questions and must not be truncated.")
        if review.get("rewrite_instructions"):
            review["pass"] = False
            review.setdefault("failure_reasons", []).append("reviewer requested rewrite; pass cannot be true when rewrite_instructions is non-empty")
        if review.get("pass") is True:
            passes += 1
        else:
            failures.append({"paper": paper, "note_path": note_path, "review": review})
        write_jsonl(review_path, {"paper_id": paper.paper_id, "note_path": str(note_path), "review": review})

    required = len(batch)
    if passes == required:
        return [note_path.read_text(encoding="utf-8", errors="ignore")[:3000] for _, _, note_path in batch]

    fixed = 0
    retry_path = review_dir / f"{direction_key}_batch_{batch_index:03d}_retry.jsonl"
    for failure in failures:
        paper: Paper = failure["paper"]
        note_path: Path = failure["note_path"]
        reason = json.dumps(failure["review"], ensure_ascii=False)
        text = trim_text(paper.text_path.read_text(encoding="utf-8", errors="ignore"), args.max_chars)
        try:
            revised = call_chat(
                config,
                note_prompt(paper, args.name_a, args.name_b, text, retry_reason=reason),
                max_tokens=args.max_tokens,
                retries=args.api_retries,
                timeout=args.api_timeout,
            )
            note_path.write_text(revised, encoding="utf-8")
        except Exception as exc:
            second_review = {"pass": False, "score": 0, "failure_reasons": [f"retry rewrite failed: {exc}"]}
            write_jsonl(retry_path, {"paper_id": paper.paper_id, "note_path": str(note_path), "review": second_review})
            print(f"retry fail {paper.direction_key} {paper.paper_id}")
            continue
        try:
            second_review = clean_json(
                call_chat(
                    config,
                    review_prompt(revised, recent_notes),
                    max_tokens=1200,
                    retries=args.api_retries,
                    timeout=args.api_timeout,
                )
            )
        except Exception as exc:
            second_review = {"pass": False, "score": 0, "failure_reasons": [f"retry review failed: {exc}"]}
        retry_structure_errors = note_structure_errors(revised)
        if retry_structure_errors:
            second_review["pass"] = False
            second_review.setdefault("failure_reasons", []).append(f"deterministic structure check failed after retry: {retry_structure_errors}")
        if second_review.get("rewrite_instructions"):
            second_review["pass"] = False
            second_review.setdefault("failure_reasons", []).append("reviewer requested rewrite after retry; final pass cannot be true when rewrite_instructions is non-empty")
        if second_review.get("pass") is True:
            fixed += 1
        write_jsonl(retry_path, {"paper_id": paper.paper_id, "note_path": str(note_path), "review": second_review})
        print(f"retry {'pass' if second_review.get('pass') is True else 'fail'} {paper.direction_key} {paper.paper_id}")

    if passes + fixed < required:
        report = out_dir / "quality_failure_report.md"
        report.write_text(
            f"# Quality Failure Report\n\nDirection: {direction_key}\nBatch: {batch_index}\nRequired final passes: {required}/{len(batch)}\nInitial pass: {passes}\nRetry pass: {fixed}\n\n"
            + "\n".join(f"- {item['paper'].paper_id}: {item['review']}" for item in failures),
            encoding="utf-8",
        )
        raise SystemExit(f"Quality gate failed. See {report}")

    return [note_path.read_text(encoding="utf-8", errors="ignore")[:3000] for _, _, note_path in batch]


def compact_note(note: str, max_chars: int = 1600) -> str:
    lines = [line.strip() for line in note.splitlines() if line.strip()]
    title = next((line for line in lines if line.startswith("#")), lines[0] if lines else "Untitled")
    chunks = [title, "\n".join(lines[:16])]
    lowered = note.lower()
    for needle in (
        "method",
        "mechanism",
        "assumption",
        "failure",
        "limitation",
        "non-working",
        "challenge",
        "evidence",
        "机制",
        "假设",
        "失败",
        "局限",
        "启发",
        "fedskills",
        "implication",
        "gap",
    ):
        idx = lowered.find(needle)
        if idx >= 0:
            chunks.append(note[max(0, idx - 400) : min(len(note), idx + 900)])
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(chunks))[:max_chars]


def agenda_text(args: argparse.Namespace) -> str:
    chunks = []
    if args.agenda:
        chunks.append(args.agenda)
    if args.agenda_file:
        path = Path(args.agenda_file)
        if not path.exists():
            raise SystemExit(f"Agenda file not found: {path}")
        chunks.append(path.read_text(encoding="utf-8-sig", errors="ignore"))
    return "\n\n".join(chunk.strip() for chunk in chunks if chunk.strip())


def synthesis_prompt(
    title: str,
    required: str,
    notes: list[str],
    name_a: str,
    name_b: str,
    agenda: str = "",
    reviewer_feedback: str = "",
) -> list[dict[str, str]]:
    joined = "\n\n--- NOTE BREAK ---\n\n".join(compact_note(note) for note in notes)
    agenda_block = f"\nUser research agenda and exclusions:\n{agenda}\n" if agenda else ""
    feedback_block = f"\nReviewer feedback to fix:\n{reviewer_feedback}\n" if reviewer_feedback else ""
    return [
        {"role": "system", "content": "You synthesize literature into actionable research gaps. Be concrete, critical, and avoid generic taxonomies."},
        {
            "role": "user",
            "content": f"""
Write a Chinese Markdown document titled: {title}

Research directions:
- {name_a}
- {name_b}

Must cover:
{required}

{agenda_block}
{feedback_block}

Rules:
- Distinguish author evidence, your inference, and uncertain but testable hypotheses.
- For every proposed gap or idea, explain why the existing work does not already solve it.
- Avoid repeating the same implication across different topics.
- End with a concise table of concrete research opportunities.

Notes:
{joined[:130000]}
""",
        },
    ]


def synthesis_review_prompt(title: str, content: str, name_a: str, name_b: str, agenda: str) -> list[dict[str, str]]:
    agenda_block = f"\nUser research agenda:\n{agenda}\n" if agenda else ""
    return [
        {"role": "system", "content": "You are a strict reviewer of literature synthesis and research-gap analysis. Return JSON only."},
        {
            "role": "user",
            "content": f"""
Review this synthesis document for whether it supports research planning across two paper corpora.

Directions:
- {name_a}
- {name_b}
Document title: {title}
{agenda_block}

Return JSON only:
{{
  "pass": true,
  "score": 9,
  "failure_reasons": [],
  "rewrite_instructions": [],
  "missing_axes": [],
  "over_generic_sections": [],
  "evidence": "short explanation"
}}

Fail if:
- it is a generic taxonomy rather than a comparison grounded in notes
- it does not state what remains unsolved and why adjacent work does not solve it
- proposed gaps lack validation experiments or failure scenarios
- improvement ideas do not name a concrete mechanism and target bottleneck
- it ignores the user's explicit agenda or exclusions
- it blurs author evidence, model inference, and uncertain hypotheses

Document:
{content[:70000]}
""",
        },
    ]


def run_synthesis(config: dict[str, str], out_dir: Path, args: argparse.Namespace) -> None:
    notes_a = [p.read_text(encoding="utf-8", errors="ignore") for p in sorted((out_dir / "notes" / "direction_a").glob("*.md"))]
    notes_b = [p.read_text(encoding="utf-8", errors="ignore") for p in sorted((out_dir / "notes" / "direction_b").glob("*.md"))]
    synth_dir = out_dir / "syntheses"
    synth_dir.mkdir(parents=True, exist_ok=True)
    review_dir = out_dir / "synthesis_reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    agenda = agenda_text(args)
    outputs = [
        (
            f"{args.name_a} Synthesis",
            synth_dir / "direction_a_synthesis.md",
            notes_a,
            f"Summarize {args.name_a}: common assumptions, methods, evidence, unresolved problems, and what matters when compared with {args.name_b}.",
        ),
        (
            f"{args.name_b} Synthesis",
            synth_dir / "direction_b_synthesis.md",
            notes_b,
            f"Summarize {args.name_b}: common assumptions, methods, evidence, unresolved problems, and what matters when compared with {args.name_a}.",
        ),
        (
            "Cross Direction Analysis",
            synth_dir / "cross_direction_analysis.md",
            notes_a + notes_b,
            "Compare the two directions horizontally: shared problems, incompatible assumptions, transferable mechanisms, warnings/counterexamples, and scenarios where one direction's methods fail under the other's deployment assumptions. Include a checklist for privacy, robustness, scale, fairness, incentives, verification, retrieval/dependency, drift, and unlearning if relevant.",
        ),
        (
            "Research Gaps",
            synth_dir / "research_gaps.md",
            notes_a + notes_b,
            "List meaningful research gaps. For each gap: unsolved problem, why important, supporting evidence, why existing papers do not solve it, validation experiment, risk, uncertainty.",
        ),
        (
            "Improvement Ideas Ranked",
            synth_dir / "improvement_ideas_ranked.md",
            notes_a + notes_b,
            "Propose and rank concrete improvement ideas. Score each idea on importance, novelty, feasibility, verifiability, and distance from the closest baseline. Each idea needs a specific new technique, target failure mode, and evaluation plan.",
        ),
    ]
    for title, path, notes, required in outputs:
        content = call_chat(
            config,
            synthesis_prompt(title, required, notes, args.name_a, args.name_b, agenda=agenda),
            max_tokens=args.synthesis_tokens,
            retries=args.api_retries,
            timeout=args.api_timeout,
        )
        path.write_text(content, encoding="utf-8")
        review = review_synthesis_document(config, title, path, notes, required, agenda, args)
        if review.get("pass") is not True:
            report = out_dir / "quality_failure_report.md"
            report.write_text(
                f"# Synthesis Quality Failure Report\n\nDocument: {path.name}\n\nReview:\n\n```json\n{json.dumps(review, ensure_ascii=False, indent=2)}\n```\n",
                encoding="utf-8",
            )
            raise SystemExit(f"Synthesis quality gate failed. See {report}")
        print(f"wrote {path}")


def review_synthesis_document(
    config: dict[str, str],
    title: str,
    path: Path,
    notes: list[str],
    required: str,
    agenda: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    review_path = path.parent.parent / "synthesis_reviews" / f"{path.stem}.json"
    content = path.read_text(encoding="utf-8", errors="ignore")
    try:
        review = clean_json(
            call_chat(
                config,
                synthesis_review_prompt(title, content, args.name_a, args.name_b, agenda),
                max_tokens=1400,
                retries=args.api_retries,
                timeout=args.api_timeout,
            )
        )
    except Exception as exc:
        review = {"pass": False, "score": 0, "failure_reasons": [f"synthesis review failed: {exc}"], "rewrite_instructions": ["Rewrite with concrete gaps, mechanisms, evidence, and validation plans."]}

    if review.get("pass") is True:
        review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
        return review

    if args.no_synthesis_retry:
        review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
        return review

    feedback = json.dumps(review, ensure_ascii=False)
    revised = call_chat(
        config,
        synthesis_prompt(title, required, notes, args.name_a, args.name_b, agenda=agenda, reviewer_feedback=feedback),
        max_tokens=args.synthesis_tokens,
        retries=args.api_retries,
        timeout=args.api_timeout,
    )
    path.write_text(revised, encoding="utf-8")
    try:
        second_review = clean_json(
            call_chat(
                config,
                synthesis_review_prompt(title, revised, args.name_a, args.name_b, agenda),
                max_tokens=1400,
                retries=args.api_retries,
                timeout=args.api_timeout,
            )
        )
    except Exception as exc:
        second_review = {"pass": False, "score": 0, "failure_reasons": [f"synthesis retry review failed: {exc}"]}
    review_path.write_text(json.dumps({"initial": review, "final": second_review}, ensure_ascii=False, indent=2), encoding="utf-8")
    return second_review


def write_manifest(out_dir: Path, args: argparse.Namespace, papers_a: list[Paper], papers_b: list[Paper]) -> None:
    manifest = {
        "direction_a": args.name_a,
        "direction_b": args.name_b,
        "dir_a": str(Path(args.dir_a).resolve()),
        "dir_b": str(Path(args.dir_b).resolve()),
        "count_a": len(papers_a),
        "count_b": len(papers_b),
        "model": os.environ.get(f"{args.env_prefix.upper()}_MODEL") if args.env_prefix else "config-file-model",
        "recursive": bool(args.recursive),
        "agenda_supplied": bool(args.agenda or args.agenda_file),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    (out_dir / "workflow_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def write_audit(out_dir: Path) -> None:
    note_counts = {p.name: len(list(p.glob("*.md"))) for p in (out_dir / "notes").glob("*") if p.is_dir()}
    synth_files = sorted(str(p.relative_to(out_dir)) for p in (out_dir / "syntheses").glob("*.md"))
    review_files = sorted((out_dir / "reviews").glob("*.jsonl")) if (out_dir / "reviews").exists() else []
    synthesis_review_files = sorted((out_dir / "synthesis_reviews").glob("*.json")) if (out_dir / "synthesis_reviews").exists() else []
    review_lines = 0
    failed_reviews = 0
    for path in review_files:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            review_lines += 1
            try:
                row = json.loads(line)
                if row.get("review", {}).get("pass") is not True and "_retry" not in path.name:
                    failed_reviews += 1
            except json.JSONDecodeError:
                failed_reviews += 1
    content = [
        "# Workflow Audit Report",
        "",
        f"- Note counts: {note_counts}",
        f"- Synthesis files: {synth_files}",
        f"- Review JSONL files: {len(review_files)}",
        f"- Review records: {review_lines}",
        f"- Initial failed review records, if later retried: {failed_reviews}",
        f"- Synthesis review files: {[str(p.relative_to(out_dir)) for p in synthesis_review_files]}",
        f"- Quality failure report exists: {(out_dir / 'quality_failure_report.md').exists()}",
        "",
        "Run `scripts/validate_outputs.py <out-dir>` for stricter validation.",
    ]
    (out_dir / "audit_report.md").write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir-a", required=True, help="PDF folder for direction A")
    parser.add_argument("--dir-b", required=True, help="PDF folder for direction B")
    parser.add_argument("--name-a", required=True)
    parser.add_argument("--name-b", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--config", default="local_config/llm.json")
    parser.add_argument("--env-file", default="", help="Optional .env file to load before reading env-prefix variables")
    parser.add_argument("--env-prefix", default="", help="Use env vars such as QWEN_API_KEY/QWEN_BASE_URL/QWEN_MODEL")
    parser.add_argument("--agenda", default="", help="User research agenda, priorities, or exclusions to enforce in synthesis")
    parser.add_argument("--agenda-file", default="", help="Markdown/text file with research agenda and exclusions")
    parser.add_argument("--recursive", action="store_true", help="Recursively collect PDFs from each direction folder")
    parser.add_argument("--limit-a", type=int, default=0)
    parser.add_argument("--limit-b", type=int, default=0)
    parser.add_argument("--max-chars", type=int, default=60000)
    parser.add_argument("--max-tokens", type=int, default=4500)
    parser.add_argument("--synthesis-tokens", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--api-retries", type=int, default=5, help="Retries per LLM API call")
    parser.add_argument("--api-timeout", type=int, default=180, help="Seconds before one LLM API attempt times out")
    parser.add_argument("--no-synthesis-retry", action="store_true", help="Do not retry synthesis documents after reviewer failure")
    parser.add_argument("--no-resume", dest="resume", action="store_false")
    parser.set_defaults(resume=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    config = read_config(args)
    papers_a = collect_papers(Path(args.dir_a), "direction_a", args.name_a, out_dir, args.limit_a, recursive=args.recursive)
    papers_b = collect_papers(Path(args.dir_b), "direction_b", args.name_b, out_dir, args.limit_b, recursive=args.recursive)
    if not papers_a or not papers_b:
        raise SystemExit("Both directions must contain at least one PDF.")

    write_manifest(out_dir, args, papers_a, papers_b)
    process_direction(config, papers_a, out_dir, args.name_a, args.name_b, args)
    process_direction(config, papers_b, out_dir, args.name_a, args.name_b, args)
    run_synthesis(config, out_dir, args)
    write_audit(out_dir)
    print(f"done. outputs: {out_dir}")


if __name__ == "__main__":
    main()
