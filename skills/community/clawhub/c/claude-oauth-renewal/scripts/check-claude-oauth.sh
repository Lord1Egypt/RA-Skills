#!/usr/bin/env bash
# Claude Code OAuth Token Health Check + Auto-Renewal
# For OpenClaw heartbeat integration
#
# Flow:
#   1. Read token expiry from macOS Keychain
#   2. Healthy (>WARN_HOURS) → silent exit
#   3. Expiring/expired → claude auth status (refresh token)
#   4. Refresh fails → claude auth login + Chrome auto-Authorize + extract code + feed to CLI
#   5. All fail → output alert for agent to relay to user
#
# Dependencies: python3, security (macOS Keychain), expect, osascript (Chrome JXA)
# Prerequisite: Chrome → View → Developer → Allow JavaScript from Apple Events
#
# Usage: bash check-claude-oauth.sh
# Env:   WARN_HOURS=6 (default, hours before expiry to trigger renewal)

set -euo pipefail

WARN_HOURS=${WARN_HOURS:-6}
KEYCHAIN_SERVICE="Claude Code-credentials"
KEYCHAIN_ACCOUNT="$(whoami)"
AUTH_TIMEOUT=30

# --- Utility functions ---

get_expires_at() {
  security find-generic-password -s "$KEYCHAIN_SERVICE" -a "$KEYCHAIN_ACCOUNT" -g 2>&1 | \
    python3 -c "
import sys, re
m = re.search(r'\"expiresAt\"\s*:\s*(\d+)', sys.stdin.read())
print(m.group(1) if m else '0')
" 2>/dev/null || echo "0"
}

now_ms() { python3 -c "import time; print(int(time.time()*1000))"; }

format_time() {
  python3 -c "import datetime; print(datetime.datetime.fromtimestamp($1/1000).strftime('%m-%d %H:%M'))"
}

# --- Click Authorize button in Chrome auth page ---
click_authorize_in_chrome() {
  osascript -l JavaScript -e '
function run() {
  const chrome = Application("Google Chrome");
  const windows = chrome.windows();
  for (const w of windows) {
    const tabs = w.tabs();
    for (let i = 0; i < tabs.length; i++) {
      const url = tabs[i].url();
      if (url.includes("claude.ai/oauth/authorize")) {
        try {
          const res = tabs[i].execute({javascript:
            "(() => { const btns = document.querySelectorAll(\"button\"); for (const b of btns) { if (b.textContent.trim() === \"Authorize\") { b.click(); return \"clicked\"; } } return \"no_button\"; })()"
          });
          if (res === "clicked") return "clicked";
        } catch(e) {
          return "js_error:" + e.message;
        }
      }
    }
  }
  return "no_tab";
}
' 2>/dev/null || echo "osascript_error"
}

# --- Extract auth code from Chrome callback page ---
extract_code_from_chrome() {
  osascript -l JavaScript -e '
function run() {
  const chrome = Application("Google Chrome");
  const windows = chrome.windows();
  for (const w of windows) {
    const tabs = w.tabs();
    for (let i = 0; i < tabs.length; i++) {
      const url = tabs[i].url();
      if (url.includes("platform.claude.com/oauth/code/callback")) {
        try {
          const code = tabs[i].execute({javascript:
            "(() => { const el = document.querySelector(\".font-mono, [class*=code], code, pre\"); return el ? el.textContent.trim() : \"no_element\"; })()"
          });
          return code || "no_code";
        } catch(e) {
          return "js_error:" + e.message;
        }
      }
    }
  }
  return "no_tab";
}
' 2>/dev/null || echo "osascript_error"
}

# --- Full browser auto-authorization flow ---
auto_authorize() {
  local auth_code=""

  # 1. Start auth login with PTY (via script command)
  script -q /tmp/claude-auth-pty.log claude auth login &>/dev/null &
  local login_pid=$!

  # 2. Wait for browser to open
  sleep 5

  # 3. Click Authorize
  local click_result=""
  for attempt in $(seq 1 $AUTH_TIMEOUT); do
    click_result=$(click_authorize_in_chrome)
    case "$click_result" in
      clicked) break ;;
      *) sleep 1 ;;
    esac
  done

  if [ "$click_result" != "clicked" ]; then
    kill "$login_pid" 2>/dev/null || true
    return 1
  fi

  # 4. Wait for callback page and extract code
  sleep 3
  auth_code=""
  for attempt in $(seq 1 10); do
    auth_code=$(extract_code_from_chrome)
    case "$auth_code" in
      no_tab|no_element|no_code|js_error:*|osascript_error)
        sleep 1
        ;;
      *)
        break
        ;;
    esac
  done

  if [ -z "$auth_code" ] || [[ "$auth_code" == no_* ]] || [[ "$auth_code" == *error* ]]; then
    kill "$login_pid" 2>/dev/null || true
    return 1
  fi

  # 5. Kill PTY process, feed code to fresh auth login via expect
  kill "$login_pid" 2>/dev/null || true
  sleep 1

  expect -c "
    set timeout 30
    spawn claude auth login
    expect {
      timeout { exit 1 }
      -re {visit:|browser} {
        sleep 6
      }
    }
    send \"$auth_code\r\"
    expect {
      timeout { exit 1 }
      -re {successful|success|Login} { exit 0 }
    }
  " &>/tmp/claude-auth-expect.log

  local expect_exit=$?

  # 6. Verify token was updated
  if [ $expect_exit -eq 0 ]; then
    sleep 2
    local new_exp
    new_exp=$(get_expires_at)
    local now
    now=$(now_ms)
    if [ "$new_exp" -gt "$now" ] 2>/dev/null; then
      return 0
    fi
  fi

  return 1
}

# === Main logic ===

EXPIRES_AT=$(get_expires_at)
if [ "$EXPIRES_AT" = "0" ]; then
  echo "[OAuth Alert] Cannot read Claude Code token. Please run: claude auth login"
  exit 0
fi

NOW=$(now_ms)
REMAINING_MS=$((EXPIRES_AT - NOW))

# 1. Healthy → silent exit
if [ "$REMAINING_MS" -gt $((WARN_HOURS * 3600000)) ]; then
  exit 0
fi

# 2. Try refresh token
if command -v claude &>/dev/null; then
  claude auth status &>/dev/null || true
  sleep 1
  NEW_EXP=$(get_expires_at)
  if [ "$NEW_EXP" -gt "$EXPIRES_AT" ] 2>/dev/null; then
    exit 0
  fi
fi

# 3. Try browser auto-authorization
if auto_authorize 2>/dev/null; then
  exit 0
fi

# 4. All failed → output alert
EXPIRES_STR=$(format_time "$EXPIRES_AT")
if [ "$REMAINING_MS" -le 0 ]; then
  echo "[OAuth Expired] Claude Code token expired at ${EXPIRES_STR}. Auto-renewal failed. Please run: claude auth login"
else
  REMAINING_HOURS=$((REMAINING_MS / 3600000))
  echo "[OAuth Expiring] Claude Code token expires in ${REMAINING_HOURS}h (${EXPIRES_STR}). Auto-renewal failed. Please run: claude auth login"
fi
