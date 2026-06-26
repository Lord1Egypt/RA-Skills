#!/bin/bash
# EPO Patent Intelligence - Weekly Automation Script
# This script coordinates deterministic data collection with LLM analysis

set -e

# Configuration
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
DATA_DIR="$SKILL_DIR/data"
REPORT_DIR="$SKILL_DIR/reports"
LOG_DIR="$SKILL_DIR/logs"

# Competitors to monitor (customize for each client)
COMPETITORS="Trumpf Mazak Okuma Haas"

# Create directories
mkdir -p "$DATA_DIR" "$REPORT_DIR" "$LOG_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/weekly_report.log"
}

log "=== Weekly EPO Patent Intelligence Report ==="
log "Starting collection for competitors: $COMPETITORS"

# Load EPO credentials
if [ -f "$SKILL_DIR/.env" ]; then
    source "$SKILL_DIR/.env"
    log "✓ EPO credentials loaded"
else
    log "❌ ERROR: .env file not found"
    exit 1
fi

# Phase 1: Data Collection (Deterministic)
log "Phase 1: Collecting patent data from EPO API..."

cd "$SKILL_DIR"

for competitor in $COMPETITORS; do
    log "  Fetching patents for: $competitor"
    python3 scripts/epo_data_mapper.py "pa=$competitor" 1 10 >> "$LOG_DIR/collection.log" 2>&1 || {
        log "  ⚠️ Failed to fetch patents for $competitor"
    }
done

# Count collected patents
PATENT_COUNT=$(python3 -c "
import sqlite3
conn = sqlite3.connect('$DATA_DIR/patents.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM patents')
print(cursor.fetchone()[0])
conn.close()
" 2>/dev/null || echo "0")

log "✓ Phase 1 complete: $PATENT_COUNT patents in database"

# Phase 2: LLM Analysis (OpenClaw Agent)
log "Phase 2: LLM analysis of collected patents..."
log "  ⚡ Triggering OpenClaw agent for patent analysis..."
log "  ⚡ Agent will:"
log "     - Load patents from database"
log "     - Analyze competitive threat for each patent"
log "     - Determine technology alignment"
log "     - Generate strategic recommendations"
log "     - Create professional HTML report"

# Note: This is where OpenClaw would take over
# The script creates a marker file that signals an agent to run analysis
ANALYSIS_MARKER="$LOG_DIR/analysis_request_$(date +%Y%m%d).json"
cat > "$ANALYSIS_MARKER" << EOF
{
  "request_type": "patent_analysis",
  "timestamp": "$(date -Iseconds)",
  "competitors": "$COMPETITORS",
  "patent_count": $PATENT_COUNT,
  "database_path": "$DATA_DIR/patents.db",
  "output_report": "$REPORT_DIR/weekly_report_$(date +%Y%m%d).html",
  "client_context": "DMG_Mori",
  "analysis_required": [
    "competitive_threat_assessment",
    "technology_categorization",
    "strategic_recommendations",
    "html_report_generation"
  ]
}
EOF

log "✓ Analysis request created: $ANALYSIS_MARKER"

# Phase 3: Report Generation (OpenClaw Agent)
log "Phase 3: Report generation and distribution..."
log "  📄 Report will be generated at: $REPORT_DIR/weekly_report_$(date +%Y%m%d).html"
log "  📧 Email notification will be sent to R&D team"

# Check if report exists (created by LLM agent)
if [ -f "$REPORT_DIR/weekly_report_$(date +%Y%m%d).html" ]; then
    REPORT_SIZE=$(stat -c%s "$REPORT_DIR/weekly_report_$(date +%Y%m%d).html")
    log "✓ Report generated: $REPORT_SIZE bytes"
else
    log "⚠️ Report not yet generated - OpenClaw agent will complete this"
fi

log "=== Weekly automation script complete ==="
log "Next: OpenClaw agent will process analysis request and generate report"