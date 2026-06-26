#!/bin/bash
# Weekly rotation script for patent reports
# Usage: ./rotate_weekly.sh [week_number]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports"

# Default to current week (KW15)
WEEK=${1:-15}
YEAR=2026

echo "🔄 Starting weekly rotation for KW$WEEK, $YEAR"
echo "=============================================="

# 1. Create directory for new week
NEW_DIR="$REPORTS_DIR/Patent_report_kw$WEEK"
mkdir -p "$NEW_DIR"

# 2. Copy template
if [ -f "$REPORTS_DIR/modern_report_template.html" ]; then
    cp "$REPORTS_DIR/modern_report_template.html" "$NEW_DIR/index.html"
    echo "✅ Copied template to $NEW_DIR/index.html"
else
    echo "❌ Template not found: $REPORTS_DIR/modern_report_template.html"
    exit 1
fi

# 3. Update week references in the template
sed -i "s/Week 14, 2026/Week $WEEK, $YEAR/g" "$NEW_DIR/index.html"
sed -i "s/KW14/KW$WEEK/g" "$NEW_DIR/index.html" 2>/dev/null || true
echo "✅ Updated week references to KW$WEEK, $YEAR"

# 4. Update main index.html
INDEX_FILE="$REPORTS_DIR/index.html"
if [ -f "$INDEX_FILE" ]; then
    # Check if this week already exists in index
    if ! grep -q "Patent_report_kw$WEEK" "$INDEX_FILE"; then
        # Add new entry after the last report-item
        sed -i "/<\/ul>/i\        <li class=\"report-item\">\n            <a href=\"Patent_report_kw$WEEK/index.html\">📊 Week $WEEK, $YEAR - Enterprise Dashboard</a>\n            <span class=\"status pending\">PREPARED</span>\n            <div class=\"report-meta\">Ready for next week's data • Template configured • Will be live at: https://hermes.sqncr.ai/Patent_report_kw$WEEK</div>\n        </li>" "$INDEX_FILE"
        echo "✅ Added KW$WEEK to index.html"
    else
        echo "⚠️  KW$WEEK already exists in index.html"
    fi
fi

# 5. Create restart script for new week
RESTART_SCRIPT="$SCRIPT_DIR/restart_tunnel_kw$WEEK.sh"
cat > "$RESTART_SCRIPT" << EOF
#!/bin/bash
# Restart tunnel for KW$WEEK
# Usage: ./restart_tunnel_kw$WEEK.sh

pkill -9 -f "python3.*http.server" 2>/dev/null
pkill -9 cloudflared 2>/dev/null
sleep 3

cd "$REPORTS_DIR"
nohup python3 -m http.server 8080 > /tmp/http_server_kw$WEEK.log 2>&1 &
sleep 3

export TUNNEL_TOKEN="eyJhIjoiNmRiMjNkNDYxZjU5YjkyZjdmM2UyM2RkZjYwNjZkYzAiLCJ0IjoiZmE1M2NmZGEtOTYzMy00NDQ0LWJiMzItZDI4ZjllMTI3NTkyIiwicyI6IllUWmlaalk0Tm1NdFptRTNNQzAwTmpoaExUbGhaREF0WkRrNU1XWTFPRFExWW1VNCJ9"
nohup cloudflared tunnel --no-autoupdate run --token "\$TUNNEL_TOKEN" --url http://localhost:8080 > /tmp/tunnel_kw$WEEK.log 2>&1 &
sleep 5

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ PATENT REPORT KW$WEEK DEPLOYMENT COMPLETE"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📊 Local Server:  http://localhost:8080"
echo "🌐 Public URL:   https://hermes.sqncr.ai/Patent_report_kw$WEEK"
echo ""
echo "📈 Modern Dashboard Features:"
echo "   • Tailwind CSS enterprise styling"
echo "   • Chart.js interactive visualizations"
echo "   • Mobile-responsive design"
echo ""
echo "⚠️  Tunnel may take 30-60 seconds to fully propagate"
echo "═══════════════════════════════════════════════════"
EOF

chmod +x "$RESTART_SCRIPT"
echo "✅ Created restart script: $RESTART_SCRIPT"

# 6. Create documentation
DOC_FILE="$SCRIPT_DIR/../docs/WEEKLY_ROTATION_GUIDE.md"
cat > "$DOC_FILE" << EOF
# Weekly Rotation Guide

## Current Week: KW$WEEK (Week $WEEK, $YEAR)

## Directory Structure
\`\`\`
reports/
├── index.html                    # Main index with all reports
├── modern_report_template.html   # Template for all weeks
├── Patent_report_kw14/           # Week 14 (current live)
│   └── index.html
└── Patent_report_kw$WEEK/        # Week $WEEK (prepared)
    └── index.html
\`\`\`

## Rotation Process

### 1. Prepare New Week
\`\`\`bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
./scripts/rotate_weekly.sh 16   # For KW16
\`\`\`

### 2. Deploy New Week
\`\`\`bash
./scripts/restart_tunnel_kw16.sh
\`\`\`

### 3. Archive Old Week
\`\`\`bash
# Move old week to archive
mv reports/Patent_report_kw14/ archive/kw14_2026/
\`\`\`

## URL Structure
- Week 14: https://hermes.sqncr.ai/Patent_report_kw14
- Week $WEEK: https://hermes.sqncr.ai/Patent_report_kw$WEEK
- Week 16: https://hermes.sqncr.ai/Patent_report_kw16

## Automation Notes
- The HTTP server always runs on port 8080
- Cloudflare tunnel routes based on subdomain path
- Each week gets its own log files
- Restart scripts are week-specific for easy management
EOF

echo "✅ Created documentation: $DOC_FILE"

echo ""
echo "=============================================="
echo "✅ WEEKLY ROTATION COMPLETE FOR KW$WEEK"
echo "=============================================="
echo ""
echo "📁 New directory: $NEW_DIR/"
echo "🚀 Restart script: $RESTART_SCRIPT"
echo "📚 Documentation: $DOC_FILE"
echo ""
echo "To deploy KW$WEEK:"
echo "  1. Run: $RESTART_SCRIPT"
echo "  2. Access: https://hermes.sqncr.ai/Patent_report_kw$WEEK"
echo ""
echo "Next week (KW16): ./rotate_weekly.sh 16"