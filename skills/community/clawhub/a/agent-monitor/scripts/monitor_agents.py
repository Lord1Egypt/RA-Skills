#!/usr/bin/env python3
"""
Agent Monitor - Agent Work Status Monitoring and Automatic Activation

Features:
1. Monitor agent runtime status
2. Detect "stalled" states where an agent exceeds the idle threshold
3. Automatically send activation messages to resume agent operation

Usage:
    python monitor_agents.py --threshold 300 --auto-activate
    python monitor_agents.py --threshold 300 --dry-run
    python monitor_agents.py --target agent-id-001
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Agent Work Status Monitoring and Automatic Activation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor and automatically activate stalled agents (5-minute threshold)
  python monitor_agents.py --threshold 300 --auto-activate
  
  # Detect only, without automatic activation
  python monitor_agents.py --threshold 300 --dry-run
  
  # Monitor a specific agent
  python monitor_agents.py --target agent-id-001 --auto-activate
        """
    )
    parser.add_argument(
        '--threshold',
        type=int,
        default=300,
        help='Stall determination threshold (seconds), default 300 (5 minutes)'
    )
    parser.add_argument(
        '--auto-activate',
        action='store_true',
        help='Automatically activate stalled agents'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Detect only, do not execute activation'
    )
    parser.add_argument(
        '--target',
        type=str,
        help='Specify a specific agent ID to monitor'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    return parser.parse_args()


def get_agent_list(recent_minutes: int = 30) -> List[Dict[str, Any]]:
    """
    Get list of agents
    
    Note: This function needs to run in an OpenClaw environment and obtain data via tool calls.
    When run standalone, returns mock data for testing.
    """
    # In an actual OpenClaw environment, this would call:
    # subagents(action="list", recentMinutes=recent_minutes)
    
    # Mock data (for testing)
    return [
        {
            "id": "agent-001",
            "status": "running",
            "lastActivity": datetime.now(timezone.utc).isoformat(),
            "task": "Processing documents"
        },
        {
            "id": "agent-002", 
            "status": "idle",
            "lastActivity": (datetime.now(timezone.utc)).isoformat(),
            "task": "Data analysis"
        }
    ]


def calculate_idle_time(last_activity: str) -> float:
    """
    Calculate agent idle time (seconds)
    
    Args:
        last_activity: ISO format time string
        
    Returns:
        Idle time (seconds)
    """
    try:
        last_time = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        idle_seconds = (now - last_time).total_seconds()
        return max(0, idle_seconds)
    except Exception as e:
        print(f"Failed to parse time: {e}", file=sys.stderr)
        return 0


def is_stalled(agent: Dict[str, Any], threshold: int = 300) -> bool:
    """
    Determine if an agent is in a stalled state
    
    Args:
        agent: Agent information dictionary
        threshold: Stall determination threshold (seconds)
        
    Returns:
        Whether the agent is stalled
    """
    last_activity = agent.get('lastActivity')
    if not last_activity:
        return False
    
    idle_time = calculate_idle_time(last_activity)
    return idle_time > threshold


def activate_agent(agent_id: str, message: str = "Please continue executing the task") -> bool:
    """
    Activate an agent
    
    Args:
        agent_id: Agent ID
        message: Activation message
        
    Returns:
        Whether successful
    """
    # In an actual OpenClaw environment, this would call:
    # subagents(action="steer", target=agent_id, message=message)
    
    print(f"  [Activate] Sending message to agent {agent_id}: {message}")
    return True


def format_duration(seconds: float) -> str:
    """Format duration as human-readable string"""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes} minutes {secs} seconds"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours} hours {minutes} minutes"


def monitor_agents(
    threshold: int = 300,
    auto_activate: bool = False,
    dry_run: bool = False,
    target: Optional[str] = None
) -> Dict[str, Any]:
    """
    Monitor agent status
    
    Args:
        threshold: Stall determination threshold (seconds)
        auto_activate: Whether to automatically activate
        dry_run: Whether to detect only without execution
        target: Specific agent ID to monitor
        
    Returns:
        Monitoring result dictionary
    """
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "threshold": threshold,
        "agents_checked": 0,
        "stalled_count": 0,
        "activated_count": 0,
        "agents": []
    }
    
    # Get agent list
    agents = get_agent_list(recent_minutes=30)
    
    print(f"\n🔍 Starting agent status monitoring (Threshold: {format_duration(threshold)})")
    print("-" * 60)
    
    for agent in agents:
        agent_id = agent.get('id', 'unknown')
        
        # If target specified, only monitor the target agent
        if target and agent_id != target:
            continue
        
        result["agents_checked"] += 1
        
        last_activity = agent.get('lastActivity', '')
        idle_time = calculate_idle_time(last_activity)
        stalled = is_stalled(agent, threshold)
        
        agent_result = {
            "id": agent_id,
            "status": agent.get('status', 'unknown'),
            "idle_time": idle_time,
            "stalled": stalled,
            "activated": False
        }
        
        # Display status
        status_icon = "🟢" if not stalled else "🔴"
        print(f"{status_icon} Agent: {agent_id}")
        print(f"   Status: {agent.get('status', 'unknown')}")
        print(f"   Idle time: {format_duration(idle_time)}")
        
        if stalled:
            result["stalled_count"] += 1
            print(f"   ⚠️  Determined as stalled!")
            
            # Auto-activate
            if auto_activate and not dry_run:
                if activate_agent(agent_id):
                    agent_result["activated"] = True
                    result["activated_count"] += 1
                    print(f"   ✅ Activation message sent")
            elif dry_run:
                print(f"   [Dry-run mode] Would send activation message")
        
        result["agents"].append(agent_result)
        print()
    
    # Summary
    print("-" * 60)
    print(f"📊 Monitoring complete: Checked {result['agents_checked']} agent(s)")
    print(f"   Stalled: {result['stalled_count']}")
    if auto_activate and not dry_run:
        print(f"   Activated: {result['activated_count']}")
    print()
    
    return result


def main():
    """Main function"""
    args = parse_args()
    
    # Execute monitoring
    result = monitor_agents(
        threshold=args.threshold,
        auto_activate=args.auto_activate,
        dry_run=args.dry_run,
        target=args.target
    )
    
    # Output results
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Return code: return 1 if there are stalled agents, for script integration
    return 1 if result["stalled_count"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())