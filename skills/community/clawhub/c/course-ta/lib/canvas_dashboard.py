#!/usr/bin/env python3
"""Canvas dashboard — aggregated views across all active courses.

Provides deadline dashboards, submission tracking, engagement monitoring,
quiz statistics, and cross-section broadcasting.

Usage:
    python3 canvas_dashboard.py deadlines [--days 7]         # Upcoming deadlines
    python3 canvas_dashboard.py submissions <course_id> <assignment_name>  # Missing submissions
    python3 canvas_dashboard.py engagement <course_id>       # Discussion engagement
    python3 canvas_dashboard.py grades <course_id>           # Grade overview per assignment
    python3 canvas_dashboard.py roster <course_id>           # Student roster
    python3 canvas_dashboard.py broadcast <message>          # Post announcement to all sections
"""

import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from canvas_api import CanvasClient, CanvasAPIError, load_canvas_credentials
from paths import CANVAS_CONFIG as CANVAS_CONFIG_PATH


def _load_config() -> dict:
    if CANVAS_CONFIG_PATH.exists():
        return json.loads(CANVAS_CONFIG_PATH.read_text())
    return {"active_courses": []}


def _parse_dt(iso_str: str) -> datetime:
    if not iso_str:
        return None
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Deadline Dashboard
# ---------------------------------------------------------------------------

def cmd_deadlines(client: CanvasClient, days: int = 7):
    """Show upcoming deadlines across all active courses."""
    config = _load_config()
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=days)

    all_deadlines = []

    for course_entry in config.get("active_courses", []):
        canvas_id = course_entry["canvas_id"]
        slug = course_entry["slug"]
        name = course_entry.get("name", slug)

        try:
            assignments = client.get_assignments(canvas_id)
        except CanvasAPIError:
            continue

        for a in assignments:
            due = a.get("due_at")
            if not due:
                continue
            due_dt = _parse_dt(due)
            if due_dt and now <= due_dt <= cutoff:
                all_deadlines.append({
                    "course": name,
                    "slug": slug,
                    "assignment": a["name"],
                    "due": due_dt,
                    "points": a.get("points_possible", 0),
                    "type": ", ".join(a.get("submission_types", [])),
                    "canvas_id": canvas_id,
                    "assignment_id": a["id"],
                })

    # Sort by due date
    all_deadlines.sort(key=lambda x: x["due"])

    print(f"\n  === Upcoming Deadlines (next {days} days) ===\n")

    if not all_deadlines:
        print("  No deadlines in this window.")
        return

    current_date = None
    for d in all_deadlines:
        date_str = d["due"].strftime("%A, %B %d")
        if date_str != current_date:
            current_date = date_str
            print(f"\n  {date_str}")
            print(f"  {'─' * 60}")

        time_str = d["due"].strftime("%I:%M %p UTC")
        delta = d["due"] - now
        hours_left = delta.total_seconds() / 3600

        if hours_left < 24:
            urgency = " ⚠️"
        elif hours_left < 48:
            urgency = " ⏰"
        else:
            urgency = ""

        print(f"    {time_str}  {d['assignment'][:45]:<47}  "
              f"({d['points']} pts){urgency}")
        print(f"             {d['course'][:55]}")

    print(f"\n  Total: {len(all_deadlines)} upcoming deadlines")


# ---------------------------------------------------------------------------
# Submission Tracker
# ---------------------------------------------------------------------------

