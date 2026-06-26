#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from mx_api import (
    data_query,
    format_data_query_markdown,
    format_news_markdown,
    format_stock_screen_markdown,
    news_search,
    stock_screen,
    write_stock_screen_csv,
    write_stock_screen_description,
)
from runtime_config import get_output_dir, require_em_api_key


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRESET_PATH = ROOT / "assets" / "mx_presets.json"


def load_presets(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip()).strip("-")
    return text or "step"


def maybe_write_json(path: Path | None, payload: dict) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def maybe_write_text(path: Path | None, content: str) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def render_news_markdown(query: str, result: dict, limit: int) -> str:
    lines = [f"# MX News Search", "", f"Query: `{query}`", ""]
    lines.append(format_news_markdown(result["items"], limit=limit))
    return "\n".join(lines).rstrip() + "\n"


def render_stock_screen_markdown(result: dict, limit: int) -> str:
    lines = [f"# MX Stock Screen", "", f"Keyword: `{result['keyword']}`", ""]
    lines.append(f"- response_code: `{result['response_code']}`")
    lines.append(f"- reflect_result: `{result['reflect_result']}`")
    lines.append(f"- security_count: `{result['security_count']}`")
    for item in result["conditions"]:
        lines.append(f"- condition: {item.get('describe', '')} -> {item.get('stockCount', '')}")
    lines.append("")
    lines.append(format_stock_screen_markdown(result["columns"], result["rows"], limit=limit))
    return "\n".join(lines).rstrip() + "\n"


def render_data_query_markdown(result: dict, limit: int) -> str:
    lines = [f"# MX Data Query", "", f"Tool Query: `{result['tool_query']}`", ""]
    lines.append(f"- question_id: `{result['question_id'] or 'n/a'}`")
    lines.append(f"- tables: `{len(result['tables'])}`")
    lines.append(f"- entities: `{len(result['entities'])}`")
    lines.append("")
    lines.append(format_data_query_markdown(result["tables"], limit=limit))
    return "\n".join(lines).rstrip() + "\n"


def save_single_run_outputs(command: str, output_dir: str | None) -> Path | None:
    if not output_dir:
        return None
    target = Path(output_dir).expanduser()
    target.mkdir(parents=True, exist_ok=True)
    return target


def run_news_search(args: argparse.Namespace) -> int:
    result = news_search(args.query, size=args.size)
    markdown = render_news_markdown(args.query, result, args.limit)
    output_dir = save_single_run_outputs("news-search", args.output_dir)
    maybe_write_json(output_dir / "raw.json" if output_dir else None, result["raw"])
    maybe_write_text(output_dir / "report.md" if output_dir else None, markdown)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print(markdown)
    if output_dir:
        print(f"Saved: {output_dir}")
    return 0


def run_stock_screen(args: argparse.Namespace) -> int:
    result = stock_screen(args.keyword, page_no=args.page_no, page_size=args.page_size)
    markdown = render_stock_screen_markdown(result, args.limit)
    output_dir = save_single_run_outputs("stock-screen", args.output_dir)
    maybe_write_json(output_dir / "raw.json" if output_dir else None, result["raw"])
    maybe_write_text(output_dir / "report.md" if output_dir else None, markdown)

    csv_out = Path(args.csv_out).expanduser() if args.csv_out else (output_dir / "screen.csv" if output_dir else None)
    desc_out = Path(args.desc_out).expanduser() if args.desc_out else (output_dir / "columns.md" if output_dir else None)
    if csv_out:
        write_stock_screen_csv(result["columns"], result["rows"], str(csv_out))
    if desc_out:
        write_stock_screen_description(result["columns"], str(desc_out))

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print(markdown)
    if csv_out:
        print(f"CSV: {csv_out}")
    if desc_out:
        print(f"Columns: {desc_out}")
    if output_dir:
        print(f"Saved: {output_dir}")
    return 0


def run_query(args: argparse.Namespace) -> int:
    result = data_query(args.tool_query)
    markdown = render_data_query_markdown(result, args.limit)
    output_dir = save_single_run_outputs("query", args.output_dir)
    maybe_write_json(output_dir / "raw.json" if output_dir else None, result["raw"])
    maybe_write_text(output_dir / "report.md" if output_dir else None, markdown)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print(markdown)
    if output_dir:
        print(f"Saved: {output_dir}")
    return 0


def render_preset_step(step: dict, result: dict) -> str:
    tool = step["tool"]
    if tool == "news-search":
        return render_news_markdown(step["query"], result, step.get("limit", 5))
    if tool == "stock-screen":
        return render_stock_screen_markdown(result, step.get("limit", 10))
    if tool == "query":
        return render_data_query_markdown(result, step.get("limit", 12))
    raise ValueError(f"unsupported tool: {tool}")


