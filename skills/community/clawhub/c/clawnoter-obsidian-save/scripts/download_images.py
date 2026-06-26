#!/usr/bin/env python3
"""
Image extraction and download script for obsidian-save-article skill.
Downloads images from a webpage and saves them to a local folder.
"""

import os
import re
import hashlib
import urllib.request
import urllib.error
import asyncio
import importlib.util
from urllib.parse import urljoin, urlparse
from html import unescape
import sys
import json

KNOWN_IMAGE_HOST_TOKENS = (
    'mmbiz',
    'qpic.cn',
    'wx.qq.com',
    'wximg.qq.com',
    'twimg.com',
)

KNOWN_NON_CONTENT_IMAGE_HOST_TOKENS = (
    'abs.twimg.com',
    'abs-0.twimg.com',
    'abs-1.twimg.com',
    'abs-2.twimg.com',
)

KNOWN_IMAGE_QUERY_KEYS = (
    'image',
    'img',
    'wx_fmt=',
    'format=',
    'mime=',
)

IMG_ATTRIBUTE_CANDIDATES = (
    'src',
    'data-src',
    'data-original',
    'data-url',
    'data-lazy-src',
    'data-actualsrc',
    'data-backsrc',
    'data-fail',
    'data-orig-src',
)

BROWSER_ARTICLE_SELECTORS = (
    '#js_content',
    '.rich_media_content',
    '#img-content',
    'article',
    'main',
    '[role="main"]',
)

def strip_html_tags(html):
    """Remove remaining HTML tags."""
    return re.sub(r'<[^>]+>', '', html)

def extract_title_from_html(html):
    """Extract a reasonable title from HTML."""
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if not match:
        match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""

    title = unescape(strip_html_tags(match.group(1)))
    return re.sub(r'\s+', ' ', title).strip()

def normalize_browser_title(title):
    """Drop common chrome/page wrappers from browser-rendered titles."""
    cleaned = re.sub(r'\s*[-|_]\s*微信公众平台\s*$', '', (title or '')).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def html_to_basic_markdown(html):
    """
    Convert HTML to simple Markdown-like text.
    This is a fallback used when Jina.ai is unavailable.
    """
    if not html:
        return ""

    content = html
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<noscript[^>]*>.*?</noscript>', '', content, flags=re.DOTALL | re.IGNORECASE)

    replacements = [
        (r'<br\s*/?>', '\n'),
        (r'</p\s*>', '\n\n'),
        (r'</div\s*>', '\n\n'),
        (r'</section\s*>', '\n\n'),
        (r'</article\s*>', '\n\n'),
        (r'</li\s*>', '\n'),
        (r'<li[^>]*>', '- '),
        (r'<h1[^>]*>', '# '),
        (r'</h1\s*>', '\n\n'),
        (r'<h2[^>]*>', '## '),
        (r'</h2\s*>', '\n\n'),
        (r'<h3[^>]*>', '### '),
        (r'</h3\s*>', '\n\n'),
        (r'<h4[^>]*>', '#### '),
        (r'</h4\s*>', '\n\n'),
    ]
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    content = strip_html_tags(content)
    content = unescape(content)
    content = content.replace('\r', '')
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+\n', '\n', content)
    content = re.sub(r'\n[ \t]+', '\n', content)
    content = re.sub(r'[ \t]{2,}', ' ', content)

    lines = [line.strip() for line in content.splitlines()]
    cleaned_lines = []
    for line in lines:
        if not line:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()

def looks_like_low_quality_markdown(markdown):
    """Detect obviously noisy fallback markdown."""
    if not markdown:
        return True

    lines = [line.strip() for line in markdown.splitlines()]
    non_empty = [line for line in lines if line]
    if len(non_empty) < 8:
        return True

    sample = non_empty[:120]
    dash_lines = sum(1 for line in sample if line in {'-', '—', '–'})
    if dash_lines >= 20:
        return True

    joined = '\n'.join(sample[:40]).lower()
    noise_tokens = (
        '微信公众平台',
        '在小说阅读器中沉浸阅读',
        '喜欢就关注我哦',
    )
    if sum(token in joined for token in noise_tokens) >= 2:
        return True

    return False

