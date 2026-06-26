#!/usr/bin/env python3
"""
Step 4: Format review findings to structured JSON.
Reads review_result.json and manual findings, outputs formatted comments.
"""

import json
import sys
from typing import List, Dict, Any


def create_comment(
    number: int,
    file_path: str,
    line: int,
    issue_type: str,
    severity: int,
    description: str,
    suggestion: str
) -> Dict[str, Any]:
    """Create a formatted comment structure."""
    
    # Build body in required format
    # Remove trailing periods from description and suggestion to avoid double periods
    desc = description.rstrip('。')
    sugg = suggestion.rstrip('。')
    body_lines = [
        f"【review】{issue_type}。{desc}。{sugg}。"
    ]
    
    return {
        "number": number,
        "path": file_path,
        "position": line,
        "severity": severity,
        "type": issue_type,
        "body": "\n".join(body_lines)
    }


def format_review(
    top3_issues: List[Dict],
    output_file: str = "formatted_review.json"
) -> Dict[str, Any]:
    """
    Format all review findings into structured JSON.
    
    Args:
        top3_issues: Top 3 issues selected for review
        output_file: Output JSON file path
    
    Returns:
        Structured review data
    """
    
    # Format as comments
    comments = []
    for i, issue in enumerate(top3_issues, 1):
        comment = create_comment(
            number=i,
            file_path=issue.get('path', ''),
            line=issue.get('position', 0),
            issue_type=issue['type'],
            severity=issue['severity'],
            description=issue['description'],
            suggestion=issue['suggestion'],
        )
        comments.append(comment)
    
    # Build output structure
    output = {
        "comments": comments
    }
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Formatted review saved to: {output_file}")
    
    return output


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python format_review.py <review_result.json> [output.json]")
        print("Or: python format_review.py --manual <manual_issues.json> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "formatted_review.json"
    
    # Load top3 issues
    top3_issues = []
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Support both 'top3_issues' (from Step 3) and 'issues' (legacy)
            top3_issues = data.get('top3_issues', data.get('issues', []))
    except Exception as e:
        print(f"Warning: Could not load {input_file}: {e}")
    
    # Format review
    result = format_review(top3_issues, output_file)
    
    # Print preview
    print("\n" + "="*60)
    print("Preview of formatted comments:")
    print("="*60)
    for comment in result['comments']:
        print(f"\n{comment['body']}")
        print("-"*60)


if __name__ == '__main__':
    main()
