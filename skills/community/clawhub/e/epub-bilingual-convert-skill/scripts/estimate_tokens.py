#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path


DEFAULT_MAX_SOURCE_CHARS = 8000
DEFAULT_RETRY_BUFFER = 0.15
DEFAULT_TOP = 5
INPUT_CHARS_PER_TOKEN = 4
SUMMARY_OUTPUT_CHARS = 220
PROMPT_OVERHEAD_PER_BATCH = (350, 700)

TARGET_OUTPUT_MULTIPLIERS = {
    "chinese": (1.15, 1.45),
    "simplified chinese": (1.15, 1.45),
    "traditional chinese": (1.15, 1.45),
    "zh": (1.15, 1.45),
    "japanese": (1.10, 1.40),
    "ja": (1.10, 1.40),
    "korean": (1.10, 1.40),
    "ko": (1.10, 1.40),
    "spanish": (1.05, 1.35),
    "french": (1.05, 1.35),
    "german": (1.05, 1.35),
    "italian": (1.05, 1.35),
    "portuguese": (1.05, 1.35),
    "es": (1.05, 1.35),
}
DEFAULT_OUTPUT_MULTIPLIER = (1.10, 1.50)


def ceil_div(value, divisor):
    if value <= 0:
        return 0
    return math.ceil(value / divisor)


def estimate_tokens_from_chars(chars):
    return ceil_div(chars, INPUT_CHARS_PER_TOKEN)


def output_multiplier(target_language):
    normalized = (target_language or "").strip().lower()
    return TARGET_OUTPUT_MULTIPLIERS.get(normalized, DEFAULT_OUTPUT_MULTIPLIER)


def article_source_chars(article):
    paragraphs = sum(len(paragraph or "") for paragraph in article.get("paragraphs") or [])
    metadata = len(article.get("title") or "") + len(article.get("section") or "")
    summary = len(article.get("plain_text") or "")
    return {
        "paragraphs": paragraphs,
        "metadata": metadata,
        "summary": summary,
        "total": paragraphs + metadata + summary,
    }


def count_complete_articles(articles):
    complete = 0
    for article in articles:
        translations = article.get("translated_paragraphs")
        paragraph_count = len(article.get("paragraphs") or [])
        if (
            article.get("title_dest_language")
            and article.get("section_dest_language")
            and article.get("summary_dest_language")
            and isinstance(translations, list)
            and len(translations) == paragraph_count
            and all(text for text in translations)
        ):
            complete += 1
    return complete


def estimate_payload(payload, max_source_chars=DEFAULT_MAX_SOURCE_CHARS, retry_buffer=DEFAULT_RETRY_BUFFER, top=DEFAULT_TOP):
    articles = payload.get("articles") or []
    per_article = []
    source_chars = {"paragraphs": 0, "metadata": 0, "summary": 0, "total": 0}

    for article in articles:
        counts = article_source_chars(article)
        for key in source_chars:
            source_chars[key] += counts[key]
        per_article.append(
            {
                "num": article.get("num"),
                "title": article.get("title") or "Untitled",
                "source_chars": counts["total"],
                "paragraph_source_chars": counts["paragraphs"],
                "estimated_batches": ceil_div(counts["paragraphs"], max_source_chars),
            }
        )

    paragraph_batches = ceil_div(source_chars["paragraphs"], max_source_chars)
    summary_batches = len(articles)
    metadata_batches = ceil_div(source_chars["metadata"], max_source_chars)
    estimated_batches = paragraph_batches + summary_batches + metadata_batches

    input_tokens = {
        "paragraphs": estimate_tokens_from_chars(source_chars["paragraphs"]),
        "metadata": estimate_tokens_from_chars(source_chars["metadata"]),
        "summary": estimate_tokens_from_chars(source_chars["summary"]),
    }
    input_total = sum(input_tokens.values())

    multiplier_min, multiplier_max = output_multiplier(payload.get("target_language"))
    paragraph_input_tokens = input_tokens["paragraphs"] + input_tokens["metadata"]
    output_min = math.ceil(paragraph_input_tokens * multiplier_min + len(articles) * estimate_tokens_from_chars(SUMMARY_OUTPUT_CHARS))
    output_max = math.ceil(paragraph_input_tokens * multiplier_max + len(articles) * estimate_tokens_from_chars(SUMMARY_OUTPUT_CHARS))

    overhead_min = estimated_batches * PROMPT_OVERHEAD_PER_BATCH[0]
    overhead_max = estimated_batches * PROMPT_OVERHEAD_PER_BATCH[1]
    subtotal_min = input_total + output_min + overhead_min
    subtotal_max = input_total + output_max + overhead_max
    retry_min = math.ceil(subtotal_min * retry_buffer)
    retry_max = math.ceil(subtotal_max * retry_buffer)

    largest = sorted(per_article, key=lambda item: item["source_chars"], reverse=True)[:top]

    return {
        "epub_title": payload.get("epub_title") or "Untitled",
        "target_language": payload.get("target_language") or "Unknown",
        "scope": "full extraction",
        "estimator": "lightweight character heuristic",
        "articles": {
            "total": len(articles),
            "complete": count_complete_articles(articles),
            "incomplete": max(0, len(articles) - count_complete_articles(articles)),
        },
        "paragraphs": sum(len(article.get("paragraphs") or []) for article in articles),
        "source_chars": source_chars,
        "tokens": {
            "input": {**input_tokens, "total": input_total},
            "output": {"min": output_min, "max": output_max},
            "prompt_overhead": {"min": overhead_min, "max": overhead_max},
            "retry_buffer_ratio": retry_buffer,
            "retry_buffer": {"min": retry_min, "max": retry_max},
            "total": {"min": subtotal_min + retry_min, "max": subtotal_max + retry_max},
        },
        "batching": {
            "max_source_chars": max_source_chars,
            "estimated_paragraph_batches": paragraph_batches,
            "estimated_total_batches": estimated_batches,
        },
        "largest_articles": largest,
    }


