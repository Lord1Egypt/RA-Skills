#!/bin/bash
set -euo pipefail

# ============================================================================
# confluence-cli.sh — Confluence Cloud REST API wrapper
#
# Dependencies: curl, python3
# Env vars: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN
# Outputs: JSON to stdout, errors to stderr
# ============================================================================

for var in ATLASSIAN_URL ATLASSIAN_EMAIL ATLASSIAN_API_TOKEN; do
    if [ -z "${!var:-}" ]; then
        echo "{\"error\": \"Missing env var: $var\"}" >&2
        exit 1
    fi
done

AUTH="$ATLASSIAN_EMAIL:$ATLASSIAN_API_TOKEN"
BASE="$ATLASSIAN_URL/wiki"

# --- HTTP helpers ---
cf_get() {
    local response http_code body
    response=$(curl -s --connect-timeout 10 --max-time 30 -w "\n%{http_code}" -u "$AUTH" -H "Accept: application/json" "$1")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        local err="{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"body\": $(echo "$body" | head -c 500)}"
        echo "$err" >&2
        echo "$err"
        exit 1
    fi
    echo "$body"
}

cf_post() {
    local response http_code body
    response=$(curl -s --connect-timeout 10 --max-time 30 -w "\n%{http_code}" -u "$AUTH" \
        -X POST -H "Content-Type: application/json" -H "Accept: application/json" \
        "$1" -d "$2")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        local err="{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"body\": $(echo "$body" | head -c 500)}"
        echo "$err" >&2
        echo "$err"
        exit 1
    fi
    echo "$body"
}

cf_put() {
    local response http_code body
    response=$(curl -s --connect-timeout 10 --max-time 30 -w "\n%{http_code}" -u "$AUTH" \
        -X PUT -H "Content-Type: application/json" -H "Accept: application/json" \
        "$1" -d "$2")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        local err="{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"body\": $(echo "$body" | head -c 500)}"
        echo "$err" >&2
        echo "$err"
        exit 1
    fi
    echo "$body"
}

urlencode() {
    python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$1"
}

# --- Commands ---

cmd_spaces() {
    cf_get "$BASE/api/v2/spaces?limit=25" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'id':s.get('id'),
    'key':s.get('key'),
    'name':s.get('name'),
    'type':s.get('type'),
    'status':s.get('status')
} for s in d.get('results',[])],indent=2))
"
}

cmd_pages() {
    local space_id="${1:?Usage: confluence-cli.sh pages SPACE_ID [limit]}"
    local limit="${2:-25}"
    cf_get "$BASE/api/v2/spaces/$space_id/pages?limit=$limit" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'id':p.get('id'),
    'title':p.get('title'),
    'status':p.get('status'),
    'parentId':p.get('parentId'),
    'authorId':p.get('authorId'),
    'created':p.get('createdAt'),
    'url':p.get('_links',{}).get('webui')
} for p in d.get('results',[])],indent=2))
"
}

cmd_get_page() {
    local page_id="${1:?Usage: confluence-cli.sh get PAGE_ID}"
    cf_get "$BASE/api/v2/pages/$page_id?body-format=storage" | python3 -c "
import sys,json,re
d=json.load(sys.stdin)
body_html=d.get('body',{}).get('storage',{}).get('value','')
body_text=re.sub(r'<[^>]+>','',body_html).strip()
truncated=len(body_html)>5000 or len(body_text)>3000
print(json.dumps({
    'id':d.get('id'),
    'title':d.get('title'),
    'status':d.get('status'),
    'spaceId':d.get('spaceId'),
    'parentId':d.get('parentId'),
    'version':(d.get('version')or{}).get('number'),
    'body_text':body_text[:3000],
    'body_html':body_html[:5000],
    'truncated':truncated,
    'created':d.get('createdAt'),
    'url':d.get('_links',{}).get('webui')
},indent=2))
"
}

cmd_children() {
    local page_id="${1:?Usage: confluence-cli.sh children PAGE_ID}"
    cf_get "$BASE/api/v2/pages/$page_id/children?limit=25" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'id':p.get('id'),
    'title':p.get('title'),
    'status':p.get('status'),
    'url':p.get('_links',{}).get('webui')
} for p in d.get('results',[])],indent=2))
"
}

