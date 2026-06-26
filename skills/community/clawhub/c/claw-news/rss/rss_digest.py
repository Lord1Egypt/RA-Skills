#!/usr/bin/env python3
"""
Digest Generator - Format news into readable digests.

Usage:
    python digest.py [options]

Options:
    --input FILE        Input JSON file from fetch_news.py or summarize.py
    --output FILE       Output file (default: stdout)
    --format FORMAT     Output format: markdown|json|text|slack (default: markdown)
    --category CAT      Filter by category
    --limit N           Max items to include (default: 10)
    --title TITLE       Custom digest title
    --template FILE     Custom template file
    --verbose, -v       Verbose output
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def get_markdown_template() -> str:
    """Default markdown template."""
    return """# {title}

*Generated: {timestamp}*

{content}

---

*Powered by Newsman* | {total} articles
"""


def get_text_template() -> str:
    """Default plain text template."""
    return """{title}
Generated: {timestamp}

{content}

---
Powered by Newsman | {total} articles
"""


def get_json_template_structure() -> Dict:
    """Default JSON structure."""
    return {
        "digest": {
            "title": "{title}",
            "generated_at": "{timestamp}",
            "total_articles": "{total}",
            "articles": []
        }
    }


def get_slack_template() -> str:
    """Default Slack Block Kit template."""
    return """{{
  "blocks": [
    {{
      "type": "header",
      "text": {{
        "type": "plain_text",
        "text": "{title}",
        "emoji": true
      }}
    }},
    {{
      "type": "section",
      "text": {{
        "type": "mrkdwn",
        "text": "*Generated:* {timestamp}\\n*{total} articles*"
      }}
    }},{content}
  ]
}}"""


def format_article_markdown(item: Dict, index: int) -> str:
    """Format single article as markdown."""
    title = item.get('title', 'Untitled')
    source = item.get('source', 'Unknown')
    published = item.get('published', '')
    link = item.get('link', '')
    
    # Use AI summary if available, otherwise use original summary
    summary = item.get('ai_summary', item.get('summary', ''))
    if not summary:
        summary = '*No summary available*'
    
    return f"""### {index}. {title}

**Source:** {source} | **Published:** {published}

{summary}

[Read more]({link})

---
"""


def format_article_text(item: Dict, index: int) -> str:
    """Format single article as plain text."""
    title = item.get('title', 'Untitled')
    source = item.get('source', 'Unknown')
    published = item.get('published', '')
    link = item.get('link', '')
    
    summary = item.get('ai_summary', item.get('summary', ''))
    if not summary:
        summary = 'No summary available'
    
    return f"""━━━━━━━━━━━━━━━━━━━━
{index}. {title}
Source: {source} | Published: {published}

{summary}

Link: {link}

"""


def format_article_slack(item: Dict, index: int) -> str:
    """Format single article as Slack Block Kit block."""
    title = item.get('title', 'Untitled')
    source = item.get('source', 'Unknown')
    link = item.get('link', '')
    
    summary = item.get('ai_summary', item.get('summary', ''))
    if not summary:
        summary = 'No summary available'
    
    # Truncate summary for Slack
    if len(summary) > 300:
        summary = summary[:297] + '...'
    
    return f"""    {{
      "type": "section",
      "text": {{
        "type": "mrkdwn",
        "text": "*{index}. {title}*\\n{summary}\\n\\nSource: {source} | <{link}|Read more>"
      }}
    }},
    {{
      "type": "divider"
    }}"""


def generate_markdown_digest(items: List[Dict], title: str) -> str:
    """Generate markdown format digest."""
    template = get_markdown_template()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    articles_content = '\n'.join(
        format_article_markdown(item, i + 1) for i, item in enumerate(items)
    )
    
    return template.format(
        title=title,
        timestamp=timestamp,
        content=articles_content,
        total=len(items)
    )


def generate_text_digest(items: List[Dict], title: str) -> str:
    """Generate plain text format digest."""
    template = get_text_template()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    articles_content = '\n'.join(
        format_article_text(item, i + 1) for i, item in enumerate(items)
    )
    
    return template.format(
        title=title,
        timestamp=timestamp,
        content=articles_content,
        total=len(items)
    )


def generate_json_digest(items: List[Dict], title: str) -> str:
    """Generate JSON format digest."""
    output = {
        "digest": {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(items),
            "articles": items
        }
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def generate_slack_digest(items: List[Dict], title: str) -> str:
    """Generate Slack Block Kit format digest."""
    template = get_slack_template()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    articles_content = ',\n'.join(
        format_article_slack(item, i + 1) for i, item in enumerate(items)
    )
    
    return template.format(
        title=title,
        timestamp=timestamp,
        content=articles_content,
        total=len(items)
    )


def get_default_title(category: str = None) -> str:
    """Generate default digest title."""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    
    if category:
        category_display = category.capitalize()
        return f"📰 {category_display} News Digest - {date_str}"
    return f"📰 Daily News Digest - {date_str}"


def filter_items(items: List[Dict], category: str = None) -> List[Dict]:
    """Filter items by category."""
    if not category:
        return items
    return [item for item in items if item.get('category') == category]


def main():
    parser = argparse.ArgumentParser(description='Generate news digest')
    parser.add_argument('--input', '-i', help='Input JSON file')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--format', '-f', default='markdown',
                        choices=['markdown', 'md', 'text', 'json', 'slack'],
                        help='Output format')
    parser.add_argument('--category', '-c', help='Filter by category')
    parser.add_argument('--limit', '-n', type=int, default=10,
                        help='Max items to include')
    parser.add_argument('--title', '-t', help='Custom digest title')
    parser.add_argument('--template', help='Custom template file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    # Extract items
    if 'items' in data:
        items = data['items']
    elif 'digest' in data and 'articles' in data['digest']:
        items = data['digest']['articles']
    else:
        items = data if isinstance(data, list) else [data]
    
    # Filter by category
    if args.category:
        items = filter_items(items, args.category)
    
    # Limit items
    items = items[:args.limit]
    
    if args.verbose:
        print(f"Generating digest with {len(items)} items...", file=sys.stderr)
    
    # Get title
    title = args.title or get_default_title(args.category)
    
    # Generate digest
    format_map = {
        'md': 'markdown',
        'markdown': 'markdown',
        'text': 'text',
        'json': 'json',
        'slack': 'slack'
    }
    fmt = format_map.get(args.format, args.format)
    
    if fmt == 'markdown':
        output = generate_markdown_digest(items, title)
    elif fmt == 'text':
        output = generate_text_digest(items, title)
    elif fmt == 'json':
        output = generate_json_digest(items, title)
    elif fmt == 'slack':
        output = generate_slack_digest(items, title)
    else:
        output = generate_markdown_digest(items, title)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        if args.verbose:
            print(f"Digest written to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
