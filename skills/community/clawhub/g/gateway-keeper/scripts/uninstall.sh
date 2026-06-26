#!/usr/bin/env bash
# Uninstall openclaw-gatewaykeeper cron job
CRON_MARKER="# openclaw-openclaw-gatewaykeeper"
(crontab -l 2>/dev/null | grep -v "$CRON_MARKER") | crontab -
echo "Removed openclaw-gatewaykeeper cron job"
