#!/usr/bin/env python3
"""Canvas course discovery, activation, and multi-course management.

Usage:
    python3 canvas_courses.py list [--active-only]
    python3 canvas_courses.py activate <course_id> [--slug <slug>]
    python3 canvas_courses.py deactivate <course_id>
    python3 canvas_courses.py map <course_id> <existing_slug>
    python3 canvas_courses.py status
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from canvas_api import CanvasClient, load_canvas_credentials, slugify_course_name
from paths import CANVAS_CONFIG, COURSES_DIR, COURSE_CONFIGS_DIR


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

CANVAS_CONFIG_PATH = CANVAS_CONFIG


# ---------------------------------------------------------------------------
# Config management
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "version": 1,
    "default_sync_interval_hours": 6,
    "active_courses": [],
    "ignored_courses": [],
    "file_download_rules": {
        "max_file_size_mb": 50,
        "allowed_extensions": [".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".csv", ".ipynb"],
        "skip_extensions": [".mp4", ".mov", ".zip", ".tar"],
    },
}


def load_config() -> dict:
    """Load canvas-config.json, creating default if missing."""
    if CANVAS_CONFIG_PATH.exists():
        return json.loads(CANVAS_CONFIG_PATH.read_text())
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    """Save canvas-config.json."""
    CANVAS_CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


def find_active_course(config: dict, canvas_id: int) -> dict:
    """Find an active course entry by canvas_id, or None."""
    for c in config["active_courses"]:
        if c["canvas_id"] == canvas_id:
            return c
    return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(client: CanvasClient, active_only: bool = False):
    """List all Canvas courses for the current user."""
    config = load_config()
    active_ids = {c["canvas_id"] for c in config["active_courses"]}

    courses = client.get_courses()

    # Group by role
    by_role = {}
    for c in courses:
        if active_only and c.get("workflow_state") != "available":
            continue
        roles = [e["type"] for e in c.get("enrollments", [])]
        primary_role = roles[0] if roles else "unknown"
        by_role.setdefault(primary_role, []).append(c)

    role_order = ["teacher", "ta", "designer", "observer", "student"]
    for role in role_order:
        group = by_role.pop(role, [])
        if not group:
            continue
        print(f"\n  === {role.upper()} ({len(group)}) ===")
        for c in sorted(group, key=lambda x: x.get("name", "")):
            state = c.get("workflow_state", "?")
            code = c.get("course_code", c["name"])[:55]
            active_marker = " [ACTIVE]" if c["id"] in active_ids else ""
            print(f"    {c['id']:>8}  {code:<57}  {state:<12}{active_marker}")

    # Any remaining roles
    for role, group in by_role.items():
        print(f"\n  === {role.upper()} ({len(group)}) ===")
        for c in sorted(group, key=lambda x: x.get("name", "")):
            print(f"    {c['id']:>8}  {c.get('course_code', c['name'])[:55]:<57}  "
                  f"{c.get('workflow_state', '?')}")

    print(f"\n  Total: {len(courses)} courses"
          f" ({len(active_ids)} activated)")


def cmd_activate(client: CanvasClient, course_id: int, slug: str = None):
    """Activate a Canvas course for local sync."""
    config = load_config()

    # Check if already active
    existing = find_active_course(config, course_id)
    if existing:
        print(f"  Course {course_id} is already active as '{existing['slug']}'")
        return

    # Fetch course info
    try:
        course = client.get_course(course_id, include=["term", "total_students"])
    except Exception as e:
        print(f"  Error fetching course {course_id}: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate slug
    if not slug:
        slug = slugify_course_name(course.get("course_code", str(course_id)))

    # Check if this slug is already used by a different course
    for c in config["active_courses"]:
        if c["slug"] == slug:
            print(f"  Slug '{slug}' is already used by "
                  f"canvas_id {c['canvas_id']}. Use --slug to specify "
                  f"a different slug.", file=sys.stderr)
            sys.exit(1)

    # Determine role
    roles = [e["type"] for e in course.get("enrollments", [])]
    role = roles[0] if roles else "unknown"

    # Term info
    term = course.get("term", {})
    term_name = term.get("name", "Unknown Term") if term else "Unknown Term"

    # Create directory structure
    canvas_dir = COURSES_DIR / slug / "canvas"
    for subdir in ["pages", "assignments", "announcements", "discussions",
                   "quizzes", "modules", "files", "syllabus", "enrollments"]:
        (canvas_dir / subdir).mkdir(parents=True, exist_ok=True)

    # Create course-info.json
    course_info = {
        "canvas_id": course_id,
        "slug": slug,
        "name": course.get("name", ""),
        "course_code": course.get("course_code", ""),
        "role": role,
        "term": term_name,
        "canvas_url": f"{client.base_url}/courses/{course_id}",
        "activated_at": datetime.now(timezone.utc).isoformat(),
        "total_students": course.get("total_students"),
    }
    (COURSES_DIR / slug / "course-info.json").write_text(
        json.dumps(course_info, indent=2) + "\n")

    # Initialize sync state
    sync_state = {
        "last_full_sync": None,
        "last_incremental_sync": None,
        "content_hashes": {},
    }
    (canvas_dir / "sync_state.json").write_text(
        json.dumps(sync_state, indent=2) + "\n")

    # Add to config
    entry = {
        "canvas_id": course_id,
        "slug": slug,
        "name": f"{course.get('course_code', '')} - {course.get('name', '')}",
        "role": role,
        "term": term_name,
        "discord_channels": [],
        "sync_enabled": True,
        "sync_interval_hours": config.get("default_sync_interval_hours", 6),
        "sync_content": {
            "pages": True,
            "assignments": True,
            "announcements": True,
            "discussions": True,
            "modules": True,
            "quizzes": True,
            "files": True,
            "syllabus": True,
            "enrollments": True,
        },
        "mapped_at": datetime.now(timezone.utc).isoformat(),
        "last_sync": None,
    }
    config["active_courses"].append(entry)
    save_config(config)

    # Create per-course config in course-configs/
    COURSE_CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    course_config = {
        "canvas_id": course_id,
        "slug": slug,
        "course_name": course.get("name", ""),
        "course_code": course.get("course_code", ""),
        "role": role,
        "term": term_name,
        "canvas_url": f"{client.base_url}/courses/{course_id}",
        "allowed_channels": [],
        "blocked_channels": [],
        "admin_users": [],
        "privileged_users": {},
        "editable_files": {},
    }
    (COURSE_CONFIGS_DIR / f"{slug}.json").write_text(
        json.dumps(course_config, indent=2) + "\n")

    print(f"  Activated course {course_id} as '{slug}'")
    print(f"    Name: {course.get('name', '?')}")
    print(f"    Role: {role}")
    print(f"    Term: {term_name}")
    print(f"    Dir:  {COURSES_DIR / slug}/")
    print(f"\n  Next: run 'python3 canvas_sync.py full {course_id}' to sync content")


def cmd_map(client: CanvasClient, course_id: int, existing_slug: str):
    """Map a Canvas course to an existing local directory."""
    config = load_config()

    # Check if this canvas_id is already active
    existing = find_active_course(config, course_id)
    if existing:
        print(f"  Course {course_id} is already active as '{existing['slug']}'")
        return

    # Check if this slug is already used by a different course
    for c in config["active_courses"]:
        if c["slug"] == existing_slug:
            print(f"  Slug '{existing_slug}' is already used by "
                  f"canvas_id {c['canvas_id']}", file=sys.stderr)
            sys.exit(1)

    # Verify the directory exists
    course_dir = COURSES_DIR / existing_slug
    if not course_dir.exists():
        print(f"  Error: directory {course_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    # Fetch course info
    try:
        course = client.get_course(course_id, include=["term", "total_students"])
    except Exception as e:
        print(f"  Error fetching course {course_id}: {e}", file=sys.stderr)
        sys.exit(1)

    roles = [e["type"] for e in course.get("enrollments", [])]
    role = roles[0] if roles else "unknown"
    term = course.get("term", {})
    term_name = term.get("name", "Unknown Term") if term else "Unknown Term"

    # Create canvas/ subdirectory (alongside existing module dirs)
    canvas_dir = course_dir / "canvas"
    for subdir in ["pages", "assignments", "announcements", "discussions",
                   "quizzes", "modules", "files", "syllabus", "enrollments"]:
        (canvas_dir / subdir).mkdir(parents=True, exist_ok=True)

    # Initialize sync state
    sync_state = {
        "last_full_sync": None,
        "last_incremental_sync": None,
        "content_hashes": {},
    }
    (canvas_dir / "sync_state.json").write_text(
        json.dumps(sync_state, indent=2) + "\n")

    # Save course info
    (course_dir / "course-info.json").write_text(json.dumps({
        "canvas_id": course_id,
        "slug": existing_slug,
        "name": course.get("name", ""),
        "course_code": course.get("course_code", ""),
        "role": role,
        "term": term_name,
        "canvas_url": f"{client.base_url}/courses/{course_id}",
        "mapped_at": datetime.now(timezone.utc).isoformat(),
        "total_students": course.get("total_students"),
    }, indent=2) + "\n")

    # Add to config
    entry = {
        "canvas_id": course_id,
        "slug": existing_slug,
        "name": f"{course.get('course_code', '')} - {course.get('name', '')}",
        "role": role,
        "term": term_name,
        "discord_channels": [],
        "sync_enabled": True,
        "sync_interval_hours": config.get("default_sync_interval_hours", 6),
        "sync_content": {
            "pages": True,
            "assignments": True,
            "announcements": True,
            "discussions": True,
            "modules": True,
            "quizzes": True,
            "files": True,
            "syllabus": True,
            "enrollments": True,
        },
        "mapped_at": datetime.now(timezone.utc).isoformat(),
        "last_sync": None,
    }
    config["active_courses"].append(entry)
    save_config(config)

    # Create per-course config
    COURSE_CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    if not (COURSE_CONFIGS_DIR / f"{existing_slug}.json").exists():
        (COURSE_CONFIGS_DIR / f"{existing_slug}.json").write_text(json.dumps({
            "canvas_id": course_id,
            "slug": existing_slug,
            "course_name": course.get("name", ""),
            "course_code": course.get("course_code", ""),
            "role": role,
            "term": term_name,
            "canvas_url": f"{client.base_url}/courses/{course_id}",
            "allowed_channels": [],
            "blocked_channels": [],
            "admin_users": [],
            "privileged_users": {},
            "editable_files": {},
        }, indent=2) + "\n")

    print(f"  Mapped Canvas course {course_id} -> existing '{existing_slug}'")
    print(f"    Name: {course.get('name', '?')}")
    print(f"    Role: {role}")
    print(f"    Canvas dir created: {canvas_dir}/")
    print(f"    Existing content preserved (module dirs, slides, etc.)")
    print(f"\n  Next: run 'python3 canvas_sync.py full {course_id}' to sync content")


def cmd_deactivate(course_id: int):
    """Deactivate a course (remove from config, keep data)."""
    config = load_config()
    entry = find_active_course(config, course_id)

    if not entry:
        print(f"  Course {course_id} is not currently active", file=sys.stderr)
        sys.exit(1)

    slug = entry["slug"]
    config["active_courses"] = [
        c for c in config["active_courses"] if c["canvas_id"] != course_id
    ]
    save_config(config)

    print(f"  Deactivated course {course_id} ('{slug}')")
    print(f"  Data preserved in: {COURSES_DIR / slug}/")
    print(f"  To reactivate: python3 canvas_courses.py activate {course_id} --slug {slug}")


def cmd_status():
    """Show status of all activated courses."""
    config = load_config()
    active = config.get("active_courses", [])

    if not active:
        print("  No courses activated yet.")
        print("  Run 'python3 canvas_courses.py list' to see available courses.")
        return

    print(f"\n  === Activated Courses ({len(active)}) ===\n")

    for c in active:
        slug = c["slug"]
        canvas_dir = COURSES_DIR / slug / "canvas"
        sync_state_path = canvas_dir / "sync_state.json"

        last_sync = c.get("last_sync", "never")

        # Count local files
        content_counts = {}
        for content_type in ["pages", "assignments", "announcements",
                             "discussions", "quizzes", "files"]:
            type_dir = canvas_dir / content_type
            if type_dir.exists():
                content_counts[content_type] = len(list(type_dir.iterdir()))
            else:
                content_counts[content_type] = 0

        # Check sync state
        if sync_state_path.exists():
            state = json.loads(sync_state_path.read_text())
            last_full = state.get("last_full_sync", "never")
            last_inc = state.get("last_incremental_sync", "never")
        else:
            last_full = "never"
            last_inc = "never"

        print(f"  [{c['canvas_id']}] {c['name']}")
        print(f"    Slug: {slug}")
        print(f"    Role: {c.get('role', '?')}")
        print(f"    Sync enabled: {c.get('sync_enabled', False)}")
        print(f"    Last full sync: {last_full}")
        print(f"    Last incremental: {last_inc}")
        print(f"    Local content: " + ", ".join(
            f"{k}:{v}" for k, v in content_counts.items() if v > 0) or "empty")
        print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        cmd_status()
        return

    if command == "deactivate":
        if len(sys.argv) < 3:
            print("Usage: canvas_courses.py deactivate <course_id>", file=sys.stderr)
            sys.exit(1)
        cmd_deactivate(int(sys.argv[2]))
        return

    # Commands that need the API client
    base_url, token = load_canvas_credentials()
    client = CanvasClient(base_url, token, write_mode="deny")

    if command == "list":
        active_only = "--active-only" in sys.argv
        cmd_list(client, active_only)

    elif command == "activate":
        if len(sys.argv) < 3:
            print("Usage: canvas_courses.py activate <course_id> [--slug <slug>]",
                  file=sys.stderr)
            sys.exit(1)
        course_id = int(sys.argv[2])
        slug = None
        if "--slug" in sys.argv:
            idx = sys.argv.index("--slug")
            if idx + 1 < len(sys.argv):
                slug = sys.argv[idx + 1]
        cmd_activate(client, course_id, slug)

    elif command == "map":
        if len(sys.argv) < 4:
            print("Usage: canvas_courses.py map <course_id> <existing_slug>",
                  file=sys.stderr)
            sys.exit(1)
        cmd_map(client, int(sys.argv[2]), sys.argv[3])

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available: list, activate, deactivate, map, status", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