def cmd_submissions(client: CanvasClient, course_id: int, assignment_search: str):
    """Show who hasn't submitted a specific assignment."""
    assignments = client.get_assignments(course_id)

    # Try ID-based lookup first
    try:
        search_id = int(assignment_search)
        matches = [a for a in assignments if a["id"] == search_id]
    except ValueError:
        # Fall back to substring search
        search_lower = assignment_search.lower()
        matches = [a for a in assignments if search_lower in a["name"].lower()]

    if not matches:
        print(f"  No assignment matching '{assignment_search}' found.")
        print(f"\n  Available assignments:")
        for a in assignments:
            print(f"    {a['id']:>8}  {a['name'][:60]}")
        return

    if len(matches) > 1:
        print(f"  Multiple matches found:")
        for a in matches:
            print(f"    {a['id']}: {a['name']}")
        print(f"  Please be more specific.")
        return

    assignment = matches[0]
    print(f"\n  === Submission Tracker: {assignment['name']} ===")
    print(f"  Due: {assignment.get('due_at', 'N/A')}")
    print(f"  Points: {assignment.get('points_possible', 'N/A')}")

    # Get submissions
    submissions = client.get_submissions(course_id, assignment["id"])

    # Get enrollments for student names
    enrollments = client.get_enrollments(course_id)
    students = {}
    for e in enrollments:
        if e["type"] == "StudentEnrollment" and e.get("enrollment_state") == "active":
            user = e.get("user", {})
            students[e["user_id"]] = user.get("name", user.get("sortable_name", "?"))

    submitted = set()
    graded = set()
    not_submitted = []

    for s in submissions:
        uid = s.get("user_id")
        if s.get("workflow_state") in ("submitted", "graded", "pending_review"):
            submitted.add(uid)
        if s.get("workflow_state") == "graded":
            graded.add(uid)

    for uid, name in sorted(students.items(), key=lambda x: x[1]):
        if uid not in submitted:
            not_submitted.append(name)

    print(f"\n  Submitted: {len(submitted)}/{len(students)}")
    print(f"  Graded:    {len(graded)}/{len(students)}")

    if not_submitted:
        print(f"\n  Missing submissions ({len(not_submitted)}):")
        for name in not_submitted:
            print(f"    - {name}")
    else:
        print(f"\n  All students have submitted!")


# ---------------------------------------------------------------------------
# Engagement Monitor
# ---------------------------------------------------------------------------

def cmd_engagement(client: CanvasClient, course_id: int):
    """Show discussion engagement rates."""
    topics = client.get_discussion_topics(course_id)
    enrollments = client.get_enrollments(course_id)

    student_count = sum(1 for e in enrollments
                        if e["type"] == "StudentEnrollment"
                        and e.get("enrollment_state") == "active")

    print(f"\n  === Discussion Engagement (course {course_id}) ===")
    print(f"  Active students: {student_count}\n")

    for topic in topics:
        if topic.get("is_announcement"):
            continue

        title = topic.get("title", "?")
        reply_count = topic.get("discussion_subentry_count", 0)
        pct = (reply_count / student_count * 100) if student_count > 0 else 0

        # Engagement indicator
        if pct >= 80:
            indicator = "🟢"
        elif pct >= 50:
            indicator = "🟡"
        elif pct >= 20:
            indicator = "🟠"
        else:
            indicator = "🔴"

        print(f"  {indicator} {title[:50]:<52}  "
              f"{reply_count:>3}/{student_count} replies ({pct:.0f}%)")

    print()


# ---------------------------------------------------------------------------
# Grade Overview
# ---------------------------------------------------------------------------

