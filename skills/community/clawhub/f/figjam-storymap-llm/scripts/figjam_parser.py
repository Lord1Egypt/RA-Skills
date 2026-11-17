"""
figjam_parser.py
================
FigJam Story Map parser (Jeff Patton methodology) -> Markdown / JSON.

Reads a FigJam board via the Figma REST API, groups stickies / shapes into
sections, maps User Stories to Tasks algorithmically by the X axis, and
renders a structured Markdown / JSON output. From there you can convert it to
a Notion page, Linear/Jira CSV import, or paste it into a coding agent
(Cursor, Claude Code, Copilot) as living spec.

Usage:
    python figjam_parser.py --file-key {FILE_KEY} --token $FIGMA_TOKEN > story-map.md
    python figjam_parser.py --file-key {FILE_KEY} --token $FIGMA_TOKEN --format json > story-map.json
    python figjam_parser.py --input saved-board.json > story-map.md

Requirements:
    pip install requests

License: MIT
Author: Monika Zapisek
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import requests


# Force UTF-8 stdout / stderr on Windows so emoji and non-ASCII sticky text
# (e.g. LINE SEPARATOR \u2028 used by FigJam) don't crash cp1252 encoding.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


FIGMA_API_BASE = "https://api.figma.com/v1/files/{file_key}"

# Canonical sections (order matters for rendering)
SECTION_ROOT = "[STORY_MAP]"
SECTION_AI_README = "[00_SECTION_AI_Readme]"
SECTION_PERSONA = "[USER_SEGMENT_or_PERSONA]"
SECTION_BACKBONE_ACTIVITIES = "[01_SECTION_BACKBONE_Activities]"
SECTION_BACKBONE_TASKS = "[02_SECTION_BACKBONE_User_Tasks]"
RELEASE_SECTION_PREFIX = "[0"  # [03_..., [04_..., [05_... — releases

# Taxonomy tags on stickies
TAG_STORY = "[STORY]"
TAG_ACT = "[ACT_"
TAG_TASK = "[TASK_"
TAG_RELEASE = re.compile(r"\[V([123])\]")
# Priority tag may have an emoji prefix inside the brackets: [P1], [💓P1], [💛P2], [💙P3].
# We match any 1-3 non-`]` characters (the emoji + optional space) before the P[n].
TAG_PRIORITY = re.compile(r"\[[^\]]{0,6}?P([123])\]")
TAG_OWNER = re.compile(r"@(UX|DEV|PM|QA)", re.IGNORECASE)

# Emoji ranges to strip from rendered Markdown output (keep parser output plain ASCII text).
# Covers common symbol ranges used as decorative prefixes on FigJam stickies.
EMOJI_STRIP = re.compile(
    "["
    "\U0001F000-\U0001FAFF"   # symbols & pictographs (hearts, stars, badges, etc.)
    "\U00002600-\U000027BF"   # misc symbols (✓ ✗ ✦ ✶ ☀ ☁)
    "\U00002B00-\U00002BFF"   # misc arrows/symbols
    "\U0001F1E6-\U0001F1FF"   # regional indicators (flags)
    "\U0000FE00-\U0000FE0F"   # variation selectors (VS15/Vs16 — usually trailing on emoji)
    "\U0000200B-\U0000200F"   # zero-width spaces (don't render, but pollute output)
    "\U00002028-\U0000202E"   # LINE SEPARATOR, PARAGRAPH SEPARATOR and friends
    "]+",
    flags=re.UNICODE,
)

# Max distance (px) between a story center-X and the nearest task center-X
# for the fallback assignment to be considered valid. Above this, the story
# is flagged as UNASSIGNED instead of being force-mapped.
X_MAPPING_MAX_DISTANCE_PX = 400

# Retry configuration for Figma API rate limiting (HTTP 429 / 5xx).
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2.0


@dataclass
class StickyItem:
    """A single sticky on the FigJam canvas (STICKY or SHAPE_WITH_TEXT)."""

    id: str
    text: str
    x: float
    y: float
    width: float
    height: float
    color: Optional[str] = None
    section_id: Optional[str] = None
    section_name: Optional[str] = None
    # Result fields (populated after mapping)
    release: Optional[str] = None
    priority: Optional[str] = None
    owner: Optional[str] = None
    acceptance_criteria: List[str] = field(default_factory=list)
    story_sentence: Optional[str] = None
    mapped_task_id: Optional[str] = None
    mapped_activity_id: Optional[str] = None

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2


@dataclass
class TaskItem:
    """A [TASK_XX] from the backbone — defines a column on the X axis."""

    id: str
    name: str
    x: float
    y: float
    width: float
    height: float
    activity_id: Optional[str] = None

    def contains_x(self, x: float) -> bool:
        return self.x <= x <= self.x + self.width

    def distance_to_center(self, x: float) -> float:
        center = self.x + self.width / 2
        return abs(x - center)

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2


@dataclass
class ActivityItem:
    """An [ACT_XX] from the backbone — User Activity (major user goal)."""

    id: str
    name: str
    x: float
    y: float
    width: float
    height: float

    def contains_x(self, x: float) -> bool:
        return self.x <= x <= self.x + self.width

    def distance_to_center(self, x: float) -> float:
        center = self.x + self.width / 2
        return abs(x - center)


@dataclass
class Connector:
    """A relation between stickies via a native FigJam Connector."""

    from_id: Optional[str]
    to_id: Optional[str]
    label: str = "CONNECTS_TO"


def fetch_figjam(file_key: str, token: str) -> Dict[str, Any]:
    """Fetch the FigJam object tree via Figma REST API with retry on 429 / 5xx."""
    url = FIGMA_API_BASE.format(file_key=file_key)
    headers = {"X-Figma-Token": token}

    last_err: Optional[requests.HTTPError] = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exc:
            last_err = exc
            status = exc.response.status_code if exc.response is not None else 0
            if status == 404:
                print(
                    f"ERROR: Figma file not found (404). Check the --file-key value: {file_key!r}.",
                    file=sys.stderr,
                )
                sys.exit(2)
            if status == 403:
                print(
                    "ERROR: Figma API returned 403. Check that FIGMA_TOKEN is valid and has access to the file.",
                    file=sys.stderr,
                )
                sys.exit(2)
            if status in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_SECONDS * (2 ** attempt)
                print(
                    f"WARN: Figma API returned {status}. Retrying in {wait:.1f}s (attempt {attempt + 1}/{MAX_RETRIES})...",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise
        except requests.RequestException as exc:
            print(f"ERROR: network error fetching Figma file: {exc}", file=sys.stderr)
            sys.exit(2)

    # Should not reach here, but keep type-checker happy.
    if last_err is not None:
        raise last_err
    raise RuntimeError("Unreachable: fetch_figjam exited without data or error.")


def get_bbox(node: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """Extract (x, y, width, height) from absoluteBoundingBox or layout.locationRelativeToParent."""
    bbox = node.get("absoluteBoundingBox") or {}
    if bbox:
        return (
            float(bbox.get("x", 0)),
            float(bbox.get("y", 0)),
            float(bbox.get("width", 0)),
            float(bbox.get("height", 0)),
        )
    layout = node.get("layout") or {}
    loc = layout.get("locationRelativeToParent") or {}
    dims = layout.get("dimensions") or {}
    return (
        float(loc.get("x", 0)),
        float(loc.get("y", 0)),
        float(dims.get("width", 0)),
        float(dims.get("height", 0)),
    )


def get_text(node: Dict[str, Any]) -> str:
    """Extract text from the `characters` field."""
    return (node.get("characters") or "").strip()


def _color_to_hex(color: Dict[str, Any]) -> Optional[str]:
    """Convert a Figma API color dict (r/g/b/a in 0-1 floats) to #RRGGBB hex."""
    try:
        r = int(round(float(color.get("r", 0)) * 255))
        g = int(round(float(color.get("g", 0)) * 255))
        b = int(round(float(color.get("b", 0)) * 255))
        return f"#{r:02X}{g:02X}{b:02X}"
    except (TypeError, ValueError):
        return None


