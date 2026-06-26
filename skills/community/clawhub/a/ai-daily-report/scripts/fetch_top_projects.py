#!/usr/bin/env python3
"""Fetch top AI open‑source projects from GitHub.
Outputs JSON list to stdout: [{"name":..., "html_url":..., "stars":..., "description":...}]
Requires environment variable GITHUB_TOKEN for authenticated search (higher rate limit).
"""
import os, sys, json, datetime, urllib.parse, http.client

TOKEN = os.getenv('GITHUB_TOKEN')
# If token is missing, we will perform an unauthenticated request (lower rate limit).
# This allows the skill to still work for demo purposes.


# date cutoff (24h ago) in ISO format
since = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

# search query: AI related topics + stars>10000 + pushed after since
query = f'topic:ai stars:>10000 pushed:>{since}'
params = urllib.parse.urlencode({
    'q': query,
    'sort': 'stars',
    'order': 'desc',
    'per_page': '5',
})

conn = http.client.HTTPSConnection('api.github.com')
headers = {
    'User-Agent': 'openclaw-ai-report',
    'Accept': 'application/vnd.github.v3+json',
}
if TOKEN:
    headers['Authorization'] = f'token {TOKEN}'
conn.request('GET', f'/search/repositories?{params}', headers=headers)
resp = conn.getresponse()
if resp.status != 200:
    sys.stderr.write(f'GitHub API error {resp.status}: {resp.read().decode()}\n')
    sys.exit(1)
data = json.loads(resp.read().decode())
items = data.get('items', [])[:3]
result = []
for repo in items:
    result.append({
        'name': repo['full_name'],
        'html_url': repo['html_url'],
        'stars': repo['stargazers_count'],
        'description': repo.get('description') or ''
    })
print(json.dumps(result, ensure_ascii=False, indent=2))
