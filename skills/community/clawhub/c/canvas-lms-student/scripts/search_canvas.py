#!/usr/bin/env python3
"""
Search across Canvas courses for files, assignments, and announcements.
"""

import argparse
import json
import re
import sys
from canvas_client import get_canvas_client


def search_in_text(text: str, query: str, case_sensitive: bool = False) -> bool:
    """Check if query exists in text."""
    if not text:
        return False
    if not case_sensitive:
        text = text.lower()
        query = query.lower()
    return query in text


def extract_context(text: str, query: str, context_chars: int = 100) -> str:
    """Extract context around the search match."""
    if not text:
        return ""
    
    text_lower = text.lower()
    query_lower = query.lower()
    
    idx = text_lower.find(query_lower)
    if idx == -1:
        return ""
    
    start = max(0, idx - context_chars)
    end = min(len(text), idx + len(query) + context_chars)
    
    context = text[start:end]
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    
    return context


def search_assignments(course, query: str, case_sensitive: bool = False, full_content: bool = False):
    """Search assignments in a course."""
    results = []
    
    for assignment in course.get_assignments(per_page=100):
        matches = []
        
        # Check name
        if search_in_text(assignment.name, query, case_sensitive):
            matches.append("name")
        
        # Check description
        desc_match = False
        desc = ""
        if hasattr(assignment, 'description') and assignment.description:
            import html
            desc = re.sub(r'<[^>]+>', '', assignment.description)
            desc = html.unescape(desc)
            if search_in_text(desc, query, case_sensitive):
                desc_match = True
                matches.append("description")
        
        if matches:
            result = {
                "course": course.name,
                "course_id": course.id,
                "type": "assignment",
                "title": assignment.name,
                "id": assignment.id,
                "matches": matches,
                "url": getattr(assignment, 'html_url', None)
            }
            
            if full_content and desc:
                result["content_preview"] = desc[:500]
            elif desc_match:
                result["match_context"] = extract_context(desc, query)
            
            results.append(result)
    
    return results


def search_files(course, query: str, case_sensitive: bool = False):
    """Search files in a course."""
    results = []
    
    for file in course.get_files(per_page=100):
        if search_in_text(file.display_name, query, case_sensitive):
            results.append({
                "course": course.name,
                "course_id": course.id,
                "type": "file",
                "title": file.display_name,
                "id": file.id,
                "size": getattr(file, 'size', None),
                "url": getattr(file, 'url', None),
                "matches": ["filename"]
            })
    
    return results


def search_announcements(course, query: str, case_sensitive: bool = False, full_content: bool = False):
    """Search announcements in a course."""
    results = []
    
    try:
        # Get announcements (as discussion topics with announcement flag)
        for topic in course.get_discussion_topics(only_announcements=True, per_page=50):
            matches = []
            
            if search_in_text(topic.title, query, case_sensitive):
                matches.append("title")
            
            message_match = False
            message = ""
            if hasattr(topic, 'message') and topic.message:
                import html
                message = re.sub(r'<[^>]+>', '', topic.message)
                message = html.unescape(message)
                if search_in_text(message, query, case_sensitive):
                    message_match = True
                    matches.append("message")
            
            if matches:
                result = {
                    "course": course.name,
                    "course_id": course.id,
                    "type": "announcement",
                    "title": topic.title,
                    "id": topic.id,
                    "posted_at": getattr(topic, 'posted_at', None),
                    "matches": matches,
                    "url": getattr(topic, 'html_url', None)
                }
                
                if full_content and message:
                    result["content_preview"] = message[:500]
                elif message_match:
                    result["match_context"] = extract_context(message, query)
                
                results.append(result)
    except Exception as e:
        # Some users may not have permission to view announcements
        pass
    
    return results


