#!/bin/bash
set -euo pipefail

# ============================================================================
# bitbucket-cli.sh — Bitbucket Cloud REST API wrapper (read-only)
#
# Dependencies: curl, python3
# Env vars: ATLASSIAN_EMAIL, BITBUCKET_API_TOKEN, BITBUCKET_WORKSPACE
# Auth: Basic auth with email + read-only scoped API token
# Outputs: JSON to stdout, errors to stderr
# ============================================================================

for var in ATLASSIAN_EMAIL BITBUCKET_API_TOKEN BITBUCKET_WORKSPACE; do
    if [ -z "${!var:-}" ]; then
        echo "{\"error\": \"Missing env var: $var\"}" >&2
        exit 1
    fi
done

AUTH="$ATLASSIAN_EMAIL:$BITBUCKET_API_TOKEN"
BASE="https://api.bitbucket.org/2.0"
WS="$BITBUCKET_WORKSPACE"

# --- HTTP helpers ---
bb_get() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" -H "Accept: application/json" "$1")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        local err="{\"error\": \"HTTP $http_code\", \"url\": \"$1\"}"
        echo "$err" >&2
        echo "$err"
        exit 1
    fi
    echo "$body"
}

bb_get_raw() {
    local http_code body
    body=$(curl -s -w "\n%{http_code}" -u "$AUTH" "$1")
    http_code=$(echo "$body" | tail -1)
    body=$(echo "$body" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        local err="{\"error\": \"HTTP $http_code\", \"url\": \"$1\"}"
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

cmd_repos() {
    bb_get "$BASE/repositories/$WS?pagelen=50" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh prs REPO [STATE]}"
    local state="${2:-OPEN}"
    bb_get "$BASE/repositories/$WS/$repo/pullrequests?state=$state&pagelen=25" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh pr REPO PR_ID}"
    local pr_id="${2:?Usage: bitbucket-cli.sh pr REPO PR_ID}"
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
    local repo="${1:?Usage: bitbucket-cli.sh diffstat REPO PR_ID}"
    local pr_id="${2:?Usage: bitbucket-cli.sh diffstat REPO PR_ID}"
    bb_get "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/diffstat" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh diff REPO PR_ID}"
    local pr_id="${2:?Usage: bitbucket-cli.sh diff REPO PR_ID}"
    bb_get_raw "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/diff"
}

cmd_comments() {
    local repo="${1:?Usage: bitbucket-cli.sh comments REPO PR_ID}"
    local pr_id="${2:?Usage: bitbucket-cli.sh comments REPO PR_ID}"
    bb_get "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/comments?pagelen=50" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh pr-commits REPO PR_ID}"
    local pr_id="${2:?Usage: bitbucket-cli.sh pr-commits REPO PR_ID}"
    bb_get "$BASE/repositories/$WS/$repo/pullrequests/$pr_id/commits?pagelen=25" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh branches REPO [filter]}"
    local filter="${2:-}"
    local url="$BASE/repositories/$WS/$repo/refs/branches?pagelen=25"
    if [ -n "$filter" ]; then
        url="$url&q=name~\"$filter\""
    fi
    bb_get "$url" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh commits REPO [BRANCH]}"
    local branch="${2:-main}"
    bb_get "$BASE/repositories/$WS/$repo/commits/$branch?pagelen=10" | python3 -c "
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
    local repo="${1:?Usage: bitbucket-cli.sh file REPO FILEPATH [REV]}"
    local filepath="${2:?Usage: bitbucket-cli.sh file REPO FILEPATH [REV]}"
    local rev="${3:-main}"
    bb_get_raw "$BASE/repositories/$WS/$repo/src/$rev/$filepath"
}

cmd_ls() {
    local repo="${1:?Usage: bitbucket-cli.sh ls REPO [PATH] [REV]}"
    local path="${2:-}"
    local rev="${3:-main}"
    bb_get "$BASE/repositories/$WS/$repo/src/$rev/$path" | python3 -c "
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

cmd_tree() {
    local repo="${1:?Usage: bitbucket-cli.sh tree REPO [PATH] [REV]}"
    local path="${2:-}"
    local rev="${3:-main}"
    local url="$BASE/repositories/$WS/$repo/src/$rev/$path?max_depth=100&pagelen=100"
    bb_get "$url" | python3 -c "
import sys,json
d=json.load(sys.stdin)
entries=[]
for v in d.get('values',[]):
    t='d' if v.get('type')=='commit_directory' else 'f'
    entries.append((v.get('path',''),t))
entries.sort(key=lambda x:x[0])
for path,t in entries:
    print(f'{t} {path}')
"
}

cmd_search() {
    local query="${1:?Usage: bitbucket-cli.sh search QUERY [REPO]}"
    local repo="${2:-}"
    local encoded_query
    encoded_query=$(urlencode "$query")
    local url="$BASE/search/code?search_query=$encoded_query&pagelen=10"
    if [ -n "$repo" ]; then
        url="$url&search_in=$WS/$repo"
    fi
    bb_get "$url" | python3 -c "
import sys,json
d=json.load(sys.stdin)
results=[]
for v in d.get('values',[]):
    f=v.get('file',{})
    results.append({
        'file':f.get('path'),
        'repo':(f.get('links',{}).get('self',{}).get('href','').split('/src/')[0].split('/')[-1] if f.get('links') else None),
        'matched_lines':len(v.get('content_matches',[]))
    })
print(json.dumps(results,indent=2))
"
}

cmd_compare() {
    local repo="${1:?Usage: bitbucket-cli.sh compare REPO BASE_REF HEAD_REF}"
    local base_ref="${2:?Usage: bitbucket-cli.sh compare REPO BASE_REF HEAD_REF}"
    local head_ref="${3:?Usage: bitbucket-cli.sh compare REPO BASE_REF HEAD_REF}"
    bb_get_raw "$BASE/repositories/$WS/$repo/diff/$base_ref..$head_ref"
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
    tree)        cmd_tree "$@";;
    search)      cmd_search "$@";;
    compare)     cmd_compare "$@";;
    help|--help|-h)
        echo "Usage: bitbucket-cli.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  repos                          List all repos in workspace"
        echo "  prs REPO [STATE]               List pull requests (OPEN/MERGED/DECLINED)"
        echo "  pr REPO PR_ID                  Get PR details"
        echo "  diffstat REPO PR_ID            Per-file change summary"
        echo "  diff REPO PR_ID                Full unified diff"
        echo "  comments REPO PR_ID            PR comments (inline + general)"
        echo "  pr-commits REPO PR_ID          Commits in a PR"
        echo "  branches REPO [filter]         List branches"
        echo "  commits REPO [BRANCH]          Recent commits on a branch"
        echo "  file REPO FILEPATH [REV]       Read file contents"
        echo "  ls REPO [PATH] [REV]           List directory contents"
        echo "  tree REPO [PATH] [REV]         Recursive directory listing"
        echo "  search QUERY [REPO]            Search code in workspace or repo"
        echo "  compare REPO BASE HEAD         Diff between two branches"
        echo ""
        echo "Env: ATLASSIAN_EMAIL, BITBUCKET_API_TOKEN, BITBUCKET_WORKSPACE";;
    *) echo "{\"error\":\"Unknown command: $CMD\"}" >&2; exit 1;;
esac