#!/usr/bin/env python3
"""Fetch ride receipt emails from Gmail into a single ride-insights emails.json file."""

import argparse
import base64
import json
import subprocess
import sys
import time
from email import policy
from email.parser import BytesParser
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUERIES = json.loads((ROOT / 'references' / 'provider_queries.json').read_text(encoding='utf-8'))


def run_json(cmd, retries: int = 3, delay_s: float = 1.5):
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
            return json.loads(out)
        except subprocess.CalledProcessError as e:
            last_err = e
            if attempt >= retries:
                break
            time.sleep(delay_s * attempt)
    raise last_err


def add_date_bounds(query: str, after: str | None, before: str | None) -> str:
    q = f'({query})'
    if after:
        y, m, d = after.split('-')
        q += f' after:{y}/{m}/{d}'
    if before:
        y, m, d = before.split('-')
        q += f' before:{y}/{m}/{d}'
    return q


def gmail_search(account: str, query: str, maxn: int):
    return run_json(['gog', 'gmail', 'messages', 'search', query, '--max', str(maxn), '--account', account, '--json', '--results-only'])


def gmail_get_full(account: str, message_id: str):
    return run_json(['gog', 'gmail', 'get', message_id, '--format=full', '--account', account, '--json', '--results-only', '--select', 'message.snippet,message.internalDate'])


def gmail_get_raw(account: str, message_id: str):
    return run_json(['gog', 'gmail', 'get', message_id, '--format=raw', '--account', account, '--json', '--results-only'])


def decode_rfc822(raw_b64url: str):
    raw_bytes = base64.urlsafe_b64decode(raw_b64url + '===')
    return BytesParser(policy=policy.default).parsebytes(raw_bytes)


def decode_part(part) -> str:
    b = part.get_payload(decode=True)
    if not b:
        return ''
    cs = part.get_content_charset() or 'utf-8'
    try:
        return b.decode(cs, errors='replace')
    except Exception:
        return b.decode('utf-8', errors='replace')


def collect_html(msg):
    parts = list(msg.walk()) if msg.is_multipart() else [msg]
    htmls = []
    for p in parts:
        if p.get_content_type() == 'text/html':
            s = decode_part(p).strip()
            if s:
                htmls.append(s)
    return '\n\n'.join(htmls).strip()


def main():
    ap = argparse.ArgumentParser(description='Fetch Gmail ride receipts for ride-insights')
    ap.add_argument('--account', required=True, help='Authenticated gog account email to use')
    ap.add_argument('--after', help='Lower date bound in YYYY-MM-DD form')
    ap.add_argument('--before', help='Upper date bound in YYYY-MM-DD form')
    ap.add_argument('--max-per-provider', type=int, default=5000, help='Maximum Gmail matches to fetch per provider query')
    ap.add_argument('--providers', default=','.join(DEFAULT_QUERIES.keys()), help='Comma-separated provider names to include')
    ap.add_argument('--out', required=True, help='Output path for the combined emails.json file')
    args = ap.parse_args()

    providers = [p.strip() for p in args.providers.split(',') if p.strip()]
    items = []
    seen = set()

    for prov in providers:
        q0 = DEFAULT_QUERIES.get(prov)
        if not q0:
            raise SystemExit(f'Unknown provider: {prov}')
        q = add_date_bounds(q0, args.after, args.before)
        msgs = gmail_search(args.account, q, args.max_per_provider)
        for m in msgs:
            mid = m.get('id')
            if not mid or mid in seen:
                continue
            seen.add(mid)
            try:
                full = gmail_get_full(args.account, mid)
                snippet = unescape(full.get('message.snippet', '') or '')
                raw = gmail_get_raw(args.account, mid)
                msg = decode_rfc822(raw['message']['raw'])
                items.append({
                    'provider': prov,
                    'gmail_message_id': mid,
                    'email_date': m.get('date'),
                    'subject': m.get('subject'),
                    'from': m.get('from'),
                    'snippet': snippet,
                    'text_html': collect_html(msg),
                })
            except subprocess.CalledProcessError as e:
                err = (e.output or str(e)).strip().replace('\n', ' ')[:500]
                print(f'WARN: skipping message {mid} for provider {prov}: {err}', file=sys.stderr)
                continue

    items.sort(key=lambda x: ((x.get('email_date') or ''), (x.get('gmail_message_id') or '')))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(items)} emails to {out_path}')


if __name__ == '__main__':
    main()