cmd_search() {
    local cql="${1:?Usage: confluence-cli.sh search \"CQL query\" [limit]}"
    local limit="${2:-10}"
    cf_get "$BASE/rest/api/content/search?cql=$(urlencode "$cql")&limit=$limit" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({
    'total':d.get('totalSize',d.get('size',0)),
    'results':[{
        'id':r.get('id'),
        'title':r.get('title'),
        'type':r.get('type'),
        'space':(r.get('space')or{}).get('key'),
        'url':r.get('_links',{}).get('webui')
    } for r in d.get('results',[])]
},indent=2))
"
}

cmd_create_page() {
    local space_id="" title="" parent_id="" body=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --space) space_id="$2"; shift 2;;
            --title) title="$2"; shift 2;;
            --parent) parent_id="$2"; shift 2;;
            --body) body="$2"; shift 2;;
            *) echo "{\"error\":\"Unknown flag: $1\"}" >&2; echo "{\"error\":\"Unknown flag: $1\"}"; exit 1;;
        esac
    done
    [ -z "$space_id" ] || [ -z "$title" ] && { echo '{"error":"Required: --space SPACE_ID --title TEXT"}' >&2; echo '{"error":"Required: --space SPACE_ID --title TEXT"}'; exit 1; }

    local payload
    payload=$(SPACE_ID="$space_id" TITLE="$title" PARENT_ID="$parent_id" BODY="$body" python3 -c "
import json, os
p = {
    'spaceId': os.environ['SPACE_ID'],
    'status': 'current',
    'title': os.environ['TITLE'],
    'body': {'representation': 'storage', 'value': os.environ.get('BODY') or '<p></p>'}
}
parent = os.environ.get('PARENT_ID', '')
if parent:
    p['parentId'] = parent
print(json.dumps(p))
")
    cf_post "$BASE/api/v2/pages" "$payload" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps({
    'id': d.get('id'),
    'title': d.get('title'),
    'url': d.get('_links', {}).get('webui')
}, indent=2))
"
}

cmd_update_page() {
    local page_id="${1:?Usage: confluence-cli.sh update PAGE_ID --title TEXT --body HTML}"
    shift
    local title="" body=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --title) title="$2"; shift 2;;
            --body) body="$2"; shift 2;;
            *) echo "{\"error\":\"Unknown flag: $1\"}" >&2; echo "{\"error\":\"Unknown flag: $1\"}"; exit 1;;
        esac
    done

    # Get current page info (version + title)
    local current
    current=$(cf_get "$BASE/api/v2/pages/$page_id")

    local payload
    payload=$(PAGE_ID="$page_id" TITLE="$title" BODY="$body" CURRENT="$current" python3 -c "
import json, os
current = json.loads(os.environ['CURRENT'])
current_version = current.get('version', {}).get('number', 1)
current_title = current.get('title', 'Untitled')
p = {
    'id': os.environ['PAGE_ID'],
    'status': 'current',
    'version': {'number': current_version + 1, 'message': 'Updated by agent'},
    'title': os.environ.get('TITLE') or current_title,
}
body = os.environ.get('BODY', '')
if body:
    p['body'] = {'representation': 'storage', 'value': body}
print(json.dumps(p))
")
    cf_put "$BASE/api/v2/pages/$page_id" "$payload" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps({
    'id': d.get('id'),
    'title': d.get('title'),
    'version': (d.get('version') or {}).get('number'),
    'url': d.get('_links', {}).get('webui')
}, indent=2))
"
}

cmd_labels() {
    local page_id="${1:?Usage: confluence-cli.sh labels PAGE_ID}"
    cf_get "$BASE/rest/api/content/$page_id/label" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'name':l.get('name'),
    'prefix':l.get('prefix')
} for l in d.get('results',[])],indent=2))
"
}

cmd_add_labels() {
    local page_id="${1:?Usage: confluence-cli.sh add-labels PAGE_ID \"label1,label2\"}"
    local labels_str="${2:?Usage: confluence-cli.sh add-labels PAGE_ID \"label1,label2\"}"
    local payload
    payload=$(python3 -c "
import json
labels='$labels_str'.split(',')
print(json.dumps([{'prefix':'global','name':l.strip()} for l in labels]))
")
    cf_post "$BASE/rest/api/content/$page_id/label" "$payload" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({'labels':[l.get('name') for l in d.get('results',d if isinstance(d,list) else [])]},indent=2))
"
}

