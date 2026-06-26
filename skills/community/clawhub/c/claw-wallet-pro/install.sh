#!/bin/bash
# claw wallet minimal installer for Linux/macOS
# Served at: https://www.clawwallet.cc/skills/install.sh  (curl -fsSL ... | bash)
# Usage: first-time install (wallet init) | upgrade (CLAW_WALLET_SKIP_INIT=1, no wallet init)
set -euo pipefail

# Piped from curl: BASH_SOURCE is "-"; use cwd (user should: mkdir -p skills/claw-wallet && cd skills/claw-wallet)
if [[ "${BASH_SOURCE[0]:-}" == "-" ]]; then
    SCRIPT_DIR="$(pwd -P)"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
cd "$SCRIPT_DIR"

CLAW_WALLET_BASE_URL="${CLAW_WALLET_BASE_URL:-https://www.clawwallet.cc}"

download_skill_bundle() {
    echo "Downloading SKILL.md and wrapper scripts from ${CLAW_WALLET_BASE_URL} ..."
    curl -fsSL "${CLAW_WALLET_BASE_URL}/skills/SKILL.md" -o SKILL.md
    curl -fsSL "${CLAW_WALLET_BASE_URL}/skills/claw-wallet.sh" -o claw-wallet.sh
    curl -fsSL "${CLAW_WALLET_BASE_URL}/skills/claw-wallet" -o claw-wallet
    chmod +x claw-wallet.sh claw-wallet
}

if [[ "${CLAW_WALLET_SKIP_SKILL_DOWNLOAD:-0}" != "1" ]]; then
    download_skill_bundle
fi

OS_TYPE="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH_TYPE="$(uname -m)"

BINARY_NAME="clay-sandbox-linux-amd64"
if [ "$OS_TYPE" = "darwin" ]; then
    if [ "$ARCH_TYPE" = "arm64" ]; then
        BINARY_NAME="clay-sandbox-darwin-arm64"
    else
        BINARY_NAME="clay-sandbox-darwin-amd64"
    fi
fi

BINARY_URL="${CLAW_WALLET_BASE_URL}/bin/${BINARY_NAME}"
BINARY_TARGET="./clay-sandbox"

# --- Common: stop, download, start ---
if [ "${CLAW_WALLET_SKIP_STOP:-0}" != "1" ]; then
    "$SCRIPT_DIR/claw-wallet.sh" stop >/dev/null 2>&1 || true
fi

echo "Downloading sandbox binary from $BINARY_URL ..."
TMP_TARGET="${BINARY_TARGET}.download"
curl -L -o "$TMP_TARGET" "$BINARY_URL"
mv -f "$TMP_TARGET" "$BINARY_TARGET"

chmod +x "$BINARY_TARGET"

"$SCRIPT_DIR/claw-wallet.sh" start

# --- First-time only: wallet init (skipped when upgrade passes CLAW_WALLET_SKIP_INIT=1) ---
read_env_value() {
    local pattern="$1"
    local file="$2"
    awk -F= -v pattern="$pattern" '
        $0 ~ pattern {
            sub(/^[^=]*=/, "", $0)
            gsub(/["\047\r]/, "", $0)
            sub(/[[:space:]]*$/, "", $0)
            print
            exit
        }
    ' "$file" 2>/dev/null || true
}

do_wallet_init() {
    echo "Waiting for sandbox and initializing wallet ..."
    for i in $(seq 1 90); do
        CLAY_SANDBOX_URL=""
        CLAY_AGENT_TOKEN=""
        if [ -f "$SCRIPT_DIR/.env.clay" ]; then
            CLAY_SANDBOX_URL="$(read_env_value '^CLAY_SANDBOX_URL=' "$SCRIPT_DIR/.env.clay")"
            CLAY_AGENT_TOKEN="$(read_env_value '^(CLAY_AGENT_TOKEN|AGENT_TOKEN)=' "$SCRIPT_DIR/.env.clay")"
        fi
        if [ -z "${CLAY_SANDBOX_URL:-}" ]; then
            REASON=".env.clay (CLAY_SANDBOX_URL)"
        elif ! curl -s -f "${CLAY_SANDBOX_URL}/health" 2>/dev/null | grep -qE '"status"[[:space:]]*:[[:space:]]*"ok"'; then
            REASON="health ok at ${CLAY_SANDBOX_URL}"
        elif [ -z "${CLAY_AGENT_TOKEN:-}" ]; then
            REASON="CLAY_AGENT_TOKEN in .env.clay"
        else
            echo "  Calling wallet/init ..."
            if init_resp="$(curl -sS -f -X POST "${CLAY_SANDBOX_URL}/api/v1/wallet/init" \
                -H "Authorization: Bearer ${CLAY_AGENT_TOKEN}" \
                -H "Content-Type: application/json" \
                -d '{}' 2>/dev/null)"; then
                if printf '%s' "$init_resp" | grep -qE '"uid"|"status"'; then
                    echo "Wallet initialized."
                    return 0
                fi
                REASON="wallet/init success payload from ${CLAY_SANDBOX_URL}"
            else
                REASON="wallet/init at ${CLAY_SANDBOX_URL}"
            fi
        fi
        [ "$((i % 10))" -eq 0 ] && echo "  Still waiting for ${REASON} ... (${i}s)"
        sleep 1
    done
    echo "Error: wallet init did not complete after 90s. Check sandbox.log, then run POST {CLAY_SANDBOX_URL}/api/v1/wallet/init manually. See SKILL.md." >&2
    return 1
}

if [ "${CLAW_WALLET_SKIP_INIT:-0}" != "1" ]; then
    do_wallet_init
fi

# --- Common: final messages ---
echo "Check .env.clay for CLAY_SANDBOX_URL and CLAY_AGENT_TOKEN (or AGENT_TOKEN)."
echo "HTTP clients (curl, agents) must call protected APIs with: Authorization: Bearer <same token>."
echo "The same value is duplicated in identity.json as agent_token. See SKILL.md section 'HTTP authentication (sandbox)'."
echo "Sandbox binary refreshed at: $BINARY_TARGET"
