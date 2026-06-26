from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ADDRESS_TERMS = (
    "先生",
    "小姐",
    "老师",
    "前辈",
    "大人",
    "殿下",
    "君",
    "酱",
    "chan",
    "san",
    "sama",
)

VERBAL_MARKERS = (
    "...",
    "......",
    "...",
    "!",
    "?",
    "吧",
    "呢",
    "啊",
    "呀",
    "吗",
    "哼",
)


def load_texts(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return [line.strip() for line in raw.splitlines() if line.strip()]
    entries = payload.get("entries")
    if isinstance(entries, list):
        return [entry.get("text", "").strip() for entry in entries if entry.get("text", "").strip()]
    return [line.strip() for line in raw.splitlines() if line.strip()]


def sentence_list(texts: list[str]) -> list[str]:
    content = "\n".join(texts)
    parts = re.split(r"(?<=[。！？!?])\s*", content)
    return [part.strip() for part in parts if part.strip()]


def count_terms(texts: list[str], terms: tuple[str, ...]) -> dict[str, int]:
    joined = "\n".join(texts)
    counts = {term: joined.count(term) for term in terms}
    return {term: count for term, count in counts.items() if count}


def punctuation_profile(sentences: list[str]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for sentence in sentences:
        if sentence[-1] in "。！？!?":
            counter[sentence[-1]] += 1
    return dict(counter)


def average_sentence_length(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    return round(sum(len(sentence) for sentence in sentences) / len(sentences), 2)


def example_lines(texts: list[str], limit: int) -> list[str]:
    samples = []
    for text in texts:
        compact = " ".join(part.strip() for part in text.splitlines() if part.strip())
        if compact and compact not in samples:
            samples.append(compact[:160])
        if len(samples) >= limit:
            break
    return samples


def extract(path: Path, max_examples: int) -> dict:
    texts = load_texts(path)
    sentences = sentence_list(texts)
    return {
        "source_path": str(path),
        "sentence_count": len(sentences),
        "average_sentence_length": average_sentence_length(sentences),
        "address_terms": count_terms(texts, ADDRESS_TERMS),
        "verbal_markers": count_terms(texts, VERBAL_MARKERS),
        "punctuation_profile": punctuation_profile(sentences),
        "example_lines": example_lines(texts, max_examples),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract simple style signals from text or normalized JSON.")
    parser.add_argument("--input", required=True, help="Path to a text file or normalized JSON.")
    parser.add_argument("--output", help="Optional JSON output path.")
    parser.add_argument("--max-examples", type=int, default=8, help="Maximum number of example lines.")
    args = parser.parse_args()

    payload = extract(Path(args.input), args.max_examples)
    content = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(content + "\n", encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
