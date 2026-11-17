#!/bin/bash
# foreman backend health probe — before dispatching, walk the worker pool in order and pick the first backend that works.
#
# Why this exists: in one day, three dispatches went red for reasons that had nothing to do with the work —
#   a subscription backend reported "Not logged in"   (the login lived in a different credential entry than the one the dispatcher reads)
#   an API-key backend returned 401 "api key invalid"  (the key was fine; a subscription token had leaked into that channel)
#   a third backend returned "usage limit … try again" (quota exhausted for weeks)
# All three surfaced *after* dispatch: the task was sent, the worktree built, the time spent. And because they
# look like failed deliveries, they would have walked into the rework loop and the circuit breaker, turning
# "the channel is down" into "the builder can't do the job". This probe moves those failures to before dispatch.
#
# Usage:
#   backend-health.sh pick               print the first usable backend in the pool (non-zero exit if none)
#   backend-health.sh check <backend>    probe one backend, print ok|auth|quota|config|net|unchecked
#   backend-health.sh mark <backend> <ok|auth|quota|config|net> [recover-at ISO]   record a failure seen mid-dispatch
#   backend-health.sh status             print the health table
#
# Configuration (all optional):
#   FOREMAN_POOL          space-separated backend names, in order of preference (default: "deepseek").
#                         Use the same names as in ~/.handoff/config.yaml.
#   FOREMAN_STATE_DIR     where the health table lives (default: ${XDG_STATE_HOME:-~/.local/state}/foreman).
#                         Backend health is a fact about your machine and accounts, not about the repo you are in,
#                         so the table is global. (A repo-relative table was tried first: probing from two directories
#                         wrote two tables that never saw each other, and cooldowns silently stopped working.)
#   FOREMAN_PROBE_<NAME>  a probe command for a backend without a built-in probe (NAME upper-cased, non-alphanumerics
#                         as _). It is your own command, run with `sh -c`; exit 0 = ok, otherwise its output is classified.
#
# Built-in probes, chosen by backend name, and what each one costs:
#   claude | opus | sonnet   `claude auth status` — local read, no request, no tokens
#   cursor                   `cursor-agent status` — local login check, no conversation request
#   deepseek                 GET https://api.deepseek.com/user/balance with $DEEPSEEK_API_KEY — no tokens.
#                            The key is sent only to that endpoint. If the variable isn't set, the result is `unchecked`.
#   codex                    one minimal `codex exec` call — this one spends a request, which is why its failures always cool down
# A backend with neither a built-in nor a FOREMAN_PROBE_<NAME> probe reports `unchecked`: pick still uses it, but says so.
set -u

POOL="${FOREMAN_POOL:-deepseek}"
STATE_DIR="${FOREMAN_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/foreman}"
STATE="$STATE_DIR/backend-health.json"
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$STATE_DIR"
[ -f "$STATE" ] || echo '{}' > "$STATE"

# Stock macOS has no `timeout`; perl's alarm is the portable fallback.
run_limited() {
  local secs="$1"; shift
  if command -v timeout >/dev/null 2>&1; then timeout "$secs" "$@"
  else perl -e 'alarm shift; exec @ARGV' "$secs" "$@"; fi
}

# ── Cooldown lookup: prints the reason if still cooling, nothing otherwise ──
cooling() {
  python3 - "$STATE" "$1" "$NOW" <<'PY'
import json,sys,datetime as dt
state,be,now=sys.argv[1],sys.argv[2],sys.argv[3]
try: d=json.load(open(state))
except Exception: d={}
e=d.get(be) or {}
until=e.get("cooldown_until")
if not until: sys.exit()
try:
    if dt.datetime.fromisoformat(until.replace("Z","+00:00")) > dt.datetime.fromisoformat(now.replace("Z","+00:00")):
        print(f'{e.get("last_error","unknown")} until {until}')
except Exception: pass
PY
}

# ── Record a result; failures get a cooldown by type ──
# auth    no cooldown (a login can be fixed at any moment — probe again next time)
# quota   the recovery time if the error gave one, otherwise the same time tomorrow
# config  6 hours (unknown model, invalid parameter — only a config change fixes it; `mark <be> ok` thaws it at once)
# net     10 minutes
mark() {
  python3 - "$STATE" "$1" "$2" "$NOW" "${3:-}" <<'PY'
import json,sys,datetime as dt
state,be,res,now,until=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],(sys.argv[5] if len(sys.argv)>5 else "")
try: d=json.load(open(state))
except Exception: d={}
e=d.setdefault(be,{})
e["last_checked"]=now; e["last_result"]=res
if res=="ok":
    e.pop("cooldown_until",None); e.pop("last_error",None)
    e["consecutive_failures"]=0