def get_color(node: Dict[str, Any]) -> Optional[str]:
    """Extract the first solid fill color as a #RRGGBB hex string, or None."""
    fills = node.get("fills") or []
    if not isinstance(fills, list) or not fills:
        return None
    first = fills[0]
    # Figma REST API returns fills as dicts; a string would be a ref (not a color).
    if not isinstance(first, dict):
        return None
    if first.get("type") not in ("SOLID", None):
        # First fill is an image / gradient; look for a SOLID among remaining fills.
        for f in fills[1:]:
            if isinstance(f, dict) and f.get("type") == "SOLID":
                first = f
                break
        else:
            return None
    color = first.get("color")
    if not isinstance(color, dict):
        return None
    return _color_to_hex(color)


def is_release_section(name: str) -> bool:
    """Return True if the section is a Release section (V1/V2/V3 or any later release index)."""
    # Matches [03_..., [04_..., [05_..., and any higher index like [06_, [07_, ...
    return bool(re.match(r"^\[\d{2}_SECTION_Release_\d+", name))


def parse_release_from_section(name: str) -> Optional[str]:
    """Parse V1/V2/V3 from a release section name. Falls back to index-based inference."""
    match = re.search(r"\[V([123])\]", name) or re.search(r"Release\s*([123])", name, re.IGNORECASE)
    if match:
        return f"V{match.group(1)}"
    # Infer from section index: [03_ -> V1, [04_ -> V2, [05_ -> V3.
    match = re.match(r"^\[(\d{2})_SECTION_Release_(\d+)", name)
    if match:
        return f"V{match.group(2)}"
    return None


