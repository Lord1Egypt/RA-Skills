#!/bin/bash
# Usage: deploy-notify.sh <project-dir> <commit-hash>
# Polls GitHub Actions for build result and sends Telegram notification

PROJECT_DIR="$1"
COMMIT="$2"

# Load swarm config (notifications, etc.)
SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SWARM_DIR/swarm.conf" ]] && source "$SWARM_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"

send_notify() {
  local msg="$1"
  [[ -z "$NOTIFY_TARGET" ]] && return 0
  openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$msg" 2>/dev/null || true
}

cd "$PROJECT_DIR" || exit 1

# Get repo name from git remote
REPO=$(git remote get-url origin | sed 's|.*github.com[:/]||' | sed 's|\.git$||')
PROJECT_NAME=$(basename "$PROJECT_DIR")

echo "Watching GitHub Actions for $REPO @ $COMMIT..."

# Poll for up to 15 minutes
for i in $(seq 1 30); do
    sleep 30

    # Check if any workflow run matches this commit
    STATUS=$(gh run list --commit "$COMMIT" --limit 1 --json status,conclusion -q '.[0]' 2>/dev/null)

    if [ -z "$STATUS" ]; then
        continue
    fi

    CONCLUSION=$(echo "$STATUS" | jq -r '.conclusion // empty')
    RUN_STATUS=$(echo "$STATUS" | jq -r '.status // empty')

    if [ "$RUN_STATUS" = "completed" ]; then
        if [ "$CONCLUSION" = "success" ]; then
            send_notify "✅ CI Build PASSED for $PROJECT_NAME (${COMMIT:0:7}) — github.com/$REPO/actions"
            echo "Build passed!"
            exit 0
        else
            RUN_URL=$(gh run list --commit "$COMMIT" --limit 1 --json url -q '.[0].url' 2>/dev/null)
            send_notify "❌ CI Build FAILED for $PROJECT_NAME (${COMMIT:0:7}) — $RUN_URL"
            echo "Build failed!"
            exit 1
        fi
    fi
done

send_notify "⏰ CI Build timed out for $PROJECT_NAME (${COMMIT:0:7}) — check GitHub Actions manually"
echo "Timed out waiting for build"
exit 2
