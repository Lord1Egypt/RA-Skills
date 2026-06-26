#!/bin/bash
# setup.sh — OpenClaw Email Checker setup wizard

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/config"
CONFIG_FILE="$CONFIG_DIR/settings.json"

echo "================================================"
echo "  OpenClaw Email Checker — Setup"
echo "================================================"
echo ""

# ── Prerequisites ─────────────────────────────────────────────────────────────
echo "Checking prerequisites..."
errors=0
if ! command -v python3 &>/dev/null; then
    echo "  ✗ python3 not found — install via Homebrew: brew install python"
    errors=$((errors + 1))
else
    echo "  ✓ python3 $(python3 --version 2>&1 | awk '{print $2}')"
fi
if ! command -v osascript &>/dev/null; then
    echo "  ✗ osascript not found — macOS only"
    errors=$((errors + 1))
else
    echo "  ✓ osascript"
fi
if [ $errors -gt 0 ]; then
    echo ""
    echo "Fix the above and re-run setup."
    exit 1
fi
echo ""

# ── Existing settings? ────────────────────────────────────────────────────────
if [ -f "$CONFIG_FILE" ]; then
    echo "Existing settings.json found."
    while true; do
        read -r -p "Reconfigure from scratch? [y/N]: " reconfigure
        reconfigure="${reconfigure:-N}"
        case "$reconfigure" in
            [Yy]) echo ""; break ;;
            [Nn]) echo "Skipped. Using existing settings."; exit 0 ;;
            *) echo "  Please enter y or n." ;;
        esac
    done
fi

# ── Discover Mail.app accounts ────────────────────────────────────────────────
echo "Discovering Mail.app accounts..."
accounts_raw=$(osascript << 'APPLESCRIPT' 2>/dev/null
tell application "Mail"
    set output to {}
    repeat with acct in accounts
        set end of output to ((id of acct) & ":::" & (name of acct))
    end repeat
    set AppleScript's text item delimiters to linefeed
    set resultText to output as text
    set AppleScript's text item delimiters to ""
    return resultText
end tell
APPLESCRIPT
) || true

declare -a accounts
if [ -n "$accounts_raw" ]; then
    while IFS= read -r line; do
        [ -n "$line" ] && accounts+=("$line")
    done <<< "$accounts_raw"
fi

if [ ${#accounts[@]} -eq 0 ]; then
    echo "  Could not auto-discover accounts. Check Mail.app is set up and"
    echo "  Terminal has Automation permission to control Mail."
    echo "  (System Settings → Privacy & Security → Automation → Terminal → Mail)"
    echo ""
    while true; do
        read -r -p "  Enter Mail.app account ID manually (or Ctrl+C to abort): " MAIL_ACCOUNT_ID
        [ -n "$MAIL_ACCOUNT_ID" ] && break
        echo "  Account ID cannot be empty."
    done
else
    echo ""
    echo "Available Mail.app accounts:"
    for i in "${!accounts[@]}"; do
        id_part="${accounts[$i]%%:::*}"
        name_part="${accounts[$i]##*:::}"
        echo "  [$((i + 1))] $name_part  ($id_part)"
    done
    echo ""
    while true; do
        read -r -p "Select account [1-${#accounts[@]}]: " acct_num
        if [[ "$acct_num" =~ ^[0-9]+$ ]] && \
           [ "$acct_num" -ge 1 ] && [ "$acct_num" -le "${#accounts[@]}" ]; then
            chosen="${accounts[$((acct_num - 1))]}"
            MAIL_ACCOUNT_ID="${chosen%%:::*}"
            break
        fi
        echo "  Invalid selection — enter a number between 1 and ${#accounts[@]}."
    done
fi
echo ""

# ── User info ─────────────────────────────────────────────────────────────────
while true; do
    read -r -p "Your full name (for LLM context): " USER_NAME
    [ -n "$USER_NAME" ] && break
    echo "  Name cannot be empty."
done

read -r -p "Bot name [EntzClawBot]: " BOT_NAME
BOT_NAME="${BOT_NAME:-EntzClawBot}"

while true; do
    read -r -p "Report recipient email: " REPORT_EMAIL
    if [[ "$REPORT_EMAIL" =~ ^[^@]+@[^@]+\.[^@]+$ ]]; then
        break
    fi
    echo "  Enter a valid email address (e.g. you@example.com)."
done

echo ""
echo "Trusted senders get a priority boost. Matched as substring of From: field."
echo "  Examples:  'Angelo'  '@company.com'  'alice@example.com'"
echo "  Leave blank to skip."
read -r -p "Trusted senders (comma-separated): " TRUSTED_SENDERS_RAW
echo ""

# ── LLM provider ──────────────────────────────────────────────────────────────
echo "LLM provider:"
echo "  [1] LM Studio  (local or remote)"
echo "  [2] Ollama     (local)"
echo "  [3] OpenAI"
echo "  [4] Skip       (no AI drafts)"
echo ""
while true; do
    read -r -p "Select provider [1-4]: " llm_choice
    case "$llm_choice" in
        1)
            LLM_PROVIDER="lm_studio"
            read -r -p "  Base URL [http://localhost:1234/v1]: " LLM_BASE_URL
            LLM_BASE_URL="${LLM_BASE_URL:-http://localhost:1234/v1}"
            read -r -p "  API key [local]: " LLM_API_KEY
            LLM_API_KEY="${LLM_API_KEY:-local}"
            while true; do
                read -r -p "  Model ID: " LLM_MODEL
                [ -n "$LLM_MODEL" ] && break
                echo "  Model ID is required."
            done
            break ;;
        2)
            LLM_PROVIDER="ollama"
            LLM_BASE_URL="http://localhost:11434/v1"
            LLM_API_KEY="ollama"
            read -r -p "  Model ID [llama3]: " LLM_MODEL
            LLM_MODEL="${LLM_MODEL:-llama3}"
            break ;;
        3)
            LLM_PROVIDER="openai"
            LLM_BASE_URL="https://api.openai.com/v1"
            while true; do
                read -r -p "  OpenAI API key: " LLM_API_KEY
                [ -n "$LLM_API_KEY" ] && break
                echo "  API key is required."
            done
            read -r -p "  Model ID [gpt-4o-mini]: " LLM_MODEL
            LLM_MODEL="${LLM_MODEL:-gpt-4o-mini}"
            break ;;
        4)
            LLM_PROVIDER="none"
            LLM_BASE_URL=""
            LLM_API_KEY=""
            LLM_MODEL=""
            break ;;
        *) echo "  Invalid — enter 1, 2, 3, or 4." ;;
    esac
