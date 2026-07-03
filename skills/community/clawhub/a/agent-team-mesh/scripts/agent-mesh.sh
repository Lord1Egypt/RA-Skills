#!/bin/bash
# agent-team-mesh v1.0.0 - OpenClaw team P2P WS mesh CLI (open-source edition)
# Changelog v0.4.0:
#   - R1 fix: Auto-detect local email prefix (USER.md / sso.json / MESH_MY_EMAIL env, 3-way fallback); removed hardcoded value
#   - R2 fix: tokens split from registry.json into ~/.config/agent-team-mesh/tokens.json (chmod 600)
#   - R3 fix: Message size check (4KB warn / 8KB block)
#   - R7 fix: email domain configurable via env var
#   - R14 add: --dry-run mode
#   - R17 fix: broadcast output atomization (in-line buffer + serial echo to prevent interleaving)

# Locate skill root (this script is in scripts/, registry in references/)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY_FILE="$SKILL_DIR/references/registry.json"
# Tokens file: prefer XDG path, fallback to ~/.config/agent-team-mesh/tokens.json
TOKENS_FILE="${MESH_TOKENS_FILE:-${XDG_CONFIG_HOME:-$HOME/.config}/agent-team-mesh/tokens.json}"
IM_FALLBACK_SCRIPT="${MESH_IM_FALLBACK:-$HOME/.openclaw/workspace/skills/im-fallback/scripts/send.py}"
EMAIL_DOMAIN="${MESH_EMAIL_DOMAIN:-example.com}"
MSG_SOFT_LIMIT="${MESH_MSG_SOFT_LIMIT:-4096}"
MSG_HARD_LIMIT="${MESH_MSG_HARD_LIMIT:-8192}"
export OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1

