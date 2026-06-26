#!/usr/bin/env bash
# setup.sh — BinanceCoach first-time setup
# Copies bundled source to ~/workspace/binance-coach, installs deps, configures .env
# No internet required — all code is bundled inside this skill.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="${BINANCE_COACH_PATH:-$HOME/workspace/binance-coach}"

echo ""
echo "🤖 BinanceCoach — Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  Before continuing, note what this setup will do:"
echo "   • Copy bundled Python source to ~/workspace/binance-coach/"
echo "   • Run 'pip install' to download dependencies from PyPI (needs internet)"
echo "   • Write your Binance API key + secret to a local .env file"
echo "   • Optionally ask to append a preference to your OpenClaw USER.md"
echo "   • Optionally configure a Telegram bot token (stored locally)"
echo ""
echo "   Nothing is sent externally except to Binance and Telegram APIs"
echo "   when you explicitly use those features."
echo ""
read -rp "   Continue? [Y/n]: " proceed
proceed="${proceed:-Y}"
[[ "${proceed,,}" == "y" ]] || { echo "Setup cancelled."; exit 0; }
echo ""

# ── Install from bundled source ───────────────────────────────────────────────
if [[ -d "$INSTALL_DIR" && -f "$INSTALL_DIR/main.py" ]]; then
    echo "📁 Found existing install at $INSTALL_DIR"
    read -rp "  Reinstall/overwrite? [y/N]: " reinstall
    [[ "${reinstall,,}" != "y" ]] && echo "  Keeping existing install." || {
        echo "📦 Copying bundled source to $INSTALL_DIR..."
        cp -r "$SKILL_DIR/src/." "$INSTALL_DIR/"
        echo "✅ Updated"
    }
else
    echo "📦 Installing BinanceCoach to $INSTALL_DIR..."
    mkdir -p "$INSTALL_DIR"
    cp -r "$SKILL_DIR/src/." "$INSTALL_DIR/"
    echo "✅ Installed"
fi

# ── Python deps ───────────────────────────────────────────────────────────────
echo ""
echo "📦 Installing Python dependencies..."
if pip3 install --break-system-packages -q -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
   pip3 install -q -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
   python3 -m pip install -q -r "$INSTALL_DIR/requirements.txt" 2>/dev/null; then
    echo "✅ Dependencies installed"
else
    echo "⚠️  pip install failed — try manually: pip3 install -r $INSTALL_DIR/requirements.txt"
fi

# ── .env helpers ──────────────────────────────────────────────────────────────
ENV_FILE="$INSTALL_DIR/.env"
[[ ! -f "$ENV_FILE" ]] && touch "$ENV_FILE"

set_env() {
    local key="$1" val="$2"
    if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
        sed -i '' "s|^${key}=.*|${key}=${val}|" "$ENV_FILE"
    else
        echo "${key}=${val}" >> "$ENV_FILE"
    fi
}

prompt_key() {
    local label="$1"
    local val=""
    while [[ -z "$val" ]]; do
        read -rsp "  $label: " val
        echo ""
        [[ -z "$val" ]] && echo "  (required, cannot be empty)"
    done
    echo "$val"
}

# ── API Keys ──────────────────────────────────────────────────────────────────
echo ""
echo "🔑 API Key Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Binance API Keys (read-only)"
echo "   → binance.com → Account → API Management → Create API"
echo "   → Enable 'Enable Reading' ONLY — no trading, no withdrawals"
echo ""
BINANCE_KEY="$(prompt_key "Binance API Key")"
BINANCE_SECRET="$(prompt_key "Binance API Secret")"
set_env "BINANCE_API_KEY" "$BINANCE_KEY"
set_env "BINANCE_API_SECRET" "$BINANCE_SECRET"

# ── Preferences ───────────────────────────────────────────────────────────────
echo ""
echo "2️⃣  Preferences"
echo ""
read -rp "  Monthly DCA budget in USD (default: 500): " budget
budget="${budget:-500}"
set_env "DCA_BUDGET_MONTHLY" "$budget"

read -rp "  Risk profile [conservative/moderate/aggressive] (default: moderate): " risk
risk="${risk:-moderate}"
[[ "$risk" != "conservative" && "$risk" != "aggressive" ]] && risk="moderate"
set_env "RISK_PROFILE" "$risk"

read -rp "  Language [en/nl] (default: en): " lang
lang="${lang:-en}"
[[ "$lang" != "nl" ]] && lang="en"
set_env "LANGUAGE" "$lang"

