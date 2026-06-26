#!/bin/bash
# Verify all documentation is complete and accessible

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
VERIFICATION_LOG="$SKILL_DIR/logs/doc_verification_$(date +%Y%m%d_%H%M).log"

echo "=== Documentation Verification ===" | tee "$VERIFICATION_LOG"
echo "Verification started: $(date)" | tee -a "$VERIFICATION_LOG"
echo "Skill directory: $SKILL_DIR" | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

cd "$SKILL_DIR"

# List of required documentation files
declare -A REQUIRED_DOCS=(
    ["SKILL.md"]="Skill definition and usage"
    ["docs/SKILL_ENHANCEMENTS_ITERATION2.md"]="Iteration 2 enhancements"
    ["docs/SYSTEM_HEALTH_REPORT_20260405.md"]="System health report"
    ["docs/MAINTENANCE_PROCEDURES.md"]="Maintenance procedures"
    ["references/AGENT_INTEGRATION.md"]="LLM agent integration"
    ["references/REPORT_FRAMEWORKS.md"]="Report framework guidelines"
    ["research/iteration-1.md"]="Iteration 1 documentation"
    ["research/iteration-2.md"]="Iteration 2 documentation"
    ["research/review_iteration2.md"]="Iteration 2 review"
    ["research/iteration-3-options.md"]="Iteration 3 planning"
)

# List of required script files
declare -A REQUIRED_SCRIPTS=(
    ["scripts/weekly_automation_enhanced.sh"]="Enhanced weekly automation"
    ["scripts/health_monitor.sh"]="Health monitoring"
    ["scripts/setup_cron.sh"]="Cron job setup"
    ["scripts/rotate_weekly.sh"]="Weekly rotation"
    ["scripts/start_tunnel.sh"]="Tunnel startup"
    ["scripts/report_server.py"]="Report server"
    ["scripts/epo_data_mapper.py"]="EPO API integration"
    ["generate_tech_trend_report.py"]="Technology trend generator"
)

echo "1. Checking required documentation files..." | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

ALL_DOCS_OK=true
for doc in "${!REQUIRED_DOCS[@]}"; do
    description="${REQUIRED_DOCS[$doc]}"
    
    if [ -f "$doc" ]; then
        size=$(stat -c%s "$doc" 2>/dev/null || echo "0")
        if [ "$size" -gt 100 ]; then
            echo "   ✅ $doc: $description ($size bytes)" | tee -a "$VERIFICATION_LOG"
        else
            echo "   ⚠️  $doc: $description (too small: $size bytes)" | tee -a "$VERIFICATION_LOG"
            ALL_DOCS_OK=false
        fi
    else
        echo "   ❌ $doc: $description (MISSING)" | tee -a "$VERIFICATION_LOG"
        ALL_DOCS_OK=false
    fi
done

echo "" | tee -a "$VERIFICATION_LOG"
echo "2. Checking required script files..." | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

ALL_SCRIPTS_OK=true
for script in "${!REQUIRED_SCRIPTS[@]}"; do
    description="${REQUIRED_SCRIPTS[$script]}"
    
    if [ -f "$script" ]; then
        if [ -x "$script" ] || [[ "$script" == *.py ]]; then
            size=$(stat -c%s "$script" 2>/dev/null || echo "0")
            echo "   ✅ $script: $description ($size bytes)" | tee -a "$VERIFICATION_LOG"
        else
            echo "   ⚠️  $script: $description (not executable)" | tee -a "$VERIFICATION_LOG"
            chmod +x "$script"
            echo "   ✅ Fixed permissions" | tee -a "$VERIFICATION_LOG"
        fi
    else
        echo "   ❌ $script: $description (MISSING)" | tee -a "$VERIFICATION_LOG"
        ALL_SCRIPTS_OK=false
    fi
done

echo "" | tee -a "$VERIFICATION_LOG"
echo "3. Checking directory structure..." | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

REQUIRED_DIRS=("data" "reports" "logs" "docs" "scripts" "references" "research")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        file_count=$(find "$dir" -type f 2>/dev/null | wc -l)
        echo "   ✅ $dir/: $file_count files" | tee -a "$VERIFICATION_LOG"
    else
        echo "   ❌ $dir/: MISSING" | tee -a "$VERIFICATION_LOG"
        ALL_DOCS_OK=false
    fi
