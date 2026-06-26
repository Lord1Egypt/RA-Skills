#!/bin/bash
# GitHub Bounty Hunter Configuration

# Scanning
SCAN_INTERVAL=1800          # Seconds between scans (30 min)
MAX_ISSUES_PER_SCAN=10      # Max issues to process per scan
LANGUAGES="javascript,python,typescript,go,rust"

# Evaluation
MIN_REPO_STARS=5            # Minimum repository stars
MIN_VALUE=10                # Minimum estimated value ($)
MAX_COMPLEXITY=5            # Max complexity (1-10)
SKIP_ORGS="AutomationSyncUser"  # Organizations to skip

# Automation
AUTO_CLAIM=true             # Auto-claim issues
AUTO_SUBMIT=true            # Auto-submit PRs
DRY_RUN=false               # Preview mode (no actions)

# Tracking
QUEUE_FILE="${SKILL_DIR:-$(dirname "$0")/..}/data/queue.json"
HISTORY_FILE="${SKILL_DIR:-$(dirname "$0")/..}/data/history.json"
LOG_FILE="${SKILL_DIR:-$(dirname "$0")/..}/data/bounty_hunter.log"

# GitHub
GH_API="https://api.github.com"
CLAIM_MESSAGE="I'd like to work on this issue. I'll submit a PR shortly."
