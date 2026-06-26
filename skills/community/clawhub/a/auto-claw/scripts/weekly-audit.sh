#!/bin/bash
# Weekly Audit Cron Wrapper — Auto-Claw
# Generates dynamic log filename based on current date
cd /root/.openclaw/workspace/auto-company/projects/auto-claw
python3 cli.py full-audit > "logs/audit-weekly-$(date +%Y-%m-%d).log" 2>&1
