#!/bin/bash
# Setup Daily Amazon Price Check Cron Job

echo "Setting up daily Amazon price check..."

# Add cron job for 9:00 AM daily
(crontab -l 2>/dev/null; echo "0 9 * * * cd /home/openclaw/workspace/skills/amazon-research/scripts && python3 price_checker.py >> /root/workspace/Projects/Amazon-Research/cron.log 2>&1") | crontab -

echo "✅ Cron job installed!"
echo ""
echo "Schedule: Daily at 9:00 AM"
echo "Log file: ~/workspace/Projects/Amazon-Research/cron.log"
echo ""
echo "To check current cron jobs:"
echo "  crontab -l"
echo ""
echo "To remove:"
echo "  crontab -r"
