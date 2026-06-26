#!/bin/bash
set -euo pipefail

# ============================================================================
# bb-cli.sh — Bitbucket Cloud REST API wrapper (read-only)
#
# SECURITY MANIFEST
# -----------------
# Environment variables read:
#   - BITBUCKET_API_TOKEN  (used for Bearer auth, never logged)
#   - BITBUCKET_WORKSPACE  (workspace slug for API URL construction)
#
# External endpoints called:
#   - https://api.bitbucket.org/2.0/*  (Bitbucket Cloud REST API, read-only)
#
# Local files read/written:
#   - None. All output goes to stdout/stderr.
#
# Network access:
#   - HTTPS GET requests only. No data is sent beyond the Authorization header.
#
# Dependencies: curl, python3
# Auth: Authorization: Bearer <BITBUCKET_API_TOKEN>
# Outputs: JSON to stdout, errors to stderr
# ============================================================================

# --- Environment validation ---
for var in BITBUCKET_API_TOKEN BITBUCKET_WORKSPACE; do
    if [ -z "${!var:-}" ]; then
        echo "{\"error\": \"Missing env var: $var\"}" >&2
        exit 1
    fi
done

BASE="https://api.bitbucket.org/2.0"
WS="$BITBUCKET_WORKSPACE"

# --- Input sanitization helpers ---
# Validates that a repo slug contains only safe characters (alphanumeric, dash, underscore, dot)
validate_repo_slug() {
    local slug="$1"
    if [[ ! "$slug" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]; then
        echo "{\"error\": \"Invalid repository slug: '$slug'. Must be alphanumeric with dashes, underscores, or dots.\"}" >&2
        exit 1
    fi
}

# Validates that a PR ID is a positive integer
validate_pr_id() {
    local pr_id="$1"
    if [[ ! "$pr_id" =~ ^[1-9][0-9]*$ ]]; then
        echo "{\"error\": \"Invalid PR ID: '$pr_id'. Must be a positive integer.\"}" >&2
        exit 1
    fi
}

# Validates that a branch/revision name contains only safe characters
validate_ref() {
    local ref="$1"
    if [[ ! "$ref" =~ ^[a-zA-Z0-9][a-zA-Z0-9._/-]*$ ]]; then
        echo "{\"error\": \"Invalid branch/revision: '$ref'. Contains disallowed characters.\"}" >&2
        exit 1
    fi
}

# Validates PR state values
validate_state() {
    local state="$1"
    case "$state" in
        OPEN|MERGED|DECLINED|SUPERSEDED) ;;
        *) echo "{\"error\": \"Invalid state: '$state'. Must be OPEN, MERGED, DECLINED, or SUPERSEDED.\"}" >&2; exit 1;;
    esac
}

# --- HTTP helpers ---
bb_get() {
    local response http_code body
    response=$(curl -s -L -w "\n%{http_code}" \
        -H "Authorization: Bearer $BITBUCKET_API_TOKEN" \
        -H "Accept: application/json" \
        "$1")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\"}" >&2
        exit 1
    fi
    echo "$body"
}

bb_get_paginated() {
    local url="${1:?Missing URL}"
    local page_body
    local all_values='[]'

    while [ -n "$url" ]; do
        page_body=$(bb_get "$url")
        all_values=$(printf '[%s,%s]' "$all_values" "$page_body" | python3 -c '
import sys, json
all_items, page = json.load(sys.stdin)
all_items.extend(page.get("values", []))
print(json.dumps(all_items))
')
        url=$(printf '%s' "$page_body" | python3 -c '
import sys, json
page = json.load(sys.stdin)
print(page.get("next", ""))
')
    done

    printf '%s' "$all_values" | python3 -c '
import sys, json
values = json.load(sys.stdin)
print(json.dumps({"size": len(values), "values": values}))
'
}

urlencode() {
    python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$1"
}

# --- Commands ---

cmd_repos() {
    bb_get_paginated "$BASE/repositories/$WS?pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'slug':r.get('slug'),
    'name':r.get('name'),
    'full_name':r.get('full_name'),
    'language':r.get('language'),
    'updated':r.get('updated_on'),
    'is_private':r.get('is_private'),
    'url':r.get('links',{}).get('html',{}).get('href')
} for r in d.get('values',[])],indent=2))
"
}

