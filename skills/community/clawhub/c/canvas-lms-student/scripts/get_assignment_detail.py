#!/usr/bin/env python3
"""
Get detailed assignment information for AI-assisted writing.
Retrieves full assignment description, rubric, and requirements.
"""

import argparse
import json
import re
import sys
from canvas_client import get_canvas_client


def clean_html(html_text: str) -> str:
    """Remove HTML tags and decode HTML entities."""
    if not html_text:
        return ""
    import html
    text = re.sub(r'<[^>]+>', '', html_text)
    text = html.unescape(text)
    return text


def format_rubric(rubric):
    """Format rubric criteria for display."""
    if not rubric:
        return None
    
    formatted = []
    for criterion in rubric:
        crit_data = {
            "description": criterion.get('description', ''),
            "points": criterion.get('points', 0),
            "ratings": []
        }
        
        for rating in criterion.get('ratings', []):
            crit_data["ratings"].append({
                "description": rating.get('description', ''),
                "points": rating.get('points', 0)
            })
        
        formatted.append(crit_data)
    
    return formatted


def get_assignment_details(course, assignment_id: int):
    """Get comprehensive assignment details."""
    assignment = course.get_assignment(assignment_id, include=['rubric_assessment', 'submission'])
    
    details = {
        "basic_info": {
            "id": assignment.id,
            "name": assignment.name,
            "course": course.name,
            "course_id": course.id,
        },
        "requirements": {},
        "submission": {},
        "rubric": None,
        "metadata": {}
    }
    
    # Requirements
    if hasattr(assignment, 'description') and assignment.description:
        details["requirements"]["description"] = clean_html(assignment.description)
    
    if hasattr(assignment, 'points_possible') and assignment.points_possible:
        details["requirements"]["points_possible"] = assignment.points_possible
    
    if hasattr(assignment, 'due_at') and assignment.due_at:
        details["requirements"]["due_date"] = assignment.due_at
    
    if hasattr(assignment, 'submission_types') and assignment.submission_types:
        details["requirements"]["submission_types"] = assignment.submission_types
    
    if hasattr(assignment, 'allowed_extensions') and assignment.allowed_extensions:
        details["requirements"]["allowed_extensions"] = assignment.allowed_extensions
    
    # Submission info
    if hasattr(assignment, 'submission') and assignment.submission:
        sub = assignment.submission
        # Handle both dict and object formats
        if isinstance(sub, dict):
            workflow_state = sub.get('workflow_state', 'unsubmitted')
            details["submission"] = {
                "submitted": workflow_state != 'unsubmitted',
                "workflow_state": workflow_state,
                "score": sub.get('score'),
                "submitted_at": sub.get('submitted_at'),
                "late": sub.get('late', False),
            }
        else:
            details["submission"] = {
                "submitted": sub.workflow_state != 'unsubmitted',
                "workflow_state": sub.workflow_state,
                "score": getattr(sub, 'score', None),
                "submitted_at": getattr(sub, 'submitted_at', None),
                "late": getattr(sub, 'late', False),
            }
    
    # Rubric
    if hasattr(assignment, 'rubric') and assignment.rubric:
        details["rubric"] = format_rubric(assignment.rubric)
    
    # Metadata
    if hasattr(assignment, 'html_url') and assignment.html_url:
        details["metadata"]["url"] = assignment.html_url
    
    if hasattr(assignment, 'created_at') and assignment.created_at:
        details["metadata"]["created_at"] = assignment.created_at
    
    if hasattr(assignment, 'updated_at') and assignment.updated_at:
        details["metadata"]["updated_at"] = assignment.updated_at
    
    return details


def print_assignment_for_ai(details: dict):
    """Print assignment in format optimized for AI processing."""
    info = details["basic_info"]
    req = details["requirements"]
    
    print("=" * 70)
    print(f"ASSIGNMENT: {info['name']}")
    print(f"COURSE: {info['course']}")
    print("=" * 70)
    print()
    
    # Requirements section
    print("## ASSIGNMENT REQUIREMENTS")
    print()
    
    if 'points_possible' in req:
        print(f"**Total Points:** {req['points_possible']}")
    
    if 'due_date' in req:
        print(f"**Due Date:** {req['due_date']}")
    
    if 'submission_types' in req:
        print(f"**Submission Type:** {', '.join(req['submission_types'])}")
    
    if 'allowed_extensions' in req:
        print(f"**Allowed File Types:** {', '.join(req['allowed_extensions'])}")
    
    print()
    
    if 'description' in req:
        print("## DESCRIPTION / PROMPT")
        print()
        print(req['description'])
        print()
    
    # Rubric section
    if details['rubric']:
        print("## GRADING RUBRIC")
        print()
        for i, criterion in enumerate(details['rubric'], 1):
            print(f"{i}. **{criterion['description']}** ({criterion['points']} points)")
            if criterion['ratings']:
                print("   Scoring:")
                for rating in criterion['ratings']:
                    print(f"   - {rating['points']} pts: {rating['description']}")
            print()
    
    # Submission status
    if details['submission']:
        print("## YOUR SUBMISSION STATUS")
        print()
        sub = details['submission']
        if sub['submitted']:
            print(f"✓ Submitted: {sub['submitted_at']}")
            if sub['score'] is not None:
                print(f"Score: {sub['score']}")
        else:
            print("✗ Not yet submitted")
        print()
    
    # URL
    if details['metadata'].get('url'):
        print(f"**Canvas Link:** {details['metadata']['url']}")


def main():
    parser = argparse.ArgumentParser(
        description="Get assignment details for AI-assisted writing"
    )
    parser.add_argument("--course", "-c", type=int, required=True,
                        help="Course ID")
    parser.add_argument("--assignment", "-a", type=int, required=True,
                        help="Assignment ID")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--save", "-s", type=str,
                        help="Save output to file")
    
    args = parser.parse_args()
    
    canvas = get_canvas_client(silent=args.json)
    
    try:
        course = canvas.get_course(args.course)
        
        if not args.json:
            print(f"Fetching assignment details...\n", file=sys.stderr)
        
        details = get_assignment_details(course, args.assignment)
        
        if args.json:
            output = json.dumps(details, indent=2)
            print(output)
        else:
            print_assignment_for_ai(details)
        
        if args.save:
            with open(args.save, 'w', encoding='utf-8') as f:
                if args.json:
                    f.write(json.dumps(details, indent=2))
                else:
                    # Redirect print output
                    import io
                    old_stdout = sys.stdout
                    sys.stdout = buffer = io.StringIO()
                    print_assignment_for_ai(details)
                    sys.stdout = old_stdout
                    f.write(buffer.getvalue())
            if not args.json:
                print(f"\n✓ Saved to {args.save}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