# R1: Auto-detect this machine's email prefix
detect_my_email_prefix() {
  # 1. env var explicit override
  if [[ -n "${MESH_MY_EMAIL:-}" ]]; then
    echo "${MESH_MY_EMAIL%@*}"
    return
  fi
  # 2. USER.md (OpenClaw workspace file)
  # Prefer OpenClaw USER.md, but also try generic locations
  local user_md=""
  for candidate in "$HOME/.openclaw/workspace/USER.md" "$HOME/.config/agent-team-mesh/USER.md" "./USER.md"; do
    [[ -f "$candidate" ]] && { user_md="$candidate"; break; }
  done
  if [[ -n "$user_md" ]]; then
    local prefix
    prefix=$(grep -i "email" "$user_md" 2>/dev/null \
      | grep -oE '[a-z0-9._-]+@[a-z0-9.-]+' | head -1 | cut -d@ -f1)
    if [[ -n "$prefix" ]]; then
      echo "$prefix"
      return
    fi
  fi
  # 3. sso.json
  if [[ -f "$HOME/sso.json" ]]; then
    local prefix
    prefix=$(python3 -c "
import json
try:
    d = json.load(open('$HOME/sso.json'))
    e = d.get('user', {}).get('email', '')
    print(e.split('@')[0] if '@' in e else '')
except: pass
" 2>/dev/null)
    if [[ -n "$prefix" ]]; then
      echo "$prefix"
      return
    fi
  fi
  echo ""
}

MY_EMAIL_PREFIX="$(detect_my_email_prefix)"

usage() {
  cat << 'USAGE'
agent-team-mesh v1.0.0 - OpenClaw team Agent cross-container P2P communication

Commands:
  list                                     List all Agents and their online status
  ping  --to <name|nickname|email-prefix>           Test connectivity to a target Agent
  send  --to <name|nickname|email-prefix>           Send a message and wait for reply
        --message <message>
        [--session <sessionKey>]           default: main
        [--rounds <N>]                     Multi-round conversation, default 1
        [--timeout <seconds>]                   Wait timeout (seconds), default 60
        [--dry-run]                        Print payload only, do not actually send
  broadcast --message <message>               Broadcast to all online Agents (excludes self)
            [--timeout <seconds>]               Default 60
            [--dry-run]                    List recipients only, do not actually send
  sync                                     (stub) Pull registry from your team source — see scripts comment
  whoami                                   Show this machine's identified email prefix

Environment variables:
  MESH_MY_EMAIL          Override auto-detected email (e.g. alice@example.com)
  MESH_TOKENS_FILE       Custom tokens file path
  MESH_EMAIL_DOMAIN      Email domain for IM fallback (default example.com)
  MESH_MSG_SOFT_LIMIT    Soft message size limit in bytes (default 4096, warns above)
  MESH_MSG_HARD_LIMIT    Hard message size limit in bytes (default 8192, blocks above)

Examples:
  ./run.sh whoami
  ./run.sh list
  ./run.sh send --to alice --message "help me with this"
  ./run.sh send --to alice --message "test" --dry-run
  ./run.sh broadcast --message "team announcement"
USAGE
}

# ── Helper functions ───────────────────────────────────────────────

# R3: message size check (return 0=pass, 1=block)
check_message_size() {
  local msg="$1"
  local bytes
  bytes=$(printf "%s" "$msg" | wc -c)
  if [[ $bytes -gt $MSG_HARD_LIMIT ]]; then
    echo "❌ Message exceeds hard limit (${bytes} > ${MSG_HARD_LIMIT} bytes), rejecting"
    echo "   Set MESH_MSG_HARD_LIMIT to raise the limit (not recommended)"
    return 1
  fi
  if [[ $bytes -gt $MSG_SOFT_LIMIT ]]; then
    echo "⚠️  Message exceeds soft limit (${bytes} > ${MSG_SOFT_LIMIT} bytes), continuing" >&2
  fi
  return 0
}

# R2: Look up token by emailPrefix from separate tokens file
get_token_for() {
  local prefix="$1"
  if [[ ! -f "$TOKENS_FILE" ]]; then
    return 1
  fi
  python3 -c "
import json, sys
try:
    d = json.load(open('$TOKENS_FILE'))
    t = d.get('tokens', {}).get(sys.argv[1], '')
    print(t)
    sys.exit(0 if t else 1)
except: sys.exit(1)
" "$prefix" 2>/dev/null
}

# Extract the last complete JSON object from openclaw gateway call output (ignore warnings)
extract_json() {
  python3 -c "
import sys, json
raw = sys.stdin.read()
pos = len(raw) - 1
while pos >= 0:
    pos = raw.rfind('{', 0, pos + 1)
    if pos < 0:
        break
    candidate = raw[pos:]
    try:
        obj = json.loads(candidate)
        print(candidate)
        sys.exit(0)
    except json.JSONDecodeError:
        pass
    pos -= 1
sys.exit(1)
"
}

# Find agent, returns "ip|display_name|emailPrefix"
get_agent_info() {
  local query="$1"
  python3 -c "
import json, sys
with open('$REGISTRY_FILE') as f:
    data = json.load(f)
query = sys.argv[1].lower()
for a in data.get('agents', []):
    if (query in a['name'].lower() or
        query in a.get('redName','').lower() or
        query == a['emailPrefix'].lower()):
        ip = a.get('ip', '')
        display = a['name'] + '(' + a.get('redName','-') + ')'
        prefix = a['emailPrefix']
        if not ip:
            print('NO_IP|' + display + '|' + prefix)
        else:
            print(ip + '|' + display + '|' + prefix)
        sys.exit(0)
print('NOT_FOUND')
sys.exit(1)
" "$query"
}

gw_call() {
  local ip="$1" token="$2" method="$3" params="$4"
  openclaw gateway call \
    --url "ws://${ip}:18789" \
    --token "$token" \
    "$method" \
    --params "$params" \
    2>/dev/null | extract_json
}

ws_send() {
  local ip="$1" token="$2" message="$3" session="${4:-main}"
  local key params result
  key=$(python3 -c "import secrets; print(secrets.token_hex(16))")
  params=$(python3 -c "
import json, sys
print(json.dumps({
  'message': sys.argv[1],
  'sessionKey': sys.argv[2],
  'idempotencyKey': sys.argv[3]
}))
" "$message" "$session" "$key")

  result=$(gw_call "$ip" "$token" chat.send "$params")
  python3 -c "
import json, sys
try:
    d = json.loads(sys.argv[1])
    print(d.get('runId',''))
except:
    print('')
" "$result"
}

ws_wait() {
  local ip="$1" token="$2" run_id="$3" timeout_ms="${4:-60000}"
  local result
  result=$(gw_call "$ip" "$token" agent.wait \
    "{\"runId\":\"$run_id\",\"timeoutMs\":$timeout_ms}")
  python3 -c "
import json, sys
try:
    d = json.loads(sys.argv[1])
    if d.get('status') == 'ok':
        print(d.get('endedAt', ''))
    else:
        print('')
except:
    print('')
" "$result"
}

ws_get_reply() {
  local ip="$1" token="$2" prev_ts="$3" session="${4:-main}"
  local result
  result=$(gw_call "$ip" "$token" chat.history \
    "{\"sessionKey\":\"$session\",\"limit\":10}")
  python3 -c "
import json, sys
prev_ts = int(sys.argv[1].strip().split('\n')[0]) if sys.argv[1].strip() else 0
try:
    d = json.loads(sys.argv[2])
    msgs = d.get('messages', [])
    for m in reversed(msgs):
        if m.get('role') != 'assistant':
            continue
        ts = m.get('timestamp', m.get('createdAt', 0)) or 0
        if prev_ts and ts and ts <= prev_ts:
            continue
        content = m.get('content', [])
        if isinstance(content, list):
            for c in content:
                if c.get('type') == 'text' and c['text'].strip():
                    print(c['text'])
                    sys.exit(0)
        elif isinstance(content, str) and content.strip():
            print(content)
            sys.exit(0)
except Exception as e:
    pass
" "$prev_ts" "$result"
}

ws_last_assistant_ts() {
  local ip="$1" token="$2" session="${3:-main}"
  local result
  result=$(gw_call "$ip" "$token" chat.history \
    "{\"sessionKey\":\"$session\",\"limit\":5}")
  python3 -c "
import json, sys
try:
    d = json.loads(sys.argv[1])
    msgs = d.get('messages', [])
    for m in reversed(msgs):
        if m.get('role') == 'assistant':
            print(m.get('timestamp', m.get('createdAt', 0)) or 0)
            sys.exit(0)
    print(0)
except:
    print(0)
" "$result"
}

im_fallback() {
  local email_prefix="$1" message="$2"
  if [[ ! -f "$IM_FALLBACK_SCRIPT" ]]; then
    echo "  ⚠️  im-fallback skill not installed, cannot fallback"
    return 1
  fi
  python3 "$IM_FALLBACK_SCRIPT" \
    --to "${email_prefix}@${EMAIL_DOMAIN}" \
    --msg "[agent-mesh fallback] $message" 2>/dev/null \
    && echo "  📨 Sent via IM" || echo "  ❌ IM also failed"
}

# ── Command implementations ────────────────────────────────────────

cmd_whoami() {
  if [[ -z "$MY_EMAIL_PREFIX" ]]; then
    echo "❌ Cannot auto-detect local email prefix"
    echo ""
    echo "Make sure one of these is readable:"
    echo "  1. Set MESH_MY_EMAIL=alice@example.com"
    echo "  2. ~/.openclaw/workspace/USER.md contains 'email: alice@example.com'"
    echo "  3. ~/sso.json contains user.email field"
    return 1
  fi
  echo "Identified as: $MY_EMAIL_PREFIX"
  # Show matching record in registry.json
  python3 << EOF
import json
try:
    with open("$REGISTRY_FILE") as f:
        data = json.load(f)
    for a in data['agents']:
        if a['emailPrefix'] == "$MY_EMAIL_PREFIX":
            print(f"Registry entry: {a['name']}({a.get('redName','-')}) | {a.get('ip','?')}")
            import os
            tokens_file = "$TOKENS_FILE"
            if os.path.exists(tokens_file):
                with open(tokens_file) as tf:
                    tokens = json.load(tf).get('tokens', {})
                    if "$MY_EMAIL_PREFIX" in tokens:
                        print(f"Token configured ({tokens['$MY_EMAIL_PREFIX'][:8]}...，{tokens_file}）")
                    else:
                        print(f"⚠️  Token not found in {tokens_file} ")
            else:
                print(f"⚠️  Tokens file not found: {tokens_file}")
            break
    else:
        print(f"⚠️  $MY_EMAIL_PREFIX not in registry.json (edit references/registry.json or implement sync)")
except Exception as e:
    print(f"❌ Read error: {e}")
EOF
}

cmd_list() {
  if [[ -z "$MY_EMAIL_PREFIX" ]]; then
    echo "⚠️  Cannot identify local email prefix (run 'whoami' for help)"
  fi
  python3 -c "
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('$REGISTRY_FILE') as f:
    data = json.load(f)
agents = data.get('agents', [])

tokens = {}
if os.path.exists('$TOKENS_FILE'):
    try:
        tokens = json.load(open('$TOKENS_FILE')).get('tokens', {})
    except: pass

print(f'{len(agents)} agents total\n')

def check(idx_a):
    idx, a = idx_a
    ip = a.get('ip', '')
    has_token = bool(tokens.get(a['emailPrefix']))
    name = f\"{a['name']}（{a.get('redName','-')}）\"
    if not ip:
        return (idx, '⏳ Pending IP', name, ip, not has_token)
    try:
        r = subprocess.run(
            ['curl','-s','-o','/dev/null','-w','%{http_code}',
             f'http://{ip}:18789/', '--connect-timeout','3','--max-time','5'],
            capture_output=True, text=True, timeout=6)
        code = r.stdout.strip()
    except subprocess.TimeoutExpired:
        code = 'timeout'
    status = '✅ Online      ' if code == '200' else f'❌ Unreachable({code})'
    return (idx, status, name, ip, not has_token)

results = [None] * len(agents)
with ThreadPoolExecutor(max_workers=len(agents)) as ex:
    futs = {ex.submit(check, (i, a)): i for i, a in enumerate(agents)}
    for f in as_completed(futs):
        idx, status, name, ip, no_token = f.result()
        results[idx] = (status, name, ip, no_token)

for status, name, ip, no_token in results:
    token_warn = '  ⚠️  token unset' if no_token else ''
    print(f'  {status}  {name} | {ip or \"?\"}  {token_warn}')
print()
print('Registry doc: https://docs.example.com/doc/YOUR_REGISTRY_DOC_ID_OR_REMOVE')
print('Tokens file: $TOKENS_FILE')
"
}

cmd_ping() {
  local to=""
  while [[ $# -gt 0 ]]; do
    case "$1" in --to) to="$2"; shift 2 ;; *) shift ;; esac
  done
  [[ -z "$to" ]] && { echo "❌ Missing --to"; exit 1; }

  local agent_info ip agent_name email_prefix agent_token code
  agent_info=$(get_agent_info "$to")
  [[ "$agent_info" == "NOT_FOUND" ]] && { echo "❌ Agent not found: $to"; exit 1; }

  ip="${agent_info%%|*}"
  agent_name=$(echo "$agent_info" | cut -d'|' -f2)
  email_prefix=$(echo "$agent_info" | cut -d'|' -f3)
  agent_token=$(get_token_for "$email_prefix" || true)

  if [[ "$ip" == "NO_IP" ]]; then
    echo "⏳ $agent_name — IP not yet registered"
    exit 1
  fi

  echo -n "→ Ping $agent_name ($ip:18789) ... "
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "http://${ip}:18789/" --connect-timeout 5 --max-time 8 2>/dev/null)
  if [[ "$code" == "200" ]]; then
    if [[ -z "$agent_token" ]]; then
      echo "✅ Online (⚠️ token not configured, cannot send)"
    else
      echo "✅ Online"
    fi
  else
    echo "❌ Unreachable (HTTP $code)"
  fi
}

cmd_send() {
  local to="" message="" session="main" rounds=1 timeout=60 dry_run=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --to)      to="$2";      shift 2 ;;
      --message) message="$2"; shift 2 ;;
      --session) session="$2"; shift 2 ;;
      --rounds)  rounds="$2";  shift 2 ;;
      --timeout) timeout="$2"; shift 2 ;;
      --dry-run) dry_run=1;    shift ;;
      *) shift ;;
    esac
  done
  [[ -z "$to" || -z "$message" ]] && { echo "❌ Missing --to or --message"; exit 1; }

  # R3: message size check
  check_message_size "$message" || exit 1

  local agent_info ip agent_name email_prefix agent_token
  agent_info=$(get_agent_info "$to")
  [[ "$agent_info" == "NOT_FOUND" ]] && { echo "❌ Agent not found: $to"; exit 1; }

  ip="${agent_info%%|*}"
  agent_name=$(echo "$agent_info" | cut -d'|' -f2)
  email_prefix=$(echo "$agent_info" | cut -d'|' -f3)
  agent_token=$(get_token_for "$email_prefix" || true)

  # R14: dry-run
  if [[ $dry_run -eq 1 ]]; then
    echo "🧪 DRY RUN — not actually sending"
    echo "  Target: $agent_name ($email_prefix)"
    echo "  IP: ${ip}:18789"
    echo "  Token: $([ -n "$agent_token" ] && echo "${agent_token:0:8}..." || echo "unset")"
    echo "  Session: $session"
    echo "  Rounds: $rounds"
    echo "  Timeout: ${timeout}s"
    echo "  Message ($(printf "%s" "$message" | wc -c) bytes):"
    echo "    $message"
    exit 0
  fi

  if [[ "$ip" == "NO_IP" ]]; then
    echo "⚠️  $agent_name has no IP, attempting IM fallback..."
    im_fallback "$email_prefix" "$message"
    exit $?
  fi

  if [[ -z "$agent_token" ]]; then
    echo "⚠️  $agent_name token not configured"
    echo "    Check that $TOKENS_FILE contains $email_prefix"
    exit 1
  fi

  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://${ip}:18789/" --connect-timeout 3 --max-time 5 2>/dev/null)
  if [[ "$code" != "200" ]]; then
    echo "⚠️  $agent_name unreachable (HTTP $code), attempting IM fallback..."
    im_fallback "$email_prefix" "$message"
    exit $?
  fi

  echo "→ Sending to: $agent_name"
  echo "→ Message: $message"
  echo ""

  local current_message="$message"
  for ((r=1; r<=rounds; r++)); do
    [[ $rounds -gt 1 ]] && echo "── Round $r ──"

    local run_id prev_ts
    prev_ts=$(ws_last_assistant_ts "$ip" "$agent_token" "$session")
    run_id=$(ws_send "$ip" "$agent_token" "$current_message" "$session")
    if [[ -z "$run_id" ]]; then
      echo "❌ Round $r send failed (no runId)"
      exit 1
    fi
    echo "⏳ Waiting for reply (runId: $run_id, timeout: ${timeout}s)..."

    local ended_at
    ended_at=$(ws_wait "$ip" "$agent_token" "$run_id" $((timeout * 1000)))
    if [[ -z "$ended_at" ]]; then
      echo "⚠️  Timeout or remote agent did not respond"
      break
    fi

    local reply
    reply=$(ws_get_reply "$ip" "$agent_token" "$prev_ts" "$session")
    if [[ -n "$reply" ]]; then
      echo "💬 $agent_name:"
      echo "$reply"
      echo ""
      current_message="$reply"
    else
      echo "⚠️  Message delivered (endedAt: $ended_at), but no reply text retrieved"
      break
    fi
  done
}

