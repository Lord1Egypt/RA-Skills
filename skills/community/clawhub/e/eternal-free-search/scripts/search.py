#!/usr/bin/env python3
"""
DDG Search — Free web search via DuckDuckGo. No API key needed.
"""

import sys
import json
import argparse


def search_web(query, max_results=5, region='wt-wt', timelimit=None):
    """Standard web search."""
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=max_results, region=region, timelimit=timelimit)
        return [{'title': r['title'], 'url': r['href'], 'snippet': r['body']} for r in results]
    except Exception as e:
        return [{'error': str(e)}]


def search_news(query, max_results=5, region='wt-wt', timelimit=None):
    """News search."""
    try:
        from ddgs import DDGS
        results = DDGS().news(query, max_results=max_results, region=region, timelimit=timelimit)
        return [{
            'title': r['title'],
            'url': r['url'],
            'snippet': r['body'],
            'source': r.get('source', ''),
            'date': r.get('date', '')
        } for r in results]
    except Exception as e:
        return [{'error': str(e)}]


def search_qna(query):
    """Instant answer."""
    try:
        from ddgs import DDGS
        result = DDGS().answers(query)
        return result
    except Exception as e:
        return [{'error': str(e)}]


def search_images(query, max_results=5):
    """Image search."""
    try:
        from ddgs import DDGS
        results = DDGS().images(query, max_results=max_results)
        return [{
            'title': r['title'],
            'url': r['url'],
            'image': r['image'],
            'source': r.get('source', '')
        } for r in results]
    except Exception as e:
        return [{'error': str(e)}]


def search_suggestions(query):
    """Search suggestions."""
    try:
        from ddgs import DDGS
        results = DDGS().suggestions(query)
        return [r['phrase'] for r in results]
    except Exception as e:
        return [f'Error: {e}']


def format_results(results, mode='web'):
    """Format results for display."""
    if not results:
        return "  No results found."
    
    if results and 'error' in results[0]:
        return f"  ❌ Error: {results[0]['error']}"
    
    lines = []
    
    if mode == 'web':
        for i, r in enumerate(results, 1):
            lines.append(f"  {i}. {r['title']}")
            lines.append(f"     {r['url']}")
            lines.append(f"     {r['snippet'][:150]}")
            lines.append(f"")
    
    elif mode == 'news':
        for i, r in enumerate(results, 1):
            source = f" ({r['source']})" if r.get('source') else ''
            date = f" [{r['date'][:10]}]" if r.get('date') else ''
            lines.append(f"  {i}. {r['title']}{source}{date}")
            lines.append(f"     {r['url']}")
            lines.append(f"     {r['snippet'][:150]}")
            lines.append(f"")
    
    elif mode == 'qna':
        for r in results:
            if isinstance(r, dict):
                lines.append(f"  💡 {r.get('text', r.get('answer', str(r)))}")
            else:
                lines.append(f"  💡 {r}")
    
    elif mode == 'images':
        for i, r in enumerate(results, 1):
            lines.append(f"  {i}. {r['title']}")
            lines.append(f"     Image: {r['image'][:80]}")
            lines.append(f"     Page:  {r['url'][:80]}")
            lines.append(f"")
    
    elif mode == 'suggest':
        lines.append(f"  Suggestions:")
        for s in results:
            lines.append(f"  • {s}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Free Web Search (DuckDuckGo)')
    parser.add_argument('query', nargs='+', help='Search query')
    parser.add_argument('--news', action='store_true', help='News search')
    parser.add_argument('--qna', action='store_true', help='Instant answer')
    parser.add_argument('--images', action='store_true', help='Image search')
    parser.add_argument('--suggest', action='store_true', help='Suggestions')
    parser.add_argument('--max', type=int, default=5, help='Max results')
    parser.add_argument('--region', default='wt-wt', help='Region code')
    parser.add_argument('--time', choices=['d', 'w', 'm', 'y'], help='Time filter')
    parser.add_argument('--json', action='store_true', help='JSON output')
    args = parser.parse_args()
    
    query = ' '.join(args.query)
    
    if args.news:
        results = search_news(query, args.max, args.region, args.time)
        mode = 'news'
    elif args.qna:
        results = search_qna(query)
        mode = 'qna'
    elif args.images:
        results = search_images(query, args.max)
        mode = 'images'
    elif args.suggest:
        results = search_suggestions(query)
        mode = 'suggest'
    else:
        results = search_web(query, args.max, args.region, args.time)
        mode = 'web'
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n  🔍 Search: \"{query}\" ({mode})\n")
        if mode == 'suggest':
            print(format_results(results, mode))
        else:
            print(format_results(results, mode))


if __name__ == '__main__':
    main()
