#!/bin/bash
set -euo pipefail

# ============================================================================
# jira-cli.sh — Jira Cloud REST API wrapper
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
BASE="$ATLASSIAN_URL/rest/api/3"

# --- HTTP helpers ---
jira_get() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" -H "Accept: application/json" "$1")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\"}" >&2
        exit 1
    fi
    echo "$body"
}

jira_post() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" \
        -X POST -H "Content-Type: application/json" -H "Accept: application/json" \
        "$1" -d "$2")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"response\": $body}" >&2
        exit 1
    fi
    echo "$body"
}

jira_put() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" \
        -X PUT -H "Content-Type: application/json" -H "Accept: application/json" \
        "$1" -d "$2")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"response\": $body}" >&2
        exit 1
    fi
    if [ -n "$body" ]; then echo "$body"; else echo '{"success":true}'; fi
}

urlencode() {
    python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$1"
}

# --- Commands ---

cmd_search() {
    local jql="${1:?Usage: jira-cli.sh search \"JQL query\" [maxResults]}"
    local max="${2:-20}"
    jira_get "$BASE/search/jql?jql=$(urlencode "$jql")&maxResults=$max" | python3 -c "
import sys,json
d=json.load(sys.stdin)
r={'total':d.get('total',0),'issues':[]}
for i in d.get('issues',[]):
    f=i.get('fields',{})
    r['issues'].append({
        'key':i.get('key'),
        'summary':f.get('summary'),
        'status':(f.get('status')or{}).get('name'),
        'priority':(f.get('priority')or{}).get('name'),
        'assignee':(f.get('assignee')or{}).get('displayName','Unassigned'),
        'type':(f.get('issuetype')or{}).get('name'),
        'created':f.get('created'),
        'updated':f.get('updated')})
print(json.dumps(r,indent=2))
"
}

cmd_get() {
    local key="${1:?Usage: jira-cli.sh get ISSUE-KEY}"
    jira_get "$BASE/issue/$key" | python3 -c "
import sys,json,os
d=json.load(sys.stdin)
f=d.get('fields',{})
desc=None
if f.get('description'):
    texts=[]
    def ex(n):
        if isinstance(n,dict):
            if 'text' in n:texts.append(n['text'])
            for c in n.get('content',[]):ex(c)
    ex(f['description'])
    desc=' '.join(texts) if texts else None
print(json.dumps({
    'key':d.get('key'),'summary':f.get('summary'),
    'status':(f.get('status')or{}).get('name'),
    'priority':(f.get('priority')or{}).get('name'),
    'type':(f.get('issuetype')or{}).get('name'),
    'assignee':(f.get('assignee')or{}).get('displayName','Unassigned'),
    'reporter':(f.get('reporter')or{}).get('displayName','Unknown'),
    'project':(f.get('project')or{}).get('key'),
    'description':desc,'labels':f.get('labels',[]),
    'created':f.get('created'),'updated':f.get('updated'),
    'url':os.environ.get('ATLASSIAN_URL','')+'/browse/'+d.get('key','')
},indent=2))
"
}

cmd_create() {
    local project="" itype="Task" summary="" description="" priority=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --project) project="$2"; shift 2;;
            --type) itype="$2"; shift 2;;
            --summary) summary="$2"; shift 2;;
            --description) description="$2"; shift 2;;
            --priority) priority="$2"; shift 2;;
            *) echo "{\"error\":\"Unknown flag: $1\"}" >&2; exit 1;;
        esac
    done
    [ -z "$project" ] || [ -z "$summary" ] && { echo '{"error":"Required: --project KEY --summary TEXT"}' >&2; exit 1; }

    local payload
    payload=$(python3 -c "
import json
f={'project':{'key':'$project'},'issuetype':{'name':'$itype'},'summary':json.loads($(python3 -c "import json;print(json.dumps(json.dumps('$summary')))"))}
d='$description'
if d:f['description']={'type':'doc','version':1,'content':[{'type':'paragraph','content':[{'type':'text','text':d}]}]}
p='$priority'
if p:f['priority']={'name':p}
print(json.dumps({'fields':f}))
")
    jira_post "$BASE/issue" "$payload" | python3 -c "
import sys,json,os
d=json.load(sys.stdin)
print(json.dumps({'key':d.get('key'),'id':d.get('id'),'url':os.environ.get('ATLASSIAN_URL','')+'/browse/'+d.get('key','')},indent=2))
"
}

