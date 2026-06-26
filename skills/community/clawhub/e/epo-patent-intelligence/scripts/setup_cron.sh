#!/bin/bash
# Setup cron job for weekly patent intelligence automation

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
CRON_LOG="$SKILL_DIR/logs/cron.log"

echo "=== Setting up Weekly Patent Intelligence Cron Job ==="
echo "Skill Directory: $SKILL_DIR"
echo ""

# Create log directory if it doesn't exist
mkdir -p "$SKILL_DIR/logs"

# Create the cron job entry
CRON_ENTRY="0 9 * * 1 cd $SKILL_DIR && ./scripts/weekly_automation_enhanced.sh >> $CRON_LOG 2>&1"

echo "Cron job to be installed:"
echo "  $CRON_ENTRY"
echo ""

# Check if cron is available
if ! command -v crontab &> /dev/null; then
    echo "❌ ERROR: crontab command not found. Cron may not be installed."
    echo "Install cron with: apt-get install cron"
    exit 1
fi

# Check if the cron job already exists
if crontab -l 2>/dev/null | grep -q "weekly_automation_enhanced.sh"; then
    echo "⚠️  Cron job already exists. Removing existing entry..."
    # Remove existing entry
    crontab -l 2>/dev/null | grep -v "weekly_automation_enhanced.sh" | crontab -
fi

# Add the new cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job installed successfully!"
    echo ""
    echo "Cron job details:"
    echo "  • Runs: Every Monday at 9:00 AM"
    echo "  • Command: cd $SKILL_DIR && ./scripts/weekly_automation_enhanced.sh"
    echo "  • Logs: $CRON_LOG"
    echo "  • Next run: $(date -d 'next Monday 9:00' '+%Y-%m-%d %H:%M')"
else
    echo "❌ Failed to install cron job"
    exit 1
fi

echo ""
echo "=== Verification ==="

# List current cron jobs
echo "Current cron jobs:"
crontab -l 2>/dev/null | grep -A2 -B2 "weekly_automation"

# Test the script path
echo ""
echo "Testing script path..."
if [ -f "$SKILL_DIR/scripts/weekly_automation_enhanced.sh" ]; then
    echo "✅ Script found: $SKILL_DIR/scripts/weekly_automation_enhanced.sh"
    
    # Test script permissions
    if [ -x "$SKILL_DIR/scripts/weekly_automation_enhanced.sh" ]; then
        echo "✅ Script is executable"
    else
        echo "⚠️  Script is not executable. Fixing permissions..."
        chmod +x "$SKILL_DIR/scripts/weekly_automation_enhanced.sh"
    fi
else
    echo "❌ Script not found: $SKILL_DIR/scripts/weekly_automation_enhanced.sh"
    echo "Please ensure the enhanced automation script exists."
    exit 1
fi

# Test the .env file
echo ""
echo "Testing environment configuration..."
if [ -f "$SKILL_DIR/.env" ]; then
    echo "✅ .env file found"
    
    # Check if EPO credentials are set
    if grep -q "EPO_CONSUMER_KEY" "$SKILL_DIR/.env" && grep -q "EPO_SECRET_KEY" "$SKILL_DIR/.env"; then
        echo "✅ EPO API credentials found"
    else
        echo "⚠️  EPO API credentials not found in .env"
    fi
    
    # Check permissions
    PERMS=$(stat -c "%a" "$SKILL_DIR/.env")
    if [ "$PERMS" = "600" ]; then
        echo "✅ .env file permissions secure (600)"
    else
        echo "⚠️  .env file permissions are $PERMS (should be 600)"
        echo "Fixing permissions..."
        chmod 600 "$SKILL_DIR/.env"
    fi
else
    echo "❌ .env file not found. Cron job will fail without credentials."
    echo "Create .env file with EPO_CONSUMER_KEY and EPO_CONSUMER_SECRET"
fi

echo ""
echo "=== Next Steps ==="
echo "1. The cron job will run every Monday at 9:00 AM"
echo "2. Check logs at: $CRON_LOG"
echo "3. Monitor system health with: $SKILL_DIR/scripts/health_monitor.sh"
echo "4. For manual testing: cd $SKILL_DIR && ./scripts/weekly_automation_enhanced.sh"

echo ""
echo "=== Setup Complete ==="
echo "Patent Intelligence automation is scheduled for weekly execution."
echo "System will generate reports every Monday morning."