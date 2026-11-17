#!/usr/bin/env bash
# Stop hook: surface unread Decent-mesh messages back to Claude, once each.
# - respects stop_hook_active (no infinite loop)
# - marks messages read so they don't re-surface every turn
# - silent + exit 0 when the inbox is empty (lets the turn end normally)
set -euo pipefail

input=$(cat 2>/dev/null || true)

# find node (nvm/homebrew/system) without relying on PATH
NODE=""
for c in node /usr/local/bin/node /opt/homebrew/bin/node "$HOME"/.nvm/versions/node/*/bin/node; do
  if command -v "$c" >/dev/null 2>&1; then NODE=$(command -v "$c"); break; fi
  [ -x "$c" ] && { NODE="$c"; break; }
done
[ -z "$NODE" ] && exit 0   # no node → can't check; don't block the turn

# respect stop_hook_active to avoid re-triggering in a loop
active=$(printf '%s' "$input" | "$NODE" -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{console.log(JSON.parse(s).stop_hook_active===true?"1":"0")}catch{console.log("0")}})' 2>/dev/null || echo 0)
[ "$active" = "1" ] && exit 0

# AGENT_NAME defaults to "agent"; export it in your environment to name this role.
# The mesh CLI lives next to this hook — resolve its path portably.
HERE=$(cd "$(dirname "$0")" && pwd)
msgs=$(AGENT_NAME="${AGENT_NAME:-agent}" "$NODE" "$HERE/mesh" inbox 2>/dev/null || true)
case "$msgs" in
  ""|*"inbox empty"*) exit 0 ;;
esac

# block the stop and hand the message content back to Claude
printf '%s' "$msgs" | "$NODE" -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{process.stdout.write(JSON.stringify({decision:"block",reason:"📨 Incoming Decent-mesh message(s) — reply via `mesh send <userid> \"...\"`:\n\n"+s}))})'
exit 0