async def _fetch_rendered_article_async(url, timeout_ms=60000):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='networkidle', timeout=timeout_ms)
            title = normalize_browser_title(await page.title())

            best_html = ""
            best_selector = ""
            for selector in BROWSER_ARTICLE_SELECTORS:
                locator = page.locator(selector)
                if await locator.count():
                    html = await locator.first.inner_html(timeout=10000)
                    if len(html) > len(best_html):
                        best_html = html
                        best_selector = selector

            if not best_html:
                best_html = await page.locator('body').inner_html(timeout=10000)
                best_selector = 'body'

            return {
                'title': title,
                'html': best_html,
                'selector': best_selector,
            }
        finally:
            await browser.close()

def fetch_rendered_article(url, timeout_ms=60000):
    """Fetch rendered article HTML via local browser when static fallbacks are poor."""
    if importlib.util.find_spec("playwright") is None:
        print("Browser fallback skipped: playwright is not installed", file=sys.stderr)
        return None
    try:
        return asyncio.run(_fetch_rendered_article_async(url, timeout_ms=timeout_ms))
    except Exception as e:
        print(f"Browser fallback failed: {e}", file=sys.stderr)
        return None

def get_url_hash(url):
    """Generate a short hash for URL to use as filename."""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def is_valid_image_url(url):
    """Check if URL is a valid image link."""
    if not url:
        return False
    # Skip data URLs, javascript, etc.
    if url.startswith('data:') or url.startswith('javascript:') or url.startswith('mailto:'):
        return False
    # Check for image extension or Content-Type hint
    parsed = urlparse(url)
    path = parsed.path.lower()
    host = parsed.netloc.lower()
    query = parsed.query.lower()
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico')
    if any(path.endswith(ext) for ext in image_extensions):
        return True
    if any(token in host for token in KNOWN_IMAGE_HOST_TOKENS):
        return True
    return any(token in query for token in KNOWN_IMAGE_QUERY_KEYS)

def should_skip_image_url(url):
    """Filter obvious spacer or tracking images."""
    lowered = url.lower()
    parsed = urlparse(lowered)
    host = parsed.netloc
    skip_tokens = (
        'pic_blank.gif',
        'transparent.gif',
        'spacer.',
        'pixel.',
        '1x1',
        'blank.',
    )
    if any(token in host for token in KNOWN_NON_CONTENT_IMAGE_HOST_TOKENS):
        return True
    return any(token in lowered for token in skip_tokens)