def cmd_grades(client: CanvasClient, course_id: int):
    """Show grade statistics per assignment."""
    assignments = client.get_assignments(course_id)

    print(f"\n  === Grade Overview (course {course_id}) ===\n")
    print(f"  {'Assignment':<45}  {'Max':>5}  {'Mean':>6}  {'Med':>5}  "
          f"{'Min':>5}  {'Max':>5}  {'Sub':>4}")
    print(f"  {'─' * 45}  {'─' * 5}  {'─' * 6}  {'─' * 5}  "
          f"{'─' * 5}  {'─' * 5}  {'─' * 4}")

    for a in sorted(assignments, key=lambda x: x.get("due_at") or "9999"):
        pts = a.get("points_possible", 0)
        if not pts or pts == 0:
            continue

        try:
            subs = client.get_submissions(course_id, a["id"])
        except CanvasAPIError:
            continue

        scores = [s.get("score") for s in subs
                  if s.get("score") is not None and s.get("workflow_state") == "graded"]

        if not scores:
            print(f"  {a['name'][:45]:<45}  {pts:>5.0f}  {'—':>6}  {'—':>5}  "
                  f"{'—':>5}  {'—':>5}  {0:>4}")
            continue

        scores.sort()
        mean = sum(scores) / len(scores)
        median = scores[len(scores) // 2]
        low = min(scores)
        high = max(scores)

        print(f"  {a['name'][:45]:<45}  {pts:>5.0f}  {mean:>6.1f}  "
              f"{median:>5.1f}  {low:>5.1f}  {high:>5.1f}  {len(scores):>4}")

    print()


# ---------------------------------------------------------------------------
# Roster
# ---------------------------------------------------------------------------

def cmd_roster(client: CanvasClient, course_id: int):
    """Show student roster for a course."""
    enrollments = client.get_enrollments(course_id)

    by_role = {}
    for e in enrollments:
        role = e.get("type", "Unknown")
        user = e.get("user", {})
        name = user.get("name", user.get("sortable_name", "?"))
        state = e.get("enrollment_state", "?")
        by_role.setdefault(role, []).append((name, state))

    print(f"\n  === Roster (course {course_id}) ===\n")

    for role in ["TeacherEnrollment", "TaEnrollment", "StudentEnrollment",
                 "ObserverEnrollment", "DesignerEnrollment"]:
        members = by_role.pop(role, [])
        if not members:
            continue
        label = role.replace("Enrollment", "").upper() + "S"
        print(f"  {label} ({len(members)})")
        for name, state in sorted(members):
            state_indicator = "" if state == "active" else f" [{state}]"
            print(f"    - {name}{state_indicator}")
        print()

    # Any remaining roles
    for role, members in by_role.items():
        print(f"  {role} ({len(members)})")
        for name, state in sorted(members):
            print(f"    - {name}")
        print()


# ---------------------------------------------------------------------------
# Cross-Section Broadcast
# ---------------------------------------------------------------------------

def cmd_broadcast(client: CanvasClient, message: str):
    """Post an announcement to all active courses (with confirmation).

    Groups courses by base course code to identify sections of the same course.
    """
    config = _load_config()
    active = config.get("active_courses", [])

    if not active:
        print("  No active courses.")
        return

    # Show what will be posted
    print(f"\n  === Cross-Section Broadcast ===\n")
    print(f"  Message:\n    {message}\n")
    print(f"  Will post to {len(active)} course(s):")
    for c in active:
        print(f"    - [{c['canvas_id']}] {c['name']}")

    # Confirmation gate
    try:
        confirm = input(f"\n  Post announcement to all {len(active)} courses? [y/N] ")
    except (EOFError, KeyboardInterrupt):
        print("\n  Cancelled.")
        return

    if confirm.strip().lower() not in ("y", "yes"):
        print("  Cancelled.")
        return

    # Use write_mode="allow" here because we already prompted above
    write_client = CanvasClient(
        client.base_url, client.access_token, write_mode="allow")

    posted = 0
    for c in active:
        try:
            write_client.post(
                f"/api/v1/courses/{c['canvas_id']}/discussion_topics",
                json_body={
                    "title": message[:80],
                    "message": f"<p>{message}</p>",
                    "is_announcement": True,
                    "published": True,
                },
                action_description=f"Post announcement to {c['name']}",
            )
            print(f"    ✅ Posted to {c['name']}")
            posted += 1
        except Exception as e:
            print(f"    ❌ Failed for {c['name']}: {e}")

    print(f"\n  Posted to {posted}/{len(active)} courses.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    base_url, token = load_canvas_credentials()
    client = CanvasClient(base_url, token, write_mode="deny")

    if command == "deadlines":
        days = 7
        if "--days" in sys.argv:
            idx = sys.argv.index("--days")
            if idx + 1 < len(sys.argv):
                days = int(sys.argv[idx + 1])
        cmd_deadlines(client, days)

    elif command == "submissions":
        if len(sys.argv) < 4:
            print("Usage: canvas_dashboard.py submissions <course_id> <assignment_name>",
                  file=sys.stderr)
            sys.exit(1)
        cmd_submissions(client, int(sys.argv[2]), " ".join(sys.argv[3:]))

    elif command == "engagement":
        if len(sys.argv) < 3:
            print("Usage: canvas_dashboard.py engagement <course_id>",
                  file=sys.stderr)
            sys.exit(1)
        cmd_engagement(client, int(sys.argv[2]))

    elif command == "grades":
        if len(sys.argv) < 3:
            print("Usage: canvas_dashboard.py grades <course_id>",
                  file=sys.stderr)
            sys.exit(1)
        cmd_grades(client, int(sys.argv[2]))

    elif command == "roster":
        if len(sys.argv) < 3:
            print("Usage: canvas_dashboard.py roster <course_id>",
                  file=sys.stderr)
            sys.exit(1)
        cmd_roster(client, int(sys.argv[2]))

    elif command == "broadcast":
        if len(sys.argv) < 3:
            print("Usage: canvas_dashboard.py broadcast '<message>'",
                  file=sys.stderr)
            sys.exit(1)
        cmd_broadcast(client, " ".join(sys.argv[2:]))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available: deadlines, submissions, engagement, grades, roster, broadcast",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
