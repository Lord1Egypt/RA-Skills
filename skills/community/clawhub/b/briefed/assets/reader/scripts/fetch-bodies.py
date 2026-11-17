#!/usr/bin/env python3
"""
fetch-bodies.py — post-processing step for the newsletter digest.
Reads newsletter-today.json, fetches full HTML bodies for any stories
missing them, and writes the file back.

Usage: python3 fetch-bodies.py
"""
import json, base64, re, sys, os

from briefed_common import get_gmail_service, write_private_json

STORIES_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'newsletter-today.json')


def b64url_decode(data):
    if not data:
        return ''
    pad = '=' * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + pad).decode('utf-8', errors='replace')


def find_html(payload):
    mime = payload.get('mimeType', '')
    if mime == 'text/html':
        data = payload.get('body', {}).get('data', '')
        if data:
            return b64url_decode(data)
    for part in payload.get('parts', []):
        result = find_html(part)
        if result:
            return result
    return None


def clean_html(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<img[^>]*(width=["\']?1["\']?|height=["\']?1["\']?)[^>]*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'(width\s*=\s*["\']?)(\d{4,})', lambda m: m.group(1) + '100%', html)
    return html


def fetch_body(service, message_id):
    try:
        raw = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        html = find_html(raw.get('payload', {}))
        return clean_html(html) if html else None
    except Exception as e:
        print(f'  Error fetching {message_id}: {e}', file=sys.stderr)
        return None


def main():
    if not os.path.exists(STORIES_FILE):
        print('No stories file found — run the digest first.', file=sys.stderr)
        sys.exit(1)

    try:
        service = get_gmail_service()
    except Exception as e:
        print(f'Auth error: {e}', file=sys.stderr)
        sys.exit(1)

    with open(STORIES_FILE) as f:
        data = json.load(f)

    stories = data.get('stories', [])
    cache = {}
    updated = 0

    for story in stories:
        msg_id = story.get('messageId') or story.get('threadId')
        if not msg_id:
            continue
        body = story.get('body', '')
        if body and len(body) > 500:
            continue

        print(f'  Fetching body: {story.get("source", msg_id)}...', end=' ', flush=True)

        if msg_id in cache:
            story['body'] = cache[msg_id]
            print('(cached)')
            continue

        html = fetch_body(service, msg_id)
        if html:
            story['body'] = html
            cache[msg_id] = html
            print(f'✅ {len(html):,} chars')
            updated += 1
        else:
            print('⚠️  no HTML found')

    write_private_json(STORIES_FILE, data)

    print(f'\nDone. Updated {updated} stories.')


if __name__ == '__main__':
    main()
