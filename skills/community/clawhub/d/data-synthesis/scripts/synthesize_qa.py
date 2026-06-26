#!/usr/bin/env python3
"""
QA synthesis pipeline: CSV → chunk → (large) questions → (large) answers → JSONL.
Set DATA_SYNTHESIS_USE_API=1 and OPENAI_API_KEY for live API calls; otherwise runs in dry-run mode.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence


def chunk_text(text: str, max_chars: int, overlap: int) -> list[str]:
    """Split text into overlapping character windows."""
    text = text.strip()
    if not text:
        return []
    if max_chars <= 0:
        return [text]
    overlap = max(0, min(overlap, max_chars - 1)) if max_chars > 1 else 0
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= n:
            break
        start = end - overlap if overlap else end
    return chunks


def _extract_json_list(raw: str) -> list[str]:
    """Parse a JSON array of strings from model output; tolerate markdown fences."""
    s = raw.strip()
    if "```" in s:
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", s, re.IGNORECASE)
        if m:
            s = m.group(1).strip()
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        # Fallback: one question per non-empty line
        return [ln.strip().lstrip("-•* ").strip() for ln in s.splitlines() if ln.strip()]
    if isinstance(data, list):
        out: list[str] = []
        for item in data:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
            elif isinstance(item, dict) and "question" in item:
                q = item["question"]
                if isinstance(q, str) and q.strip():
                    out.append(q.strip())
        return out
    return []


@dataclass
class LLMConfig:
    api_key: str | None = None
    # Can be either:
    # - Base URL ending with /v1 (or without), e.g. https://api.openai.com/v1
    # - Full chat completions URL, e.g. http://host/.../v1/chat/completions
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout_sec: float = 120.0


class BaseLLMClient(ABC):
    @abstractmethod
    def complete(self, model: str, system: str, user: str) -> str:
        pass


class DryRunLLM(BaseLLMClient):
    def complete(self, model: str, system: str, user: str) -> str:
        if "阅读理解助教" in system or "JSON 数组" in system:
            return json.dumps(
                [
                    "这段文字的主要观点是什么？",
                    "有哪些关键细节值得注意？",
                ],
                ensure_ascii=False,
            )
        return "这是基于给定文本与问题的示例答案（dry-run 模式）。"


class OpenAICompatibleLLM(BaseLLMClient):
    def __init__(self, cfg: LLMConfig) -> None:
        self._cfg = cfg
        self._base = cfg.base_url.rstrip("/")

    def complete(self, model: str, system: str, user: str) -> str:
        if self._base.endswith("/chat/completions"):
            url = self._base
        elif self._base.endswith("/v1"):
            url = f"{self._base}/chat/completions"
        else:
            url = f"{self._base}/v1/chat/completions"
        body: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": int(self._cfg.max_tokens),
            "temperature": float(self._cfg.temperature),
        }
        data = json.dumps(body).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self._cfg.api_key:
            headers["Authorization"] = f"Bearer {self._cfg.api_key}"
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self._cfg.timeout_sec) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
        try:
            return str(payload["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected API response: {payload!r}") from e


def build_llm() -> BaseLLMClient:
    use_api = os.environ.get("DATA_SYNTHESIS_USE_API", "").strip() in ("1", "true", "yes")
    if not use_api:
        return DryRunLLM()
    key = os.environ.get("OPENAI_API_KEY", "").strip() or None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    model = (
        os.environ.get("DATA_SYNTHESIS_MODEL", "").strip()
        or os.environ.get("DATA_SYNTHESIS_LARGE_MODEL", "").strip()
        or "Qwen3-14B"
    )
    max_tokens = int(os.environ.get("DATA_SYNTHESIS_MAX_TOKENS", "1000").strip() or "1000")
    temperature = float(os.environ.get("DATA_SYNTHESIS_TEMPERATURE", "0.7").strip() or "0.7")
    cfg = LLMConfig(
        api_key=key,
        base_url=base,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return OpenAICompatibleLLM(cfg)


def generate_questions(llm: BaseLLMClient, model: str, chunk: str) -> list[str]:
    system = (
        "你是阅读理解助教。根据用户提供的文本，输出 3-8 个可用于训练的高质量问题。"
        "只输出 JSON 数组，元素为字符串（每个字符串是一个问题），不要其它说明。"
    )
    user = f"文本：\n\n{chunk}\n\n/no_think"
    raw = llm.complete(model, system, user)
    return _extract_json_list(raw)


def generate_answer(llm: BaseLLMClient, model: str, chunk: str, question: str) -> str:
    system = (
        "你是助手。根据给定文本回答问题，答案应可在文本中推断或合理总结；"
        "简洁准确，使用与问题相同的语言。"
    )
    user = f"文本：\n\n{chunk}\n\n问题：\n{question}\n\n请直接给出答案。\n/no_think"
    return llm.complete(model, system, user).strip()


def read_csv_rows(path: Path, text_column: str | None) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        fields = list(reader.fieldnames)
        col = text_column
        if col is None:
            for name in fields:
                if name and name.lower() in ("text", "content", "body", "正文", "文本"):
                    col = name
                    break
            if col is None:
                col = fields[0]
        rows: list[dict[str, str]] = []
        for r in reader:
            rows.append({k: (v or "").strip() for k, v in r.items()})
        return col, rows


@dataclass
class PipelineStats:
    rows: int = 0
    chunks: int = 0
    questions_generated: int = 0
    qa_pairs_written: int = 0
    errors: list[str] = field(default_factory=list)


def run_pipeline(
    input_csv: Path,
    output_jsonl: Path,
    text_column: str | None,
    chunk_size: int,
    chunk_overlap: int,
    max_rows: int | None,
    sleep_sec: float,
    llm: BaseLLMClient | None = None,
    model: str | None = None,
) -> PipelineStats:
    stats = PipelineStats()
    llm = llm or build_llm()
    if isinstance(llm, OpenAICompatibleLLM):
        m = model or os.environ.get("DATA_SYNTHESIS_MODEL", "").strip() or os.environ.get(
            "DATA_SYNTHESIS_LARGE_MODEL", "gpt-4o"
        ).strip()
    else:
        m = model or "dry-run"

    col, rows = read_csv_rows(input_csv, text_column)
    if max_rows is not None:
        rows = rows[: max(0, max_rows)]

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    stats.rows = len(rows)

    with output_jsonl.open("w", encoding="utf-8") as out:
        for row_idx, row in enumerate(rows):
            text = row.get(col, "")
            if not text:
                continue
            for c_idx, chunk in enumerate(chunk_text(text, chunk_size, chunk_overlap)):
                stats.chunks += 1
                chunk_id = f"r{row_idx}-c{c_idx}"
                try:
                    questions = generate_questions(llm, m, chunk)
                except Exception as e:
                    stats.errors.append(f"{chunk_id} generate_questions: {e}")
                    questions = []
                stats.questions_generated += len(questions)
                if sleep_sec > 0:
                    time.sleep(sleep_sec)
                for q_idx, question in enumerate(questions):
                    if sleep_sec > 0:
                        time.sleep(sleep_sec)
                    try:
                        answer = generate_answer(llm, m, chunk, question)
                    except Exception as e:
                        stats.errors.append(f"{chunk_id} q{q_idx} answer: {e}")
                        continue
                    if sleep_sec > 0:
                        time.sleep(sleep_sec)
                    record = {
                        "chunk_id": chunk_id,
                        "row_index": row_idx,
                        "chunk_index": c_idx,
                        "question_index": q_idx,
                        "text_column": col,
                        "source_fields": {k: v for k, v in row.items() if k != col and v},
                        "chunk": chunk,
                        "question": question,
                        "answer": answer,
                    }
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    stats.qa_pairs_written += 1

    return stats


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="CSV → QA synthesis pipeline")
    p.add_argument("input_csv", type=Path, help="Input corpus CSV path")
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSONL path (default: <input_stem>_qa.jsonl next to input)",
    )
    p.add_argument("--text-column", default=None, help="Column name for body text (auto-detect if omitted)")
    p.add_argument("--chunk-size", type=int, default=2000, help="Max characters per chunk")
    p.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    p.add_argument("--max-rows", type=int, default=None, help="Process only first N data rows")
    p.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Seconds to sleep between API calls (rate limiting)",
    )
    p.add_argument(
        "--model",
        default=None,
        help="Chat model name (overrides DATA_SYNTHESIS_MODEL / DATA_SYNTHESIS_LARGE_MODEL)",
    )
    args = p.parse_args(list(argv) if argv is not None else None)

    if not args.input_csv.is_file():
        print(f"Error: file not found: {args.input_csv}", file=sys.stderr)
        return 2

    out_path = args.output
    if out_path is None:
        out_path = args.input_csv.with_name(args.input_csv.stem + "_qa.jsonl")

    stats = run_pipeline(
        args.input_csv,
        out_path,
        args.text_column,
        args.chunk_size,
        args.chunk_overlap,
        args.max_rows,
        args.sleep,
        model=args.model,
    )

    print(json.dumps({"output": str(out_path), **stats.__dict__}, ensure_ascii=False, indent=2))
    if stats.errors:
        print("\nWarnings/errors:", file=sys.stderr)
        for e in stats.errors[:20]:
            print(f"  - {e}", file=sys.stderr)
        if len(stats.errors) > 20:
            print(f"  ... and {len(stats.errors) - 20} more", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
