#!/usr/bin/env python3
"""Canvas content sync engine — full and incremental sync with change detection.

Downloads all Canvas content for activated courses, converts to markdown,
and generates memory files for RAG indexing. Uses SHA-256 hashing to detect
changes and only write files that actually differ.

Usage:
    python3 canvas_sync.py full <course_id>           # Full sync
    python3 canvas_sync.py incremental <course_id>    # Only changes since last sync
    python3 canvas_sync.py all [--incremental]        # Sync all active courses
    python3 canvas_sync.py status <course_id>         # Show sync state
"""

import hashlib
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from canvas_api import (CanvasClient, CanvasAPIError, load_canvas_credentials,
                        slugify_course_name)
from canvas_content import (html_to_markdown, format_page_markdown,
                            format_assignment_markdown, format_announcement_markdown,
                            format_discussion_markdown, format_quiz_markdown,
                            format_module_summary_markdown, format_syllabus_markdown,
                            format_file_index_markdown, memory_filename, _slugify)
from paths import (COURSES_DIR, MEMORY_DIR, CANVAS_CONFIG as CANVAS_CONFIG_PATH)

# Default sync_content — all enabled
ALL_CONTENT_TYPES = {
    "pages": True, "assignments": True, "announcements": True,
    "discussions": True, "modules": True, "quizzes": True,
    "files": True, "syllabus": True, "enrollments": True,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _content_hash(data) -> str:
    """SHA-256 hash of content for change detection."""
    if isinstance(data, str):
        raw = data.encode("utf-8")
    else:
        raw = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Course Syncer
# ---------------------------------------------------------------------------

class CourseSyncer:
    """Syncs all Canvas content for a single course."""

    def __init__(self, client: CanvasClient, canvas_id: int, slug: str):
        self.client = client
        self.canvas_id = canvas_id
        self.slug = slug

        self.course_dir = COURSES_DIR / slug
        self.canvas_dir = self.course_dir / "canvas"
        self.sync_state_path = self.canvas_dir / "sync_state.json"

        self.changes = []  # Track what changed
        self.errors = []   # Track errors per content type

        # Ensure directories exist
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        for subdir in ["pages", "assignments", "announcements", "discussions",
                        "quizzes", "modules", "files", "syllabus", "enrollments"]:
            (self.canvas_dir / subdir).mkdir(parents=True, exist_ok=True)

    def load_sync_state(self) -> dict:
        if self.sync_state_path.exists():
            return json.loads(self.sync_state_path.read_text())
        return {"last_full_sync": None, "last_incremental_sync": None,
                "content_hashes": {}}

    def save_sync_state(self, state: dict):
        self.sync_state_path.write_text(json.dumps(state, indent=2) + "\n")

    def _write_if_changed(self, state: dict, key: str,
                          content: str, local_path: Path,
                          memory_path: Optional[Path] = None) -> bool:
        """Write file only if content hash changed. Returns True if written."""
        new_hash = _content_hash(content)
        old_hash = state["content_hashes"].get(key)

        if new_hash == old_hash:
            return False

        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text(content)

        if memory_path:
            memory_path.parent.mkdir(parents=True, exist_ok=True)
            memory_path.write_text(content)

        state["content_hashes"][key] = new_hash
        return True

    # -- Sync methods -------------------------------------------------------

    def sync_pages(self, state: dict) -> int:
        """Sync all Canvas pages. Returns count of changed items."""
        print(f"    Syncing pages...", end=" ", flush=True)
        changed = 0

        try:
            pages_list = self.client.get_pages(self.canvas_id)
        except CanvasAPIError as e:
            msg = f"pages: {e}"
            self.errors.append(msg)
            print(f"ERROR: {e}")
            return 0

        for page_summary in pages_list:
            page_url = page_summary.get("url", "")
            if not page_url:
                continue

            try:
                page = self.client.get_page(self.canvas_id, page_url)
            except CanvasAPIError:
                continue

            md = format_page_markdown(page, self.slug, self.client.base_url)
            key = f"pages/{page_url}"
            local_path = self.canvas_dir / "pages" / f"{page_url}.md"
            mem_path = MEMORY_DIR / memory_filename(
                self.slug, "canvas-page", page.get("title", page_url))

            if self._write_if_changed(state, key, md, local_path, mem_path):
                changed += 1
                self.changes.append(f"page: {page.get('title', page_url)}")

        print(f"{changed} changed out of {len(pages_list)}")
        return changed

    def sync_assignments(self, state: dict) -> int:
        """Sync all assignments."""
        print(f"    Syncing assignments...", end=" ", flush=True)
        changed = 0

        try:
            assignments = self.client.get_assignments(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"assignments: {e}")
            print(f"ERROR: {e}")
            return 0

        for a in assignments:
            name = a.get("name", "untitled")
            md = format_assignment_markdown(a, self.slug, self.client.base_url)
            key = f"assignments/{a['id']}"
            safe_name = _slugify(name)
            local_path = self.canvas_dir / "assignments" / f"{a['id']}-{safe_name}.md"
            mem_path = MEMORY_DIR / memory_filename(
                self.slug, "canvas-assignment", name)

            if self._write_if_changed(state, key, md, local_path, mem_path):
                changed += 1
                self.changes.append(f"assignment: {name}")

        print(f"{changed} changed out of {len(assignments)}")
        return changed

    def sync_announcements(self, state: dict) -> int:
        """Sync all announcements."""
        print(f"    Syncing announcements...", end=" ", flush=True)
        changed = 0

        try:
            announcements = self.client.get_announcements(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"announcements: {e}")
            print(f"ERROR: {e}")
            return 0

        for ann in announcements:
            title = ann.get("title", "untitled")
            posted = ann.get("posted_at", "")
            date_prefix = posted[:10] if posted else "undated"
            md = format_announcement_markdown(ann, self.slug, self.client.base_url)
            key = f"announcements/{ann['id']}"
            safe_title = _slugify(title)
            local_path = self.canvas_dir / "announcements" / f"{date_prefix}-{safe_title}.md"
            mem_path = MEMORY_DIR / memory_filename(
                self.slug, "canvas-announcement", f"{date_prefix}-{title}")

            if self._write_if_changed(state, key, md, local_path, mem_path):
                changed += 1
                self.changes.append(f"announcement: {title}")

        print(f"{changed} changed out of {len(announcements)}")
        return changed

    def sync_discussions(self, state: dict) -> int:
        """Sync discussion topics with replies."""
        print(f"    Syncing discussions...", end=" ", flush=True)
        changed = 0

        try:
            topics = self.client.get_discussion_topics(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"discussions: {e}")
            print(f"ERROR: {e}")
            return 0

        non_announcement_topics = [t for t in topics if not t.get("is_announcement")]

        for topic in non_announcement_topics:
            title = topic.get("title", "untitled")
            replies = []
            try:
                entries = self.client.get_discussion_entries(
                    self.canvas_id, topic["id"])
                replies = entries[:20]  # Cap replies
            except CanvasAPIError:
                pass

            md = format_discussion_markdown(
                topic, replies, self.slug, self.client.base_url)
            key = f"discussions/{topic['id']}"
            safe_title = _slugify(title)
            local_path = self.canvas_dir / "discussions" / f"{topic['id']}-{safe_title}.md"
            mem_path = MEMORY_DIR / memory_filename(
                self.slug, "canvas-discussion", title)

            if self._write_if_changed(state, key, md, local_path, mem_path):
                changed += 1
                self.changes.append(f"discussion: {title}")

        print(f"{changed} changed out of {len(non_announcement_topics)}")
        return changed

    def sync_quizzes(self, state: dict) -> int:
        """Sync quiz metadata (no questions for academic integrity)."""
        print(f"    Syncing quizzes...", end=" ", flush=True)
        changed = 0

        try:
            quizzes = self.client.get_quizzes(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"quizzes: {e}")
            print(f"ERROR: {e}")
            return 0

        for q in quizzes:
            title = q.get("title", "untitled")
            md = format_quiz_markdown(q, self.slug)
            key = f"quizzes/{q['id']}"
            safe_title = _slugify(title)
            local_path = self.canvas_dir / "quizzes" / f"{q['id']}-{safe_title}.md"
            mem_path = MEMORY_DIR / memory_filename(
                self.slug, "canvas-quiz", title)

            if self._write_if_changed(state, key, md, local_path, mem_path):
                changed += 1
                self.changes.append(f"quiz: {title}")

        print(f"{changed} changed out of {len(quizzes)}")
        return changed

    def sync_modules(self, state: dict) -> int:
        """Sync module structure as a course table of contents."""
        print(f"    Syncing modules...", end=" ", flush=True)

        try:
            modules = self.client.get_modules(self.canvas_id, include_items=True)
        except CanvasAPIError as e:
            self.errors.append(f"modules: {e}")
            print(f"ERROR: {e}")
            return 0

        # Save raw structure as JSON
        struct_path = self.canvas_dir / "modules" / "structure.json"
        struct_path.parent.mkdir(parents=True, exist_ok=True)
        struct_path.write_text(json.dumps(modules, indent=2, default=str) + "\n")

        # Generate summary markdown
        md = format_module_summary_markdown(modules, self.slug)
        key = "modules/summary"
        local_path = self.canvas_dir / "modules" / "summary.md"
        mem_path = MEMORY_DIR / f"{self.slug}__canvas-modules.md"

        changed = 0
        if self._write_if_changed(state, key, md, local_path, mem_path):
            changed = 1
            self.changes.append("modules: course structure")

        print(f"{changed} changed ({len(modules)} modules)")
        return changed

    def sync_files(self, state: dict, config: dict = None) -> int:
        """Sync course files (download based on rules)."""
        print(f"    Syncing files...", end=" ", flush=True)

        # Load download rules
        rules = (config or {}).get("file_download_rules", {})
        max_size = rules.get("max_file_size_mb", 50) * 1024 * 1024
        allowed_ext = set(rules.get("allowed_extensions",
                                    [".pdf", ".docx", ".pptx", ".xlsx",
                                     ".txt", ".csv", ".ipynb"]))
        skip_ext = set(rules.get("skip_extensions",
                                 [".mp4", ".mov", ".zip", ".tar"]))

        try:
            files = self.client.get_files(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"files: {e}")
            print(f"ERROR: {e}")
            return 0

        downloaded = 0
        skipped = 0
        failed = 0

        for f in files:
            name = f.get("display_name", "unknown")
            size = f.get("size", 0)
            ext = os.path.splitext(name)[1].lower()

            # Skip based on rules
            if size > max_size:
                skipped += 1
                continue
            if ext in skip_ext:
                skipped += 1
                continue
            if allowed_ext and ext not in allowed_ext:
                skipped += 1
                continue

            # Validate download URL
            if not f.get("url"):
                skipped += 1
                continue

            # Check if file changed (using updated_at + size as proxy)
            key = f"files/{f['id']}"
            file_hash = f"{f.get('updated_at', '')}_{size}"
            old_hash = state["content_hashes"].get(key)
            if file_hash == old_hash:
                continue

            # Download
            dest = self.canvas_dir / "files" / name
            try:
                self.client.download_file(f, dest)
                state["content_hashes"][key] = file_hash
                downloaded += 1
                self.changes.append(f"file: {name}")
            except Exception as e:
                failed += 1
                self.errors.append(f"file download '{name}': {e}")

        # Generate file index for memory
        idx_md = format_file_index_markdown(files, self.slug)
        idx_key = "files/index"
        idx_path = self.canvas_dir / "files" / "_index.md"
        mem_path = MEMORY_DIR / f"{self.slug}__canvas-files.md"
        self._write_if_changed(state, idx_key, idx_md, idx_path, mem_path)

        parts = [f"{downloaded} downloaded"]
        if skipped:
            parts.append(f"{skipped} skipped")
        if failed:
            parts.append(f"{failed} FAILED")
        print(f"{', '.join(parts)} (of {len(files)} total)")
        return downloaded

    def sync_syllabus(self, state: dict) -> int:
        """Sync course syllabus body."""
        print(f"    Syncing syllabus...", end=" ", flush=True)

        try:
            course = self.client.get_syllabus(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"syllabus: {e}")
            print(f"ERROR: {e}")
            return 0

        body = course.get("syllabus_body", "")
        if not body:
            print("no syllabus body")
            return 0

        md = format_syllabus_markdown(course, self.slug, self.client.base_url)
        key = "syllabus"
        local_path = self.canvas_dir / "syllabus" / "syllabus.md"
        mem_path = MEMORY_DIR / f"{self.slug}__canvas-syllabus.md"

        changed = 0
        if self._write_if_changed(state, key, md, local_path, mem_path):
            changed = 1
            self.changes.append("syllabus")

        print(f"{changed} changed")
        return changed

    def sync_enrollments(self, state: dict) -> int:
        """Sync enrollment roster (JSON only, NOT indexed in memory for privacy)."""
        print(f"    Syncing enrollments...", end=" ", flush=True)

        try:
            enrollments = self.client.get_enrollments(self.canvas_id)
        except CanvasAPIError as e:
            self.errors.append(f"enrollments: {e}")
            print(f"ERROR: {e}")
            return 0

        # Build roster (sanitized — just names, roles, no emails)
        roster = []
        for e in enrollments:
            user = e.get("user", {})
            roster.append({
                "user_id": e.get("user_id"),
                "name": user.get("name", user.get("sortable_name", "?")),
                "role": e.get("type", "?"),
                "state": e.get("enrollment_state", "?"),
            })

        key = "enrollments"
        content = json.dumps(roster, indent=2)
        new_hash = _content_hash(content)
        old_hash = state["content_hashes"].get(key)

        changed = 0
        if new_hash != old_hash:
            roster_path = self.canvas_dir / "enrollments" / "roster.json"
            roster_path.parent.mkdir(parents=True, exist_ok=True)
            roster_path.write_text(content + "\n")
            state["content_hashes"][key] = new_hash
            changed = 1
            self.changes.append(f"enrollments: {len(roster)} users")

        from collections import Counter
        counts = Counter(e["role"] for e in roster)
        roles_str = ", ".join(f"{k}:{v}" for k, v in sorted(counts.items()))
        print(f"{changed} changed ({len(roster)} users: {roles_str})")
        return changed

    # -- Orchestration ------------------------------------------------------

    def _run_sync(self, state: dict, sync_content: dict,
                  config: dict = None) -> dict:
        """Run sync methods based on sync_content flags. Returns summary."""
        summary = {}

        sync_methods = {
            "pages": lambda: self.sync_pages(state),
            "assignments": lambda: self.sync_assignments(state),
            "announcements": lambda: self.sync_announcements(state),
            "discussions": lambda: self.sync_discussions(state),
            "quizzes": lambda: self.sync_quizzes(state),
            "modules": lambda: self.sync_modules(state),
            "files": lambda: self.sync_files(state, config),
            "syllabus": lambda: self.sync_syllabus(state),
            "enrollments": lambda: self.sync_enrollments(state),
        }

        for content_type, sync_fn in sync_methods.items():
            if sync_content.get(content_type, True):
                summary[content_type] = sync_fn()
            else:
                summary[content_type] = 0

        return summary

    def full_sync(self, config: dict = None,
                  sync_content: dict = None) -> dict:
        """Run all enabled sync methods. Returns summary."""
        state = self.load_sync_state()
        self.changes = []
        self.errors = []

        content_flags = sync_content or ALL_CONTENT_TYPES

        print(f"\n  === Full sync: {self.slug} "
              f"(canvas_id: {self.canvas_id}) ===\n")

        summary = self._run_sync(state, content_flags, config)

        state["last_full_sync"] = _now_iso()
        state["last_incremental_sync"] = _now_iso()
        self.save_sync_state(state)

        _update_config_last_sync(self.canvas_id)

        total_changed = sum(summary.values())
        print(f"\n    Total: {total_changed} items changed")

        if self.errors:
            print(f"\n    Errors ({len(self.errors)}):")
            for err in self.errors:
                print(f"      ! {err}")

        if total_changed > 0:
            print(f"\n    Changed items:")
            for c in self.changes:
                print(f"      - {c}")
            print(f"\n    >> Run 'openclaw memory index --force' "
                  f"to update RAG index")

        return summary

    def incremental_sync(self, config: dict = None,
                         sync_content: dict = None) -> dict:
        """Same as full sync but relies on hash-based change detection.

        Canvas API doesn't reliably support filtering by updated_at for
        all endpoints, so we fetch everything but only write changed files.
        """
        state = self.load_sync_state()
        self.changes = []
        self.errors = []

        content_flags = sync_content or ALL_CONTENT_TYPES

        print(f"\n  === Incremental sync: {self.slug} "
              f"(canvas_id: {self.canvas_id}) ===\n")

        summary = self._run_sync(state, content_flags, config)

        state["last_incremental_sync"] = _now_iso()
        self.save_sync_state(state)

        _update_config_last_sync(self.canvas_id)

        total_changed = sum(summary.values())
        print(f"\n    Total: {total_changed} items changed")

        if self.errors:
            print(f"\n    Errors ({len(self.errors)}):")
            for err in self.errors:
                print(f"      ! {err}")

        if total_changed > 0:
            print(f"\n    Changed items:")
            for c in self.changes:
                print(f"      - {c}")
            print(f"\n    >> Run 'openclaw memory index --force' "
                  f"to update RAG index")
        else:
            print("    Everything up to date.")

        return summary


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _load_canvas_config() -> dict:
    if CANVAS_CONFIG_PATH.exists():
        return json.loads(CANVAS_CONFIG_PATH.read_text())
    return {"active_courses": []}


def _update_config_last_sync(canvas_id: int):
    """Update last_sync in canvas-config.json."""
    config = _load_canvas_config()
    for c in config["active_courses"]:
        if c["canvas_id"] == canvas_id:
            c["last_sync"] = _now_iso()
            break
    CANVAS_CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


def _find_course_in_config(canvas_id: int) -> dict:
    """Find a course entry in canvas-config.json."""
    config = _load_canvas_config()
    for c in config["active_courses"]:
        if c["canvas_id"] == canvas_id:
            return c
    return None


def _get_sync_content_for_course(canvas_id: int) -> dict:
    """Get the sync_content flags for a specific course."""
    entry = _find_course_in_config(canvas_id)
    if entry:
        return entry.get("sync_content", ALL_CONTENT_TYPES)
    return dict(ALL_CONTENT_TYPES)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_full(client: CanvasClient, course_id: int):
    config = _load_canvas_config()
    entry = _find_course_in_config(course_id)
    if not entry:
        print(f"  Course {course_id} is not activated. "
              f"Run 'canvas_courses.py activate {course_id}' first.",
              file=sys.stderr)
        sys.exit(1)

    sync_content = entry.get("sync_content", ALL_CONTENT_TYPES)
    syncer = CourseSyncer(client, course_id, entry["slug"])
    syncer.full_sync(config, sync_content)


def cmd_incremental(client: CanvasClient, course_id: int):
    config = _load_canvas_config()
    entry = _find_course_in_config(course_id)
    if not entry:
        print(f"  Course {course_id} is not activated.", file=sys.stderr)
        sys.exit(1)

    sync_content = entry.get("sync_content", ALL_CONTENT_TYPES)
    syncer = CourseSyncer(client, course_id, entry["slug"])
    syncer.incremental_sync(config, sync_content)


def cmd_all(client: CanvasClient, incremental: bool = False):
    config = _load_canvas_config()
    active = config.get("active_courses", [])

    if not active:
        print("  No active courses. Run 'canvas_courses.py activate' first.")
        return

    print(f"\n  Syncing {len(active)} active course(s)...")

    succeeded = []
    failed = {}

    for entry in active:
        if not entry.get("sync_enabled", True):
            print(f"\n  Skipping {entry['slug']} (sync disabled)")
            continue

        sync_content = entry.get("sync_content", ALL_CONTENT_TYPES)
        syncer = CourseSyncer(client, entry["canvas_id"], entry["slug"])
        try:
            if incremental:
                syncer.incremental_sync(config, sync_content)
            else:
                syncer.full_sync(config, sync_content)
            succeeded.append(entry["slug"])
        except Exception as e:
            failed[entry["slug"]] = str(e)
            print(f"\n  ERROR syncing {entry['slug']}: {e}", file=sys.stderr)
            traceback.print_exc()

    # Final summary
    print(f"\n  {'=' * 50}")
    print(f"  Sync complete: {len(succeeded)} succeeded, "
          f"{len(failed)} failed")
    if failed:
        for slug, error in failed.items():
            print(f"    FAILED: {slug} -- {error[:100]}")


def cmd_status(course_id: int):
    entry = _find_course_in_config(course_id)
    if not entry:
        print(f"  Course {course_id} is not activated.", file=sys.stderr)
        sys.exit(1)

    slug = entry["slug"]
    canvas_dir = COURSES_DIR / slug / "canvas"
    sync_state_path = canvas_dir / "sync_state.json"

    print(f"\n  === Sync status: {slug} ===\n")

    if sync_state_path.exists():
        state = json.loads(sync_state_path.read_text())
        print(f"    Last full sync:        "
              f"{state.get('last_full_sync', 'never')}")
        print(f"    Last incremental sync: "
              f"{state.get('last_incremental_sync', 'never')}")
        print(f"    Tracked items:         "
              f"{len(state.get('content_hashes', {}))}")
    else:
        print("    No sync state found. Run a full sync first.")

    # Sync content flags
    sync_content = entry.get("sync_content", ALL_CONTENT_TYPES)
    disabled = [k for k, v in sync_content.items() if not v]
    if disabled:
        print(f"    Disabled content types: {', '.join(disabled)}")

    print(f"\n    Local content:")
    for content_type in ["pages", "assignments", "announcements",
                         "discussions", "quizzes", "modules", "files",
                         "syllabus", "enrollments"]:
        type_dir = canvas_dir / content_type
        if type_dir.exists():
            count = len([f for f in type_dir.iterdir()
                         if not f.name.startswith("_")])
            print(f"      {content_type:<16} {count} files")

    # Count memory files
    prefix = f"{slug}__canvas-"
    if MEMORY_DIR.exists():
        mem_count = len([f for f in MEMORY_DIR.iterdir()
                         if f.name.startswith(prefix)])
    else:
        mem_count = 0
    print(f"\n    Memory files (RAG):    {mem_count}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        if len(sys.argv) < 3:
            print("Usage: canvas_sync.py status <course_id>", file=sys.stderr)
            sys.exit(1)
        cmd_status(int(sys.argv[2]))
        return

    # Commands that need the API client
    base_url, token = load_canvas_credentials()
    client = CanvasClient(base_url, token, write_mode="deny")

    if command == "full":
        if len(sys.argv) < 3:
            print("Usage: canvas_sync.py full <course_id>", file=sys.stderr)
            sys.exit(1)
        cmd_full(client, int(sys.argv[2]))

    elif command == "incremental":
        if len(sys.argv) < 3:
            print("Usage: canvas_sync.py incremental <course_id>",
                  file=sys.stderr)
            sys.exit(1)
        cmd_incremental(client, int(sys.argv[2]))

    elif command == "all":
        incremental = "--incremental" in sys.argv
        cmd_all(client, incremental)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available: full, incremental, all, status", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
