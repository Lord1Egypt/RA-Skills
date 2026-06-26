import argparse
from textwrap import dedent
from typing import List, Dict


def build_default_metrics() -> List[Dict[str, str]]:
    """
    Return a default GEO metrics catalog for AIGVR / SoM / citation volume / coverage.
    """
    return [
        {
            "metric": "AIGVR",
            "description": "AI-generated visibility rate for our brand on a given intent/platform.",
            "formula": "brand_answers / total_sampled_answers",
            "dimensions": "platform, intent, locale",
            "cadence": "weekly",
        },
        {
            "metric": "SoM",
            "description": "Share of Model vs competitors for a given intent.",
            "formula": "brand_answers / (brand_answers + competitor_answers)",
            "dimensions": "platform, intent, competitor",
            "cadence": "weekly",
        },
        {
            "metric": "Citation Volume",
            "description": "Count of AI citations (links/brand mentions) of our resources.",
            "formula": "number_of_citations_in_sampled_outputs",
            "dimensions": "platform, page, intent",
            "cadence": "daily",
        },
        {
            "metric": "Intent Coverage",
            "description": "Number of intents where we appear at least once.",
            "formula": "count_intents_with_at_least_one_brand_citation",
            "dimensions": "platform, intent_cluster",
            "cadence": "monthly",
        },
    ]


def build_table(metrics: List[Dict[str, str]]) -> str:
    """
    Generate a markdown table for the metrics catalog.
    """
    headers = ["Metric", "Description", "Formula / Approximation", "Dimensions", "Cadence"]
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["-" * (len(h) + 2) for h in headers]) + "|")

    for m in metrics:
        row = [
            m.get("metric", ""),
            m.get("description", ""),
            m.get("formula", ""),
            m.get("dimensions", ""),
            m.get("cadence", ""),
        ]
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def build_schema_table() -> str:
    """
    Return a default markdown table describing a GEO metrics storage schema.
    """
    template = """
    | Column            | Type       | Description                                                         |
    |-------------------|-----------|---------------------------------------------------------------------|
    | date              | DATE      | Statistics date (business timezone or UTC; document the choice).   |
    | platform          | STRING    | AI platform (chatgpt, perplexity, gemini, claude, sge, etc.).      |
    | intent_id         | STRING    | Internal ID of the intent/query cluster.                           |
    | intent_name       | STRING    | Human-readable name of the intent.                                 |
    | locale            | STRING    | Locale code (e.g. en-US, zh-CN).                                   |
    | brand             | STRING    | Brand name being tracked.                                          |
    | competitor        | STRING    | Competitor name if applicable, else NULL/'none'.                   |
    | aigvr             | FLOAT     | AIGVR value for this slice on this date.                           |
    | som               | FLOAT     | Share of Model value for this slice on this date.                  |
    | citation_volume   | INT       | Count of citations in sampled outputs.                             |
    | coverage_flag     | BOOLEAN   | Whether at least one brand citation was observed.                  |
    | sample_size       | INT       | Number of sampled answers underlying this row.                     |
    | data_source       | STRING    | Origin of data (manual_sample, report_export, api, logs, etc.).    |
    | updated_at        | TIMESTAMP | Last update timestamp for this row.                                |
    """
    return dedent(template).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate markdown snippets for a GEO metrics catalog and storage schema\n"
            "to support the geo-metrics-tracker skill."
        )
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Optional path to write the markdown to. Prints to stdout if omitted.",
    )
    args = parser.parse_args()

    metrics = build_default_metrics()
    catalog = build_table(metrics)
    schema = build_schema_table()

    content = "# GEO Metrics Catalog & Schema\n\n"
    content += "## Metrics Catalog\n\n"
    content += catalog + "\n\n"
    content += "## Tracking Schema (example)\n\n"
    content += schema

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content)


if __name__ == "__main__":
    main()