set_env "AI_MODEL" "claude-haiku-4-5-20251001"

# ── Anthropic (optional) ──────────────────────────────────────────────────────
echo ""
echo "3️⃣  Anthropic API Key"
echo "   ℹ️  Not needed if using via OpenClaw — skip this."
echo "      Only required for the standalone Telegram bot or CLI."
echo ""
read -rp "  Set up Anthropic API key? [y/N]: " setup_anthropic
if [[ "${setup_anthropic,,}" == "y" ]]; then
    ANTHROPIC_KEY="$(prompt_key "Anthropic API Key")"
    set_env "ANTHROPIC_API_KEY" "$ANTHROPIC_KEY"
else
    echo "   ⏭️  Skipped."
fi

# ── Telegram (optional) ───────────────────────────────────────────────────────
echo ""
echo "4️⃣  Telegram Bot"
echo "   ℹ️  Not needed if using via OpenClaw — skip this."
echo "      Only required for a dedicated standalone Telegram bot."
echo ""
read -rp "  Set up standalone Telegram bot? [y/N]: " setup_tg
if [[ "${setup_tg,,}" == "y" ]]; then
    echo "   → Message @BotFather on Telegram: /newbot → copy token"
    echo "   → Your Telegram user ID: message @userinfobot"
    echo ""
    TG_TOKEN="$(prompt_key "Bot Token")"
    TG_UID="$(prompt_key "Your Telegram User ID")"
    set_env "TELEGRAM_BOT_TOKEN" "$TG_TOKEN"
    set_env "TELEGRAM_USER_ID" "$TG_UID"
else
    echo "   ⏭️  Skipped."
fi

# ── Verify Binance connectivity ───────────────────────────────────────────────
echo ""
echo "🔍 Verifying Binance connection..."
cd "$INSTALL_DIR"
python3 -c "
from dotenv import load_dotenv; load_dotenv()
import os
from binance.spot import Spot
try:
    c = Spot(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))
    c.account_status()
    print('✅ Binance connection successful')
except Exception as e:
    print(f'⚠️  Binance check failed: {e}')
    print('   Check your API key and permissions.')
" 2>/dev/null || echo "⚠️  Could not verify — check your keys if commands fail."

# ── Hook into OpenClaw USER.md (with consent) ────────────────────────────────
echo ""
echo "🔗 OpenClaw Integration (optional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   BinanceCoach can register itself as the default handler for all"
echo "   crypto questions in your OpenClaw assistant. This adds a preference"
echo "   block to your USER.md so every future session uses BinanceCoach"
echo "   automatically — without you needing to ask."
echo ""
echo "   What gets added to USER.md:"
echo "   ┌─────────────────────────────────────────────────────────────┐"
echo "   │ ## BinanceCoach (Auto-installed)                            │"
echo "   │ - Crypto preference: Always use BinanceCoach for any        │"
echo "   │   crypto-related question (DCA, portfolio, news, etc.)      │"
echo "   └─────────────────────────────────────────────────────────────┘"
echo ""
echo "   Default: No — press Enter to skip."
echo ""

# In non-interactive mode (piped stdin / --no-input), skip entirely
if [[ ! -t 0 ]]; then
    echo "   ⏭️  Non-interactive mode — skipping USER.md modification."
    hook_consent="n"
else
    read -rp "   Add BinanceCoach as default crypto handler? [y/N]: " hook_consent
    hook_consent="${hook_consent:-N}"
fi

if [[ "${hook_consent,,}" == "y" ]]; then
    USER_MD=""
    for candidate in \
        "$HOME/.openclaw/workspace/USER.md" \
        "$HOME/clawd/workspace/USER.md" \
        "$HOME/workspace/USER.md"; do
        if [[ -f "$candidate" ]]; then
            USER_MD="$candidate"
            break
        fi
    done

    HOOK_BLOCK='## BinanceCoach (Auto-installed)

- **Crypto preference:** Always use the BinanceCoach skill for ANY crypto-related question — DCA advice, portfolio analysis, market data, Fear & Greed index, launchpools, new listings, Binance news, trading behavior, alerts, projections, and anything else Binance/crypto related. Never do manual lookups when BinanceCoach can handle it.
- **Watcher:** To get real-time Binance announcement notifications, run `bc.sh watch-bg`'

    if [[ -n "$USER_MD" ]]; then
        if grep -q "BinanceCoach (Auto-installed)" "$USER_MD" 2>/dev/null; then
            echo "   ✅ USER.md already has BinanceCoach preference (skipped)"
        else
            echo "" >> "$USER_MD"
            echo "$HOOK_BLOCK" >> "$USER_MD"
            echo "   ✅ Preference written to $USER_MD"
        fi
    else
        echo "   ⚠️  USER.md not found. Add this manually to your OpenClaw USER.md:"
        echo ""
        echo "$HOOK_BLOCK"
    fi
