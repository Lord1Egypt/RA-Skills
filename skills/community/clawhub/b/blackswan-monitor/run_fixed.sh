#!/bin/bash
# A股黑天鹅监控执行脚本

cd /root/.openclaw/workspace/blackswan-monitor
python3 fixed_monitor.py >> /root/.openclaw/workspace/blackswan_data/cron.log 2>&1
