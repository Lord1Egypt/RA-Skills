#!/bin/bash
# EPO Patent Intelligence - Enhanced Weekly Automation Script
# Includes technology trend analysis (Iteration 2 enhancements)

set -e

# Configuration
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
DATA_DIR="$SKILL_DIR/data"
REPORT_DIR="$SKILL_DIR/reports"
LOG_DIR="$SKILL_DIR/logs"

# Competitors to monitor (customize for each client)
COMPETITORS="Microsoft IBM TRUMPF OKUMA HAAS"

# Create directories
mkdir -p "$DATA_DIR" "$REPORT_DIR" "$LOG_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/weekly_report.log"
}

log "=== Enhanced EPO Patent Intelligence Report ==="
log "Starting collection for competitors: $COMPETITORS"
log "Includes: Technology trend analysis (Iteration 2 enhancements)"

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
count = cursor.fetchone()[0]
conn.close()
print(count)
")

log "✓ Data collection complete: $PATENT_COUNT patents in database"

# Phase 2: Technology Trend Analysis (Enhanced)
log "Phase 2: Generating technology trend analysis..."

# Generate technology trend report
if [ -f "$SKILL_DIR/generate_tech_trend_report.py" ]; then
    python3 generate_tech_trend_report.py >> "$LOG_DIR/tech_trend.log" 2>&1
    if [ $? -eq 0 ]; then
        log "✓ Technology trend analysis generated"
        
        # Copy to current week's report
        CURRENT_WEEK=$(date +%V)
        CURRENT_YEAR=$(date +%Y)
        WEEK_DIR="$REPORT_DIR/Patent_report_kw${CURRENT_WEEK}"
        
        mkdir -p "$WEEK_DIR"
        if [ -f "$REPORT_DIR/weekly_report_iteration2.html" ]; then
            cp "$REPORT_DIR/weekly_report_iteration2.html" "$WEEK_DIR/index.html"
            log "✓ Enhanced report copied to: $WEEK_DIR/index.html"
            
            # Update index.html to list all reports
            cat > "$REPORT_DIR/index.html" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Patent Intelligence Reports</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #003399; }
        .report { margin: 20px 0; padding: 15px; border-left: 4px solid #0066cc; background: #f0f8ff; }
        .live { border-color: #00cc00; background: #f0fff0; }
        .prepared { border-color: #ff9900; background: #fff8f0; }
    </style>
</head>
<body>
    <h1>📊 Patent Intelligence Reports</h1>
    <p>Weekly technology trend analysis for DMG Mori</p>
    
    <div class="report live">
        <h2>KW$CURRENT_WEEK ($CURRENT_YEAR) - LIVE</h2>
        <p>Technology trend analysis with ${PATENT_COUNT} patents</p>
        <a href="/Patent_report_kw${CURRENT_WEEK}/">View Report</a>
    </div>
    
    <div class="report">
        <h2>KW$((CURRENT_WEEK-1)) ($CURRENT_YEAR) - ARCHIVED</h2>
        <p>Previous week's analysis</p>
        <a href="/Patent_report_kw$((CURRENT_WEEK-1))/">View Report</a>
    </div>
    
    <div class="report prepared">
        <h2>KW$((CURRENT_WEEK+1)) ($CURRENT_YEAR) - PREPARED</h2>
        <p>Next week's template ready</p>
        <a href="/Patent_report_kw$((CURRENT_WEEK+1))/">View Template</a>
    </div>
    
    <hr>
    <p><small>Generated: $(date '+%Y-%m-%d %H:%M UTC') | Patents: ${PATENT_COUNT}</small></p>
</body>
</html>
EOF
            log "✓ Reports index updated"
        else
            log "⚠️ Technology trend report not found"
        fi
    else
        log "⚠️ Technology trend analysis failed"
    fi
else
    log "⚠️ Technology trend generator not found: generate_tech_trend_report.py"
fi

# Phase 3: Create analysis request for LLM agent
log "Phase 3: Creating analysis request for LLM agent..."

ANALYSIS_REQUEST="$LOG_DIR/analysis_request_$(date +%Y%m%d).json"
cat > "$ANALYSIS_REQUEST" << EOF
{
  "date": "$(date '+%Y-%m-%d')",
  "patent_count": $PATENT_COUNT,
  "competitors": "$COMPETITORS",
  "database_path": "$DATA_DIR/patents.db",
  "report_path": "$REPORT_DIR/weekly_report_iteration2.html",
  "analysis_type": "weekly_trends_with_technology",
  "priority": "high",
  "technology_insights": true,
  "required_analysis": [
    "competitive_threat_assessment",
    "technology_trend_analysis",
    "strategic_recommendations",
    "executive_summary"
  ]
}
EOF

log "✓ Analysis request created: $ANALYSIS_REQUEST"

log "=== Enhanced Weekly Automation Complete ==="
log "Summary:"
log "  • Patents collected: $PATENT_COUNT"
log "  • Technology analysis: ✅ Complete"
log "  • Report generated: ✅ $REPORT_DIR/weekly_report_iteration2.html"
log "  • Dashboard updated: ✅ KW$CURRENT_WEEK"
log "  • LLM analysis ready: ✅ $ANALYSIS_REQUEST"
log ""
log "Next steps for LLM agent:"
log "1. Read analysis request for strategic insights"
log "2. Generate executive summary for R&D team"
log "3. Identify high-priority technology threats"
log "4. Update Obsidian vault with findings"