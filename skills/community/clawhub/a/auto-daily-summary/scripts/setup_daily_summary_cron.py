#!/usr/bin/env python3
"""
Auto Daily Summary Cron Setup Script
Cross-platform compatible for OpenClaw environments

This script automatically detects available agents and sets up daily summary cron jobs
for each agent to write their own diary entries at 23:30.

Features:
- Cross-platform compatibility (Windows, Linux, macOS)
- Automatic agent detection via openclaw CLI
- Direct workspace path usage from agents list
- Idempotent operation (safe to run multiple times)
- Configurable timezone and schedule
- Proper duplicate detection using openclaw cron list command
"""

import subprocess
import json
import os
import sys
from pathlib import Path
import re


def get_system_timezone():
    """Get system timezone in IANA format (e.g., Asia/Shanghai)."""
    try:
        # Try to get timezone from /etc/timezone (Linux)
        if os.path.exists('/etc/timezone'):
            with open('/etc/timezone', 'r') as f:
                tz = f.read().strip()
                if tz:
                    return tz
        
        # Try to get timezone from timedatectl (Linux)
        result = subprocess.run(['timedatectl', 'show', '--value', '--property=Timezone'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        
        # Try to get timezone from environment variable
        tz_env = os.environ.get('TZ')
        if tz_env:
            return tz_env
        
        # Fallback to system default
        import time
        local_time = time.localtime()
        if hasattr(time, 'tzname'):
            tz_name = time.tzname[local_time.tm_isdst]
            # Map common timezone names to IANA format
            tz_mapping = {
                'CST': 'Asia/Shanghai',
                'EST': 'America/New_York',
                'PST': 'America/Los_Angeles',
                'GMT': 'Europe/London'
            }
            return tz_mapping.get(tz_name, 'UTC')
        
    except Exception as e:
        print(f"Warning: Could not determine system timezone: {e}")
    
    # Default fallback
    return 'UTC'


def run_openclaw_command(command):
    """Execute openclaw CLI command and return output."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return result
    except Exception as e:
        print(f"Command error: {e}")
        return None


def get_available_agents_with_workspaces():
    """Get list of available agents with their workspace paths from openclaw."""
    result = run_openclaw_command("openclaw agents list --json")
    if result and result.returncode == 0:
        # Extract JSON from output that may contain Doctor messages
        output = result.stdout
        
        # Find JSON array in the output
        json_match = re.search(r'\[.*\]', output, re.DOTALL)
        if json_match:
            try:
                agents_data = json.loads(json_match.group(0))
                agents = []
                for agent in agents_data:
                    if 'id' in agent and 'workspace' in agent:
                        agents.append({
                            'id': agent['id'],
                            'workspace': agent['workspace']
                        })
                return agents
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                return []
        else:
            print("No JSON array found in output")
            return []
    else:
        print(f"Command failed: {result.stderr if result else 'Unknown error'}")
        return []


def get_existing_daily_summary_agents():
    """Get agents that already have daily summary cron jobs using openclaw cron list command."""
    result = run_openclaw_command("openclaw cron list --json")
    if result and result.returncode == 0:
        # Extract JSON from output that may contain Doctor messages
        output = result.stdout
        
        # Find JSON array in the output
        json_match = re.search(r'\[.*\]', output, re.DOTALL)
        if json_match:
            try:
                cron_jobs = json.loads(json_match.group(0))
                existing_agents = set()
                for job in cron_jobs:
                    if isinstance(job, dict) and 'payload' in job and 'message' in job['payload']:
                        message = job['payload']['message']
                        # Check if this is a daily summary message
                        if '请总结今天完成但未记录的任务到你的日记文件' in message and ('YYYY-MM-DD.md' in message or '/daily/' in message):
                            if 'agentId' in job:
                                existing_agents.add(job['agentId'])
                return existing_agents
            except json.JSONDecodeError as e:
                print(f"JSON parse error in cron list: {e}")
                return set()
        else:
            print("No JSON array found in cron list output")
            return set()
    else:
        print(f"Cron list command failed: {result.stderr if result else 'Unknown error'}")
        return set()


def create_cron_job(agent_id, workspace_path, timezone):
    """Create a cron job for the specified agent."""
    # Use YYYY-MM-DD format instead of specific date
    diary_path = f"{workspace_path}/memory/daily/YYYY-MM-DD.md"
    
    # Create the cron job command
    message = f"请总结今天完成但未记录的任务到你的日记文件 {diary_path} 中。将YYYY-MM-DD换成今天的日期。检查是否有重要任务遗漏，确保所有复杂多步任务、跨Agent协作、学习收获都完整记录。"
    
    cron_command = (
        f'openclaw cron add '
        f'--name "Daily Summary - {agent_id}" '
        f'--cron "30 23 * * *" '
        f'--tz "{timezone}" '
        f'--session isolated '
        f'--agent {agent_id} '
        f'--message "{message}" '
        f'--announce'
    )
    
    result = run_openclaw_command(cron_command)
    if result and result.returncode == 0:
        print(f"✓ Daily Summary - {agent_id} created successfully")
        return True
    else:
        print(f"✗ Failed to create cron job for {agent_id}")
        if result:
            print(f"Error: {result.stderr}")
        return False


def main():
    """Main function to set up daily summary cron jobs."""
    # Get system timezone
    system_tz = get_system_timezone()
    print(f"🌍 System timezone detected: {system_tz}")
    
    print("🔍 Detecting available agents with workspaces...")
    agents = get_available_agents_with_workspaces()
    
    if not agents:
        print("⚠️  No agents found. Please ensure OpenClaw is properly configured.")
        return False
    
    print(f"📋 Found {len(agents)} agents with workspaces:")
    for agent in agents:
        print(f"   - {agent['id']}: {agent['workspace']}")
    
    # Check existing cron jobs using openclaw cron list command
    print("🔍 Checking existing cron jobs using openclaw cron list command...")
    existing_agents = get_existing_daily_summary_agents()
    
    # Setup cron jobs for each agent that doesn't already have one
    success_count = 0
    for agent in agents:
        agent_id = agent['id']
        if agent_id in existing_agents:
            print(f"⏭️  Skipping {agent_id} (already configured)")
            success_count += 1
            continue
        
        print(f"🔧 Setting up cron job for {agent_id}...")
        if create_cron_job(agent_id, agent['workspace'], system_tz):
            success_count += 1
    
    print(f"\n✅ Setup complete! {success_count}/{len(agents)} agents configured.")
    return success_count == len(agents)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)