else:
    e["last_error"]=res
    e["consecutive_failures"]=e.get("consecutive_failures",0)+1
    n=dt.datetime.fromisoformat(now.replace("Z","+00:00"))
    if until: e["cooldown_until"]=until
    elif res=="quota":  e["cooldown_until"]=(n+dt.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    elif res=="net":    e["cooldown_until"]=(n+dt.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    elif res=="config": e["cooldown_until"]=(n+dt.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:               e.pop("cooldown_until",None)   # auth: no cooldown
json.dump(d,open(state,"w"),ensure_ascii=False,indent=2)
PY
}

# ── Classify free-form error output ──
# Order matters: quota wording often also mentions "login" or "upgrade", so quota is tested first.
# (The first version tested auth first and misread an exhausted quota as a logged-out account.)
classify() {
  if   printf '%s' "$1" | grep -qiE "usage limit|rate.?limit|quota|try again at|insufficient balance"; then echo quota
  elif printf '%s' "$1" | grep -qiE "model is not supported|model.*not found|invalid_request_error|unknown model"; then echo config
  elif printf '%s' "$1" | grep -qiE "401|403|token_expired|not logged in|not authenticated|please (run|use).*login|invalid api key"; then echo auth
  else echo net; fi
}

# ── Which CLAUDE_CONFIG_DIR will handoff really use for this backend? ──
# The claude CLI keys its stored login by that directory, so "unset" and "set to the same path explicitly"
# can be two different credential entries. Probing the default entry while handoff reads another gives a false ok.
claude_config_dir() {
  local d=""
  if command -v handoff >/dev/null 2>&1; then
    d=$(cd /tmp && handoff run --dry-run --backend "$1" --text hi 2>/dev/null \
      | grep -oE 'CLAUDE_CONFIG_DIR=[^ ]*' | head -1 | cut -d= -f2)
  fi
  d="${d/#\~/$HOME}"
  printf '%s' "${d:-$HOME/.claude}"
}

# ── Probe one backend ──
check() {
  local be="$1" var out
  var="FOREMAN_PROBE_$(printf '%s' "$be" | tr '[:lower:]' '[:upper:]' | tr -c 'A-Z0-9\n' '_')"
  if [ -n "${!var:-}" ]; then
    if out=$(run_limited 60 sh -c "${!var}" 2>&1); then echo ok; else classify "$out"; fi
    return
  fi
  case "$be" in
    claude|opus|sonnet)
      command -v claude >/dev/null 2>&1 || { echo config; return; }
      if [ "$(CLAUDE_CONFIG_DIR="$(claude_config_dir "$be")" claude auth status 2>/dev/null \
              | python3 -c 'import json,sys; print(json.load(sys.stdin).get("loggedIn", False))' 2>/dev/null)" = "True" ]
      then echo ok; else echo auth; fi
      ;;
    cursor)
      local bin; bin=$(command -v cursor-agent || command -v agent) || { echo config; return; }
      out=$(run_limited 15 "$bin" status 2>&1)
      if printf '%s' "$out" | grep -qi "logged in as"; then echo ok; else classify "$out"; fi
      ;;
    deepseek)
      [ -n "${DEEPSEEK_API_KEY:-}" ] || { echo unchecked; return; }
      python3 - <<'PY'
import os,json,urllib.request,urllib.error
try:
    r=urllib.request.urlopen(urllib.request.Request(
        "https://api.deepseek.com/user/balance",
        headers={"Authorization": "Bearer " + os.environ["DEEPSEEK_API_KEY"]}), timeout=15)
    print("ok" if json.load(r).get("is_available") else "quota")
except urllib.error.HTTPError as e: print("auth" if e.code in (401,403) else "quota" if e.code in (402,429) else "net")
except Exception: print("net")
PY
      ;;
    codex)
      command -v codex >/dev/null 2>&1 || { echo config; return; }
      out=$(cd /tmp && run_limited 120 codex exec --skip-git-repo-check --sandbox read-only \
        'reply with exactly: PROBE_OK' < /dev/null 2>&1 | tail -5)
      if printf '%s' "$out" | grep -q 'PROBE_OK'; then echo ok; else classify "$out"; fi
      ;;
    *) echo unchecked ;;
  esac
}

case "${1:-pick}" in
  check)
    be="${2:?usage: check <backend>}"
    c=$(cooling "$be"); [ -n "$c" ] && { echo "cooling: $c"; exit 1; }
    r=$(check "$be"); [ "$r" = unchecked ] || mark "$be" "$r"; echo "$r"
    [ "$r" = ok ] || [ "$r" = unchecked ] || exit 1
    ;;
  mark)
    mark "${2:?backend}" "${3:?ok|auth|quota|config|net}" "${4:-}"; echo "recorded: $2 -> $3 ${4:+(cooling until $4)}"
    ;;
  status)
    echo "pool order: $POOL"
    python3 - "$STATE" "$NOW" <<'PY'
import json,sys,datetime as dt
d=json.load(open(sys.argv[1])); now=sys.argv[2]
if not d: print("  (no records yet — nothing probed)"); raise SystemExit
for be,e in d.items():
    cd=e.get("cooldown_until","")
    hot = cd and dt.datetime.fromisoformat(cd.replace("Z","+00:00")) > dt.datetime.fromisoformat(now.replace("Z","+00:00"))
    print(f"  {be:10} {e.get('last_result','?'):6} consecutive_failures={e.get('consecutive_failures',0)}"
          f" checked={e.get('last_checked','-')}" + (f"  cooling until {cd}" if hot else ""))
PY
    ;;
  pick)
    for be in $POOL; do
      c=$(cooling "$be")
      if [ -n "$c" ]; then echo "  skip $be: $c" >&2; continue; fi
      r=$(check "$be")
      if [ "$r" = unchecked ]; then
        echo "  picked $be — NOT probed (no built-in probe, no FOREMAN_PROBE_ override, or no credential in the environment)" >&2
        echo "$be"; exit 0
      fi
      mark "$be" "$r"
      if [ "$r" = ok ]; then echo "  picked $be" >&2; echo "$be"; exit 0; fi
      echo "  $be unavailable ($r), trying the next one" >&2
    done
    echo "  no usable backend in the pool — stop dispatching and report to the user" >&2
    exit 1
    ;;
  *) echo "usage: $0 {pick|check <backend>|mark <backend> <ok|auth|quota|config|net> [ISO]|status}" >&2; exit 2 ;;
esac