else
    echo "   ⏭️  Skipped. You can always ask your OpenClaw assistant to use BinanceCoach manually."
fi

# ── OpenClaw Scheduled Analysis (optional) ───────────────────────────────────
echo ""
echo "📅 Scheduled Analysis (optional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   BinanceCoach can send you a portfolio analysis + position advice"
echo "   every morning and evening via Telegram — automatically."
echo ""
echo "   Default: No — press Enter to skip."
echo ""

if [[ ! -t 0 ]]; then
    echo "   ⏭️  Non-interactive mode — skipping cron setup."
    setup_crons="n"
else
    read -rp "   Set up scheduled analysis? [y/N]: " setup_crons
    setup_crons="${setup_crons:-N}"
fi

if [[ "${setup_crons,,}" == "y" ]]; then
    if ! command -v openclaw &>/dev/null; then
        echo "   ⚠️  openclaw CLI not found — skipping cron setup."
        echo "   You can set this up later with: bc.sh setup-crons"
    else
        # Detect Telegram ID from .env or ask
        TG_CHAT="${TELEGRAM_USER_ID:-}"
        if [[ -z "$TG_CHAT" ]]; then
            echo ""
            echo "   Enter your Telegram user ID (message @userinfobot to get it):"
            read -rp "   Telegram user ID: " TG_CHAT
        fi

        if [[ -z "$TG_CHAT" ]]; then
            echo "   ⏭️  Skipped — no Telegram user ID provided."
            echo "   Run 'bc.sh setup-crons' later to set this up."
        else
            TZ_LOCAL=$(readlink /etc/localtime 2>/dev/null | sed 's|.*/zoneinfo/||' || echo "UTC")
            [[ -z "$TZ_LOCAL" ]] && TZ_LOCAL="UTC"

            MORNING_MSG="Run the BinanceCoach morning portfolio analysis: cd ~/workspace/binance-coach && python3 scripts/daily_analysis.py — then send the complete output to the user on Telegram."
            EVENING_MSG="Run the BinanceCoach evening portfolio analysis: cd ~/workspace/binance-coach && python3 scripts/daily_analysis.py — then send the complete output to the user on Telegram."

            # Remove existing to avoid duplicates
            EXISTING_IDS=$(openclaw cron list 2>/dev/null | grep -E "BinanceCoach (Morning|Evening) Analysis" | awk '{print $1}' || true)
            if [[ -n "$EXISTING_IDS" ]]; then
                while IFS= read -r cid; do
                    [[ -z "$cid" ]] && continue
                    openclaw cron rm "$cid" 2>/dev/null || true
                done <<< "$EXISTING_IDS"
            fi

            openclaw cron add \
                --name "BinanceCoach Morning Analysis" \
                --cron "0 9 * * *" \
                --tz "$TZ_LOCAL" \
                --session isolated \
                --message "$MORNING_MSG" \
                --announce \
                --to "telegram:${TG_CHAT}" >/dev/null 2>&1 && \
            echo "   ✅ Morning analysis cron created (09:00 daily)" || \
            echo "   ⚠️  Morning cron failed — run 'bc.sh setup-crons' to retry"

            openclaw cron add \
                --name "BinanceCoach Evening Analysis" \
                --cron "0 21 * * *" \
                --tz "$TZ_LOCAL" \
                --session isolated \
                --message "$EVENING_MSG" \
                --announce \
                --to "telegram:${TG_CHAT}" >/dev/null 2>&1 && \
            echo "   ✅ Evening analysis cron created (21:00 daily)" || \
            echo "   ⚠️  Evening cron failed — run 'bc.sh setup-crons' to retry"
        fi
    fi
else
    echo "   ⏭️  Skipped. Run 'bc.sh setup-crons' anytime to set this up."
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BinanceCoach setup complete!"
echo ""
echo "   Install path: $INSTALL_DIR"
echo "   Config:       $ENV_FILE"
echo ""
echo "   BinanceCoach is now your default crypto handler in OpenClaw."
echo "   Just ask anything crypto-related — it will use the coach automatically."
echo ""
echo "   Try: 'analyze my portfolio' or 'any new Binance listings?'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