def extract_img_candidates(tag_html):
    """Extract candidate image URLs from common lazy-load attributes."""
    candidates = []
    for attr in IMG_ATTRIBUTE_CANDIDATES:
        pattern = re.compile(rf'{attr}\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
        for match in pattern.finditer(tag_html):
            value = unescape(match.group(1).strip())
            if value and value not in candidates:
                candidates.append(value)
    return candidates

def download_image(url, save_dir, timeout=10):
    """
    Download an image from URL and save to save_dir.
    Returns the local filename if successful, None otherwise.
    """
    try:
        # Create headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            content_type = response.headers.get('Content-Type', '')
            
            # Determine extension
            ext = '.jpg'
            if 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            elif 'svg' in content_type:
                ext = '.svg'
            elif 'bmp' in content_type:
                ext = '.bmp'
            elif not any(content_type.startswith(t) for t in ['image/', 'application/octet-stream']):
                # Not a valid image
                return None
            
            # Generate filename
            url_hash = get_url_hash(url)
            filename = f"img-{url_hash}{ext}"
            filepath = os.path.join(save_dir, filename)
            
            # Save file
            with open(filepath, 'wb') as f:
                f.write(content)
            
            return filename
            
    except Exception as e:
        print(f"Failed to download {url}: {e}", file=sys.stderr)
        return None

def extract_images_from_html(html_content, base_url):
    """
    Extract image URLs from HTML content.
    Returns a list of unique image URLs found in the content.
    """
    image_urls = set()
    
    # Pattern to find img tags and common lazy-load attributes.
    img_pattern = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
    
    for match in img_pattern.finditer(html_content):
        tag_html = match.group(0)
        for src in extract_img_candidates(tag_html):
            full_url = urljoin(base_url, src)
            if full_url and not should_skip_image_url(full_url):
                image_urls.add(full_url)
    
    # Also find images in style="background-image: url(...)"
    bg_pattern = re.compile(r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)', re.IGNORECASE)
    for match in bg_pattern.finditer(html_content):
        src = match.group(1)
        full_url = urljoin(base_url, unescape(src))
        if is_valid_image_url(full_url):
            image_urls.add(full_url)
    
    return list(image_urls)

def extract_images_from_markdown(markdown_content, base_url):
    """
    Extract image URLs from markdown, including images nested inside links.
    """
    image_urls = []
    if not markdown_content:
        return image_urls

    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    for match in img_pattern.finditer(markdown_content):
        img_url = match.group(2).strip()
        if img_url.startswith('data:'):
            continue
        full_url = urljoin(base_url, img_url)
        if full_url not in image_urls:
            image_urls.append(full_url)
    return image_urls

def process_article(url, output_dir, images_subdir='images'):
    """
    Main function to fetch article, extract images, and prepare for markdown conversion.
    
    Returns a dict with:
    - html: Full HTML content
    - images: List of (original_url, local_filename) pairs
    - markdown: HTML converted to markdown (images as local refs)
    """
    print(f"Fetching article from: {url}", file=sys.stderr)
    preferred_title = ""
    
    # First, try to fetch raw HTML for image extraction
    html_content = None
    try:
        # Fetch raw HTML using a simple request
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            print(f"Fetched raw HTML, length: {len(html_content)}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to fetch raw HTML: {e}", file=sys.stderr)
    
    # Also get markdown content via Jina.ai
    markdown_content = ""
    generated_from_raw_html = False
    try:
        jina_url = f"https://r.jina.ai/{url}"
        req = urllib.request.Request(jina_url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            markdown_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch via Jina: {e}", file=sys.stderr)

    if not markdown_content and html_content:
        title = extract_title_from_html(html_content)
        body_markdown = html_to_basic_markdown(html_content)
        markdown_parts = []
        if title:
            markdown_parts.append(f"# {title}")
        if body_markdown:
            markdown_parts.append(body_markdown)
        markdown_content = "\n\n".join(part for part in markdown_parts if part).strip()
        generated_from_raw_html = True
        print("Generated fallback markdown from raw HTML", file=sys.stderr)

    should_try_browser = generated_from_raw_html or looks_like_low_quality_markdown(markdown_content)
    rendered_html = None
    if should_try_browser:
        rendered = fetch_rendered_article(url)
        if rendered and rendered.get('html'):
            rendered_html = rendered['html']
            preferred_title = rendered.get('title', '') or preferred_title
            rendered_markdown = html_to_basic_markdown(rendered_html)
            if rendered_markdown and (
                not markdown_content or
                looks_like_low_quality_markdown(markdown_content)
            ):
                markdown_content = rendered_markdown
                print(f"Used browser fallback content from selector: {rendered.get('selector')}", file=sys.stderr)

    # Extract images from HTML
    image_urls = []
    if html_content:
        html_image_urls = extract_images_from_html(html_content, url)
        image_urls.extend(html_image_urls)
        print(f"Found {len(html_image_urls)} images from HTML", file=sys.stderr)
    if rendered_html:
        rendered_image_urls = extract_images_from_html(rendered_html, url)
        for img_url in rendered_image_urls:
            if img_url not in image_urls:
                image_urls.append(img_url)
        print(f"Found {len(rendered_image_urls)} images from browser HTML", file=sys.stderr)

    markdown_image_urls = extract_images_from_markdown(markdown_content, url)
    for img_url in markdown_image_urls:
        if img_url not in image_urls:
            image_urls.append(img_url)
    if markdown_content:
        print(f"Found {len(markdown_image_urls)} images from Markdown", file=sys.stderr)
    
    # Create images directory
    images_dir = os.path.join(output_dir, images_subdir)
    os.makedirs(images_dir, exist_ok=True)
    
    # Download images
    downloaded_images = []
    for img_url in image_urls:
        if is_valid_image_url(img_url) and not should_skip_image_url(img_url):
            local_name = download_image(img_url, images_dir)
            if local_name:
                downloaded_images.append((img_url, local_name))
                print(f"Downloaded: {local_name}", file=sys.stderr)
    
    # Replace image URLs in markdown with local paths
    final_markdown = replace_image_urls_in_markdown(markdown_content, downloaded_images, url, images_subdir)
    final_markdown = ensure_downloaded_images_present(final_markdown, downloaded_images, images_subdir)
    
    return {
        'html': html_content or '',
        'title': preferred_title,
        'images': downloaded_images,
        'markdown': final_markdown or markdown_content
    }

def convert_html_to_markdown_with_local_images(html, downloaded_images, images_subdir):
    """
    Convert HTML to Markdown, replacing image URLs with local paths.
    """
    markdown = html_to_basic_markdown(html)

    # Create a mapping of original URL to local filename
    url_to_local = {orig: local for orig, local in downloaded_images}
    
    # Replace img src with local paths
    def replace_img_src(match):
        src = match.group(1)
        # Resolve relative URLs
        full_url = urljoin('', unescape(src))  # base is empty, so this just unescapes
        
        if full_url in url_to_local:
            local_file = url_to_local[full_url]
            return f'src="{images_subdir}/{local_file}"'
        return match.group(0)
    
    markdown = re.sub(r'<img[^>]+src=["\']([^"\']+)["\']', replace_img_src, markdown)
    
    # Clean up HTML tags but keep images
    # This is a simple conversion - for better results, consider using a proper HTML-to-Markdown library
    markdown = clean_html_to_markdown(markdown)
    
    return markdown

def replace_image_urls_in_markdown(markdown, downloaded_images, base_url, images_subdir):
    """
    Replace image URLs in markdown with local paths.
    """
    if not downloaded_images:
        return markdown
    
    # Create mapping of original URL to local filename
    url_to_local = {}
    for orig_url, local_name in downloaded_images:
        # Normalize the original URL for matching
        normalized_orig = orig_url
        url_to_local[normalized_orig] = local_name
        
    def resolve_local_ref(img_url):
        full_url = urljoin(base_url, img_url)
        if full_url in url_to_local:
            return f'{images_subdir}/{url_to_local[full_url]}'
        if img_url in url_to_local:
            return f'{images_subdir}/{url_to_local[img_url]}'
        return None

    # Replace markdown image syntax: ![alt](url)
    def replace_markdown_img(match):
        alt_text = match.group(1) or ''
        img_url = match.group(2)
        local_ref = resolve_local_ref(img_url)
        if local_ref:
            return f'![{alt_text}]({local_ref})'
        return match.group(0)

    # Replace linked-image syntax: [![alt](url)](target)
    def replace_linked_markdown_img(match):
        alt_text = match.group(1) or ''
        img_url = match.group(2)
        local_ref = resolve_local_ref(img_url)
        if local_ref:
            return f'![{alt_text}]({local_ref})'
        return match.group(0)

    result = re.sub(r'\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)', replace_linked_markdown_img, markdown)
    result = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_markdown_img, result)
    return result

def ensure_downloaded_images_present(markdown, downloaded_images, images_subdir):
    """
    If the source markdown does not expose any image syntax at all, prepend
    downloaded images as a last-resort fallback.
    """
    if not downloaded_images:
        return markdown

    local_refs = [f'{images_subdir}/{local_name}' for _orig_url, local_name in downloaded_images]
    markdown = markdown or ''
    if re.search(r'(\[)?!\[[^\]]*\]\(([^)]+)\)', markdown):
        return markdown

    existing_refs = set(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', markdown))
    missing_refs = [ref for ref in local_refs if ref not in existing_refs]

    if not missing_refs:
        return markdown

    image_block = '\n'.join(f'![]({ref})' for ref in missing_refs)
    if not markdown:
        return image_block
    return f'{image_block}\n\n{markdown.lstrip()}'

def clean_html_to_markdown(html):
    """Simple HTML to Markdown conversion."""
    return html_to_basic_markdown(html)

if __name__ == '__main__':
    # This script is now an internal helper. The public entrypoint is save_article.py.
    if len(sys.argv) >= 2 and sys.argv[1] == '--internal-ok':
        if len(sys.argv) < 4:
            print("Usage: python download_images.py --internal-ok <url> <output_dir>", file=sys.stderr)
            sys.exit(1)
        url = sys.argv[2]
        output_dir = sys.argv[3]
        result = process_article(url, output_dir)
        print(json.dumps(result))
    else:
        print(
            "download_images.py is an internal helper. "
            "Use: python save_article.py <url> <output_dir> [page_comment]",
            file=sys.stderr,
        )
        sys.exit(2)
