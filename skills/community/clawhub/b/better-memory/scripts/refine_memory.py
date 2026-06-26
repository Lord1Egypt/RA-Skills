#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
import json
import re
from pathlib import Path
from textwrap import dedent

from memory_os_common import (
    MANAGED_MEMORY_BLOCK_END,
    MANAGED_MEMORY_BLOCK_START,
    load_settings,
    load_state,
    save_state,
    sidecar_dir,
    upsert_marked_block,
)

ENTRY_RE = re.compile(
    r"^- \[(?P<date>\d{4}-\d{2}-\d{2})\|(?P<id>M-\d{8}-\d{3})\|"
    r"(?P<kind>experience|value|standard|preference)\|(?P<axis>[a-z]+)\|"
    r"(?P<status>active|candidate|stale|conflicted|superseded)\|"
    r"(?P<confidence>low|medium|high)\|(?P<topic>[^\]]+)\] (?P<statement>.+)$"
)
ENTRY_ID_RE = re.compile(r"^M-(?P<ymd>\d{8})-(?P<seq>\d{3})$")

KIND_ALIAS = {"preference": "value"}
KIND_ORDER = ("experience", "value", "standard")


@dataclass
class Entry:
    entry_date: date
    entry_id: str
    kind: str
    axis: str
    status: str
    confidence: str
    topic: str
    statement: str
    path: Path
    line_index: int

    def to_line(self) -> str:
        return (
            f"- [{self.entry_date.isoformat()}|{self.entry_id}|{self.kind}|"
            f"{self.axis}|{self.status}|{self.confidence}|{self.topic}] {self.statement}"
        )


def normalize_kind(kind: str) -> str:
    return KIND_ALIAS.get(kind, kind)


def parse_entry_id(entry_id: str) -> tuple[int, int]:
    match = ENTRY_ID_RE.match(entry_id)
    if not match:
        return (0, 0)
    return (int(match.group("ymd")), int(match.group("seq")))


