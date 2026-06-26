#!/usr/bin/env python3
"""Sync keyword-based arXiv topics into a daily local archive."""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from arxiv_api import DEFAULT_LIMIT, VALID_ORDERS, VALID_SORTS, safe_dir_name, search_papers  # noqa: E402
from arxiv_to_md import fetch_paper_to_directory  # noqa: E402
from search_arxiv import write_search_outputs  # noqa: E402

DEFAULT_ROOT_DIR = Path.cwd() / "artifacts" / "arxiv-monitor"
DEFAULT_STATE_NAME = "sync_state.json"
DEFAULT_TOPICS_NAME = "topics.json"
SUMMARY_HEADINGS = [
    "## One-line takeaway",
    "## Problem and motivation",
    "## Method",
    "## Main findings",
    "## Limits and caveats",
    "## Follow-up questions",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def today_local() -> str:
    return datetime.now().astimezone().date().isoformat()


def normalize_slug(value: str, fallback: str) -> str:
    slug = safe_dir_name(value).replace("_", "-").strip("._-").lower()
    return slug or fallback


def validate_limit(value: object, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")
    if value < 1:
        raise ValueError(f"{field_name} must be greater than or equal to 1")
    return value


def validate_sort_value(value: object, field_name: str) -> str:
    if not isinstance(value, str) or value not in VALID_SORTS:
        raise ValueError(f"{field_name} must be one of: {', '.join(sorted(VALID_SORTS))}")
    return value


def validate_order_value(value: object, field_name: str) -> str:
    if not isinstance(value, str) or value not in VALID_ORDERS:
        raise ValueError(f"{field_name} must be one of: {', '.join(sorted(VALID_ORDERS))}")
    return value


def parse_iso_date(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format") from error


def read_topics_config(path: Path) -> dict:
    if not path.exists():
        sample_path = SKILL_DIR / "references" / "topics.example.json"
        raise FileNotFoundError(
            f"topics config not found: {path}. Copy {sample_path} to that location and edit it for your interests."
        )
    config = load_json(path)
    if not isinstance(config, dict):
        raise ValueError("topics config must be a JSON object")
    return config


def flatten_topics(config: dict) -> tuple[dict[str, object], list[dict[str, object]]]:
    defaults = config.get("defaults")
    groups = config.get("groups")

    if not isinstance(defaults, dict):
        raise ValueError("topics config defaults must be an object")
    if not isinstance(groups, list) or not groups:
        raise ValueError("topics config groups must be a non-empty list")

    resolved_defaults = {
        "per_topic_limit": validate_limit(defaults.get("per_topic_limit", DEFAULT_LIMIT), "defaults.per_topic_limit"),
        "sort_by": validate_sort_value(defaults.get("sort_by", "submittedDate"), "defaults.sort_by"),
        "sort_order": validate_order_value(defaults.get("sort_order", "descending"), "defaults.sort_order"),
    }

    flattened: list[dict[str, object]] = []
    used_slugs: set[str] = set()
    topic_index = 0

    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("each group must be an object")
        group_name = group.get("name")
        if not isinstance(group_name, str) or not group_name.strip():
            raise ValueError("each group must define a non-empty name")
        topics = group.get("topics")
        if not isinstance(topics, list):
            raise ValueError(f"group {group_name} must define a topics list")

        for topic in topics:
            topic_index += 1
            if not isinstance(topic, dict):
                raise ValueError(f"group {group_name} contains an invalid topic entry")
            if topic.get("enabled", True) is False:
                continue

            topic_name = topic.get("name")
            query = topic.get("query")
            if not isinstance(topic_name, str) or not topic_name.strip():
                raise ValueError(f"group {group_name} has a topic without a non-empty name")
            if not isinstance(query, str) or not query.strip():
                raise ValueError(f"topic {topic_name} must define a non-empty query")

            raw_slug = topic.get("slug")
            if raw_slug is not None and (not isinstance(raw_slug, str) or not raw_slug.strip()):
                raise ValueError(f"topic {topic_name} has an invalid slug")
            base_slug = normalize_slug(raw_slug or query, f"topic-{topic_index}")
            topic_slug = base_slug
            suffix = 2
            while topic_slug in used_slugs:
                topic_slug = f"{base_slug}-{suffix}"
                suffix += 1
            used_slugs.add(topic_slug)

            per_topic_limit = validate_limit(
                topic.get("per_topic_limit", resolved_defaults["per_topic_limit"]),
                f"topic {topic_name} per_topic_limit",
            )

            flattened.append(
                {
                    "group_name": group_name.strip(),
                    "topic_name": topic_name.strip(),
                    "query": query.strip(),
                    "topic_slug": topic_slug,
                    "per_topic_limit": per_topic_limit,
                    "sort_by": resolved_defaults["sort_by"],
                    "sort_order": resolved_defaults["sort_order"],
                }
            )

    if not flattened:
        raise ValueError("topics config does not contain any enabled topics")
    return resolved_defaults, flattened


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"topics": {}}
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError("sync state must be a JSON object")
    topics = payload.get("topics")
    if not isinstance(topics, dict):
        raise ValueError("sync state topics must be an object")
    return payload


def determine_sync_window(
    *,
    daily: bool,
    topic_slug: str,
    state: dict,
    today_value: str,
    start_date: str | None,
    end_date: str | None,
) -> tuple[str | None, str | None, str]:
    if not daily:
        if not start_date or not end_date:
            raise ValueError("start_date and end_date are required when --daily is not used")
        return start_date, end_date, "backfill"

    topics_state = state.setdefault("topics", {})
    topic_state = topics_state.get(topic_slug, {})
    if not isinstance(topic_state, dict):
        topic_state = {}

    today_date = parse_iso_date(today_value, "today")
    previous_end = topic_state.get("end_date")
    if previous_end:
        previous_date = parse_iso_date(str(previous_end), f"state end_date for {topic_slug}")
        next_date = previous_date + timedelta(days=1)
        if next_date > today_date:
            return None, None, "up_to_date"
        return next_date.isoformat(), today_value, "daily"

    return today_value, today_value, "daily"


def build_paper_dir(root_dir: Path, topic_slug: str, capture_date: str, paper_id: str, title: str) -> Path:
    title_slug = normalize_slug(title, paper_id.replace("/", "-"))
    return root_dir / "topics" / topic_slug / capture_date / f"{safe_dir_name(paper_id)}__{title_slug}"


def paper_dir_complete(paper_dir: Path) -> bool:
    required = ["paper.pdf", "paper.md", "metadata.json", "summary.md"]
    return all((paper_dir / filename).exists() for filename in required)


def read_paper_sections(markdown_text: str) -> tuple[str, str]:
    abstract_match = re.search(r"## Abstract\s+(.*?)(?:\n## Full Text|\Z)", markdown_text, flags=re.DOTALL)
    full_text_match = re.search(r"## Full Text\s+(.*)\Z", markdown_text, flags=re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""
    full_text = full_text_match.group(1).strip() if full_text_match else ""
    return abstract, full_text


def split_sentences(text: str) -> list[str]:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    parts = re.split(r"(?<=[.!?])\s+", compact)
    return [part.strip() for part in parts if part.strip()]


def first_meaningful_paragraph(full_text: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", full_text) if block.strip()]
    for block in blocks:
        if block.startswith("#"):
            continue
        if len(block) >= 80:
            return re.sub(r"\s+", " ", block)
    for block in blocks:
        if not block.startswith("#"):
            return re.sub(r"\s+", " ", block)
    return ""


def heading_candidates(full_text: str) -> list[str]:
    headings = re.findall(r"^#{2,6}\s+(.*)$", full_text, flags=re.MULTILINE)
    return [heading.strip() for heading in headings if heading.strip()]


def build_summary_markdown(metadata: dict[str, object], paper_markdown: str) -> str:
    title = str(metadata.get("title") or "Untitled paper").strip()
    abstract, full_text = read_paper_sections(paper_markdown)
    sentences = split_sentences(abstract)
    takeaway = sentences[0] if sentences else f"This paper studies {title}."
    problem = " ".join(sentences[:2]) if sentences else (abstract or f"The paper is about {title}.")

    method_paragraph = first_meaningful_paragraph(full_text)
    if not method_paragraph:
        method_paragraph = "The converter could not recover enough full-text detail, so review paper.md for the full methodology."

    finding_items = sentences[2:5]
    if not finding_items:
        finding_items = heading_candidates(full_text)[:3]
    if not finding_items:
        finding_items = ["Review the abstract and paper.md for the primary empirical or conceptual findings."]

    limit_items = [
        "This summary is auto-generated from arXiv metadata, the abstract, and converted Markdown, so nuanced claims may be compressed.",
    ]
    if metadata.get("source_kind") == "abstract-only":
        limit_items.append("Only the abstract was available during conversion, so method and evidence details may be incomplete.")
    else:
        limit_items.append("Validate implementation details, dataset setup, and ablations against paper.md before relying on this summary.")

    follow_up_items = [
        "Which evaluation setup or benchmark best demonstrates the claimed gains?",
        "What assumptions or threat model boundaries matter most for real deployment?",
        "What evidence would you want to inspect next in paper.md before trusting the conclusions?",
    ]

    lines = [
        f"# {title}",
        "",
        SUMMARY_HEADINGS[0],
        "",
        takeaway,
        "",
        SUMMARY_HEADINGS[1],
        "",
        problem,
        "",
        SUMMARY_HEADINGS[2],
        "",
        method_paragraph,
        "",
        SUMMARY_HEADINGS[3],
        "",
    ]
    lines.extend([f"- {item}" for item in finding_items])
    lines.extend(
        [
            "",
            SUMMARY_HEADINGS[4],
            "",
        ]
    )
    lines.extend([f"- {item}" for item in limit_items])
    lines.extend(
        [
            "",
            SUMMARY_HEADINGS[5],
            "",
        ]
    )
    lines.extend([f"- {item}" for item in follow_up_items])
    return "\n".join(lines).strip() + "\n"


def build_summary_path(paper_dir: Path) -> Path:
    return paper_dir / "summary.md"


def build_existing_result(paper_id: str, paper_dir: Path, source_kind: str = "existing") -> dict[str, str]:
    return {
        "paper_id": paper_id,
        "output_dir": str(paper_dir),
        "paper_pdf": str(paper_dir / "paper.pdf"),
        "paper_md": str(paper_dir / "paper.md"),
        "metadata_json": str(paper_dir / "metadata.json"),
        "source_kind": source_kind,
    }


def render_manifest_markdown(manifest: dict) -> str:
    lines = [
        "# arXiv Topic Sync Run",
        "",
        f"- Mode: `{manifest['mode']}`",
        f"- Capture date: `{manifest['capture_date']}`",
        f"- Run timestamp: `{manifest['run_at']}`",
        f"- Root dir: `{manifest['root_dir']}`",
        f"- Start date: `{manifest['start_date']}`" if manifest.get("start_date") else "- Start date: none",
        f"- End date: `{manifest['end_date']}`" if manifest.get("end_date") else "- End date: none",
        f"- Topics processed: {len(manifest['topics'])}",
        f"- Papers captured: {len(manifest['papers'])}",
        "",
        "## Topics",
        "",
    ]

    if not manifest["topics"]:
        lines.append("No topics were processed.")
    else:
        for index, topic in enumerate(manifest["topics"], start=1):
            lines.extend(
                [
                    f"{index}. {topic['topic_name']} (`{topic['topic_slug']}`)",
                    f"   - Group: {topic['group_name']}",
                    f"   - Query: {topic['query']}",
                    f"   - Window: {topic.get('start_date') or 'none'} -> {topic.get('end_date') or 'none'}",
                    f"   - Status: {topic['status']}",
                    f"   - Returned results: {topic.get('returned_results', 0)}",
                    f"   - New papers: {topic.get('new_papers', 0)}",
                ]
            )
            if topic.get("search_results_md"):
                lines.append(f"   - Search results: {topic['search_results_md']}")
            if topic.get("error"):
                lines.append(f"   - Error: {topic['error']}")
            lines.append("")

    lines.extend(["## Papers", ""])
    if not manifest["papers"]:
        lines.append("No papers were captured in this run.")
    else:
        for index, paper in enumerate(manifest["papers"], start=1):
            lines.extend(
                [
                    f"{index}. {paper['title']} (`{paper['paper_id']}`)",
                    f"   - Topic: {paper['topic_name']} (`{paper['topic_slug']}`)",
                    f"   - Group: {paper['group_name']}",
                    f"   - Status: {paper['status']}",
                    f"   - Output dir: {paper['output_dir']}",
                    f"   - PDF: {paper['paper_pdf']}",
                    f"   - Markdown: {paper['paper_md']}",
                    f"   - Metadata: {paper['metadata_json']}",
                    f"   - Summary: {paper['summary_md']}",
                    "",
                ]
            )
    return "\n".join(lines).strip() + "\n"


def sync_topics(
    *,
    root_dir: Path,
    config_path: Path,
    daily: bool,
    start_date: str | None,
    end_date: str | None,
    timeout: float,
    capture_date: str | None = None,
) -> tuple[dict, int]:
    capture_value = capture_date or today_local()
    config = read_topics_config(config_path)
    _, topics = flatten_topics(config)
    state_path = root_dir / DEFAULT_STATE_NAME
    state = load_state(state_path)

    run_dir = root_dir / "runs" / capture_value
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "mode": "daily" if daily else "backfill",
        "capture_date": capture_value,
        "run_at": datetime.now().astimezone().isoformat(),
        "root_dir": str(root_dir),
        "config_path": str(config_path),
        "state_path": str(state_path),
        "start_date": start_date,
        "end_date": end_date,
        "topics": [],
        "papers": [],
    }

    failures = 0

    for topic in topics:
        topic_slug = str(topic["topic_slug"])
        topic_name = str(topic["topic_name"])
        group_name = str(topic["group_name"])
        query = str(topic["query"])
        limit = int(topic["per_topic_limit"])
        sort_by = str(topic["sort_by"])
        sort_order = str(topic["sort_order"])

        topic_record = {
            "group_name": group_name,
            "topic_name": topic_name,
            "topic_slug": topic_slug,
            "query": query,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "status": "pending",
            "start_date": None,
            "end_date": None,
            "search_results_json": None,
            "search_results_md": None,
            "total_results": 0,
            "returned_results": 0,
            "new_papers": 0,
            "skipped_papers": 0,
            "error": None,
        }
        manifest["topics"].append(topic_record)

        try:
            window_start, window_end, mode_label = determine_sync_window(
                daily=daily,
                topic_slug=topic_slug,
                state=state,
                today_value=capture_value,
                start_date=start_date,
                end_date=end_date,
            )
            topic_record["start_date"] = window_start
            topic_record["end_date"] = window_end

            if mode_label == "up_to_date":
                topic_record["status"] = "up_to_date"
                continue

            topic_dir = root_dir / "topics" / topic_slug / capture_value
            topic_dir.mkdir(parents=True, exist_ok=True)

            response = search_papers(
                query,
                start_date=window_start,
                end_date=window_end,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit,
                timeout=timeout,
            )
            search_outputs = write_search_outputs(topic_dir, response)
            topic_record["search_results_json"] = str(search_outputs["json"])
            topic_record["search_results_md"] = str(search_outputs["md"])
            topic_record["total_results"] = response.total_results
            topic_record["returned_results"] = response.returned_results

            for entry in response.entries:
                paper_dir = build_paper_dir(root_dir, topic_slug, capture_value, entry.paper_id, entry.title)
                summary_path = build_summary_path(paper_dir)
                if paper_dir_complete(paper_dir):
                    topic_record["skipped_papers"] += 1
                    result = build_existing_result(entry.paper_id, paper_dir)
                    paper_status = "existing"
                else:
                    extra_metadata = {
                        "topic_name": topic_name,
                        "topic_slug": topic_slug,
                        "group_name": group_name,
                        "capture_date": capture_value,
                        "summary_md": str(summary_path),
                    }
                    result = fetch_paper_to_directory(
                        entry.paper_id,
                        paper_dir,
                        timeout=timeout,
                        extra_metadata=extra_metadata,
                    )
                    paper_markdown = Path(result["paper_md"]).read_text(encoding="utf-8")
                    metadata_payload = load_json(Path(result["metadata_json"]))
                    summary_path.write_text(build_summary_markdown(metadata_payload, paper_markdown), encoding="utf-8")
                    topic_record["new_papers"] += 1
                    paper_status = "captured"

                manifest["papers"].append(
                    {
                        "group_name": group_name,
                        "topic_name": topic_name,
                        "topic_slug": topic_slug,
                        "capture_date": capture_value,
                        "paper_id": entry.paper_id,
                        "title": entry.title,
                        "status": paper_status,
                        "output_dir": result["output_dir"],
                        "paper_pdf": result["paper_pdf"],
                        "paper_md": result["paper_md"],
                        "metadata_json": result["metadata_json"],
                        "summary_md": str(summary_path),
                    }
                )

            topic_record["status"] = "success"
            if daily:
                state.setdefault("topics", {}).setdefault(topic_slug, {})
                state["topics"][topic_slug] = {
                    "end_date": window_end,
                    "updated_at": manifest["run_at"],
                }
        except Exception as error:
            failures += 1
            topic_record["status"] = "failed"
            topic_record["error"] = str(error)

    manifest_path_json = run_dir / "run_manifest.json"
    manifest_path_md = run_dir / "run_manifest.md"
    write_json(manifest_path_json, manifest)
    manifest_path_md.write_text(render_manifest_markdown(manifest), encoding="utf-8")

    if daily:
        write_json(state_path, state)

    exit_code = 1 if failures else 0
    return {
        "mode": manifest["mode"],
        "root_dir": str(root_dir),
        "config_path": str(config_path),
        "state_path": str(state_path),
        "capture_date": capture_value,
        "start_date": start_date,
        "end_date": end_date,
        "run_manifest_json": str(manifest_path_json),
        "run_manifest_md": str(manifest_path_md),
        "topics_processed": len(manifest["topics"]),
        "papers_captured": len(manifest["papers"]),
        "failures": failures,
    }, exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sync configured arXiv keyword topics into a daily local archive.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              python sync_arxiv_topics.py --daily
              python sync_arxiv_topics.py --start-date 2026-03-01 --end-date 2026-03-07
              python sync_arxiv_topics.py --daily --root-dir ./artifacts/arxiv-monitor
            """
        ),
    )
    parser.add_argument("--daily", action="store_true", help="run the stateful daily sync workflow")
    parser.add_argument("--start-date", default=None, help="inclusive submittedDate lower bound in YYYY-MM-DD")
    parser.add_argument("--end-date", default=None, help="inclusive submittedDate upper bound in YYYY-MM-DD")
    parser.add_argument("--root-dir", type=Path, default=DEFAULT_ROOT_DIR, help="root archive directory")
    parser.add_argument("--timeout", type=float, default=30.0, help="network timeout in seconds")
    args = parser.parse_args(argv)

    if args.daily and (args.start_date or args.end_date):
        print("error: --daily cannot be combined with --start-date/--end-date", file=sys.stderr)
        return 1
    if not args.daily and (not args.start_date or not args.end_date):
        print("error: either use --daily or provide both --start-date and --end-date", file=sys.stderr)
        return 1

    config_path = args.root_dir / DEFAULT_TOPICS_NAME
    try:
        result, exit_code = sync_topics(
            root_dir=args.root_dir,
            config_path=config_path,
            daily=args.daily,
            start_date=args.start_date,
            end_date=args.end_date,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False))
        return exit_code
    except Exception as error:  # pragma: no cover - surfaced in CLI output
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
