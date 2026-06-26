"""
Git Publisher Runner - Downloads articles from Notion and publishes to Git
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
import importlib.util
from dotenv import load_dotenv

# Load .env
env_path = '/Users/nabang/Documents/OpenClaw/.env'
load_dotenv(env_path, override=True)

# Load NotionPublisher directly
spec = importlib.util.spec_from_file_location(
    "notion_publisher",
    "/Users/nabang/Documents/OpenClaw/modules/intelligence/notion_publisher.py"
)
notion_publisher_module = importlib.util.module_from_spec(spec)

class MockLogger:
    def info(self, msg): print(f"[INFO] {msg}")
    def warning(self, msg): print(f"[WARN] {msg}")
    def error(self, msg): print(f"[ERROR] {msg}")

class MockUtils:
    @staticmethod
    def setup_logger(name, log_file):
        return MockLogger()

sys.modules['modules'] = type(sys)('modules')
sys.modules['modules.intelligence'] = type(sys)('intelligence')
sys.modules['modules.intelligence.config'] = type('Config', (), {
    'NOTION_API_KEY': os.getenv('NOTION_API_KEY', ''),
    'NOTION_DATABASE_ID': os.getenv('NOTION_DATABASE_ID') or os.getenv('BLOG_DATABASE_ID', ''),
    'BLOG_REPO_PATH': Path(os.getenv('BLOG_REPO_PATH', '~/Documents/OpenClaw/rebugui.github.io')),
    'BLOG_URL': os.getenv('BLOG_URL', 'https://rebugui.github.io/'),
})
sys.modules['modules.intelligence.utils'] = MockUtils

import requests
spec.loader.exec_module(notion_publisher_module)
NotionPublisher = notion_publisher_module.NotionPublisher

def publish_article(article, publisher, blog_repo_path, blog_url):
    """Publish a single article from Notion to Git"""
    try:
        page_id = article.get('id', '')
        props = article.get('properties', {})
        title_prop = props.get('내용', {}).get('title', [])
        title = title_prop[0].get('text', {}).get('content', 'N/A') if title_prop else 'N/A'

        print(f"\n{'='*60}")
        print(f"Publishing: {title}")
        print(f"{'='*60}")

        # Get content
        content = publisher.get_page_content(page_id)
        if not content:
            content = "이 글은 LLM을 기반으로 작성되었습니다."

        # Check for Mermaid
        mermaid_count = content.count('```mermaid')
        if mermaid_count > 0:
            print(f"✓ Found {mermaid_count} Mermaid diagram(s)")

        # Get metadata
        category = props.get('카테고리', {}).get('select', {}).get('name', '보안')
        tags_objs = props.get('테그', {}).get('multi_select', [])
        tags_list = [tag.get('name', '') for tag in tags_objs]

        # Create slug
        import re
        if re.search(r'[가-힣]', title):
            slug = title.replace(' ', '-')
        else:
            slug = title.lower().replace(' ', '-')
        slug = re.sub(r'[^\w\-]', '', slug)

        # Create directory
        post_dir = blog_repo_path / "content" / "post" / category / slug
        post_dir.mkdir(parents=True, exist_ok=True)

        # Create markdown file
        md_file = post_dir / "index.md"
        front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")}
draft: false
tags:
{chr(10).join(f'  - "{tag}"' for tag in tags_list)}
categories:
  - "{category}"
---

{content}
"""

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(front_matter)

        print(f"✓ Created: {md_file}")
        print(f"  Category: {category}")
        print(f"  Tags: {', '.join(tags_list)}")
        print(f"  Content length: {len(content)} chars")

        # Git operations
        print("\n[Git] Adding changes...")
        subprocess.run(['git', 'add', '.'],
                      cwd=blog_repo_path,
                      check=True,
                      capture_output=True)

        print("[Git] Committing...")
        subprocess.run(['git', 'commit', '-m', f"feat: 블로그 글 추가 - {title}"],
                      cwd=blog_repo_path,
                      check=True,
                      capture_output=True)

        print("[Git] Pushing to remote...")
        subprocess.run(['git', 'push', 'origin', 'main'],
                      cwd=blog_repo_path,
                      check=True,
                      capture_output=True)

        print("✓ Git push completed")

        # Update Notion
        blog_url_full = f"{blog_url}p/{slug}/"
        publisher.update_published_url(page_id, blog_url_full)
        publisher.update_status(page_id, "게시 완료")

        print(f"✓ Published: {blog_url_full}")

        return True

    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 70)
    print("Git Publisher - Notion → Git → GitHub")
    print("=" * 70)

    publisher = NotionPublisher()
    blog_repo_path = Path(os.getenv('BLOG_REPO_PATH', '~/Documents/OpenClaw/rebugui.github.io')).expanduser()
    blog_url = os.getenv('BLOG_URL', 'https://rebugui.github.io/')

    print(f"\nBlog Repository: {blog_repo_path}")
    print(f"Blog URL: {blog_url}")

    # Get review done articles
    print("\n[Step 1] Fetching '검토 완료' articles from Notion...")
    articles = publisher.get_review_done_articles()

    if not articles:
        print("⚠️  No articles with '검토 완료' status found.")
        return

    print(f"✓ Found {len(articles)} article(s)")

    # Publish each article
    results = []
    for idx, article in enumerate(articles, 1):
        print(f"\n[Step 2.{idx}] Processing article {idx}/{len(articles)}...")
        success = publish_article(article, publisher, blog_repo_path, blog_url)
        results.append(success)

    # Summary
    print("\n" + "=" * 70)
    print("Publishing Summary")
    print("=" * 70)
    print(f"Total: {len(articles)} articles")
    print(f"Success: {sum(results)} articles")
    print(f"Failed: {len(results) - sum(results)} articles")

    if all(results):
        print("\n✅ All articles published successfully!")

        # Next steps
        print("\nNext steps:")
        print(f"1. Check the blog repository: {blog_repo_path}")
        print("2. Build Hugo site:")
        print(f"   cd {blog_repo_path} && hugo")
        print("3. Check the deployed blog")
    else:
        print("\n⚠️  Some articles failed to publish. Check the errors above.")

if __name__ == "__main__":
    main()