done
echo ""

# ── Test LLM connection ────────────────────────────────────────────────────────
if [ "$LLM_PROVIDER" != "none" ]; then
    echo "Testing LLM connection — please wait up to 15 seconds..."
    llm_test_output=$(BASE_URL="$LLM_BASE_URL" API_KEY="$LLM_API_KEY" MODEL="$LLM_MODEL" \
        python3 - << 'PYEOF' 2>&1
import urllib.request, json, os, sys

url   = os.environ['BASE_URL'].rstrip('/') + '/chat/completions'
model = os.environ['MODEL']
key   = os.environ['API_KEY']

payload = json.dumps({
    'model': model,
    'messages': [{'role': 'user', 'content': 'ping'}],
    'max_tokens': 5
}).encode()

req = urllib.request.Request(
    url, data=payload,
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key},
    method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        body = json.loads(r.read())
        if 'choices' in body or 'content' in str(body):
            print('OK')
        else:
            print('UNEXPECTED_RESPONSE: ' + str(body)[:200])
except urllib.error.HTTPError as e:
    print('HTTP_ERROR: ' + str(e.code) + ' ' + e.reason)
except urllib.error.URLError as e:
    print('CONNECTION_ERROR: ' + str(e.reason))
except Exception as e:
    print('ERROR: ' + str(e))
PYEOF
    ) || true

    llm_test_output="${llm_test_output:-NO_OUTPUT}"

    if [ "$llm_test_output" = "OK" ]; then
        echo "  ✓ LLM connection successful"
    else
        echo "  ✗ LLM connection failed: $llm_test_output"
        echo ""
        echo "  Common fixes:"
        echo "    CONNECTION_ERROR  → check the Base URL is reachable from this machine"
        echo "    HTTP_ERROR 401    → wrong API key"
        echo "    HTTP_ERROR 404    → wrong Base URL or model ID"
        echo "    HTTP_ERROR 400    → model ID not found on this server"
        echo ""
        # Flush any keypresses the user typed while waiting for the LLM test
        read -r -t 0.1 -s -d '' _flush 2>/dev/null || true
        while true; do
            read -r -p "  Continue anyway and fix later? [Y/n]: " cont
            cont="${cont:-Y}"
            case "$cont" in
                [Yy]) break ;;
                [Nn]) echo "Aborted. Fix the LLM settings and re-run setup."; exit 1 ;;
                *) echo "  Please enter y or n." ;;
            esac
        done
    fi
    echo ""
fi

# ── Check interval ─────────────────────────────────────────────────────────────
echo "How often should the checker run?"
echo "  [1] Every 15 minutes"
echo "  [2] Every 30 minutes"
echo "  [3] Every hour (default)"
echo "  [4] Custom interval"
echo ""
while true; do
    read -r -p "Select interval [1-4]: " interval_choice
    case "$interval_choice" in
        1) INTERVAL_MINUTES=15;  break ;;
        2) INTERVAL_MINUTES=30;  break ;;
        3) INTERVAL_MINUTES=60;  break ;;
        4)
            while true; do
                read -r -p "  Enter interval in minutes: " INTERVAL_MINUTES
                if [[ "$INTERVAL_MINUTES" =~ ^[0-9]+$ ]] && [ "$INTERVAL_MINUTES" -ge 1 ]; then
                    break
                fi
                echo "  Must be a positive whole number."
            done
            break ;;
        *) echo "  Invalid — enter 1, 2, 3, or 4." ;;
    esac
done
echo ""

# ── Write settings.json ────────────────────────────────────────────────────────
mkdir -p "$CONFIG_DIR"