def parse_entries(workspace: Path) -> tuple[list[Entry], dict[Path, list[str]]]:
    entries: list[Entry] = []
    file_lines: dict[Path, list[str]] = {}
    memory_dir = workspace / "memory"
    if not memory_dir.exists():
        return entries, file_lines

    for path in sorted(memory_dir.glob("20??-??-??.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        file_lines[path] = lines
        for idx, line in enumerate(lines):
            match = ENTRY_RE.match(line)
            if not match:
                continue
            payload = match.groupdict()
            entries.append(
                Entry(
                    entry_date=date.fromisoformat(payload["date"]),
                    entry_id=payload["id"],
                    kind=normalize_kind(payload["kind"]),
                    axis=payload["axis"],
                    status=payload["status"],
                    confidence=payload["confidence"],
                    topic=payload["topic"].strip().lower(),
                    statement=payload["statement"].strip(),
                    path=path,
                    line_index=idx,
                )
            )
    entries.sort(key=lambda item: (item.entry_date, parse_entry_id(item.entry_id)))
    return entries, file_lines


def apply_stale_status(entries: list[Entry], stale_days: int, file_lines: dict[Path, list[str]]) -> int:
    cutoff = date.today() - timedelta(days=stale_days)
    touched = 0
    for entry in entries:
        if entry.status != "active":
            continue
        if entry.entry_date >= cutoff:
            continue
        entry.status = "stale"
        file_lines[entry.path][entry.line_index] = entry.to_line()
        touched += 1
    return touched


def write_modified_files(file_lines: dict[Path, list[str]]) -> None:
    for path, lines in file_lines.items():
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def detect_contradictions(entries: list[Entry]) -> dict[tuple[str, str], list[Entry]]:
    grouped: dict[tuple[str, str], list[Entry]] = defaultdict(list)
    for entry in entries:
        if entry.status not in {"active", "candidate"}:
            continue
        grouped[(entry.kind, entry.topic)].append(entry)

    conflicts: dict[tuple[str, str], list[Entry]] = {}
    for key, group in grouped.items():
        kind, _topic = key
        axes = {item.axis for item in group}
        if kind == "value" and {"good", "bad"} <= axes:
            conflicts[key] = group
        if kind == "standard" and {"right", "wrong"} <= axes:
            conflicts[key] = group
    return conflicts


def cluster_entries(entries: list[Entry]) -> dict[str, dict[str, list[Entry]]]:
    clusters: dict[str, dict[str, list[Entry]]] = defaultdict(lambda: defaultdict(list))
    seen: set[tuple[str, str, str]] = set()
    for entry in entries:
        if entry.status not in {"active", "candidate"}:
            continue
        statement_key = " ".join(entry.statement.lower().split())
        dedupe_key = (entry.kind, entry.topic, statement_key)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        clusters[entry.kind][entry.topic].append(entry)
    for by_topic in clusters.values():
        for topic in by_topic:
            by_topic[topic].sort(key=lambda item: (item.entry_date, parse_entry_id(item.entry_id)))
    return clusters


def format_axis_mix(group: list[Entry]) -> str:
    counts = Counter(item.axis for item in group)
    return ", ".join(f"{axis}({count})" for axis, count in sorted(counts.items()))


def build_l2_snapshot(
    clusters: dict[str, dict[str, list[Entry]]],
    conflicts: dict[tuple[str, str], list[Entry]],
    stale_entries: list[Entry],
) -> dict:
    by_kind: dict[str, dict] = {}
    for kind in KIND_ORDER:
        by_kind[kind] = {}
        for topic, group in sorted(clusters.get(kind, {}).items()):
            canonical = group[-1]
            by_kind[kind][topic] = {
                "evidence_count": len(group),
                "last_seen": canonical.entry_date.isoformat(),
                "axis_mix": format_axis_mix(group),
                "canonical_statement": canonical.statement,
                "supporting_ids": [item.entry_id for item in group[-8:]],
                "axes": sorted({item.axis for item in group}),
                "has_conflict": (kind, topic) in conflicts,
            }

    conflict_items = []
    for (kind, topic), group in sorted(conflicts.items()):
        conflict_items.append(
            {
                "kind": kind,
                "topic": topic,
                "axes": sorted({item.axis for item in group}),
                "ids": [item.entry_id for item in group],
            }
        )

    stale_items = [
        {
            "entry_id": entry.entry_id,
            "kind": entry.kind,
            "topic": entry.topic,
            "entry_date": entry.entry_date.isoformat(),
            "statement": entry.statement,
        }
        for entry in stale_entries[:100]
    ]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "by_kind": by_kind,
        "conflicts": conflict_items,
        "stale_candidates": stale_items,
    }


def render_l2(kind: str, snapshot: dict) -> str:
    title = kind.capitalize()
    lines = [
        f"# {title} Memory (L2)",
        "",
        f"Updated: {date.today().isoformat()}",
        "",
    ]
    topics = snapshot.get("by_kind", {}).get(kind, {})
    if not topics:
        lines.extend(["- (no active entries)", ""])
        return "\n".join(lines)

    for topic in sorted(topics):
        row = topics[topic]
        lines.extend(
            [
                f"## {topic}",
                f"- Evidence count: {row['evidence_count']}",
                f"- Last seen: {row['last_seen']}",
                f"- Axis mix: {row['axis_mix']}",
                f"- Canonical: {row['canonical_statement']}",
                f"- Supporting IDs: {', '.join(row['supporting_ids']) if row['supporting_ids'] else '(none)'}",
                f"- Conflict: {'yes' if row['has_conflict'] else 'no'}",
                "",
            ]
        )
    return "\n".join(lines)


def write_l2_files(workspace: Path, snapshot: dict) -> list[Path]:
    l2_dir = sidecar_dir(workspace) / "l2"
    l2_dir.mkdir(parents=True, exist_ok=True)
    changed: list[Path] = []
    for kind in KIND_ORDER:
        path = l2_dir / f"{kind}.md"
        content = render_l2(kind, snapshot).rstrip() + "\n"
        path.write_text(content, encoding="utf-8")
        changed.append(path)

    summary_path = l2_dir / "summary.json"
    summary_path.write_text(json.dumps(snapshot, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    changed.append(summary_path)
    return changed


def read_l2_snapshot(workspace: Path) -> dict | None:
    path = sidecar_dir(workspace) / "l2" / "summary.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def render_l3_block_from_snapshot(snapshot: dict, settings: dict) -> str:
    max_l3_per_kind = settings["max_l3_per_kind"]
    min_evidence_for_l3 = settings["min_evidence_for_l3"]

    def section(kind: str, heading: str) -> list[str]:
        lines = [f"## {heading}"]
        topics = snapshot.get("by_kind", {}).get(kind, {})
        if not topics:
            lines.append("- (empty)")
            lines.append("")
            return lines

        ranked = sorted(
            topics.items(),
            key=lambda item: (item[1]["evidence_count"], item[1]["last_seen"]),
            reverse=True,
        )

        emitted = 0
        for topic, row in ranked:
            if row["evidence_count"] < min_evidence_for_l3:
                continue
            lines.append(
                f"- {topic}: {row['canonical_statement']} "
                f"(axes={','.join(row['axes'])}, evidence={row['evidence_count']}, last={row['last_seen']})"
            )
            emitted += 1
            if emitted >= max_l3_per_kind:
                break
        if emitted == 0:
            lines.append("- (empty)")
        lines.append("")
        return lines

    output = [MANAGED_MEMORY_BLOCK_START]
    output.extend(section("experience", "L3 Experience"))
    output.extend(section("value", "L3 Values"))
    output.extend(section("standard", "L3 Standards"))

    output.append("## Contradictions To Resolve")
    conflicts = snapshot.get("conflicts", [])
    if conflicts:
        for item in conflicts:
            output.append(
                f"- {item['kind']}/{item['topic']}: axes={','.join(item['axes'])}; ids={','.join(item['ids'])}"
            )
    else:
        output.append("- (none)")
    output.append("")

    output.append("## Stale Candidates")
    stale_candidates = snapshot.get("stale_candidates", [])
    if stale_candidates:
        for item in stale_candidates[:20]:
            output.append(
                f"- {item['entry_id']} | {item['kind']}/{item['topic']} | "
                f"{item['entry_date']} | {item['statement']}"
            )
    else:
        output.append("- (none)")
    output.append("")

    output.append("## Last Distillation")
    output.append(f"- Generated at {datetime.now().isoformat(timespec='seconds')}")
    output.append(MANAGED_MEMORY_BLOCK_END)
    output.append("")
    return "\n".join(output)


def write_memory_md(workspace: Path, l3_block: str) -> Path:
    memory_path = workspace / "MEMORY.md"
    if memory_path.exists():
        original = memory_path.read_text(encoding="utf-8")
    else:
        original = dedent(
            """
            # MEMORY.md (L3 Long-Term Memory)

            This file stores distilled long-term memory only.
            """
        ).strip() + "\n"
    original = original.replace("## L3 Preferences", "## L3 Values")
    updated = upsert_marked_block(original, MANAGED_MEMORY_BLOCK_START, MANAGED_MEMORY_BLOCK_END, l3_block)
    memory_path.write_text(updated, encoding="utf-8")
    return memory_path


def write_review_file(workspace: Path, conflicts: dict[tuple[str, str], list[Entry]], stale_entries: list[Entry], stale_days: int) -> Path:
    reviews_dir = sidecar_dir(workspace) / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    review_path = reviews_dir / f"{date.today().isoformat()}.md"

    lines = [
        f"# Memory Review {date.today().isoformat()}",
        "",
        f"- stale_days_threshold: {stale_days}",
        f"- contradictions: {len(conflicts)}",
        f"- stale_candidates: {len(stale_entries)}",
        "",
        "## Contradictions",
    ]
    if conflicts:
        for (kind, topic), group in sorted(conflicts.items()):
            ids = ", ".join(item.entry_id for item in group)
            axes = ", ".join(sorted({item.axis for item in group}))
            lines.append(f"- {kind}/{topic}: axes={axes}; ids={ids}")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Stale Candidates"])
    if stale_entries:
        for entry in stale_entries[:50]:
            lines.append(
                f"- {entry.entry_id} | {entry.kind}/{entry.topic} | "
                f"{entry.entry_date.isoformat()} | {entry.statement}"
            )
    else:
        lines.append("- (none)")
    lines.append("")

    review_path.write_text("\n".join(lines), encoding="utf-8")
    return review_path


def last_cursor_key_from_state(state: dict) -> tuple[int, int]:
    cursor = state.get("last_processed_l1_entry_id")
    if not cursor:
        return (0, 0)
    return parse_entry_id(cursor)


def run_daily_review(
    workspace: Path,
    *,
    stale_days: int | None = None,
    entry_threshold: int | None = None,
    threshold_only: bool = False,
    apply_stale: bool = False,
) -> dict:
    settings = load_settings(workspace)
    state = load_state(workspace)
    stale_days_value = stale_days if stale_days is not None else settings["stale_days"]
    threshold_value = entry_threshold if entry_threshold is not None else settings["l1_entry_threshold"]

    entries, file_lines = parse_entries(workspace)
    cursor_key = last_cursor_key_from_state(state)
    new_entries = [entry for entry in entries if parse_entry_id(entry.entry_id) > cursor_key]

    if threshold_only and len(new_entries) < threshold_value:
        return {
            "workspace": str(workspace),
            "executed": False,
            "reason": "threshold_not_met",
            "new_entries": len(new_entries),
            "entry_threshold": threshold_value,
        }

    changed_stale = 0
    if apply_stale and entries:
        changed_stale = apply_stale_status(entries, stale_days_value, file_lines)
        if changed_stale:
            write_modified_files(file_lines)

    stale_cutoff = date.today() - timedelta(days=stale_days_value)
    stale_entries = [entry for entry in entries if entry.status == "active" and entry.entry_date < stale_cutoff]
    conflicts = detect_contradictions(entries)
    clusters = cluster_entries(entries)
    snapshot = build_l2_snapshot(clusters, conflicts, stale_entries)
    l2_paths = write_l2_files(workspace, snapshot)
    review_path = write_review_file(workspace, conflicts, stale_entries, stale_days_value)

    latest_id = entries[-1].entry_id if entries else state.get("last_processed_l1_entry_id")
    save_state(
        workspace,
        {
            "last_daily_review_at": datetime.now().isoformat(timespec="seconds"),
            "last_processed_l1_entry_id": latest_id,
        },
    )

    return {
        "workspace": str(workspace),
        "executed": True,
        "new_entries": len(new_entries),
        "entry_threshold": threshold_value,
        "threshold_triggered": len(new_entries) >= threshold_value,
        "stale_statuses_changed": changed_stale,
        "l2_files": [str(path) for path in l2_paths],
        "review_file": str(review_path),
    }


def run_weekly_rollup(workspace: Path) -> dict:
    settings = load_settings(workspace)
    snapshot = read_l2_snapshot(workspace)
    if snapshot is None:
        run_daily_review(workspace, apply_stale=False, threshold_only=False)
        snapshot = read_l2_snapshot(workspace)
    if snapshot is None:
        raise SystemExit("Unable to build L2 snapshot for weekly rollup.")

    l3_block = render_l3_block_from_snapshot(snapshot, settings)
    memory_path = write_memory_md(workspace, l3_block)
    save_state(workspace, {"last_weekly_rollup_at": datetime.now().isoformat(timespec="seconds")})

    return {
        "workspace": str(workspace),
        "memory_file": str(memory_path),
        "topics_experience": len(snapshot.get("by_kind", {}).get("experience", {})),
        "topics_value": len(snapshot.get("by_kind", {}).get("value", {})),
        "topics_standard": len(snapshot.get("by_kind", {}).get("standard", {})),
        "conflicts": len(snapshot.get("conflicts", [])),
    }


def run_monthly_review(workspace: Path) -> dict:
    settings = load_settings(workspace)
    entries, _file_lines = parse_entries(workspace)
    conflicts = detect_contradictions(entries)

    by_topic: dict[tuple[str, str], list[Entry]] = defaultdict(list)
    by_statement: dict[tuple[str, str, str], list[Entry]] = defaultdict(list)
    for entry in entries:
        by_topic[(entry.kind, entry.topic)].append(entry)
        statement_key = " ".join(entry.statement.lower().split())
        by_statement[(entry.kind, entry.topic, statement_key)].append(entry)

    bloat_topics = [
        (kind, topic, len(group))
        for (kind, topic), group in by_topic.items()
        if len(group) > settings["max_l3_per_kind"]
    ]
    redundant_groups = [
        (kind, topic, statement, len(group))
        for (kind, topic, statement), group in by_statement.items()
        if len(group) > 1
    ]
    stale_cutoff = date.today() - timedelta(days=settings["stale_days"])
    stale_or_superseded = [
        entry
        for entry in entries
        if entry.status in {"stale", "superseded"} or (entry.status == "active" and entry.entry_date < stale_cutoff)
    ]

    reviews_dir = sidecar_dir(workspace) / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    month_slug = date.today().strftime("%Y-%m")
    report_path = reviews_dir / f"monthly-{month_slug}.md"
    plan_path = reviews_dir / f"monthly-{month_slug}-plan.json"

    id_to_entry = {entry.entry_id: entry for entry in entries}
    plan_actions: list[dict] = []

    for (kind, topic), group in sorted(conflicts.items()):
        target_ids = [entry.entry_id for entry in group if entry.status in {"active", "candidate"}]
        if not target_ids:
            continue
        plan_actions.append(
            {
                "id": f"conflict-{kind}-{topic}",
                "enabled": False,
                "type": "mark_conflicted",
                "reason": f"conflict axes in {kind}/{topic}",
                "kind": kind,
                "topic": topic,
                "target_entry_ids": target_ids,
            }
        )

    for kind, topic, statement, _count in sorted(redundant_groups, key=lambda item: item[3], reverse=True):
        dup_group = [
            entry
            for entry in entries
            if entry.kind == kind
            and entry.topic == topic
            and " ".join(entry.statement.lower().split()) == statement
        ]
        if len(dup_group) < 2:
            continue
        dup_group.sort(key=lambda item: (item.entry_date, parse_entry_id(item.entry_id)))
        keep = dup_group[-1]
        target_ids = [entry.entry_id for entry in dup_group[:-1] if entry.status in {"active", "candidate"}]
        if not target_ids:
            continue
        plan_actions.append(
            {
                "id": f"dedupe-{kind}-{topic}-{keep.entry_id}",
                "enabled": False,
                "type": "mark_superseded",
                "reason": f"redundant statements under {kind}/{topic}",
                "kind": kind,
                "topic": topic,
                "keep_entry_id": keep.entry_id,
                "target_entry_ids": target_ids,
            }
        )

    for entry in entries:
        if entry.entry_id not in id_to_entry:
            continue
        if entry.status != "active":
            continue
        if entry.entry_date >= stale_cutoff:
            continue
        plan_actions.append(
            {
                "id": f"stale-{entry.entry_id}",
                "enabled": False,
                "type": "mark_stale",
                "reason": f"older than stale_days={settings['stale_days']}",
                "kind": entry.kind,
                "topic": entry.topic,
                "target_entry_ids": [entry.entry_id],
            }
        )

    lines = [
        f"# Monthly Memory Review {date.today().strftime('%Y-%m')}",
        "",
        "This report is advisory only. No automatic cleanup has been applied.",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- total_entries: {len(entries)}",
        f"- conflicts: {len(conflicts)}",
        f"- bloat_topics: {len(bloat_topics)}",
        f"- redundant_statement_groups: {len(redundant_groups)}",
        f"- stale_or_superseded_candidates: {len(stale_or_superseded)}",
        f"- cleanup_plan_actions: {len(plan_actions)}",
        "",
        "## Conflict Groups",
    ]
    if conflicts:
        for (kind, topic), group in sorted(conflicts.items()):
            ids = ", ".join(item.entry_id for item in group)
            axes = ", ".join(sorted({item.axis for item in group}))
            lines.append(f"- {kind}/{topic}: axes={axes}; ids={ids}")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Bloat Topic Candidates"])
    if bloat_topics:
        for kind, topic, count in sorted(bloat_topics, key=lambda item: item[2], reverse=True)[:30]:
            lines.append(f"- {kind}/{topic}: evidence_count={count} (suggest topic-level merge)")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Redundant Statement Groups"])
    if redundant_groups:
        for kind, topic, statement, count in sorted(redundant_groups, key=lambda item: item[3], reverse=True)[:30]:
            lines.append(f"- {kind}/{topic}: repeated={count} :: {statement}")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Stale or Superseded Candidates"])
    if stale_or_superseded:
        for entry in stale_or_superseded[:60]:
            lines.append(
                f"- {entry.entry_id} | {entry.kind}/{entry.topic} | {entry.status} | "
                f"{entry.entry_date.isoformat()} | {entry.statement}"
            )
    else:
        lines.append("- (none)")

    lines.extend(
        [
            "",
            "## Suggested Cleanup Conversation",
            "1. Confirm whether each conflict should resolve to one axis or remain contextual.",
            "2. Merge or supersede repeated statements under the same topic.",
            "3. Archive stale entries that are no longer useful.",
            "4. Re-run weekly rollup after manual decisions.",
            "",
            "## Cleanup Plan",
            f"- Plan file: `{plan_path}`",
            "- All actions are disabled by default.",
            "- Enable selected actions in plan JSON, then apply with:",
            "  `python3 skills/better-memory/scripts/apply_monthly_cleanup.py --workspace . --rerollup`",
            "",
        ]
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")
    plan_payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "month": month_slug,
        "workspace": str(workspace),
        "report_file": str(report_path),
        "actions": plan_actions,
    }
    plan_path.write_text(json.dumps(plan_payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    save_state(workspace, {"last_monthly_review_at": datetime.now().isoformat(timespec="seconds")})

    return {
        "workspace": str(workspace),
        "report_file": str(report_path),
        "plan_file": str(plan_path),
        "conflicts": len(conflicts),
        "bloat_topics": len(bloat_topics),
        "redundant_groups": len(redundant_groups),
        "stale_or_superseded": len(stale_or_superseded),
        "plan_actions": len(plan_actions),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compatibility wrapper: run daily review and weekly rollup (L1 -> L2 -> L3)."
    )
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--stale-days", type=int, help="Days after which active memory becomes stale candidate")
    parser.add_argument("--apply-stale", action="store_true", help="Update old active entries to stale status in L1 files")
    parser.add_argument("--entry-threshold", type=int, help="Threshold for new L1 entries")
    parser.add_argument("--threshold-only", action="store_true", help="Skip daily review when new entries are below threshold")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    daily = run_daily_review(
        workspace,
        stale_days=args.stale_days,
        entry_threshold=args.entry_threshold,
        threshold_only=args.threshold_only,
        apply_stale=args.apply_stale,
    )
    if not daily["executed"]:
        print(f"Workspace: {workspace}")
        print("Daily review skipped.")
        print(f"Reason: {daily['reason']}")
        print(f"New entries: {daily['new_entries']}")
        print(f"Entry threshold: {daily['entry_threshold']}")
        return 0

    weekly = run_weekly_rollup(workspace)
    print(f"Workspace: {workspace}")
    print(f"Daily review executed: {daily['executed']}")
    print(f"New entries: {daily['new_entries']}")
    print(f"Threshold triggered: {daily['threshold_triggered']}")
    print(f"Stale statuses changed: {daily['stale_statuses_changed']}")
    print(f"Daily review file: {daily['review_file']}")
    print(f"Weekly rollup memory file: {weekly['memory_file']}")
    print(
        "Weekly topics: "
        f"experience={weekly['topics_experience']}, value={weekly['topics_value']}, standard={weekly['topics_standard']}"
    )
    print(f"Conflicts: {weekly['conflicts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