cmd_comments() {
    local page_id="${1:?Usage: confluence-cli.sh comments PAGE_ID}"
    cf_get "$BASE/api/v2/pages/$page_id/footer-comments?limit=25&body-format=storage" | python3 -c "
import sys, json, re
d = json.load(sys.stdin)
comments = []
for c in d.get('results', []):
    body_html = c.get('body', {}).get('storage', {}).get('value', '')
    body_text = re.sub(r'<[^>]+>', '', body_html).strip()
    comments.append({
        'id': c.get('id'),
        'body': body_text[:500],
        'created': c.get('createdAt'),
        'version': (c.get('version') or {}).get('number')
    })
print(json.dumps({'count': len(comments), 'comments': comments}, indent=2))
"
}

cmd_add_comment() {
    local page_id="${1:?Usage: confluence-cli.sh add-comment PAGE_ID \"comment text\"}"
    local comment_text="${2:?Usage: confluence-cli.sh add-comment PAGE_ID \"comment text\"}"
    local payload
    payload=$(COMMENT="$comment_text" python3 -c "
import json, os
print(json.dumps({
    'pageId': '$page_id',
    'body': {'representation': 'storage', 'value': '<p>' + os.environ['COMMENT'] + '</p>'}
}))
")
    cf_post "$BASE/api/v2/footer-comments" "$payload" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps({
    'id': d.get('id'),
    'pageId': d.get('pageId'),
    'created': d.get('createdAt')
}, indent=2))
"
}

cmd_attachments() {
    local page_id="${1:?Usage: confluence-cli.sh attachments PAGE_ID}"
    cf_get "$BASE/api/v2/pages/$page_id/attachments?limit=25" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(json.dumps([{
    'id': a.get('id'),
    'title': a.get('title'),
    'mediaType': a.get('mediaType'),
    'fileSize': a.get('fileSize'),
    'downloadUrl': a.get('downloadLink')
} for a in d.get('results', [])], indent=2))
"
}

cmd_get_by_title() {
    local space_id="${1:?Usage: confluence-cli.sh get-by-title SPACE_ID \"Page Title\"}"
    local title="${2:?Usage: confluence-cli.sh get-by-title SPACE_ID \"Page Title\"}"
    local encoded_title=$(urlencode "$title")
    cf_get "$BASE/api/v2/spaces/$space_id/pages?title=$encoded_title&limit=1&body-format=storage" | python3 -c "
import sys, json, re
d = json.load(sys.stdin)
results = d.get('results', [])
if not results:
    print(json.dumps({'error': 'Page not found', 'title': '$title'}))
else:
    p = results[0]
    body_html = p.get('body', {}).get('storage', {}).get('value', '')
    body_text = re.sub(r'<[^>]+>', '', body_html).strip()
    print(json.dumps({
        'id': p.get('id'),
        'title': p.get('title'),
        'status': p.get('status'),
        'spaceId': p.get('spaceId'),
        'version': (p.get('version') or {}).get('number'),
        'body_text': body_text[:3000],
        'body_html': body_html[:5000],
        'url': p.get('_links', {}).get('webui')
    }, indent=2))
"
}

# --- Dispatch ---
CMD="${1:-help}"; shift || true
case "$CMD" in
    spaces)      cmd_spaces;;
    pages)       cmd_pages "$@";;
    get)         cmd_get_page "$@";;
    children)    cmd_children "$@";;
    search)      cmd_search "$@";;
    create)      cmd_create_page "$@";;
    update)      cmd_update_page "$@";;
    labels)      cmd_labels "$@";;
    add-labels)  cmd_add_labels "$@";;
    comments)    cmd_comments "$@";;
    add-comment) cmd_add_comment "$@";;
    attachments) cmd_attachments "$@";;
    get-by-title) cmd_get_by_title "$@";;
    help|--help|-h)
        echo "Usage: confluence-cli.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  spaces                       List all spaces"
        echo "  pages SPACE_ID [limit]       List pages in a space"
        echo "  get PAGE_ID                  Get page content"
        echo "  children PAGE_ID             List child pages"
        echo "  search \"CQL\" [limit]         Search with CQL"
        echo "  create --space ID --title TEXT [--parent ID] [--body HTML]"
        echo "  update PAGE_ID [--title TEXT] [--body HTML]"
        echo "  labels PAGE_ID               Get page labels"
        echo "  add-labels PAGE_ID \"l1,l2\"   Add labels to page"
        echo "  comments PAGE_ID               Get page comments"
        echo "  add-comment PAGE_ID \"text\"     Add comment to page"
        echo "  attachments PAGE_ID            List page attachments"
        echo "  get-by-title SPACE_ID \"title\"  Find page by exact title"
        echo ""
        echo "Env: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN";;
    *) echo "{\"error\":\"Unknown command: $CMD\"}" >&2; exit 1;;
esac