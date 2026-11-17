#!/usr/bin/env bash
# verify_setup.sh — Check all prerequisites for Apple Music DJ
# Run this once after install to verify everything is ready.

set -euo pipefail

# Testing hook: APPLE_MUSIC_API_BASE may point at a local mock server (tests/mock_api.py).
# Loopback addresses only, so real tokens can never be sent to another host.
BASE="https://api.music.apple.com"
if [[ -n "${APPLE_MUSIC_API_BASE:-}" ]]; then
    if [[ "$APPLE_MUSIC_API_BASE" =~ ^http://(127\.0\.0\.1|localhost)(:[0-9]+)?$ ]]; then
        BASE="$APPLE_MUSIC_API_BASE"
    else
        echo "ERROR: APPLE_MUSIC_API_BASE must be http://127.0.0.1[:port] or http://localhost[:port]" >&2
        exit 1
    fi
fi

# The token check below writes the tokens into a temporary curl config (mode 600). Remove those
# files however we exit — including Ctrl-C or `kill` mid-request. Names carry this script's pid,
# so the cleanup only ever touches this run's files.
# shellcheck disable=SC2317,SC2329  # invoked via the traps below (older ShellCheck says 2317, newer 2329)
_cleanup() {
    if [[ -n "${_CURL_PID:-}" ]]; then
        kill "$_CURL_PID" 2>/dev/null || true
    fi
    rm -f "${TMPDIR:-/tmp}"/am_verify_$$_* 2>/dev/null || true
}
_CURL_PID=""
trap _cleanup EXIT
trap '_cleanup; exit 130' INT
trap '_cleanup; exit 143' TERM

# _http_status <curl-config> <url> — sets HTTP_CODE ("000" on failure). curl runs in the
# background and we `wait` for it: bash defers traps until a foreground command finishes, so a
# plain `$(curl ...)` would ignore Ctrl-C/TERM until the request ended.
HTTP_CODE="000"
_http_status() {
    local cfg="$1" url="$2" out rc=0
    out=$(mktemp "${TMPDIR:-/tmp}/am_verify_$$_XXXXXX")
    curl -s -o /dev/null -w "%{http_code}" --max-time 20 -K "$cfg" "$url" > "$out" 2>/dev/null &
    _CURL_PID=$!
    wait "$_CURL_PID" || rc=$?
    if (( rc >= 128 )); then
        _cleanup
        exit "$rc"
    fi
    _CURL_PID=""
    HTTP_CODE=$(cat "$out" 2>/dev/null || true)
    [[ -n "$HTTP_CODE" ]] || HTTP_CODE="000"
    rm -f "$out"
}

PASS="✅"
FAIL="❌"
WARN="⚠️"
errors=0
warnings=0

echo "🎧 Apple Music DJ — Setup Verification"
echo "========================================"
echo ""

# ── Required binaries ──────────────────────────────────────

echo "Checking required tools..."

for bin in curl jq python3; do
    if command -v "$bin" &>/dev/null; then
        version=$("$bin" --version 2>&1 | head -1)
        echo "  $PASS $bin — $version"
    else
        echo "  $FAIL $bin — NOT FOUND"
        errors=$((errors + 1))
    fi
done

echo ""

# ── Python version check ──────────────────────────────────

echo "Checking Python version..."
py_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "  $PASS Python $py_version (≥ 3.10 required)"
else
    echo "  $FAIL Python $py_version (≥ 3.10 required)"
    errors=$((errors + 1))
fi

echo ""

# ── Optional: PyJWT (only for token generation) ───────────

echo "Checking optional dependencies..."
if python3 -c "import jwt" 2>/dev/null; then
    echo "  $PASS PyJWT — installed (needed for token generation)"
else
    echo "  $WARN PyJWT — not installed (only needed if generating dev tokens locally)"
    echo "       Install with: pip3 install PyJWT"
    warnings=$((warnings + 1))
fi

echo ""

# ── Environment variables ─────────────────────────────────

echo "Checking environment variables..."

if [[ -n "${APPLE_MUSIC_DEV_TOKEN:-}" ]]; then
    echo "  $PASS APPLE_MUSIC_DEV_TOKEN — set"
else
    echo "  $FAIL APPLE_MUSIC_DEV_TOKEN — NOT SET"
    echo "       Set up both tokens in one step: python3 scripts/setup_auth.py"
    echo "       Or try the skill first with no tokens: python3 scripts/demo.py tour"
    errors=$((errors + 1))
fi

if [[ -n "${APPLE_MUSIC_USER_TOKEN:-}" ]]; then
    token_len=${#APPLE_MUSIC_USER_TOKEN}
    echo "  $PASS APPLE_MUSIC_USER_TOKEN — set ($token_len chars)"
else
    echo "  $FAIL APPLE_MUSIC_USER_TOKEN — NOT SET"
    echo "       Set it up with: python3 scripts/setup_auth.py (see references/auth-setup.md)"
    errors=$((errors + 1))
fi

if [[ -n "${APPLE_MUSIC_STOREFRONT:-}" ]]; then
    echo "  $PASS APPLE_MUSIC_STOREFRONT — ${APPLE_MUSIC_STOREFRONT} (override)"
else
    echo "  $WARN APPLE_MUSIC_STOREFRONT — not set (will auto-detect)"
fi

echo ""

# ── Dev token expiry check ────────────────────────────────

echo "Checking dev token expiry..."

if [[ -n "${APPLE_MUSIC_DEV_TOKEN:-}" ]]; then
    # JWT is header.payload.signature — decode the payload (middle segment)
    jwt_payload=$(echo "$APPLE_MUSIC_DEV_TOKEN" | cut -d. -f2)
    # Add base64 padding
    padding=$(( 4 - ${#jwt_payload} % 4 ))
    [[ "$padding" -lt 4 ]] && jwt_payload="${jwt_payload}$(printf '=%.0s' $(seq 1 $padding))"

    exp_ts=$(echo "$jwt_payload" | base64 -d 2>/dev/null | jq -r '.exp // empty' 2>/dev/null || true)

    if [[ -n "$exp_ts" && "$exp_ts" =~ ^[0-9]+$ ]]; then
        now_ts=$(date +%s)
        remaining=$(( exp_ts - now_ts ))
        days_remaining=$(( remaining / 86400 ))

        if [[ "$remaining" -le 0 ]]; then
            echo "  $FAIL Dev token has EXPIRED!"
            echo "       Regenerate with: python3 scripts/setup_auth.py --new-dev-token"
            errors=$((errors + 1))
        elif [[ "$days_remaining" -le 14 ]]; then
            echo "  $WARN Dev token expires in ${days_remaining} day(s) — consider regenerating soon"
            echo "       Regenerate with: python3 scripts/setup_auth.py --new-dev-token"
            warnings=$((warnings + 1))
        else
            echo "  $PASS Dev token valid for ${days_remaining} more day(s)"
        fi
    else
        echo "  $WARN Could not decode token expiry — skipping check"
        warnings=$((warnings + 1))
    fi
else
    echo "  $WARN Skipped — APPLE_MUSIC_DEV_TOKEN not set"
fi

echo ""

# ── User token age ────────────────────────────────────────
# The user token carries no expiry, so _common records (by fingerprint) when it was first seen.

echo "Checking user token age..."

if [[ -n "${APPLE_MUSIC_USER_TOKEN:-}" ]]; then
    age_json=$(AMDJ_SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" python3 -c '
import json, os, sys
sys.path.insert(0, os.environ["AMDJ_SCRIPTS"])
from _common import check_user_token_age
print(json.dumps(check_user_token_age()))' 2>/dev/null || echo null)
    age_msg=$(jq -r '.message // empty' <<< "$age_json" 2>/dev/null || true)
    if [[ -z "$age_msg" ]]; then
        echo "  $WARN Could not track the user token's age — skipping check"
    elif [[ "$(jq -r '.warning' <<< "$age_json")" == "true" ]]; then
        echo "  $WARN ${age_msg#⚠️  }"
        warnings=$((warnings + 1))
    else
        echo "  $PASS ${age_msg#✅ }"
    fi
else
    echo "  $WARN Skipped — APPLE_MUSIC_USER_TOKEN not set"
fi

echo ""

# ── Script files ──────────────────────────────────────────

echo "Checking scripts..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

expected_scripts=(
    "apple_music_api.sh"
    "taste_profiler.py"
    "build_playlist.sh"
    "generate_dev_token.py"
    "taste_card.py"
    "compatibility.py"
    "listening_insights.py"
    "catalog_explorer.py"
    "daily_pick.py"
    "concert_prep.sh"
    "new_releases.sh"
    "playlist_health.py"
    "playlist_history.py"
    "strategy_engine.py"
    "setup_cron.py"
    "setup_auth.py"
    "demo.py"
    "verify_setup.sh"
)

for script in "${expected_scripts[@]}"; do
    if [[ -f "$SCRIPT_DIR/$script" ]]; then
        echo "  $PASS $script"
    else
        echo "  $FAIL $script — MISSING"
        errors=$((errors + 1))
    fi
done

echo ""

# ── API connectivity ──────────────────────────────────────

echo "Checking API connectivity..."

if [[ -n "${APPLE_MUSIC_DEV_TOKEN:-}" && -n "${APPLE_MUSIC_USER_TOKEN:-}" ]]; then
    # Verify dev token
    echo "  Verifying dev token against API..." >&2
    auth_cfg=$(mktemp "${TMPDIR:-/tmp}/am_verify_$$_XXXXXX")
    chmod 600 "$auth_cfg"
    printf -- '-H "Authorization: Bearer %s"\n' "$APPLE_MUSIC_DEV_TOKEN" > "$auth_cfg"
    _http_status "$auth_cfg" "${BASE}/v1/storefronts/us"
    dev_code="$HTTP_CODE"
    rm -f "$auth_cfg"

    case "$dev_code" in
        200)
            echo "  $PASS Dev token — valid (HTTP $dev_code)"
            ;;
        401)
            echo "  $FAIL Dev token — invalid or expired (HTTP 401)"
            echo "       Regenerate with: python3 scripts/setup_auth.py --new-dev-token"
            errors=$((errors + 1))
            ;;
        *)
            echo "  $WARN Dev token — unexpected response (HTTP $dev_code)"
            warnings=$((warnings + 1))
            ;;
    esac

    # Verify user token
    echo "  Verifying user token against API..." >&2
    auth_cfg=$(mktemp "${TMPDIR:-/tmp}/am_verify_$$_XXXXXX")
    chmod 600 "$auth_cfg"
    printf -- '-H "Authorization: Bearer %s"\n-H "Music-User-Token: %s"\n' \
        "$APPLE_MUSIC_DEV_TOKEN" "$APPLE_MUSIC_USER_TOKEN" > "$auth_cfg"
    _http_status "$auth_cfg" "${BASE}/v1/me/recent/played/tracks?limit=1"
    user_code="$HTTP_CODE"
    rm -f "$auth_cfg"

    case "$user_code" in
        200)
            echo "  $PASS User token — valid (HTTP $user_code)"
            ;;
        401)
            echo "  $FAIL Dev token rejected by personalized endpoint (HTTP 401)"
            errors=$((errors + 1))
            ;;
        403)
            echo "  $FAIL User token expired (HTTP 403)"
            echo "       Renew it: python3 scripts/setup_auth.py"
            errors=$((errors + 1))
            ;;
        429)
            echo "  $WARN Rate limited (HTTP 429) — API is reachable, try again shortly"
            warnings=$((warnings + 1))
            ;;
        000)
            echo "  $FAIL Network error — cannot reach api.music.apple.com"
            errors=$((errors + 1))
            ;;
        *)
            echo "  $WARN Unexpected response (HTTP $user_code)"
            warnings=$((warnings + 1))
            ;;
    esac
