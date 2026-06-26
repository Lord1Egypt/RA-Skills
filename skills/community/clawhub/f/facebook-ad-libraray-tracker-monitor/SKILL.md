---
name: facebook-ad-tracker-monitor
description: Monitor Facebook ads and advertisers with PPSPY. Create tracking tasks, analyze ad activity over time, inspect landing pages and products, and manage ad monitoring groups.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PPSPY_API_KEY
      bins:
        - npm
    install:
      command: npm
      args:
        - install
        - -g
        - "ppspy-mcp-server@1.0.1"
    primaryEnv: PPSPY_API_KEY
    emoji: "🔍"
    homepage: https://www.ppspy.com
    mcpServers:
      ppspy:
        command: ppspy-mcp-server
        env:
          PPSPY_API_KEY: "{{PPSPY_API_KEY}}"
---

# Facebook Ad Tracker & Monitor

Track Facebook advertisers and monitor ad performance, creatives, landing pages, and linked products over time.

Keywords: Facebook Ad Tracker, Facebook Ad Monitor, Facebook Ad Tracker & Monitor.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (24 total)

### Ad Monitoring (24 tools)
- `ppspy_ad_monitor_create_group` — Create monitoring group
- `ppspy_ad_monitor_group_list` — List all monitoring groups
- `ppspy_ad_monitor_edit_group` — Edit group name
- `ppspy_ad_monitor_delete_group` — Delete group
- `ppspy_ad_monitor_advertiser_search` — Search Facebook advertisers by name
- `ppspy_ad_monitor_create_task` — Create monitoring task(s)
- `ppspy_ad_monitor_task_list` — List monitoring tasks
- `ppspy_ad_monitor_task_set_group` — Assign task to group
- `ppspy_ad_monitor_task_cancel` — Cancel monitoring task
- `ppspy_ad_monitor_task_details` — Get task details
- `ppspy_ad_monitor_task_real_time_overview` — Real-time overview stats
- `ppspy_ad_monitor_task_daily_overview` — Daily overview
- `ppspy_ad_monitor_task_running_overview` — Dashboard stats for running tasks
- `ppspy_ad_monitor_task_landing_page_overview` — Landing page overview
- `ppspy_ad_monitor_task_landing_page_list` — Landing page list with filters
- `ppspy_ad_monitor_task_latest_ad_product` — Latest advertised products
- `ppspy_ad_monitor_task_ad_product_overview` — Product overview by ad count
- `ppspy_ad_monitor_task_ad_product_list` — Product list with filters
- `ppspy_ad_monitor_task_ad_count_stats` — Ad count statistics over time
- `ppspy_ad_monitor_task_ad_deep_analysis` — Ad placement analysis
- `ppspy_ad_monitor_task_ad_content_most_used` — Most used ad copy
- `ppspy_ad_monitor_task_ad_content_longest_run` — Longest running ad content
- `ppspy_ad_monitor_task_ad_list` — Ad list with extensive filters
- `ppspy_ad_monitor_task_ad_details` — Detailed info for a specific monitored ad

## Usage Examples

- "Create a Facebook Ad Tracker task for this advertiser"
- "Show all monitored Facebook ad tasks"
- "Get the most used ad copy for this monitoring task"
- "Analyze landing pages and products linked to this ad monitor"
- "Show ad count trends over time for this advertiser"

## Credits

Each API call consumes credits from your PPSPY account:
- **Ad Monitoring**: 1 monitoring quota per task
- **Detail/Analysis APIs**: Free