write_output=$(CONFIG_FILE="$CONFIG_FILE" \
USER_NAME="$USER_NAME" \
BOT_NAME="$BOT_NAME" \
REPORT_EMAIL="$REPORT_EMAIL" \
TRUSTED_SENDERS_RAW="$TRUSTED_SENDERS_RAW" \
MAIL_ACCOUNT_ID="$MAIL_ACCOUNT_ID" \
LLM_PROVIDER="$LLM_PROVIDER" \
LLM_BASE_URL="$LLM_BASE_URL" \
LLM_API_KEY="$LLM_API_KEY" \
LLM_MODEL="$LLM_MODEL" \
INTERVAL_MINUTES="$INTERVAL_MINUTES" \
python3 - << 'PYEOF' 2>&1
import json, os, sys

trusted_raw = os.environ.get('TRUSTED_SENDERS_RAW', '')
trusted = [s.strip() for s in trusted_raw.split(',') if s.strip()]

config = {
    "user": {
        "name":            os.environ['USER_NAME'],
        "bot_name":        os.environ['BOT_NAME'],
        "report_email":    os.environ['REPORT_EMAIL'],
        "trusted_senders": trusted
    },
    "mail": {
        "account_id":  os.environ['MAIL_ACCOUNT_ID'],
        "inbox_name":  "INBOX"
    },
    "schedule": {
        "interval_minutes": int(os.environ['INTERVAL_MINUTES'])
    },
    "llm": {
        "provider":   os.environ['LLM_PROVIDER'],
        "base_url":   os.environ['LLM_BASE_URL'],
        "api_key":    os.environ['LLM_API_KEY'],
        "model":      os.environ['LLM_MODEL'],
        "max_tokens": 800,
        "timeout":    45
    }
}

config_path = os.environ.get('CONFIG_FILE', '')
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print('OK')
PYEOF
)

if [ "$write_output" = "OK" ] && [ -f "$CONFIG_FILE" ]; then
    echo "  ✓ settings.json written to $CONFIG_FILE"
else
    echo "  ✗ Failed to write settings.json: $write_output"
    echo "  Setup cannot continue."
    exit 1
fi

# ── Install crontab ────────────────────────────────────────────────────────────
WRAPPER="$SCRIPT_DIR/scripts/email/checker_wrapper.sh"

if [ "$INTERVAL_MINUTES" -eq 60 ]; then
    CRON_SCHEDULE="0 * * * *"
else
    CRON_SCHEDULE="*/$INTERVAL_MINUTES * * * *"
fi

echo ""
echo "Cron schedule: every ${INTERVAL_MINUTES} min + on startup"
echo ""
while true; do
    read -r -p "Install/update crontab? [Y/n]: " install_cron
    install_cron="${install_cron:-Y}"
    case "$install_cron" in
        [Yy])
            ( crontab -l 2>/dev/null | grep -v checker_wrapper || true
              echo "# Email checker — runs at startup and every ${INTERVAL_MINUTES} min"
              echo "@reboot $WRAPPER"
              echo "$CRON_SCHEDULE $WRAPPER"
            ) | crontab -
            if [ $? -eq 0 ]; then
                echo "  ✓ Crontab installed"
            else
                echo "  ✗ Crontab install failed — add manually:"
                echo "    @reboot $WRAPPER"
                echo "    $CRON_SCHEDULE $WRAPPER"
            fi
            break ;;
        [Nn]) echo "  Skipped crontab."; break ;;
        *) echo "  Please enter y or n." ;;
    esac
done

# ── Permissions reminder ───────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  PERMISSIONS (if not already granted)"
echo "================================================"
echo ""
echo "  System Settings → Privacy & Security → Automation"
echo "  → Allow Terminal to control Mail"
echo ""
echo "  If cron runs fail, also add:"
echo "  → Full Disk Access → Terminal (or cron)"
echo ""

# ── Optional test run ──────────────────────────────────────────────────────────
while true; do
    read -r -p "Run a test check right now? [Y/n]: " run_test
    run_test="${run_test:-Y}"
    case "$run_test" in
        [Yy])
            echo ""
            echo "Running test..."
            echo "--------------------------------------------"
            python3 "$SCRIPT_DIR/scripts/email/checker.py"
            test_exit=$?
            echo "--------------------------------------------"
            if [ $test_exit -eq 0 ]; then
                echo "  ✓ Test run successful"
            else
                echo "  ✗ Test run exited with code $test_exit"
                echo "    Check the output above for errors."
            fi
            break ;;
        [Nn]) break ;;
        *) echo "  Please enter y or n." ;;
    esac
done

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo "================================================"
echo "  Setup complete!"
echo "================================================"
echo ""
echo "  Config:    $CONFIG_FILE"
echo "  Schedule:  every ${INTERVAL_MINUTES} min + on startup"
echo "  Reports:   $REPORT_EMAIL"
if [ -n "$LLM_MODEL" ]; then
echo "  LLM:       $LLM_MODEL  ($LLM_PROVIDER)"
fi
echo ""
echo "  To reconfigure: bash $SCRIPT_DIR/setup.sh"
echo "  Logs:           $SCRIPT_DIR/logs/email_check.log"
echo ""