def execute_preset_step(step: dict, output_dir: Path) -> dict:
    tool = step["tool"]
    slug = step.get("slug") or slugify(step.get("query") or step.get("keyword") or step.get("tool_query") or tool)
    step_dir = output_dir / slug
    step_dir.mkdir(parents=True, exist_ok=True)

    if tool == "news-search":
        result = news_search(step["query"], size=step.get("size"))
        markdown = render_news_markdown(step["query"], result, step.get("limit", 5))
        maybe_write_json(step_dir / "raw.json", result["raw"])
        maybe_write_text(step_dir / "report.md", markdown)
        return {"tool": tool, "slug": slug, "markdown": markdown, "saved_dir": str(step_dir)}

    if tool == "stock-screen":
        result = stock_screen(step["keyword"], page_no=step.get("page_no", 1), page_size=step.get("page_size", 20))
        markdown = render_stock_screen_markdown(result, step.get("limit", 10))
        maybe_write_json(step_dir / "raw.json", result["raw"])
        maybe_write_text(step_dir / "report.md", markdown)
        write_stock_screen_csv(result["columns"], result["rows"], str(step_dir / "screen.csv"))
        write_stock_screen_description(result["columns"], str(step_dir / "columns.md"))
        return {
            "tool": tool,
            "slug": slug,
            "markdown": markdown,
            "saved_dir": str(step_dir),
            "security_count": result["security_count"],
        }

    if tool == "query":
        result = data_query(step["tool_query"])
        markdown = render_data_query_markdown(result, step.get("limit", 12))
        maybe_write_json(step_dir / "raw.json", result["raw"])
        maybe_write_text(step_dir / "report.md", markdown)
        return {"tool": tool, "slug": slug, "markdown": markdown, "saved_dir": str(step_dir)}

    raise ValueError(f"unsupported tool: {tool}")


def run_list_presets(args: argparse.Namespace) -> int:
    presets = load_presets(args.preset_path)
    print("# MX Presets\n")
    for name, config in presets.items():
        print(f"- `{name}`: {config.get('description', '')}")
    return 0


def run_preset(args: argparse.Namespace) -> int:
    presets = load_presets(args.preset_path)
    if args.name not in presets:
        available = ", ".join(sorted(presets))
        raise SystemExit(f"unknown preset: {args.name}. available: {available}")

    preset = presets[args.name]
    base_dir = Path(args.output_dir).expanduser() if args.output_dir else get_output_dir("mx-presets")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / f"{args.name}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    sections = [f"# MX Preset Run", "", f"Preset: `{args.name}`", ""]
    if preset.get("description"):
        sections.append(preset["description"])
        sections.append("")

    for index, step in enumerate(preset.get("steps", []), start=1):
        result = execute_preset_step(step, output_dir)
        sections.append(f"## Step {index}: {result['slug']}")
        sections.append(f"- tool: `{result['tool']}`")
        sections.append(f"- saved_dir: `{result['saved_dir']}`")
        sections.append("")
        sections.append(result["markdown"].strip())
        sections.append("")

    report = "\n".join(sections).rstrip() + "\n"
    maybe_write_text(output_dir / "preset_report.md", report)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "preset": args.name,
                    "description": preset.get("description", ""),
                    "output_dir": str(output_dir),
                    "steps": preset.get("steps", []),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(report)
    print(f"Preset output: {output_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Use the Meixiang / Eastmoney APIs with the local EM_API_KEY.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    presets_parser = subparsers.add_parser("list-presets", help="List the preset MX workflows.")
    presets_parser.add_argument("--preset-path", default=str(DEFAULT_PRESET_PATH), help="Preset config JSON path.")
    presets_parser.set_defaults(func=run_list_presets)

    preset_parser = subparsers.add_parser("preset", help="Run a preset MX workflow and save all artifacts.")
    preset_parser.add_argument("--name", required=True, help="Preset name.")
    preset_parser.add_argument("--preset-path", default=str(DEFAULT_PRESET_PATH), help="Preset config JSON path.")
    preset_parser.add_argument("--output-dir", help="Optional base output directory.")
    preset_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    preset_parser.set_defaults(func=run_preset)

    news_parser = subparsers.add_parser("news-search", help="Run a real MX financial news search.")
    news_parser.add_argument("--query", required=True, help="Natural-language financial news query.")
    news_parser.add_argument("--size", type=int, default=8, help="Requested result size.")
    news_parser.add_argument("--limit", type=int, default=5, help="Rendered result limit.")
    news_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    news_parser.add_argument("--output-dir", help="Optional directory to save raw JSON and markdown report.")
    news_parser.set_defaults(func=run_news_search)

    screen_parser = subparsers.add_parser("stock-screen", help="Run a real MX stock screen and optionally export CSV.")
    screen_parser.add_argument("--keyword", required=True, help="Natural-language stock-screen query.")
    screen_parser.add_argument("--page-no", type=int, default=1, help="Page number.")
    screen_parser.add_argument("--page-size", type=int, default=20, help="Page size.")
    screen_parser.add_argument("--limit", type=int, default=10, help="Rendered row limit.")
    screen_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    screen_parser.add_argument("--output-dir", help="Optional directory to save raw JSON, report, CSV, and columns.")
    screen_parser.add_argument("--csv-out", help="Optional path to save the full result CSV.")
    screen_parser.add_argument("--desc-out", help="Optional path to save a columns description markdown file.")
    screen_parser.set_defaults(func=run_stock_screen)

    query_parser = subparsers.add_parser("query", help="Run a real MX structured data query.")
    query_parser.add_argument("--tool-query", required=True, help="Natural-language data query.")
    query_parser.add_argument("--limit", type=int, default=12, help="Rendered metric limit.")
    query_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    query_parser.add_argument("--output-dir", help="Optional directory to save raw JSON and markdown report.")
    query_parser.set_defaults(func=run_query)

    return parser


def main() -> int:
    require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
