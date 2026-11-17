#!/usr/bin/env python3
"""
pre-fetch.py — Fetch newsletters from Gmail API and produce compact JSON
that Haiku can read without context overflow.

Writes newsletter-inbox.json with just the fields needed for summarisation:
  threadId, messageId, source, subject, snippet, date

Usage: python3 pre-fetch.py
"""
import json, sys, os, re
from datetime import datetime, timezone

from briefed_common import append_private, get_gmail_service, write_private_json

INBOX_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'newsletter-inbox.json')
FILTER_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'filter-rules.json')
SKIP_LOG_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'newsletter-filter-skips.jsonl')
USER_FILTER_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'newsletter-filter-rules.json')

# Default rules, used when config/filter-rules.json is missing. Keep in sync with it.
# Substrings that mark an email as transactional (case-insensitive).
SKIP_SUBJECT_PATTERNS = [
    "your invoice",
    "your receipt",
    "your order",
    "order confirmation",
    "has shipped",
    "has been dispatched",
    "out for delivery",
    "has been delivered",
    "payment confirmation",
    "payment received",
    "payment failed",
    "has been charged",
    "refund",
    "your statement",
    "statement is ready",
    "verify your email",
    "confirm your email",
    "password reset",
    "reset your password",
    "verification code",
    "security alert",
    "new sign-in",
    "account alert",
    "subscription confirmed",
    "unsubscribe confirmation",
    "renewal reminder",
    "domain renewal",
    "document renewal",
    "[action needed]",
    "action required",
    "booking is confirmed",
    "booking confirmation",
    "reservation confirmed",
    "your appointment",
    "appointment confirmation",
    "appointment reminder",
    "your dependabot alerts",
    "survey",
    "questionnaire",
    "how did we do",
    "rate your experience",
]

SKIP_SENDERS = [
    "paypal",
    "stripe",
    "amazon",
    "ebay",
    "github",
]

SKIP_SNIPPET_PATTERNS = [
    "booking is confirmed",
    "you can find full details of your booking",
    "verification code is",
    "security alert digest",
    "if you didn't request this",
]


def read_rules_file(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f'Warning: failed to load {path} ({e}), ignoring.', file=sys.stderr)
        return {}


def load_filter_rules():
    """Bundled rules, extended by the user's own rules file if present.

    User rules live outside the skill directory so reinstalling or updating
    Briefed doesn't overwrite them.
    """
    bundled = read_rules_file(FILTER_CONFIG_FILE) if os.path.exists(FILTER_CONFIG_FILE) else {}
    user = read_rules_file(USER_FILTER_FILE) if os.path.exists(USER_FILTER_FILE) else {}

    rules = {}
    for key, default in [
        ('skipSubjectPatterns', SKIP_SUBJECT_PATTERNS),
        ('skipSenders', SKIP_SENDERS),
        ('skipSnippetPatterns', SKIP_SNIPPET_PATTERNS),
    ]:
        patterns = bundled.get(key, default) + user.get(key, [])
        rules[key] = list(dict.fromkeys(p.lower() for p in patterns))
    return rules


def is_transactional(subject, sender, rules):
    subj = (subject or '').lower()
    send = (sender or '').lower()
    return any(p in subj for p in rules['skipSubjectPatterns']) or any(p in send for p in rules['skipSenders'])


def is_transactional_snippet(snippet, rules):
    body = (snippet or '').lower()
    return any(p in body for p in rules['skipSnippetPatterns'])


def skip_reason(subject, sender, snippet, rules):
    subj = (subject or '').lower()
    send = (sender or '').lower()
    body = (snippet or '').lower()
    for p in rules['skipSubjectPatterns']:
        if p in subj:
            return f'subject:{p}'
    for p in rules['skipSenders']:
        if p in send:
            return f'sender:{p}'
    for p in rules['skipSnippetPatterns']:
        if p in body:
            return f'snippet:{p}'
    return 'unknown'


def append_skip_log(thread_id, source, subject, snippet, reason):
    entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'threadId': thread_id,
        'source': source,
        'subject': subject,
        'snippet': (snippet or '')[:160],
        'reason': reason,
    }
    append_private(SKIP_LOG_FILE, json.dumps(entry) + '\n')


def get_sender_name(from_header):
    m = re.match(r'^"?([^"<]+)"?\s*(?:<[^>]+>)?$', (from_header or '').strip())
    if m:
        name = m.group(1).strip().strip('"')
        return name if name else (from_header or '')
    return from_header or ''


def headers_map(payload):
    out = {}
    for h in payload.get('headers', []):
        name = h.get('name', '').lower()
        if name:
            out[name] = h.get('value', '')
    return out


def fallback_date(msg):
    internal = msg.get('internalDate')
    if internal:
        try:
            ts = int(internal) / 1000
            return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
        except Exception:
            pass
    return ''


def main():
    rules = load_filter_rules()
    print(
        f"Loaded filter rules: subjects={len(rules['skipSubjectPatterns'])}, senders={len(rules['skipSenders'])}, snippets={len(rules['skipSnippetPatterns'])}",
        flush=True,
    )
    print('Connecting to Gmail API...', flush=True)
    try:
        service = get_gmail_service()
    except Exception as e:
        print(f'Auth error: {e}', file=sys.stderr)
        sys.exit(1)

    query = 'category:updates OR category:promotions newer_than:1d'
    print('Fetching newsletter list...', flush=True)
    try:
        resp = service.users().messages().list(userId='me', q=query, maxResults=30).execute()
        messages = resp.get('messages', [])
    except Exception as e:
        print(f'Error fetching list: {e}', file=sys.stderr)
        sys.exit(1)

    print(f'Found {len(messages)} emails. Filtering...', flush=True)

    newsletters = []
    seen_threads = set()

    for m in messages:
        msg_id = m.get('id')
        thread_id = m.get('threadId')
        if not msg_id or not thread_id or thread_id in seen_threads:
            continue
        seen_threads.add(thread_id)

        try:
            full = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        except Exception as e:
            print(f'  Skip {thread_id}: {e}', file=sys.stderr)
            continue

        payload = full.get('payload', {})
        h = headers_map(payload)
        subject = h.get('subject', '(no subject)')
        source = get_sender_name(h.get('from', ''))
        date = h.get('date', '') or fallback_date(full)
        snippet = (full.get('snippet') or '')[:400]

        if is_transactional(subject, source, rules) or is_transactional_snippet(snippet, rules):
            reason = skip_reason(subject, source, snippet, rules)
            append_skip_log(thread_id, source, subject, snippet, reason)
            print(f'  SKIP (transactional): {source} — {subject[:50]} [{reason}]')
            continue

        newsletters.append({
            'threadId': thread_id,
            'messageId': msg_id,
            'source': source,
            'subject': subject,
            'snippet': snippet,
            'date': date,
        })
        print(f'  KEEP: {source} — {subject[:60]}')

    write_private_json(INBOX_FILE, {'count': len(newsletters), 'newsletters': newsletters})

    print(f'\nDone. {len(newsletters)} newsletters written to newsletter-inbox.json')


if __name__ == '__main__':
    main()
