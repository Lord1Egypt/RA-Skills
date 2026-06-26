#!/usr/bin/env python3
"""
Query Gangtise knowledge base API.
Usage: python3 query_kb.py "your query" [--type 10,40] [--top 5]
"""
import json
import sys
import argparse
from datetime import datetime
import time
from pathlib import Path

# Add scripts directory to path for importing configure module
sys.path.insert(0, str(Path(__file__).parent))

from configure import get_credentials, check_configured

BASE_URL = "https://open.gangtise.com"
KNOWLEDGE_ENDPOINT = "/application/open-data/ai/search/knowledge/batch"


def check_configuration():
    """Check if the skill is configured, print helpful message if not."""
    if not check_configured():
        print("=" * 60, file=sys.stderr)
        print("ERROR: Gangtise Knowledge Base is not configured.", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(file=sys.stderr)
        print("Please run the configuration script first:", file=sys.stderr)
        print(file=sys.stderr)
        print("  python3 scripts/configure.py", file=sys.stderr)
        print(file=sys.stderr)
        print("You can obtain your Access Key and Secret Key from:", file=sys.stderr)
        print("  https://open.gangtise.com", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        return False
    return True


def get_access_token():
    """Authenticate and get access token."""
    import urllib.request
    import urllib.error
    import ssl

    ACCESS_KEY, SECRET_KEY = get_credentials()

    url = f"{BASE_URL}/application/auth/oauth/open/loginV2"

    data = {"accessKey": ACCESS_KEY, "secretAccessKey": SECRET_KEY}

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        method='POST'
    )

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == '000000' and result.get('data'):
                return result['data'].get('accessToken')
    except Exception as e:
        print(f"Auth error: {e}", file=sys.stderr)
    return None


def query_knowledge(queries, resource_types=None, top=5, days_back=365, token=None, knowledge_name='system_knowledge_doc'):
    """Query knowledge base."""
    import urllib.request
    import urllib.error
    import ssl

    if token is None:
        token = get_access_token()
    if not token:
        return None

    url = f"{BASE_URL}{KNOWLEDGE_ENDPOINT}"

    end_time = int(time.time() * 1000)
    start_time = end_time - (days_back * 24 * 60 * 60 * 1000)

    if resource_types is None:
        resource_types = [10, 40]

    data = {
        "queries": queries if isinstance(queries, list) else [queries],
        "resourceTypes": resource_types,
        "knowledgeNames": [knowledge_name],
        "startTime": start_time,
        "endTime": end_time,
        "top": min(top, 20)
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': token if token.startswith('Bearer ') else f'Bearer {token}'
        },
        method='POST'
    )

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Query error: {e}", file=sys.stderr)
        return None


def format_results(result):
    """Format query results for display."""
    if not result or result.get('code') != '000000':
        print(f"Query failed: {result.get('msg', 'Unknown error')}")
        return

    data = result.get('data', [])
    if not data:
        print("No results found.")
        return

    for query_result in data:
        query = query_result.get('query', '')
        items = query_result.get('data', [])

        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")

        if not items:
            print("  No results for this query.")
            continue

        for i, item in enumerate(items, 1):
            print(f"\n--- Result {i} ---")
            print(f"Title: {item.get('title', 'N/A')}")
            print(f"Company: {item.get('company', 'N/A')}")
            rt = item.get('resourceType')
            rt_name = {10:'券商研报',20:'内部研报',40:'分析师观点',50:'公告',60:'会议纪要'}.get(rt, 'Other')
            print(f"Type: {rt_name} ({rt})")

            ts = item.get('time')
            if ts:
                dt = datetime.fromtimestamp(ts / 1000)
                print(f"Time: {dt.strftime('%Y-%m-%d')}")

            content = item.get('content', '')
            if content:
                if len(content) > 800:
                    content = content[:800] + "..."
                print(f"Content: {content}")


def main():
    parser = argparse.ArgumentParser(description='Query Gangtise knowledge base')
    parser.add_argument('query', help='Query string')
    parser.add_argument('--type', default='10,40', help='Resource types (comma-separated, default: 10,40)')
    parser.add_argument('--top', type=int, default=5, help='Number of results per query (default: 5, max: 20)')
    parser.add_argument('--days', type=int, default=365, help='Search days back (default: 365)')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    parser.add_argument('--token', help='Access token (optional)')

    args = parser.parse_args()

    # Check configuration before proceeding
    if not check_configuration():
        sys.exit(1)

    resource_types = [int(t.strip()) for t in args.type.split(',')]
    result = query_knowledge(args.query, resource_types, args.top, args.days, args.token)

    if result:
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            format_results(result)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
