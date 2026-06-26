#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule Configuration for XI Stock System
羲股票监控系统定时任务配置

This script provides configuration for OpenClaw cron jobs to schedule automatic updates.
本脚本提供OpenClaw定时任务的配置，用于安排自动更新。
"""

import json
from datetime import datetime, timedelta

def generate_cron_config():
    """Generate cron job configuration for OpenClaw"""
    
    config = {
        "name": "XI Stock System - Daily Updates",
        "description": "Automated stock data fetching for A-share market",
        "jobs": [
            {
                "name": "Daily Stock Data Update",
                "description": "Fetch daily data for 10 stocks each time",
                "schedule": {
                    "kind": "cron",
                    "expr": "30 15 * * 1-5",  # 工作日15:30（收盘后）
                    "tz": "Asia/Shanghai"
                },
                "payload": {
                    "kind": "agentTurn",
                    "message": "Run daily stock data update: python day.py get --limit 10",
                    "model": "deepseek-v3.2"
                },
                "sessionTarget": "isolated",
                "delivery": {
                    "mode": "announce",
                    "channel": "telegram"
                }
            },
            {
                "name": "Weekly Reset and Update",
                "description": "Reset week_get and fetch weekly data on Monday",
                "schedule": {
                    "kind": "cron",
                    "expr": "0 9 * * 1",  # 周一9:00
                    "tz": "Asia/Shanghai"
                },
                "payload": {
                    "kind": "agentTurn",
                    "message": "Reset week_get and fetch weekly data: python db_reset.py reset week && python week.py get all --limit 20",
                    "model": "deepseek-v3.2"
                },
                "sessionTarget": "isolated",
                "delivery": {
                    "mode": "announce",
                    "channel": "telegram"
                }
            },
            {
                "name": "Monthly Reset and Update",
                "description": "Reset month_get and fetch monthly data on 1st of month",
                "schedule": {
                    "kind": "cron",
                    "expr": "0 9 1 * *",  # 每月1日9:00
                    "tz": "Asia/Shanghai"
                },
                "payload": {
                    "kind": "agentTurn",
                    "message": "Reset month_get and fetch monthly data: python db_reset.py reset month && python month.py get all --limit 20",
                    "model": "deepseek-v3.2"
                },
                "sessionTarget": "isolated",
                "delivery": {
                    "mode": "announce",
                    "channel": "telegram"
                }
            },
            {
                "name": "Database Status Check",
                "description": "Check database status every day at 10:00",
                "schedule": {
                    "kind": "cron",
                    "expr": "0 10 * * *",  # 每天10:00
                    "tz": "Asia/Shanghai"
                },
                "payload": {
                    "kind": "agentTurn",
                    "message": "Check database status: python db_reset.py reset status",
                    "model": "deepseek-v3.2"
                },
                "sessionTarget": "isolated",
                "delivery": {
                    "mode": "announce",
                    "channel": "telegram"
                }
            }
        ]
    }
    
    return config

def generate_heartbeat_config():
    """Generate heartbeat configuration for periodic checks"""
    
    config = {
        "name": "XI Stock System - Heartbeat Checks",
        "description": "Periodic checks during heartbeats",
        "checks": [
            {
                "name": "Check Database Status",
                "command": "python db_reset.py reset status",
                "frequency": "every_heartbeat",  # 每次心跳时检查
                "condition": "always"
            },
            {
                "name": "Check if Need Daily Update",
                "command": "python day.py get --limit 1 --test-only",
                "frequency": "every_4_hours",
                "condition": "if_business_hours"
            },
            {
                "name": "Check Data Directory",
                "command": "dir D:\\xistock\\day /b | find /c \".txt\"",
                "frequency": "daily",
                "condition": "always"
            }
        ]
    }
    
    return config

def generate_quick_commands():
    """Generate quick commands for manual execution"""
    
    commands = {
        "daily_update_10": "python day.py get --limit 10",
        "daily_update_all": "python day.py get all",
        "weekly_update": "python week.py get all --limit 20",
        "monthly_update": "python month.py get all --limit 20",
        "reset_all": "python db_reset.py reset all",
        "status": "python db_reset.py reset status",
        "fetch_single": "python db_reset.py fetch day 000001",
        "fetch_random": "python db_reset.py fetch day rand --limit 5",
        "parallel_day": "python day_parallel.py",
        "parallel_week": "python week_parallel.py",
        "parallel_month": "python month_parallel.py"
    }
    
    return commands

def main():
    """Main function to display configuration"""
    print("=" * 70)
    print("XI Stock System - Schedule Configuration")
    print("羲股票监控系统 - 定时任务配置")
    print("=" * 70)
    
    # Generate configurations
    cron_config = generate_cron_config()
    heartbeat_config = generate_heartbeat_config()
    quick_commands = generate_quick_commands()
    
    print("\n📅 Cron Job Configuration (for OpenClaw):")
    print("-" * 70)
    for job in cron_config["jobs"]:
        print(f"  • {job['name']}")
        print(f"    时间: {job['schedule']['expr']} ({job['schedule']['tz']})")
        print(f"    命令: {job['payload']['message']}")
        print()
    
    print("\n💓 Heartbeat Checks:")
    print("-" * 70)
    for check in heartbeat_config["checks"]:
        print(f"  • {check['name']}")
        print(f"    频率: {check['frequency']}")
        print(f"    条件: {check['condition']}")
        print(f"    命令: {check['command']}")
        print()
    
    print("\n⚡ Quick Commands (for manual execution):")
    print("-" * 70)
    for name, cmd in quick_commands.items():
        print(f"  {name:20} → {cmd}")
    
    print("\n📋 To add cron jobs to OpenClaw:")
    print("-" * 70)
    print("1. Save this configuration to a file")
    print("2. Use OpenClaw cron tool to add jobs:")
    print("   openclaw cron add --config schedule_config.json")
    print("\n3. Or add manually using OpenClaw web interface")
    print("=" * 70)
    
    # Save configuration to files
    with open("schedule_config.json", "w", encoding="utf-8") as f:
        json.dump(cron_config, f, ensure_ascii=False, indent=2)
    
    with open("quick_commands.json", "w", encoding="utf-8") as f:
        json.dump(quick_commands, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Configuration files saved:")
    print("   - schedule_config.json")
    print("   - quick_commands.json")

if __name__ == "__main__":
    main()