def clean_name(name: str) -> str:
    """Normalize a sticky / task / activity name: strip emoji, collapse whitespace + newlines.

    FigJam sticky `characters` often contain literal newlines between the tag and the label
    (e.g. `[TASK_01]\\nTask`), emoji prefixes inside priority brackets (`[💓P1]`), and
    LINE SEPARATOR / PARAGRAPH SEPARATOR codepoints from rich text. This helper returns a
    single-line, emoji-free, whitespace-collapsed string for display in Markdown.
    """
    if not name:
        return ""
    s = EMOJI_STRIP.sub("", name)
    s = re.sub(r"[\u2028\u2029]+", " ", s)
    s = re.sub(r"\s*\\n\s*", " ", s)  # literal "\n" if it ever appears as text
    s = re.sub(r"\s*\n\s*", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_story_text(text: str) -> Dict[str, Any]:
    """Parse the body of a [STORY] sticky into components."""
    result: Dict[str, Any] = {
        "release": None,
        "priority": None,
        "owner": None,
        "story_sentence": None,
        "acceptance_criteria": [],
    }

    if not text:
        return result

    release_match = TAG_RELEASE.search(text)
    if release_match:
        result["release"] = f"V{release_match.group(1)}"

    priority_match = TAG_PRIORITY.search(text)
    if priority_match:
        result["priority"] = f"P{priority_match.group(1)}"

    owner_match = TAG_OWNER.search(text)
    if owner_match:
        result["owner"] = owner_match.group(0).upper()

    # Split into main body and AC section (after the "Acceptance Criteria:" marker on its own line).
    ac_split = re.split(r"\n\s*Acceptance\s+Criteria\s*:?\s*\n", text, maxsplit=1, flags=re.IGNORECASE)
    main_part = ac_split[0]
    ac_part = ac_split[1] if len(ac_split) > 1 else ""

    # Strip taxonomy tags, owner markers, and emoji from the main sentence.
    sentence = re.sub(r"\[[^\]]{0,40}?(STORY|V[123]|P[123])[^\]]{0,40}?\]", "", main_part)
    sentence = re.sub(r"@(UX|DEV|PM|QA)\b", "", sentence, flags=re.IGNORECASE)
    sentence = EMOJI_STRIP.sub("", sentence)
    # Collapse whitespace (including any LINE SEPARATOR / PARAGRAPH SEPARATOR left over).
    sentence = re.sub(r"[\u2028\u2029]+", " ", sentence)
    sentence = re.sub(r"\s+", " ", sentence).strip()
    result["story_sentence"] = sentence or None

    if ac_part:
        # AC lines: bullet (-), bullet (*), or plain newline-separated. Strip emoji from each line.
        lines = []
        for ln in re.split(r"\n", ac_part):
            ln = ln.strip().lstrip("-*").strip()
            ln = EMOJI_STRIP.sub("", ln).strip()
            ln = re.sub(r"[\u2028\u2029]+", " ", ln)
            ln = re.sub(r"\s+", " ", ln).strip()
            if ln:
                lines.append(ln)
        result["acceptance_criteria"] = lines

    return result


def traverse(
    node: Dict[str, Any],
    current_section_id: Optional[str],
    current_section_name: Optional[str],
    sections: Dict[str, Dict[str, Any]],
    stickies: List[StickyItem],
    tasks: List[TaskItem],
    activities: List[ActivityItem],
    connectors: List[Connector],
) -> None:
    """Recursively walk the FigJam node tree, collecting sections, stickies, tasks, activities, connectors."""
    node_type = node.get("type")
    node_id = node.get("id", "")
    node_name = node.get("name", "")

    if node_type == "SECTION":
        current_section_id = node_id
        current_section_name = node_name
        sections[node_id] = {
            "name": node_name,
            "parent_id": None,
            "children_section_ids": [],
            "stickies": [],
        }

    elif node_type in ("STICKY", "SHAPE_WITH_TEXT"):
        text = get_text(node)
        x, y, w, h = get_bbox(node)
        color = get_color(node)
        sticky = StickyItem(
            id=node_id,
            text=text,
            x=x,
            y=y,
            width=w,
            height=h,
            color=color,
            section_id=current_section_id,
            section_name=current_section_name,
        )

        # Identify backbone vs story vs other content.
        is_task = TAG_TASK in text
        is_act = TAG_ACT in text
        is_story = TAG_STORY in text

        if is_task:
            tasks.append(
                TaskItem(
                    id=node_id,
                    name=clean_name(text),
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                )
            )
        elif is_act:
            activities.append(
                ActivityItem(
                    id=node_id,
                    name=clean_name(text),
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                )
            )
        elif is_story:
            parsed = parse_story_text(text)
            sticky.release = parsed["release"]
            sticky.priority = parsed["priority"]
            sticky.owner = parsed["owner"]
            sticky.story_sentence = parsed["story_sentence"]
            sticky.acceptance_criteria = parsed["acceptance_criteria"]
            stickies.append(sticky)
        else:
            # Other stickies (legend, persona, decorative text) — keep without parsing.
            stickies.append(sticky)

    elif node_type == "CONNECTOR":
        cstart = node.get("connectorStart") or {}
        cend = node.get("connectorEnd") or {}
        label = get_text(node) or "CONNECTS_TO"
        connectors.append(
            Connector(
                from_id=cstart.get("endpointNodeId"),
                to_id=cend.get("endpointNodeId"),
                label=label,
            )
        )

    # Recurse into children.
    for child in node.get("children") or []:
        traverse(
            child,
            current_section_id,
            current_section_name,
            sections,
            stickies,
            tasks,
            activities,
            connectors,
        )


def map_stories_to_tasks(stickies: List[StickyItem], tasks: List[TaskItem]) -> None:
    """Map each [STORY] to a [TASK] algorithmically by the X axis.

    Algorithm:
      1. Take the story's center X (x + width / 2).
      2. Find a task whose X range (task.x .. task.x + task.width) contains that center.
      3. Fallback: nearest task center on X — but only if within X_MAPPING_MAX_DISTANCE_PX.
         Otherwise, flag the story as UNASSIGNED (mapped_task_id = None).
    """
    if not tasks:
        return

    for sticky in stickies:
        if TAG_STORY not in sticky.text:
            continue
        cx = sticky.center_x

        # Range match (preferred).
        candidate: Optional[TaskItem] = None
        for t in tasks:
            if t.contains_x(cx):
                candidate = t
                break

        # Nearest-center fallback with distance threshold.
        if candidate is None:
            nearest = min(tasks, key=lambda t: t.distance_to_center(cx))
            if nearest.distance_to_center(cx) <= X_MAPPING_MAX_DISTANCE_PX:
                candidate = nearest
            # else: leave mapped_task_id as None -> rendered as UNASSIGNED

        sticky.mapped_task_id = candidate.id if candidate is not None else None


def map_tasks_to_activities(tasks: List[TaskItem], activities: List[ActivityItem]) -> None:
    """Map each [TASK] to an [ACT] by X-axis overlap (activity sits above its tasks in the same column).

    Algorithm:
      1. For each task, take center X.
      2. Find an activity whose X range contains that center.
      3. Fallback: nearest activity center on X (no threshold — tasks should always have an activity).
    """
    if not activities:
        return
    for t in tasks:
        cx = t.center_x
        candidate: Optional[ActivityItem] = None
        for a in activities:
            if a.contains_x(cx):
                candidate = a
                break
        if candidate is None:
            candidate = min(activities, key=lambda a: a.distance_to_center(cx))
        t.activity_id = candidate.id if candidate is not None else None


def group_stickies_by_section(stickies: List[StickyItem]) -> Dict[str, List[StickyItem]]:
    """Group stickies by section_name."""
    groups: Dict[str, List[StickyItem]] = {}
    for s in stickies:
        key = s.section_name or "(unsectioned)"
        groups.setdefault(key, []).append(s)
    return groups


def render_markdown(
    sections: Dict[str, Dict[str, Any]],
    stickies: List[StickyItem],
    tasks: List[TaskItem],
    activities: List[ActivityItem],
    connectors: List[Connector],
) -> str:
    """Render structured Markdown with Release -> Activity -> Task -> Story hierarchy."""
    out: List[str] = ["# Story Map - parsed backlog\n"]
    out.append("_Source: FigJam, parsed by `figjam-storymap-llm` skill._\n")

    # AI Readme section (legend)
    readme_items = [s for s in stickies if s.section_name and "00_" in s.section_name]
    if readme_items:
        out.append("## 00. AI ReadMe (legend)\n")
        for s in readme_items:
            if s.text:
                out.append(f"```\n{s.text}\n```\n")

    # Persona
    persona_items = [s for s in stickies if s.section_name and "USER_SEGMENT" in s.section_name.upper()]
    if persona_items:
        out.append("## Persona / User Segment\n")
        for s in persona_items:
            if s.text:
                out.append(f"- {s.text}\n")
        out.append("")

    # Backbone - Activities
    out.append("## 01. Backbone - Activities\n")
    for a in activities:
        out.append(f"- **{a.id}** - {a.name}")
    out.append("")

    # Backbone - Tasks
    out.append("## 02. Backbone - Tasks\n")
    for t in tasks:
        activity_name = next((a.name for a in activities if a.id == t.activity_id), None)
        activity_suffix = f" (activity: {activity_name})" if activity_name else ""
        out.append(f"- **{t.id}** - {t.name} (x={t.x:.0f}, w={t.width:.0f}){activity_suffix}")
    out.append("")

    # Releases (V1, V2, V3 in order, then any extras)
    releases: Dict[str, List[StickyItem]] = {"V1": [], "V2": [], "V3": []}
    for s in stickies:
        if TAG_STORY not in s.text:
            continue
        if s.release:
            releases.setdefault(s.release, []).append(s)
        elif s.section_name and is_release_section(s.section_name):
            r = parse_release_from_section(s.section_name)
            if r:
                s.release = r
                releases.setdefault(r, []).append(s)

    for release_key in sorted(releases.keys()):
        items = releases.get(release_key, [])
        if not items:
            continue
        out.append(f"## {release_key} - Release {release_key[1]}\n")
        # Group by mapped_task_id.
        by_task: Dict[Optional[str], List[StickyItem]] = {}
        for s in items:
            by_task.setdefault(s.mapped_task_id, []).append(s)

        for task_id, stories in by_task.items():
            task_name = next((t.name for t in tasks if t.id == task_id), None)
            if task_id:
                out.append(f"### Task: {task_name or task_id}\n")
            else:
                out.append(f"### Task: (UNASSIGNED - outside any task column)\n")
            for s in stories:
                line = f"- [STORY] "
                if s.release:
                    line += f"[{s.release}] "
                if s.priority:
                    line += f"[{s.priority}] "
                if s.story_sentence:
                    line += s.story_sentence
                if s.owner:
                    line += f" {s.owner}"
                out.append(line)
                if s.acceptance_criteria:
                    out.append("  - **Acceptance Criteria:**")
                    for ac in s.acceptance_criteria:
                        out.append(f"    - {ac}")
            out.append("")

    # Connectors
    if connectors:
        out.append("## Connector relations\n")
        for c in connectors:
            out.append(f"- `{c.from_id}` --[{c.label}]--> `{c.to_id}`")
        out.append("")

    # Unsectioned warnings
    unsectioned = [s for s in stickies if not s.section_id]
    if unsectioned:
        out.append("## Warning: Unsectioned items (outside `[STORY_MAP]` root)\n")
        for s in unsectioned:
            out.append(f"- {s.id}: {s.text[:80]}")
        out.append("")

    return "\n".join(out)


def render_json(
    stickies: List[StickyItem],
    tasks: List[TaskItem],
    activities: List[ActivityItem],
    connectors: List[Connector],
) -> str:
    """Render JSON output. Convert it to a Notion DB, Linear/Jira CSV import,
    or feed it to PM tooling via MCP — the parser itself stops at JSON."""
    payload = {
        "activities": [
            {"id": a.id, "name": a.name, "x": a.x, "y": a.y, "width": a.width, "height": a.height}
            for a in activities
        ],
        "tasks": [
            {
                "id": t.id,
                "name": t.name,
                "x": t.x,
                "y": t.y,
                "width": t.width,
                "height": t.height,
                "activity_id": t.activity_id,
            }
            for t in tasks
        ],
        "stories": [
            {
                "id": s.id,
                "release": s.release,
                "priority": s.priority,
                "owner": s.owner,
                "story_sentence": s.story_sentence,
                "acceptance_criteria": s.acceptance_criteria,
                "mapped_task_id": s.mapped_task_id,
                "section_name": s.section_name,
                "raw_text": s.text,
            }
            for s in stickies
            if TAG_STORY in s.text
        ],
        "connectors": [
            {"from": c.from_id, "to": c.to_id, "label": c.label} for c in connectors
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="FigJam Story Map parser -> Markdown/JSON (Patton methodology, LLM-ready)."
    )
    parser.add_argument(
        "--file-key",
        help="Figma file key from the board URL: figma.com/board/{key}/...",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("FIGMA_TOKEN", ""),
        help="Figma personal access token (or FIGMA_TOKEN env var).",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--input",
        help="Optional: path to a saved FigJam JSON file (instead of calling the Figma API).",
    )

    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print(f"ERROR: input file is not valid JSON: {exc}", file=sys.stderr)
            return 2
    else:
        if not args.file_key:
            print("ERROR: --file-key is required when --input is not provided.", file=sys.stderr)
            return 2
        if not args.token:
            print(
                "ERROR: FIGMA_TOKEN is missing. Set the env var or pass --token.",
                file=sys.stderr,
            )
            return 2
        data = fetch_figjam(args.file_key, args.token)

    document = data.get("document") or data
    if "nodes" in data and not document:
        # /nodes endpoint returns {nodes: {id: {document: ...}}}
        first_node = next(iter(data["nodes"].values()), {})
        document = first_node.get("document", {})

    sections: Dict[str, Dict[str, Any]] = {}
    stickies: List[StickyItem] = []
    tasks: List[TaskItem] = []
    activities: List[ActivityItem] = []
    connectors: List[Connector] = []

    traverse(document, None, None, sections, stickies, tasks, activities, connectors)

    map_stories_to_tasks(stickies, tasks)
    map_tasks_to_activities(tasks, activities)

    if args.format == "json":
        print(render_json(stickies, tasks, activities, connectors))
    else:
        print(render_markdown(sections, stickies, tasks, activities, connectors))

    return 0


if __name__ == "__main__":
    sys.exit(main())