def fmt_int(value):
    return f"{value:,}"


def format_report(result):
    tokens = result["tokens"]
    source = result["source_chars"]
    articles = result["articles"]
    batching = result["batching"]
    lines = [
        f"EPUB: {result['epub_title']}",
        f"Target language: {result['target_language']}",
        "Estimator: lightweight character heuristic, not tokenizer exact count.",
        f"Estimate scope: {result['scope']}",
        "",
        "Content size:",
        f"  Articles: {fmt_int(articles['total'])}",
        f"  Paragraphs: {fmt_int(result['paragraphs'])}",
        f"  Complete articles: {fmt_int(articles['complete'])} / {fmt_int(articles['total'])}",
        f"  Source chars: {fmt_int(source['total'])}",
        f"    Paragraphs: {fmt_int(source['paragraphs'])}",
        f"    Metadata: {fmt_int(source['metadata'])}",
        f"    Summary sources: {fmt_int(source['summary'])}",
        "",
        "Estimated translation tokens:",
        f"  Input: {fmt_int(tokens['input']['total'])}",
        f"    Paragraphs: {fmt_int(tokens['input']['paragraphs'])}",
        f"    Metadata: {fmt_int(tokens['input']['metadata'])}",
        f"    Summary sources: {fmt_int(tokens['input']['summary'])}",
        f"  Output: {fmt_int(tokens['output']['min'])} - {fmt_int(tokens['output']['max'])}",
        f"  Prompt overhead: {fmt_int(tokens['prompt_overhead']['min'])} - {fmt_int(tokens['prompt_overhead']['max'])}",
        f"  Retry/rework buffer ({tokens['retry_buffer_ratio']:.0%}): "
        f"{fmt_int(tokens['retry_buffer']['min'])} - {fmt_int(tokens['retry_buffer']['max'])}",
        f"  Total: {fmt_int(tokens['total']['min'])} - {fmt_int(tokens['total']['max'])}",
        "",
        "Recommended batching:",
        f"  Max source chars per batch: {fmt_int(batching['max_source_chars'])}",
        f"  Estimated paragraph batches: {fmt_int(batching['estimated_paragraph_batches'])}",
        f"  Estimated total translation tasks: {fmt_int(batching['estimated_total_batches'])}",
        "",
        "Largest articles by source chars:",
    ]
    if result["largest_articles"]:
        for index, article in enumerate(result["largest_articles"], start=1):
            lines.append(
                f"  {index}. {article['title']} - {fmt_int(article['source_chars'])} chars, "
                f"est. {fmt_int(article['estimated_batches'])} paragraph batches"
            )
    else:
        lines.append("  None")
    lines.extend(["", "No cost estimate included."])
    return "\n".join(lines)


def load_payload(path):
    with Path(path).expanduser().open(encoding="utf-8") as fh:
        return json.load(fh)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Estimate translation token usage for an EPUB extraction.json.")
    parser.add_argument("extraction_json", help="Path to extraction.json produced by scripts/extract.py")
    parser.add_argument("--max-source-chars", type=int, default=DEFAULT_MAX_SOURCE_CHARS)
    parser.add_argument("--retry-buffer", type=float, default=DEFAULT_RETRY_BUFFER)
    parser.add_argument("--top", type=int, default=DEFAULT_TOP)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.max_source_chars <= 0:
        raise SystemExit("--max-source-chars must be greater than 0")
    if args.retry_buffer < 0:
        raise SystemExit("--retry-buffer must be non-negative")
    if args.top < 0:
        raise SystemExit("--top must be non-negative")

    payload = load_payload(args.extraction_json)
    result = estimate_payload(
        payload,
        max_source_chars=args.max_source_chars,
        retry_buffer=args.retry_buffer,
        top=args.top,
    )
    print(format_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