def search_discussions(course, query: str, case_sensitive: bool = False, full_content: bool = False):
    """Search discussion topics (non-announcements) in a course."""
    results = []
    
    try:
        # Get discussion topics (excluding announcements)
        for topic in course.get_discussion_topics(only_announcements=False, per_page=50):
            # Skip announcements (already searched)
            if getattr(topic, 'is_announcement', False):
                continue
            
            matches = []
            
            if search_in_text(topic.title, query, case_sensitive):
                matches.append("title")
            
            message_match = False
            message = ""
            if hasattr(topic, 'message') and topic.message:
                import html
                message = re.sub(r'<[^>]+>', '', topic.message)
                message = html.unescape(message)
                if search_in_text(message, query, case_sensitive):
                    message_match = True
                    matches.append("message")
            
            if matches:
                result = {
                    "course": course.name,
                    "course_id": course.id,
                    "type": "discussion",
                    "title": topic.title,
                    "id": topic.id,
                    "posted_at": getattr(topic, 'posted_at', None),
                    "matches": matches,
                    "url": getattr(topic, 'html_url', None)
                }
                
                if full_content and message:
                    result["content_preview"] = message[:500]
                elif message_match:
                    result["match_context"] = extract_context(message, query)
                
                results.append(result)
    except Exception as e:
        # Some users may not have permission to view discussions
        pass
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Search Canvas content")
    parser.add_argument("--query", "-q", type=str, required=True,
                        help="Search query")
    parser.add_argument("--course", "-c", type=int,
                        help="Search specific course only")
    parser.add_argument("--type", choices=['assignment', 'file', 'announcement', 'discussion', 'all'],
                        default='all', help="Content type to search")
    parser.add_argument("--case-sensitive", action="store_true",
                        help="Case-sensitive search")
    parser.add_argument("--full-content", action="store_true",
                        help="Show full content preview")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--limit", type=int, default=50,
                        help="Maximum results (default: 50)")
    
    args = parser.parse_args()
    
    canvas = get_canvas_client(silent=args.json)
    
    all_results = []
    
    try:
        # Get courses to search
        if args.course:
            courses = [canvas.get_course(args.course)]
        else:
            courses = list(canvas.get_courses(enrollment_state='active'))
        
        if not args.json:
            print(f"Searching in {len(courses)} course(s) for: '{args.query}'\n", file=sys.stderr)
        
        for course in courses:
            try:
                if args.type in ['all', 'assignment']:
                    results = search_assignments(course, args.query, args.case_sensitive, args.full_content)
                    all_results.extend(results)
                
                if args.type in ['all', 'file']:
                    results = search_files(course, args.query, args.case_sensitive)
                    all_results.extend(results)
                
                if args.type in ['all', 'announcement']:
                    results = search_announcements(course, args.query, args.case_sensitive, args.full_content)
                    all_results.extend(results)
                
                if args.type in ['all', 'discussion']:
                    results = search_discussions(course, args.query, args.case_sensitive, args.full_content)
                    all_results.extend(results)
            except Exception as e:
                # Skip courses where we don't have permission
                if "unauthorized" in str(e).lower() or "not authorized" in str(e).lower():
                    continue
                raise
        
        # Apply limit
        all_results = all_results[:args.limit]
        
        # Output results
        if args.json:
            print(json.dumps(all_results, indent=2))
        else:
            if not all_results:
                print("No results found.")
                return
            
            print(f"Found {len(all_results)} result(s):\n")
            print("=" * 70)
            
            for result in all_results:
                print(f"\n[{result['type'].upper()}] {result['title']}")
                print(f"  Course: {result['course']}")
                print(f"  Matched in: {', '.join(result['matches'])}")
                
                if 'match_context' in result:
                    print(f"  Context: {result['match_context']}")
                
                if 'content_preview' in result:
                    preview = result['content_preview'].replace('\n', ' ')[:300]
                    print(f"  Preview: {preview}...")
                
                if result.get('url'):
                    print(f"  Link: {result['url']}")
                
                print()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