else
    echo "  $WARN Skipped — tokens not set"
fi

echo ""

# ── Cache & config status ─────────────────────────────────

echo "Checking cache..."

cache_file="${HOME}/.apple-music-dj/taste_profile.json"
if [[ -f "$cache_file" ]]; then
    cache_size=$(wc -c < "$cache_file" | tr -d ' ')
    cache_mod=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$cache_file" 2>/dev/null || { stat -c "%y" "$cache_file" 2>/dev/null | cut -d. -f1; })
    echo "  $PASS Taste profile cached ($cache_size bytes, last modified: $cache_mod)"
else
    echo "  $WARN No cached taste profile yet"
    echo "       Run: python3 scripts/taste_profiler.py"
fi

sf_cache="${HOME}/.apple-music-dj/storefront.cache"
if [[ -f "$sf_cache" ]]; then
    sf_val=$(tr -d '[:space:]' < "$sf_cache")
    echo "  $PASS Storefront cached: $sf_val"
else
    echo "  $WARN No storefront cache (will auto-detect on first run)"
fi

config_file="${HOME}/.apple-music-dj/config.json"
if [[ -f "$config_file" ]]; then
    echo "  $PASS User config found: $config_file"
else
    echo "  $WARN No user config (optional). Create ~/.apple-music-dj/config.json to set defaults."
fi

echo ""

# ── Summary ───────────────────────────────────────────────

echo "========================================"
if [[ $errors -eq 0 && $warnings -eq 0 ]]; then
    echo "$PASS All checks passed! You're ready to go."
elif [[ $errors -eq 0 ]]; then
    echo "$WARN All critical checks passed ($warnings warning(s))"
else
    echo "$FAIL $errors error(s), $warnings warning(s)"
    echo "  Fix the issues above before using the skill."
fi

exit $errors
