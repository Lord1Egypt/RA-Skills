#!/bin/bash
# Test cron job execution simulation
# Simulates the Monday 9:00 AM weekly automation run

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
TEST_LOG="$SKILL_DIR/logs/test_cron_$(date +%Y%m%d_%H%M).log"

echo "=== Testing Cron Job Execution ===" | tee "$TEST_LOG"
echo "Test started: $(date)" | tee -a "$TEST_LOG"
echo "Simulating Monday 9:00 AM weekly automation" | tee -a "$TEST_LOG"
echo "" | tee -a "$TEST_LOG"

# Check if we're in the right directory
echo "1. Checking working directory..." | tee -a "$TEST_LOG"
echo "   Current directory: $(pwd)" | tee -a "$TEST_LOG"
echo "   Skill directory: $SKILL_DIR" | tee -a "$TEST_LOG"

if [ "$(pwd)" = "$SKILL_DIR" ]; then
    echo "   ✅ In correct directory" | tee -a "$TEST_LOG"
else
    echo "   ❌ Not in skill directory" | tee -a "$TEST_LOG"
    echo "   Changing to skill directory..." | tee -a "$TEST_LOG"
    cd "$SKILL_DIR"
fi

# Check if script exists and is executable
echo "" | tee -a "$TEST_LOG"
echo "2. Checking automation script..." | tee -a "$TEST_LOG"
if [ -f "./scripts/weekly_automation_enhanced.sh" ]; then
    echo "   ✅ Script found: weekly_automation_enhanced.sh" | tee -a "$TEST_LOG"
    
    if [ -x "./scripts/weekly_automation_enhanced.sh" ]; then
        echo "   ✅ Script is executable" | tee -a "$TEST_LOG"
    else
        echo "   ❌ Script is not executable" | tee -a "$TEST_LOG"
        chmod +x "./scripts/weekly_automation_enhanced.sh"
        echo "   ✅ Fixed permissions" | tee -a "$TEST_LOG"
    fi
else
    echo "   ❌ Script not found" | tee -a "$TEST_LOG"
    exit 1
fi

# Check .env file
echo "" | tee -a "$TEST_LOG"
echo "3. Checking environment configuration..." | tee -a "$TEST_LOG"
if [ -f ".env" ]; then
    echo "   ✅ .env file found" | tee -a "$TEST_LOG"
    
    # Check permissions
    PERMS=$(stat -c "%a" .env)
    if [ "$PERMS" = "600" ]; then
        echo "   ✅ .env permissions secure (600)" | tee -a "$TEST_LOG"
    else
        echo "   ⚠️  .env permissions are $PERMS (should be 600)" | tee -a "$TEST_LOG"
        chmod 600 .env
        echo "   ✅ Fixed permissions" | tee -a "$TEST_LOG"
    fi
    
    # Check EPO credentials
    if grep -q "EPO_CONSUMER_KEY" .env && grep -q "EPO_SECRET_KEY" .env; then
        echo "   ✅ EPO API credentials found" | tee -a "$TEST_LOG"
    else
        echo "   ❌ EPO API credentials missing" | tee -a "$TEST_LOG"
    fi
else
    echo "   ❌ .env file not found" | tee -a "$TEST_LOG"
    exit 1
fi

# Execute the automation script
echo "" | tee -a "$TEST_LOG"
echo "4. Executing weekly automation script..." | tee -a "$TEST_LOG"
echo "   Command: ./scripts/weekly_automation_enhanced.sh" | tee -a "$TEST_LOG"
echo "" | tee -a "$TEST_LOG"

# Run the script and capture output
START_TIME=$(date +%s)
./scripts/weekly_automation_enhanced.sh 2>&1 | tee -a "$TEST_LOG"
EXIT_CODE=${PIPESTATUS[0]}
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "" | tee -a "$TEST_LOG"
echo "5. Execution results..." | tee -a "$TEST_LOG"
echo "   Exit code: $EXIT_CODE" | tee -a "$TEST_LOG"
echo "   Duration: $DURATION seconds" | tee -a "$TEST_LOG"

if [ $EXIT_CODE -eq 0 ]; then
    echo "   ✅ Script executed successfully" | tee -a "$TEST_LOG"
else
    echo "   ❌ Script execution failed" | tee -a "$TEST_LOG"
fi

# Check results
echo "" | tee -a "$TEST_LOG"
echo "6. Verifying results..." | tee -a "$TEST_LOG"

# Check if report was generated
if [ -f "reports/weekly_report_iteration2.html" ]; then
    REPORT_SIZE=$(stat -c%s "reports/weekly_report_iteration2.html")
    echo "   ✅ Report generated: $REPORT_SIZE bytes" | tee -a "$TEST_LOG"
else
    echo "   ❌ Report not generated" | tee -a "$TEST_LOG"
fi

# Check if analysis request was created
ANALYSIS_COUNT=$(find logs/ -name "analysis_request_*.json" -mmin -5 | wc -l)
if [ $ANALYSIS_COUNT -gt 0 ]; then
    echo "   ✅ Analysis request created" | tee -a "$TEST_LOG"
else
    echo "   ❌ Analysis request not created" | tee -a "$TEST_LOG"
fi

# Check database
PATENT_COUNT=$(python3 -c "
import sqlite3
conn = sqlite3.connect('data/patents.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM patents')
print(cursor.fetchone()[0])
conn.close()
" 2>/dev/null || echo "0")

echo "   ✅ Database contains $PATENT_COUNT patents" | tee -a "$TEST_LOG"

# Check dashboard update
CURRENT_WEEK=$(date +%V)
if [ -f "reports/Patent_report_kw$CURRENT_WEEK/index.html" ]; then
    echo "   ✅ Dashboard KW$CURRENT_WEEK updated" | tee -a "$TEST_LOG"
else
    echo "   ❌ Dashboard not updated" | tee -a "$TEST_LOG"
fi

echo "" | tee -a "$TEST_LOG"
echo "=== Test Summary ===" | tee -a "$TEST_LOG"
echo "Test completed: $(date)" | tee -a "$TEST_LOG"
echo "Log file: $TEST_LOG" | tee -a "$TEST_LOG"

if [ $EXIT_CODE -eq 0 ]; then
    echo "Result: ✅ CRON EXECUTION TEST PASSED" | tee -a "$TEST_LOG"
    echo "The cron job would execute successfully on Monday at 9:00 AM" | tee -a "$TEST_LOG"
else
    echo "Result: ❌ CRON EXECUTION TEST FAILED" | tee -a "$TEST_LOG"
    echo "Check the log file for details: $TEST_LOG" | tee -a "$TEST_LOG"
fi