cmd_prs() {
    local repo="${1:?Usage: bb-cli.sh prs REPO [STATE]}"
    local state="${2:-OPEN}"
    validate_repo_slug "$repo"
    validate_state "$state"
    bb_get_paginated "$BASE/repositories/$WS/$repo/pullrequests?state=$state&pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({
    'total':d.get('size',len(d.get('values',[]))),
    'pullrequests':[{
        'id':pr.get('id'),
        'title':pr.get('title'),
        'author':(pr.get('author')or{}).get('display_name'),
        'source':(pr.get('source')or{}).get('branch',{}).get('name'),
        'destination':(pr.get('destination')or{}).get('branch',{}).get('name'),
        'state':pr.get('state'),
        'created':pr.get('created_on'),
        'updated':pr.get('updated_on'),
        'url':(pr.get('links')or{}).get('html',{}).get('href')
    } for pr in d.get('values',[])
]},indent=2))
"
}

cmd_pr() {
    local repo="${1:?Usage: bb-cli.sh pr REPO PR_ID}"
    local pr_id="${2:?Usage: bb-cli.sh pr REPO PR_ID}"
    validate_repo_slug "$repo"
    validate_pr_id "$pr_id"
    bb_get "$BASE/repositories/$WS/$repo/pullrequests/$pr_id" | python3 -c "
import sys,json
pr=json.load(sys.stdin)
print(json.dumps({
    'id':pr.get('id'),
    'title':pr.get('title'),
    'description':pr.get('description'),
    'author':(pr.get('author')or{}).get('display_name'),
    'source':(pr.get('source')or{}).get('branch',{}).get('name'),
    'destination':(pr.get('destination')or{}).get('branch',{}).get('name'),
    'state':pr.get('state'),
    'reviewers':[r.get('display_name') for r in pr.get('reviewers',[])],
    'created':pr.get('created_on'),
    'updated':pr.get('updated_on'),
    'comment_count':pr.get('comment_count'),
    'url':(pr.get('links')or{}).get('html',{}).get('href')
},indent=2))
"
}

cmd_diffstat() {
    local repo="${1:?Usage: bb-cli.sh diffstat REPO PR_ID}"
    local pr_id="${2:?Usage: bb-cli.sh diffstat REPO PR_ID}"
    validate_repo_slug "$repo"
    validate_pr_id "$pr_id"
    bb_get_paginated "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/diffstat?pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
files=[]
for f in d.get('values',[]):
    old_path=(f.get('old')or{}).get('path')
    new_path=(f.get('new')or{}).get('path')
    files.append({
        'path':new_path or old_path,
        'status':f.get('status'),
        'lines_added':f.get('lines_added',0),
        'lines_removed':f.get('lines_removed',0)
    })
total_added=sum(x['lines_added'] for x in files)
total_removed=sum(x['lines_removed'] for x in files)
print(json.dumps({
    'files_changed':len(files),
    'total_added':total_added,
    'total_removed':total_removed,
    'files':files
},indent=2))
"
}

cmd_diff() {
    local repo="${1:?Usage: bb-cli.sh diff REPO PR_ID [FILEPATH]}"
    local pr_id="${2:?Usage: bb-cli.sh diff REPO PR_ID [FILEPATH]}"
    local filepath="${3:-}"
    validate_repo_slug "$repo"
    validate_pr_id "$pr_id"
    local url="$BASE/repositories/$WS/$repo/pullrequests/$pr_id/diff"
    if [ -n "$filepath" ]; then
        url="$url?path=$(urlencode "$filepath")"
    fi
    bb_get "$url"
}

cmd_comments() {
    local repo="${1:?Usage: bb-cli.sh comments REPO PR_ID}"
    local pr_id="${2:?Usage: bb-cli.sh comments REPO PR_ID}"
    validate_repo_slug "$repo"
    validate_pr_id "$pr_id"
    bb_get_paginated "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/comments?pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
comments=[]
for c in d.get('values',[]):
    inline=c.get('inline')
    loc=None
    if inline:
        loc={'path':inline.get('path'),'from':inline.get('from'),'to':inline.get('to')}
    content=c.get('content',{}).get('raw','')
    comments.append({
        'id':c.get('id'),
        'author':(c.get('user')or{}).get('display_name'),
        'content':content[:500] if content else None,
        'inline':loc,
        'created':c.get('created_on')
    })
print(json.dumps({'count':len(comments),'comments':comments},indent=2))
"
}

