#!/usr/bin/env bash
# Run health report and save latest, plus print to stdout
LOGDIR="/home/welderjustin/.openclaw/workspace/logs"
LATEST="$LOGDIR/latest-health-report.txt"
mkdir -p "$LOGDIR"
/home/welderjustin/.openclaw/workspace/scripts/health_report.sh 2>&1 | tee "$LATEST"
