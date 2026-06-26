#!/usr/bin/env python3
"""
Export Canvas assignment deadlines to iCalendar (.ics) format.
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from typing import List
from canvas_client import get_canvas_client


def format_ics_datetime(dt: datetime) -> str:
    """Format datetime for iCalendar (UTC)."""
    return dt.strftime("%Y%m%dT%H%M%SZ")


def escape_ics_text(text: str) -> str:
    """Escape special characters for iCalendar text."""
    return text.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')


def generate_ics_event(assignment, course_name: str, base_url: str) -> str:
    """Generate iCalendar VEVENT for an assignment."""
    lines = ["BEGIN:VEVENT"]
    
    # UID
    lines.append(f"UID:canvas-assignment-{assignment.id}@canvas-lms")
    
    # Summary
    summary = escape_ics_text(f"[{course_name}] {assignment.name}")
    lines.append(f"SUMMARY:{summary}")
    
    # Due date
    if hasattr(assignment, 'due_at') and assignment.due_at:
        try:
            due = datetime.fromisoformat(assignment.due_at.replace('Z', '+00:00'))
            lines.append(f"DTSTART:{format_ics_datetime(due)}")
            lines.append(f"DTEND:{format_ics_datetime(due + timedelta(hours=1))}")
            lines.append(f"DTSTAMP:{format_ics_datetime(datetime.now(timezone.utc))}")
        except:
            pass
    
    # Description
    desc_parts = [f"Course: {course_name}"]
    if hasattr(assignment, 'points_possible') and assignment.points_possible:
        desc_parts.append(f"Points: {assignment.points_possible}")
    if hasattr(assignment, 'description') and assignment.description:
        import re
        desc = re.sub(r'<[^>]+>', '', assignment.description)
        desc = desc[:200] + "..." if len(desc) > 200 else desc
        desc_parts.append(f"Description: {desc}")
    
    description = escape_ics_text("\\n".join(desc_parts))
    lines.append(f"DESCRIPTION:{description}")
    
    # URL
    if hasattr(assignment, 'html_url') and assignment.html_url:
        lines.append(f"URL:{assignment.html_url}")
    
    # Categories
    lines.append(f"CATEGORIES:{escape_ics_text(course_name)}")
    
    # Priority based on points (higher points = higher priority)
    if hasattr(assignment, 'points_possible') and assignment.points_possible:
        if assignment.points_possible >= 50:
            lines.append("PRIORITY:1")
        elif assignment.points_possible >= 20:
            lines.append("PRIORITY:5")
        else:
            lines.append("PRIORITY:9")
    
    lines.append("END:VEVENT")
    return "\n".join(lines)


def generate_ics_calendar(events: List[str], course_names: List[str]) -> str:
    """Generate complete iCalendar content."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Canvas LMS Skill//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:Canvas Assignments - {', '.join(course_names)}",
        "X-WR-TIMEZONE:UTC",
    ]
    
    for event in events:
        lines.append(event)
    
    lines.append("END:VCALENDAR")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Export Canvas deadlines to calendar")
    parser.add_argument("--course", "-c", type=str,
                        help="Comma-separated course IDs")
    parser.add_argument("--courses", type=str,
                        help="Comma-separated course IDs (alias)")
    parser.add_argument("--output", "-o", type=str, default="canvas-deadlines.ics",
                        help="Output file (default: canvas-deadlines.ics)")
    parser.add_argument("--unsubmitted-only", action="store_true",
                        help="Only export unsubmitted assignments")
    
    args = parser.parse_args()
    
    # Get course IDs
    course_ids_str = args.course or args.courses
    if not course_ids_str:
        print("Error: Must specify --course or --courses with comma-separated IDs")
        print("Example: --course 12345,12346,12347")
        sys.exit(1)
    
    course_ids = [int(c.strip()) for c in course_ids_str.split(",")]
    
    canvas = get_canvas_client()
    base_url = canvas._Canvas__requester.base_url
    
    all_events = []
    course_names = []
    
    try:
        for course_id in course_ids:
            course = canvas.get_course(course_id)
            course_names.append(course.name)
            print(f"Processing: {course.name}")
            
            # Get assignments
            kwargs = {'per_page': 100}
            if args.unsubmitted_only:
                kwargs['bucket'] = 'unsubmitted'
            kwargs['include'] = ['submission']
            
            assignments = list(course.get_assignments(**kwargs))
            
            # Filter only assignments with due dates
            assignments = [a for a in assignments if hasattr(a, 'due_at') and a.due_at]
            
            print(f"  Found {len(assignments)} assignments with deadlines")
            
            for assignment in assignments:
                event = generate_ics_event(assignment, course.name, base_url)
                all_events.append(event)
        
        if not all_events:
            print("\nNo assignments with deadlines found.")
            return
        
        # Generate calendar
        ics_content = generate_ics_calendar(all_events, course_names)
        
        # Write to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(ics_content)
        
        print(f"\n✓ Exported {len(all_events)} assignments to {args.output}")
        print(f"\nImport to your calendar:")
        print(f"  - Google Calendar: https://calendar.google.com → '+' → Import")
        print(f"  - Apple Calendar: File → Import")
        print(f"  - Outlook: Add Calendar → From file")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