cmd_comment() {
    local key="${1:?Usage: jira-cli.sh comment ISSUE-KEY \"text\"}"
    local text="${2:?Usage: jira-cli.sh comment ISSUE-KEY \"text\"}"
    local payload
    payload=$(python3 -c "
import json
print(json.dumps({'body':{'type':'doc','version':1,'content':[{'type':'paragraph','content':[{'type':'text','text':json.loads($(python3 -c "import json;print(json.dumps(json.dumps('$text')))"))}]}]}}))
")
    jira_post "$BASE/issue/$key/comment" "$payload" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({'id':d.get('id'),'created':d.get('created'),'author':(d.get('author')or{}).get('displayName')},indent=2))
"
}

cmd_transitions() {
    local key="${1:?Usage: jira-cli.sh transitions ISSUE-KEY}"
    jira_get "$BASE/issue/$key/transitions" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({'transitions':[{'id':t['id'],'name':t['name'],'to':t.get('to',{}).get('name')} for t in d.get('transitions',[])]},indent=2))
"
}

cmd_transition() {
    local key="${1:?Usage: jira-cli.sh transition ISSUE-KEY TRANSITION-ID}"
    local tid="${2:?Usage: jira-cli.sh transition ISSUE-KEY TRANSITION-ID}"
    jira_post "$BASE/issue/$key/transitions" "{\"transition\":{\"id\":\"$tid\"}}" > /dev/null
    echo "{\"success\":true,\"issue\":\"$key\",\"transitionId\":\"$tid\"}"
}

cmd_assign() {
    local key="${1:?Usage: jira-cli.sh assign ISSUE-KEY ACCOUNT-ID}"
    local aid="${2:?Usage: jira-cli.sh assign ISSUE-KEY ACCOUNT-ID}"
    jira_put "$BASE/issue/$key/assignee" "{\"accountId\":\"$aid\"}"
}

cmd_update() {
    local key="${1:?Usage: jira-cli.sh update ISSUE-KEY --field value}"
    shift
    local summary="" priority="" labels=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --summary) summary="$2"; shift 2;;
            --priority) priority="$2"; shift 2;;
            --labels) labels="$2"; shift 2;;
            *) echo "{\"error\":\"Unknown flag: $1\"}" >&2; exit 1;;
        esac
    done
    local payload
    payload=$(python3 -c "
import json
f={}
s='$summary';p='$priority';l='$labels'
if s:f['summary']=s
if p:f['priority']={'name':p}
if l:f['labels']=l.split(',')
print(json.dumps({'fields':f}))
")
    jira_put "$BASE/issue/$key" "$payload"
}

cmd_users() {
    local query="${1:?Usage: jira-cli.sh users \"query\"}"
    jira_get "$BASE/user/search?query=$(urlencode "$query")&maxResults=10" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{'accountId':u.get('accountId'),'displayName':u.get('displayName'),'email':u.get('emailAddress'),'active':u.get('active')} for u in d],indent=2))
"
}

cmd_projects() {
    jira_get "$BASE/project" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{'key':p.get('key'),'name':p.get('name'),'type':p.get('projectTypeKey')} for p in d],indent=2))
"
}

# --- Dispatch ---
CMD="${1:-help}"; shift || true
case "$CMD" in
    search)      cmd_search "$@";;
    get)         cmd_get "$@";;
    create)      cmd_create "$@";;
    comment)     cmd_comment "$@";;
    transitions) cmd_transitions "$@";;
    transition)  cmd_transition "$@";;
    assign)      cmd_assign "$@";;
    update)      cmd_update "$@";;
    users)       cmd_users "$@";;
    projects)    cmd_projects "$@";;
    help|--help|-h)
        echo "Usage: jira-cli.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  search \"JQL\" [max]         Search issues"
        echo "  get ISSUE-KEY              Get issue details"
        echo "  create --project --type --summary [--description] [--priority]"
        echo "  comment ISSUE-KEY \"text\"   Add a comment"
        echo "  transitions ISSUE-KEY      List available transitions"
        echo "  transition ISSUE-KEY ID    Transition issue to new status"
        echo "  assign ISSUE-KEY ACCT-ID   Assign issue to user"
        echo "  update ISSUE-KEY [--summary] [--priority] [--labels]"
        echo "  users \"query\"              Search users (get account IDs)"
        echo "  projects                   List all projects"
        echo ""
        echo "Env: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN";;
    *) echo "{\"error\":\"Unknown command: $CMD\"}" >&2; exit 1;;
esac