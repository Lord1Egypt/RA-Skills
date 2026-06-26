#!/usr/bin/env python3
"""
List Canvas courses for the current user.
"""

import argparse
import json
import sys
from canvas_client import get_canvas_client


def format_course(course, include_grades: bool = False) -> str:
    """Format course information for display."""
    lines = [
        f"Course: {course.name}",
        f"  ID: {course.id}",
        f"  Code: {course.course_code}",
    ]
    
    if hasattr(course, 'enrollment_term_id') and course.enrollment_term_id:
        lines.append(f"  Term ID: {course.enrollment_term_id}")
    
    if include_grades and hasattr(course, 'enrollments') and course.enrollments:
        for enrollment in course.enrollments:
            if 'computed_current_score' in enrollment:
                score = enrollment['computed_current_score']
                grade = enrollment.get('computed_current_grade', 'N/A')
                lines.append(f"  Current Grade: {grade} ({score}%)")
    
    lines.append("")
    return "\n".join(lines)


def course_to_dict(course, include_grades: bool = False) -> dict:
    """Convert course object to dictionary."""
    result = {
        "id": course.id,
        "name": course.name,
        "code": course.course_code,
    }
    
    if hasattr(course, 'enrollment_term_id') and course.enrollment_term_id:
        result["term_id"] = course.enrollment_term_id
    
    if include_grades and hasattr(course, 'enrollments') and course.enrollments:
        for enrollment in course.enrollments:
            if 'computed_current_score' in enrollment:
                result["grade"] = {
                    "score": enrollment['computed_current_score'],
                    "letter": enrollment.get('computed_current_grade', 'N/A')
                }
    
    return result


def resolve_course_identifier(canvas, identifier: str):
    """
    Resolve a course identifier (ID or name) to a course object.
    
    Args:
        canvas: Canvas client
        identifier: Course ID (numeric) or course name/code
    
    Returns:
        Tuple of (course, matches) where matches is a list if multiple found
    """
    # Try to parse as ID first
    try:
        course_id = int(identifier)
        return canvas.get_course(course_id), None
    except ValueError:
        pass
    
    # Search by name (case-insensitive, normalize spaces/hyphens)
    search_term = identifier.lower().replace(' ', '').replace('-', '').replace('_', '')
    matches = []
    
    for course in canvas.get_courses(enrollment_state='active'):
        # Normalize course name for comparison
        course_normalized = course.name.lower().replace(' ', '').replace('-', '').replace('_', '')
        code_normalized = course.course_code.lower().replace(' ', '').replace('-', '').replace('_', '')
        
        # Exact match
        if search_term == course_normalized or search_term == code_normalized:
            return course, None
        
        # Partial match
        if search_term in course_normalized or search_term in code_normalized:
            matches.append(course)
    
    if len(matches) == 1:
        return matches[0], None
    elif len(matches) > 1:
        return None, matches
    else:
        return None, []


def main():
    parser = argparse.ArgumentParser(description="List Canvas courses")
    parser.add_argument("--active-only", action="store_true", 
                        help="Show only active enrollments")
    parser.add_argument("--with-grades", action="store_true",
                        help="Include current grades")
    parser.add_argument("--enrollment-type", choices=['student', 'teacher', 'ta', 'observer'],
                        help="Filter by enrollment type")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--resolve", type=str, metavar="IDENTIFIER",
                        help="Resolve course name/code to ID (returns matching course)")
    
    args = parser.parse_args()
    
    canvas = get_canvas_client(silent=args.json or args.resolve)
    
    # Handle course resolution mode
    if args.resolve:
        course, matches = resolve_course_identifier(canvas, args.resolve)
        
        if course:
            if args.json:
                print(json.dumps(course_to_dict(course, args.with_grades), indent=2))
            else:
                print(f"Resolved '{args.resolve}' to:")
                print(format_course(course, args.with_grades))
            return 0
        elif matches:
            if args.json:
                print(json.dumps([course_to_dict(c, args.with_grades) for c in matches], indent=2))
            else:
                print(f"Multiple matches found for '{args.resolve}':\n")
                for c in matches:
                    print(format_course(c, args.with_grades))
            return 0
        else:
            print(f"No course found matching '{args.resolve}'", file=sys.stderr)
            return 1
    
    # Build query parameters
    kwargs = {}
    if args.active_only:
        kwargs['enrollment_state'] = 'active'
    if args.enrollment_type:
        kwargs['enrollment_type'] = args.enrollment_type
    if args.with_grades:
        kwargs['include'] = ['total_scores']
    
    if not args.json:
        print("Fetching courses...\n", file=sys.stderr)
    
    try:
        courses = list(canvas.get_courses(**kwargs))
        
        if args.json:
            print(json.dumps([course_to_dict(c, args.with_grades) for c in courses], indent=2))
        else:
            if not courses:
                print("No courses found.")
                return
            
            print(f"Found {len(courses)} course(s):\n")
            print("=" * 50)
            
            for course in courses:
                print(format_course(course, args.with_grades))
            
            print("\nUse the Course ID with other scripts (e.g., --course 12345)")
            print("Or use --resolve to find by name (e.g., --resolve 'CS101')")
        
    except Exception as e:
        print(f"Error fetching courses: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
