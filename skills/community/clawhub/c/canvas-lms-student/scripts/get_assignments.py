#!/usr/bin/env python3
"""
Get assignments for a specific Canvas course.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from canvas_client import get_canvas_client


def parse_date(date_str: str) -> datetime:
    """Parse ISO format date string."""
    if not date_str:
        return None
    date_str = date_str.replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None


def format_assignment(assignment, include_description: bool = False) -> str:
    """Format assignment information for display."""
    lines = [
        f"Assignment: {assignment.name}",
        f"  ID: {assignment.id}",
    ]
    
    if hasattr(assignment, 'points_possible') and assignment.points_possible:
        lines.append(f"  Points: {assignment.points_possible}")
    
    if hasattr(assignment, 'due_at') and assignment.due_at:
        due = parse_date(assignment.due_at)
        if due:
            lines.append(f"  Due: {due.strftime('%Y-%m-%d %H:%M')}")
        else:
            lines.append(f"  Due: {assignment.due_at}")
    else:
        lines.append(f"  Due: No deadline")
    
    if hasattr(assignment, 'submission_types') and assignment.submission_types:
        lines.append(f"  Submission: {', '.join(assignment.submission_types)}")
    
    if hasattr(assignment, 'workflow_state'):
        lines.append(f"  State: {assignment.workflow_state}")
    
    if include_description and hasattr(assignment, 'description') and assignment.description:
        desc = re.sub(r'<[^>]+>', '', assignment.description)
        desc = desc[:500] + "..." if len(desc) > 500 else desc
        lines.append(f"  Description:\n    {desc}")
    
    lines.append("")
    return "\n".join(lines)


def assignment_to_dict(assignment) -> dict:
    """Convert assignment object to dictionary."""
    result = {
        "id": assignment.id,
        "name": assignment.name,
    }
    
    if hasattr(assignment, 'points_possible') and assignment.points_possible:
        result["points_possible"] = assignment.points_possible
    
    if hasattr(assignment, 'due_at') and assignment.due_at:
        result["due_at"] = assignment.due_at
    
    if hasattr(assignment, 'submission_types') and assignment.submission_types:
        result["submission_types"] = assignment.submission_types
    
    if hasattr(assignment, 'workflow_state'):
        result["workflow_state"] = assignment.workflow_state
    
    # Add submission status if available
    if hasattr(assignment, 'submission') and assignment.submission:
        sub = assignment.submission
        if isinstance(sub, dict):
            result["submission"] = {
                "submitted": sub.get('workflow_state') != 'unsubmitted',
                "workflow_state": sub.get('workflow_state'),
                "score": sub.get('score'),
                "late": sub.get('late', False),
            }
        else:
            result["submission"] = {
                "submitted": sub.workflow_state != 'unsubmitted',
                "workflow_state": sub.workflow_state,
                "score": getattr(sub, 'score', None),
                "late": getattr(sub, 'late', False),
            }
    
    return result


def resolve_assignment_by_name(course, name_query: str):
    """
    Resolve an assignment by name (partial match).
    
    Args:
        course: Canvas course object
        name_query: Assignment name or partial name
    
    Returns:
        Tuple of (assignment, matches) where matches is a list if multiple found
    """
    search_term = name_query.lower().replace(' ', '')
    matches = []
    
    for assignment in course.get_assignments(per_page=100):
        assignment_normalized = assignment.name.lower().replace(' ', '')
        
        # Exact match
        if search_term == assignment_normalized:
            return assignment, None
        
        # Partial match
        if search_term in assignment_normalized:
            matches.append(assignment)
    
    if len(matches) == 1:
        return matches[0], None
    elif len(matches) > 1:
        return None, matches
    else:
        return None, []


def main():
    parser = argparse.ArgumentParser(description="Get Canvas course assignments")
    parser.add_argument("--course", "-c", type=str, required=True,
                        help="Course ID (numeric) or course name/code (use --resolve-name to search)")
    parser.add_argument("--resolve-name", action="store_true",
                        help="Treat --course as a name to resolve (fuzzy match)")
    parser.add_argument("--assignment-name", type=str,
                        help="Find specific assignment by name (fuzzy match)")
    parser.add_argument("--upcoming", action="store_true",
                        help="Show only upcoming assignments")
    parser.add_argument("--overdue", action="store_true",
                        help="Show only overdue assignments")
    parser.add_argument("--submitted", action="store_true",
                        help="Show only submitted assignments")
    parser.add_argument("--unsubmitted", action="store_true",
                        help="Show only unsubmitted assignments")
    parser.add_argument("--with-description", action="store_true",
                        help="Include assignment descriptions")
    parser.add_argument("--limit", type=int, default=50,
                        help="Maximum assignments to show (default: 50)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    
    args = parser.parse_args()
    
    canvas = get_canvas_client(silent=args.json)
    
    try:
        # Resolve course if needed
        if args.resolve_name:
            from list_courses import resolve_course_identifier
            course, matches = resolve_course_identifier(canvas, args.course)
            if not course:
                if matches:
                    print(f"Multiple courses matched '{args.course}':", file=sys.stderr)
                    for c in matches:
                        print(f"  - {c.name} (ID: {c.id})", file=sys.stderr)
                else:
                    print(f"No course found matching '{args.course}'", file=sys.stderr)
                sys.exit(1)
        else:
            course = canvas.get_course(int(args.course))
        
        if not args.json:
            print(f"Course: {course.name}\n", file=sys.stderr)
        
        # If looking for specific assignment by name
        if args.assignment_name:
            assignment, matches = resolve_assignment_by_name(course, args.assignment_name)
            if assignment:
                if args.json:
                    print(json.dumps(assignment_to_dict(assignment), indent=2))
                else:
                    print(f"Found assignment:\n")
                    print(format_assignment(assignment, args.with_description))
                return
            elif matches:
                if args.json:
                    print(json.dumps([assignment_to_dict(a) for a in matches], indent=2))
                else:
                    print(f"Multiple assignments matched '{args.assignment_name}':\n")
                    for a in matches:
                        print(format_assignment(a, args.with_description))
                return
            else:
                print(f"No assignment found matching '{args.assignment_name}'", file=sys.stderr)
                sys.exit(1)
        
        # Build query parameters
        kwargs = {'per_page': 100}
        
        if args.upcoming:
            kwargs['bucket'] = 'future'
        elif args.overdue:
            kwargs['bucket'] = 'overdue'
        elif args.submitted:
            kwargs['bucket'] = 'submitted'
        elif args.unsubmitted:
            kwargs['bucket'] = 'unsubmitted'
        
        kwargs['include'] = ['submission']
        kwargs['order_by'] = 'due_at'
        
        assignments = list(course.get_assignments(**kwargs))
        
        # Apply limit
        assignments = assignments[:args.limit]
        
        if args.json:
            print(json.dumps([assignment_to_dict(a) for a in assignments], indent=2))
        else:
            if not assignments:
                print("No assignments found matching criteria.")
                return
            
            print(f"Found {len(assignments)} assignment(s):\n")
            print("=" * 60)
            
            for assignment in assignments:
                print(format_assignment(assignment, args.with_description))
            
            if assignments:
                print(f"\nUse --assignment {assignments[0].id} with get_assignment_detail.py for full info")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