cmd_broadcast() {
  local message="" timeout=60 dry_run=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --message) message="$2"; shift 2 ;;
      --timeout) timeout="$2"; shift 2 ;;
      --dry-run) dry_run=1;    shift ;;
      *) shift ;;
    esac
  done
  [[ -z "$message" ]] && { echo "❌ Missing --message"; exit 2; }
  [[ -z "$MY_EMAIL_PREFIX" ]] && { echo "❌ Cannot identify local email prefix (run './agent-mesh.sh whoami' to debug). Aborting broadcast to avoid sending to self."; exit 1; }

  # R3: message size check
  check_message_size "$message" || exit 1

  echo "📢 Broadcast from: $MY_EMAIL_PREFIX"
  echo "📢 Message: $message"
  [[ $dry_run -eq 1 ]] && echo "🧪 DRY RUN — not actually sending"
  echo ""

  # R17: Collect recipients first, then send concurrently, output atomically
  python3 -c "
import json, os
with open('$REGISTRY_FILE') as f:
    data = json.load(f)
tokens = {}
if os.path.exists('$TOKENS_FILE'):
    try:
        tokens = json.load(open('$TOKENS_FILE')).get('tokens', {})
    except: pass

for a in data.get('agents', []):
    if a['emailPrefix'] == '$MY_EMAIL_PREFIX':
        continue
    ip = a.get('ip','')
    token = tokens.get(a['emailPrefix'], '')
    name = a['name'] + '(' + a.get('redName','-') + ')'
    print(f'{ip}|{name}|{a[\"emailPrefix\"]}|{token}')
