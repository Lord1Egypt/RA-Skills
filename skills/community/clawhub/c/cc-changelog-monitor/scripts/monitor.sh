#!/bin/bash
# cc-changelog-monitor.sh - Zero AI credits Claude Code version monitor
# Monitors @anthropic-ai/claude-code on npm and sends Telegram alerts

set -e

# Config
STORED_FILE=~/.cc-changelog-version
OUTDIR=~/clawd/projects/cc-changelog
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8587009442:AAE9gvBicxM2T2NMmqNGDE9yXPQy3pB8pP8}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:--1002381931352}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 1. Check npm for latest version
log_info "Checking npm for latest Claude Code version..."
LATEST=$(curl -s https://registry.npmjs.org/@anthropic-ai/claude-code/latest | jq -r .version 2>/dev/null) || {
    log_error "Failed to fetch npm version"
    exit 1
}

if [ -z "$LATEST" ] || [ "$LATEST" = "null" ]; then
    log_error "Invalid version from npm"
    exit 1
fi

log_info "Latest version: $LATEST"

# 2. Get stored version
STORED=$(cat $STORED_FILE 2>/dev/null || echo "0.0.0")
log_info "Stored version: $STORED"

# 3. If same version, exit silently
if [ "$LATEST" = "$STORED" ]; then
    log_info "No new version. Exiting."
    exit 0
fi

log_warn "New version detected: $STORED -> $LATEST"

# 4. Get version details from npm
VERSION_INFO=$(curl -s "https://registry.npmjs.org/@anthropic-ai/claude-code/$LATEST" 2>/dev/null)
PUBLISHED=$(echo "$VERSION_INFO" | jq -r '.time.published' 2>/dev/null | cut -d'T' -f1)
 tarball=$(echo "$VERSION_INFO" | jq -r '.dist.tarball' 2>/dev/null)

# 5. Build changelog-style comparison (from npm registry - no AI needed)
CHANGES="• Version: $LATEST (was $STORED)
• Published: $PUBLISHED
• Tarball: $(echo $tarball | cut -d'/' -f5- | cut -c1-50)..."

# 6. Try to get release notes from GitHub (if available)
RELEASE_NOTES=""
if command -v curl &> /dev/null; then
    GITHUB_JSON=$(curl -s "https://api.github.com/repos/anthropics/claude-code/releases/tags/v${LATEST}" 2>/dev/null || echo "{}")
    BODY=$(echo "$GITHUB_JSON" | jq -r '.body[0:500]' 2>/dev/null || echo "")
    if [ -n "$BODY" ] && [ "$BODY" != "null" ]; then
        RELEASE_NOTES="
Release notes (first 500 chars):
$BODY..."
    fi
fi

# 7. Send Telegram alert
MESSAGE="🤖 *Claude Code v${LATEST}* released!

Previous: v${STORED}
Published: ${PUBLISHED:-unknown}

${CHANGES}${RELEASE_NOTES}

_Monitored by OpenClaw_"

log_info "Sending Telegram alert..."
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{
        \"chat_id\": \"${TELEGRAM_CHAT_ID}\",
        \"text\": $(echo "$MESSAGE" | jq -Rs .),
        \"parse_mode\": \"Markdown\"
    }" > /dev/null 2>&1 && log_info "Alert sent!" || log_error "Failed to send alert"

# 8. Save new version
echo "$LATEST" > $STORED_FILE
log_info "Version saved to $STORED_FILE"

# 9. Optionally download and extract for future diffs
if [ ! -d "$OUTDIR/$LATEST" ]; then
    log_info "Downloading package for future diffs..."
    mkdir -p "$OUTDIR/$LATEST"
    TMP_TARBALL="/tmp/claude-code-${LATEST}.tgz"
    curl -sL "$tarball" -o "$TMP_TARBALL" 2>/dev/null && \
        tar -xzf "$TMP_TARBALL" -C "$OUTDIR/$LATEST" 2>/dev/null && \
        rm -f "$TMP_TARBALL" && \
        log_info "Package extracted to $OUTDIR/$LATEST" || \
        log_warn "Failed to extract package (non-critical)"
fi

echo "✅ Claude Code $LATEST alert complete"