cmd_pr_commits() {
    local repo="${1:?Usage: bb-cli.sh pr-commits REPO PR_ID}"
    local pr_id="${2:?Usage: bb-cli.sh pr-commits REPO PR_ID}"
    validate_repo_slug "$repo"
    validate_pr_id "$pr_id"
    bb_get_paginated "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/commits?pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'hash':c.get('hash','')[:12],
    'message':(c.get('message')or'').split('\n')[0],
    'author':(c.get('author')or{}).get('raw'),
    'date':c.get('date')
} for c in d.get('values',[])],indent=2))
"
}

cmd_branches() {
    local repo="${1:?Usage: bb-cli.sh branches REPO [filter]}"
    local filter="${2:-}"
    validate_repo_slug "$repo"
    local url="$BASE/repositories/$WS/$repo/refs/branches?pagelen=100"
    if [ -n "$filter" ]; then
        url="$url&q=name~\"$filter\""
    fi
    bb_get_paginated "$url" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'name':b.get('name'),
    'hash':(b.get('target')or{}).get('hash','')[:12],
    'date':(b.get('target')or{}).get('date'),
    'author':((b.get('target')or{}).get('author')or{}).get('raw')
} for b in d.get('values',[])],indent=2))
"
}

cmd_commits() {
    local repo="${1:?Usage: bb-cli.sh commits REPO [BRANCH]}"
    local branch="${2:-master}"
    validate_repo_slug "$repo"
    validate_ref "$branch"
    bb_get_paginated "$BASE/repositories/$WS/$repo/commits/$branch?pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'hash':c.get('hash','')[:12],
    'message':(c.get('message')or'').split('\n')[0],
    'author':(c.get('author')or{}).get('raw'),
    'date':c.get('date')
} for c in d.get('values',[])],indent=2))
"
}

cmd_file() {
    local repo="${1:?Usage: bb-cli.sh file REPO FILEPATH [REV]}"
    local filepath="${2:?Usage: bb-cli.sh file REPO FILEPATH [REV]}"
    local rev="${3:-master}"
    validate_repo_slug "$repo"
    validate_ref "$rev"
    bb_get "$BASE/repositories/$WS/$repo/src/$rev/$filepath"
}

cmd_ls() {
    local repo="${1:?Usage: bb-cli.sh ls REPO [PATH] [REV]}"
    local path="${2:-}"
    local rev="${3:-master}"
    validate_repo_slug "$repo"
    validate_ref "$rev"
    bb_get_paginated "$BASE/repositories/$WS/$repo/src/$rev/$path?pagelen=100" | python3 -c "
import sys,json
d=json.load(sys.stdin)
entries=[]
for v in d.get('values',[]):
    entries.append({
        'path':v.get('path'),
        'type':v.get('type'),
        'size':v.get('size')
    })
print(json.dumps(entries,indent=2))
"
}

# --- Dispatch ---
CMD="${1:-help}"; shift || true
case "$CMD" in
    repos)       cmd_repos;;
    prs)         cmd_prs "$@";;
    pr)          cmd_pr "$@";;
    diffstat)    cmd_diffstat "$@";;
    diff)        cmd_diff "$@";;
    comments)    cmd_comments "$@";;
    pr-commits)  cmd_pr_commits "$@";;
    branches)    cmd_branches "$@";;
    commits)     cmd_commits "$@";;
    file)        cmd_file "$@";;
    ls)          cmd_ls "$@";;
    help|--help|-h)
        echo "Usage: bb-cli.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  repos                          List all repos in workspace"
        echo "  prs REPO [STATE]               List pull requests (OPEN/MERGED/DECLINED)"
        echo "  pr REPO PR_ID                  Get PR details"
        echo "  diffstat REPO PR_ID            Per-file change summary"
        echo "  diff REPO PR_ID [FILEPATH]     Full diff, or diff for a single file"
        echo "  comments REPO PR_ID            PR comments (inline + general)"
        echo "  pr-commits REPO PR_ID          Commits in a PR"
        echo "  branches REPO [filter]         List branches"
        echo "  commits REPO [BRANCH]          Recent commits on a branch"
        echo "  file REPO FILEPATH [REV]       Read file contents"
        echo "  ls REPO [PATH] [REV]           List directory contents"
        echo ""
        echo "Env: BITBUCKET_API_TOKEN, BITBUCKET_WORKSPACE";;
    *) echo "{\"error\":\"Unknown command: $CMD\"}" >&2; exit 1;;
esac