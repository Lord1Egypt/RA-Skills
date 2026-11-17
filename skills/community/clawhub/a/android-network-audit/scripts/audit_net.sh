#!/usr/bin/env bash
# android-network-audit: READ-ONLY network exposure audit for Termux/Android.
#
# This script NEVER modifies the system, network, proxy, or any config.
# It only inspects and prints findings. If a tool is missing it falls back to
# /proc where possible and reports what it could not read.
#
# No secrets are printed. Credentials found in env/config are masked.
#
# Usage:
#   ./audit_net.sh            # full read-only checklist
#   ./audit_net.sh --json     # machine-readable summary
set -uo pipefail

JSON=0
[ "${1:-}" = "--json" ] && JSON=1

log() { [ "$JSON" = 0 ] && echo "$@"; }
kv()  { [ "$JSON" = 1 ] && printf '%s' "$2" || printf '%-18s %s\n' "$1" "$2"; }

PLATFORM="UNKNOWN"
if [[ "${PREFIX:-} ${HOME:-}" == *com.termux* ]]; then
  PLATFORM="TERMUX"
elif [[ "$(uname -s 2>/dev/null)" == "Linux" ]]; then
  PLATFORM="ANDROID_RESTRICTED"
fi

# 1. Connectivity (brief ping, read-only)
CONN="FAILED"
if command -v ping >/dev/null 2>&1; then
  if ping -c1 -W3 8.8.8.8 >/dev/null 2>&1 || ping -c1 -W3 1.1.1.1 >/dev/null 2>&1; then
    CONN="OK"
  fi
fi

# 2. Interface / IP
INTERFACES=""
if command -v ip >/dev/null 2>&1; then
  INTERFACES=$(ip -o addr show 2>/dev/null | awk '{print $2, $4}' | tr '\n' ';')
elif command -v ifconfig >/dev/null 2>&1; then
  INTERFACES=$(ifconfig 2>/dev/null | grep -E 'inet ' | tr '\n' ';')
elif [ -r /proc/net/fib_trie ]; then
  INTERFACES="(fallback /proc/net/fib_trie present)"
fi

# 3. DNS
DNS=""
[ -r /etc/resolv.conf ] && DNS=$(grep -E '^(nameserver|search)' /etc/resolv.conf 2>/dev/null | tr '\n' ';')
for p in net.dns1 net.dns2; do
  v=$(getprop "$p" 2>/dev/null)
  [ -n "$v" ] && DNS="${DNS}${p}=${v};"
done

# 4. Proxy (values masked: only host:port shown, never credentials)
PROXY=""
env | grep -iE 'proxy' | while IFS='=' read -r k v; do
  # mask anything that looks like a credential
  echo "  $k=$(echo "$v" | sed -E 's#(://[^:@/]+:)[^@/]+@#\1****@#')"
done >/dev/null
PROXY_RAW=$(env | grep -iE 'proxy' | wc -l | tr -d ' ')
PROXY="${PROXY_RAW} proxy var(s) in env; values masked"

# 5. Listening ports (flag 0.0.0.0 / :: as exposed)
PORTS=""
RISK="LOW"
if command -v ss >/dev/null 2>&1; then
  PORTS=$(ss -tulpen 2>/dev/null | grep -E 'LISTEN' | tr '\n' '|')
elif command -v netstat >/dev/null 2>&1; then
  PORTS=$(netstat -tulpen 2>/dev/null | grep -E 'LISTEN' | tr '\n' '|')
else
  PORTS=$( ( [ -r /proc/net/tcp ] && echo "fallback /proc/net/tcp"; ) 2>/dev/null)
fi
if echo "$PORTS" | grep -qE '0\.0\.0\.0|:::' ; then
  RISK="MEDIUM"
fi

# Report
if [ "$JSON" = 1 ]; then
  printf '{'
  printf '"platform":"%s",' "$PLATFORM"
  printf '"connectivity":"%s",' "$CONN"
  printf '"dns":"%s",' "$DNS"
  printf '"proxy":"%s",' "$PROXY"
  printf '"interfaces":"%s",' "$INTERFACES"
  printf '"listening_ports":"%s",' "$PORTS"
  printf '"exposure_risk":"%s"' "$RISK"
  printf '}\n'
else
  echo "NETWORK AUDIT"
  kv "Platform:" "$PLATFORM"
  kv "Connectivity:" "$CONN"
  kv "DNS:" "${DNS:-<none>}"
  kv "Proxy:" "$PROXY"
  kv "Interfaces:" "${INTERFACES:-<none>}"
  kv "Listening Ports:" "${PORTS:-<none>}"
  kv "Exposure Risk:" "$RISK"
  echo
  echo "Recommendation: this is a READ-ONLY report. Do not change config without explicit user request."
fi