" | while IFS='|' read -r ip agent_name email_prefix agent_token; do
    if [[ $dry_run -eq 1 ]]; then
      [[ -z "$ip" ]] && { echo "  ⏳ $agent_name (IPpending，skipping)"; continue; }
      [[ -z "$agent_token" ]] && { echo "  ⚠️  $agent_name (tokenunset，skipping)"; continue; }
      echo "  📨 $agent_name ($ip)"
      continue
    fi
    {
      out="  → $agent_name ... "
      if [[ -z "$ip" ]]; then
        echo "${out}⏳ IP not registered, skipping"
        exit 0
      fi
      if [[ -z "$agent_token" ]]; then
        echo "${out}⚠️  token not configured, skipping"
        exit 0
      fi
      code=$(curl -s -o /dev/null -w "%{http_code}" "http://${ip}:18789/" \
        --connect-timeout 3 --max-time 5 2>/dev/null)
      if [[ "$code" != "200" ]]; then
        echo "${out}❌ Unreachable ($code)"
        exit 0
      fi
      prev_ts=$(ws_last_assistant_ts "$ip" "$agent_token" "main")
      run_id=$(ws_send "$ip" "$agent_token" "$message" "main")
      if [[ -z "$run_id" ]]; then
        echo "${out}❌ Send failed"
        exit 0
      fi
      ended_at=$(ws_wait "$ip" "$agent_token" "$run_id" $((timeout * 1000)))
      if [[ -z "$ended_at" ]]; then
        echo "${out}⚠️  Timeout"
        exit 0
      fi
      reply=$(ws_get_reply "$ip" "$agent_token" "$prev_ts" "main")
      if [[ -n "$reply" ]]; then
        # R17: single echo to prevent interleaving
        printf "%s✅\n    💬 %s\n" "$out" "$(echo "$reply" | head -3 | tr '\n' ' ')"
      else
        echo "${out}✅ Delivered"
      fi
    } &
  done
  wait
  echo ""
  [[ $dry_run -eq 1 ]] && echo "📢 DRY RUN complete" || echo "📢 Broadcast complete"
}

cmd_sync() {
  echo "❌ sync command is not implemented in the open-source version."
  echo ""
  echo "The original version pulls from a shared wiki table via internal CLI."
  echo "For your team, choose one:"
  echo "  1. Maintain references/registry.json manually (simplest)"
  echo "  2. Wire your own sync logic (Notion/Confluence/Google Sheets/Git)"
  echo "  3. Edit this function in scripts/agent-mesh.sh to fetch from your source"
  echo ""
  echo "Registry schema (references/registry.json):"
  echo '  {"agents": [{"name":"Alice", "emailPrefix":"alice", "ip":"10.0.0.1", "hostname":"...", "note":"..."}]}'
  exit 1
}

# ── Main entry ─────────────────────────────────────────────────────

case "${1:-help}" in
  list)      cmd_list ;;
  ping)      shift; cmd_ping "$@" ;;
  send)      shift; cmd_send "$@" ;;
  broadcast) shift; cmd_broadcast "$@" ;;
  sync)      cmd_sync ;;
  whoami)    cmd_whoami ;;
  help|--help|-h) usage ;;
  *) echo "Unknown command: $1"; usage; exit 1 ;;
esac