done

echo "" | tee -a "$VERIFICATION_LOG"
echo "4. Checking configuration files..." | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

# Check .env file
if [ -f ".env" ]; then
    perms=$(stat -c "%a" .env)
    if [ "$perms" = "600" ]; then
        echo "   ✅ .env: Configuration file (secure permissions: $perms)" | tee -a "$VERIFICATION_LOG"
    else
        echo "   ⚠️  .env: Insecure permissions ($perms), should be 600" | tee -a "$VERIFICATION_LOG"
        chmod 600 .env
        echo "   ✅ Fixed permissions" | tee -a "$VERIFICATION_LOG"
    fi
else
    echo "   ❌ .env: MISSING (critical)" | tee -a "$VERIFICATION_LOG"
    ALL_DOCS_OK=false
fi

# Check database
if [ -f "data/patents.db" ]; then
    db_size=$(stat -c%s "data/patents.db")
    echo "   ✅ data/patents.db: Database ($db_size bytes)" | tee -a "$VERIFICATION_LOG"
else
    echo "   ❌ data/patents.db: MISSING" | tee -a "$VERIFICATION_LOG"
    ALL_DOCS_OK=false
fi

echo "" | tee -a "$VERIFICATION_LOG"
echo "5. Checking report structure..." | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

# Check reports
REPORT_WEEKS=("kw14" "kw15" "kw16" "kw17")
for week in "${REPORT_WEEKS[@]}"; do
    if [ -d "reports/Patent_report_$week" ]; then
        if [ -f "reports/Patent_report_$week/index.html" ]; then
            size=$(stat -c%s "reports/Patent_report_$week/index.html")
            echo "   ✅ reports/Patent_report_$week/: Dashboard ($size bytes)" | tee -a "$VERIFICATION_LOG"
        else
            echo "   ❌ reports/Patent_report_$week/: Missing index.html" | tee -a "$VERIFICATION_LOG"
            ALL_DOCS_OK=false
        fi
    else
        echo "   ❌ reports/Patent_report_$week/: MISSING" | tee -a "$VERIFICATION_LOG"
        ALL_DOCS_OK=false
    fi
done

# Check reports index
if [ -f "reports/index.html" ]; then
    echo "   ✅ reports/index.html: Reports index" | tee -a "$VERIFICATION_LOG"
else
    echo "   ❌ reports/index.html: MISSING" | tee -a "$VERIFICATION_LOG"
    ALL_DOCS_OK=false
fi

echo "" | tee -a "$VERIFICATION_LOG"
echo "=== Verification Summary ===" | tee -a "$VERIFICATION_LOG"
echo "" | tee -a "$VERIFICATION_LOG"

TOTAL_FILES=$((${#REQUIRED_DOCS[@]} + ${#REQUIRED_SCRIPTS[@]} + ${#REQUIRED_DIRS[@]} + 5))  # +5 for .env, db, reports
echo "Total items checked: $TOTAL_FILES" | tee -a "$VERIFICATION_LOG"

if $ALL_DOCS_OK && $ALL_SCRIPTS_OK; then
    echo "Result: ✅ ALL DOCUMENTATION VERIFIED" | tee -a "$VERIFICATION_LOG"
    echo "All required files are present and accessible." | tee -a "$VERIFICATION_LOG"
    echo "The skill is properly documented for production use." | tee -a "$VERIFICATION_LOG"
else
    echo "Result: ❌ DOCUMENTATION INCOMPLETE" | tee -a "$VERIFICATION_LOG"
    echo "Some required files are missing or incomplete." | tee -a "$VERIFICATION_LOG"
    echo "Check the log for details: $VERIFICATION_LOG" | tee -a "$VERIFICATION_LOG"
fi

echo "" | tee -a "$VERIFICATION_LOG"
echo "Verification completed: $(date)" | tee -a "$VERIFICATION_LOG"
echo "Log file: $VERIFICATION_LOG" | tee -a "$VERIFICATION_LOG"