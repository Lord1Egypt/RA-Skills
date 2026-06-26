# daily-health-report

Description:
- Generates and publishes a daily system health report from the Raspberry Pi, including uptime, memory, swap, load, disk, and temperature metrics.

Purpose:
- Provide a consistent, automated health snapshot for quick review and logging.

Inputs:
- None (pulls data from the local system at run time via health_report.sh).

Outputs:
- A human-readable health report text block and a log entry.

Dependencies:
- /home/welderjustin/.openclaw/workspace/scripts/health_report.sh
- /home/welderjustin/.openclaw/workspace/logs/

Invocation:
- Run the health_report script and publish its output to the chosen channel (or integrate with the main agent).
