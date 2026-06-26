"""
Blog Automation for OpenClaw
Publish articles to WordPress blog
"""

import os
import json
import re
import argparse
import base64
from datetime import datetime
import requests

try:
    import markdown
except ImportError:
    # Simple fallback markdown converter
    def simple_md_to_html(text):
        text = re.sub(r'^(#{1,6})\s+(.+)$', lambda m: f"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>", text, flags=re.M)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = text.replace('\n\n', '</p><p>')
        return f"<p>{text}</p>"
    markdown = type('obj', (object,), {'markdown': simple_md_to_html})()

class BlogPublisher:
    def __init__(self, wp_url, username, app_token):
        self.wp_url = wp_url.rstrip('/')
        self.username = username
        self.app_token = app_token
        self.base_url = f"{self.wp_url}/wp-json/wp/v2"

    def _get_auth_header(self):
        credentials = f"{self.username}:{self.app_token}"
        token = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {token}"}

    def publish(self, article_json_path, schedule=None, categories=None, tags=None):
        """Publish article to WordPress"""
        # Load article
        with open(article_json_path, 'r') as f:
            article = json.load(f)

        # Convert content to HTML
        content_html = markdown.markdown(article['content'])

        # Prepare post data
        post_data = {
            "title": article['title'],
            "content": content_html,
            "status": "future" if schedule else "publish",
            "author": article.get('author', 'PayLessTax Team')
        }

        if schedule:
            post_data["date"] = schedule

        if categories:
            post_data["categories"] = categories
        if tags:
            post_data["tags"] = tags

        # Make API request
        headers = {
            **self._get_auth_header(),
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                f"{self.base_url}/posts",
                headers=headers,
                json=post_data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            return {
                "status": "scheduled" if schedule else "published",
                "wordpress_id": result.get('id'),
                "url": result.get('link'),
                "title": article['title'],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            # Save locally if publishing fails
            failed_path = article_json_path.replace('.json', '_failed.html')
            with open(failed_path, 'w') as f:
                f.write(content_html)

            return {
                "status": "failed",
                "error": str(e),
                "saved_locally": failed_path,
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--wp-url', required=True, help='WordPress site URL')
    parser.add_argument('--username', required=True, help='WordPress username')
    parser.add_argument('--app-token', required=True, help='WordPress app password')
    parser.add_argument('--article', required=True, help='Path to article JSON')
    parser.add_argument('--schedule', help='Schedule publish time (ISO format)')
    parser.add_argument('--categories', help='Comma-separated category IDs')
    parser.add_argument('--tags', help='Comma-separated tag IDs')
    parser.add_argument('--log', default='./log.txt', help='Log file path')

    args = parser.parse_args()

    categories = [int(c.strip()) for c in args.categories.split(',')] if args.categories else None
    tags = [int(t.strip()) for t in args.tags.split(',')] if args.tags else None

    publisher = BlogPublisher(args.wp_url, args.username, args.app_token)
    result = publisher.publish(args.article, args.schedule, categories, tags)

    # Log result
    log_entry = f"[{result['timestamp']}] {args.article} -> {result['status']}"
    if result['status'] == 'failed':
        log_entry += f" | Error: {result.get('error', 'Unknown')}"
    else:
        log_entry += f" | URL: {result.get('url', 'N/A')}"

    with open(args.log, 'a') as f:
        f.write(log_entry + '\n')

    print(json.dumps(result, indent=2))
