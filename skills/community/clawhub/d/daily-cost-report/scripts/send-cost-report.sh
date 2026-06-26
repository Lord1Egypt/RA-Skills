#!/bin/bash
# Send daily cost report via email
# Usage: send-cost-report.sh [recipient-email] [date]

RECIPIENT="${1:-}" 
DATE="${2:-yesterday}"

if [ -z "$RECIPIENT" ]; then
  echo "❌ Usage: $0 <email> [date]"
  exit 1
fi

# Generate HTML report
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/daily-cost-report-email.sh" "$DATE"

# Determine report date
if date -v-1d +%Y-%m-%d >/dev/null 2>&1; then
  DATE_STR=$(date -j -f "%Y-%m-%d" "$DATE" "+%Y-%m-%d" 2>/dev/null || date -j -v-1d "+%Y-%m-%d")
else
  DATE_STR=$(date -d "$DATE" "+%Y-%m-%d" 2>/dev/null || date -d "yesterday" "+%Y-%m-%d")
fi

HTML_FILE="/tmp/cost-report-${DATE_STR}.html"
REPORT_FILE="/tmp/cost-report-${DATE_STR}.md"

if [ ! -f "$HTML_FILE" ]; then
  echo "❌ HTML file not found: $HTML_FILE"
  exit 1
fi

# Extract cost from report for subject
TOTAL_COST=$(grep "Total Cost" "$REPORT_FILE" 2>/dev/null | head -1 | awk -F'|' '{print $3}' | xargs 2>/dev/null || echo "unknown")
PRETTY_DATE=$(date -j -f "%Y-%m-%d" "$DATE_STR" "+%B %d, %Y" 2>/dev/null || date -d "$DATE_STR" "+%B %d, %Y")

# Send via mail command (macOS/Linux compatible)
{
  # Email headers
  echo "From: Bernie <$(whoami)@localhost>"
  echo "To: $RECIPIENT"
  echo "Subject: 🐈‍⬛ OpenClaw Cost Report - $PRETTY_DATE ($TOTAL_COST)"
  echo "MIME-Version: 1.0"
  echo "Content-Type: text/html; charset=UTF-8"
  echo "Content-Transfer-Encoding: 8bit"
  echo ""
  # Email body (HTML)
  cat "$HTML_FILE"
} | mail -t -v "$RECIPIENT" 2>/dev/null || {
  echo "⚠️  mail command failed. Trying alternative method..."
  # Fallback: write to file instead
  cp "$HTML_FILE" "/tmp/cost-report-${DATE_STR}-UNSENT.html"
  echo "ℹ️  Report saved to: /tmp/cost-report-${DATE_STR}-UNSENT.html"
  echo "ℹ️  To send: mail -s 'Cost Report' -a 'Content-Type: text/html' $RECIPIENT < /tmp/cost-report-${DATE_STR}.html"
}

echo "✅ Cost report processed for $PRETTY_DATE"
