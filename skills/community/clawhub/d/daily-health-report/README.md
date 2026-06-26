# daily-health-report

Description:
- Generates and publishes a daily system health report from the Raspberry Pi, including uptime, memory, swap, load, disk, and temperature metrics.

Usage:
- Run: ./scripts/run.sh
- Output: prints the report to stdout and writes latest-health-report.txt in the logs directory.

Dependencies:
- /home/welderjustin/.openclaw/workspace/scripts/health_report.sh
- /home/welderjustin/.openclaw/workspace/logs/

Automation:
- The report can be integrated into a scheduler (cron) to post daily at 3:00 PM MDT. See HEARTBEAT.md for details.

Notes:
- The script prints a human-readable report suitable for chat posting or journaling.
