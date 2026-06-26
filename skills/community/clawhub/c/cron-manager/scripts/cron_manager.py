#!/usr/bin/env python3
"""
Claw Cron Manager — Schedule, monitor, and manage recurring tasks for autonomous agents.

This script provides a file-based cron management system that integrates with OpenClaw agents.
It stores task definitions in JSON and provides command-line interface for managing schedules.

Usage:
    python cron_manager.py <action> [options]

Actions:
    list [--status all|active|paused|failed]  List all cron tasks
    show <task_id>                            Show task details and recent runs
    add <name> --command "<cmd>" --schedule "<pattern>"  Add new task
    remove <task_id>                          Delete a task
    pause <task_id>                           Pause task execution
    resume <task_id>                          Resume paused task
    run <task_id>                             Force run a task immediately
    logs <task_id> [--count 10]               View recent execution logs
    stats [--hours 168]                       Show execution statistics
    health                                    Overall system health check
"""

import json
import os
import sys
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import re
import pytz

# Configuration
DATA_DIR = os.environ.get('CRON_DATA_DIR', str(Path.home() / '.openclaw' / 'workspace' / 'skills' / 'cron-manager' / 'data'))
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')


def init_dirs():
    """Initialize data directories if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)


def load_tasks() -> list:
    """Load tasks from JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks: list):
    """Save tasks to JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


def parse_schedule(schedule_str: str) -> Optional[dict]:
    """
    Parse a schedule string into a cron-like structure.
    Supports standard cron patterns and human-friendly formats.
    """
    schedule_str = schedule_str.strip()
    
    # Handle shorthands
    shorthand_patterns = {
        '@hourly': {'minute': '*', 'hour': '*', 'day': '*', 'month': '*', 'weekday': '*'},
        '@daily': {'minute': '0', 'hour': '0', 'day': '*', 'month': '*', 'weekday': '*'},
        '@weekly': {'minute': '0', 'hour': '0', 'day': '*', 'month': '*', 'weekday': '1'},
        '@monthly': {'minute': '0', 'hour': '0', 'day': '1', 'month': '*', 'weekday': '*'},
        '@yearly': {'minute': '0', 'hour': '0', 'day': '1', 'month': '1', 'weekday': '*'},
    }
    
    if schedule_str.lower() in shorthand_patterns:
        return shorthand_patterns[schedule_str.lower()]
    
    # Parse standard 5-field cron pattern
    fields = schedule_str.split()
    if len(fields) == 5:
        return {
            'minute': fields[0],
            'hour': fields[1],
            'day': fields[2],
            'month': fields[3],
            'weekday': fields[4]
        }
    
    # Try human-friendly format
    human_patterns = [
        (r'every\s+(\d+)\s+minutes', lambda m: {'minute': '*/' + m.group(1), 'hour': '*', 'day': '*', 'month': '*', 'weekday': '*'}),
        (r'every\s+(\d+)\s+hours', lambda m: {'minute': '0', 'hour': '*/' + m.group(1), 'day': '*', 'month': '*', 'weekday': '*'}),
        (r'daily\s+at\s+(\d+):?(\d*)', lambda m: {'minute': m.group(2) or '0', 'hour': m.group(1), 'day': '*', 'month': '*', 'weekday': '*'}),
        (r'weekly\s+on\s+(\w+)\s+at\s+(\d+):?(\d*)', lambda m: {'minute': m.group(3) or '0', 'hour': m.group(2), 'day': '*', 'month': '*', 'weekday': str(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'].index(m.group(1).lower()) + 1)}),
        (r'every\s+monday', lambda m: {'minute': '0', 'hour': '0', 'day': '*', 'month': '*', 'weekday': '1'}),
    ]
    
    for pattern, handler in human_patterns:
        match = re.search(pattern, schedule_str.lower())
        if match:
            return handler(match)
    
    return None


def next_run_time(schedule: dict, timezone: str = 'UTC', after: datetime = None) -> Optional[datetime]:
    """Calculate the next run time based on schedule pattern."""
    if after is None:
        after = datetime.now(pytz.UTC)
    
    try:
        tz = pytz.timezone(timezone)
        after = tz.fromutc(after)
    except:
        tz = pytz.UTC
    
    # Simple implementation: check every minute for next match
    current = after.replace(second=0, microsecond=0)
    for _ in range(525600):  # Max 1 year of minutes
        if (current.minute % (int(schedule['minute'].split('/')[-1]) if '/' in schedule['minute'] else 60) == 0 and
            current.hour % (int(schedule['hour'].split('/')[-1]) if '/' in schedule['hour'] else 24) == 0 and
            current.day % (int(schedule['day'].split('/')[-1]) if '/' in schedule['day'] else 31) == 0 and
            current.month % (int(schedule['month'].split('/')[-1]) if '/' in schedule['month'] else 12) == 0 and
            current.weekday() % (int(schedule['weekday'].split('/')[-1]) if '/' in schedule['weekday'] else 7) == 0):
            return current
        current += timedelta(minutes=1)
    
    return None


def get_task_logs(task_id: str) -> list:
    """Get execution logs for a task."""
    log_file = os.path.join(LOGS_DIR, f"{task_id}.jsonl")
    if not os.path.exists(log_file):
        return []
    
    with open(log_file, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]


def add_log_entry(task_id: str, entry: dict):
    """Add a log entry for task execution."""
    log_file = os.path.join(LOGS_DIR, f"{task_id}.jsonl")
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')


def cmd_list(args):
    """List all cron tasks."""
    tasks = load_tasks()
    status_filter = getattr(args, 'status', None)
    
    if status_filter and status_filter != 'all':
        tasks = [t for t in tasks if t.get('status') == status_filter]
    
    result = []
    for task in tasks:
        task_info = {
            'id': task['id'],
            'name': task['name'],
            'status': task['status'],
            'schedule': task['schedule'],
            'last_run': task.get('last_run', 'never'),
            'success_rate': task.get('success_rate', 0),
        }
        
        # Calculate next run
        if task.get('schedule_parsed') and task['status'] == 'active':
            next_run = next_run_time(task['schedule_parsed'], task.get('timezone', 'UTC'))
            task_info['next_run'] = next_run.isoformat() if next_run else 'unknown'
        
        result.append(task_info)
    
    return {'status': 'success', 'data': {'tasks': result}}


def cmd_show(args):
    """Show task details and recent runs."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == args.task_id), None)
    
    if not task:
        return {'status': 'error', 'message': f'Task {args.task_id} not found'}
    
    logs = get_task_logs(args.task_id)
    recent = logs[-5:] if logs else []
    
    return {
        'status': 'success',
        'data': {
            'task': task,
            'recent_runs': recent
        }
    }


def cmd_add(args):
    """Add a new cron task."""
    tasks = load_tasks()
    
    # Check for duplicate ID
    if any(t['id'] == args.name for t in tasks):
        return {'status': 'error', 'message': f'Task {args.name} already exists'}
    
    schedule = parse_schedule(args.schedule)
    if not schedule:
        return {'status': 'error', 'message': f'Failed to parse schedule: {args.schedule}'}
    
    new_task = {
        'id': args.name,
        'name': args.name,
        'command': args.command,
        'schedule': args.schedule,
        'schedule_parsed': schedule,
        'timezone': args.timezone or 'UTC',
        'status': 'active',
        'created_at': datetime.now(pytz.UTC).isoformat(),
        'last_run': None,
        'success_count': 0,
        'failure_count': 0,
        'total_runs': 0,
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    
    return {
        'status': 'success',
        'message': f'Task {args.name} added successfully',
        'data': new_task
    }


def cmd_remove(args):
    """Remove a cron task."""
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != args.task_id]
    save_tasks(tasks)
    
    # Clean up logs
    log_file = os.path.join(LOGS_DIR, f"{args.task_id}.jsonl")
    if os.path.exists(log_file):
        os.remove(log_file)
    
    return {'status': 'success', 'message': f'Task {args.task_id} removed'}


def cmd_pause(args):
    """Pause a cron task."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == args.task_id), None)
    
    if not task:
        return {'status': 'error', 'message': f'Task {args.task_id} not found'}
    
    task['status'] = 'paused'
    save_tasks(tasks)
    
    return {'status': 'success', 'message': f'Task {args.task_id} paused'}


def cmd_resume(args):
    """Resume a paused cron task."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == args.task_id), None)
    
    if not task:
        return {'status': 'error', 'message': f'Task {args.task_id} not found'}
    
    task['status'] = 'active'
    save_tasks(tasks)
    
    return {'status': 'success', 'message': f'Task {args.task_id} resumed'}


def cmd_run(args):
    """Force run a task immediately."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == args.task_id), None)
    
    if not task:
        return {'status': 'error', 'message': f'Task {args.task_id} not found'}
    
    # Execute the command
    start = datetime.now(pytz.UTC)
    try:
        result = subprocess.run(task['command'], shell=True, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0
        output = result.stdout[-1000:] if result.stdout else ''
        error = result.stderr[-1000:] if result.stderr else ''
    except Exception as e:
        success = False
        output = ''
        error = str(e)
    
    end = datetime.now(pytz.UTC)
    
    # Update task stats
    task['last_run'] = start.isoformat()
    task['total_runs'] = task.get('total_runs', 0) + 1
    
    if success:
        task['success_count'] = task.get('success_count', 0) + 1
    else:
        task['failure_count'] = task.get('failure_count', 0) + 1
    
    task['success_rate'] = task['success_count'] / task['total_runs'] if task['total_runs'] > 0 else 0
    
    save_tasks(tasks)
    
    # Log the execution
    add_log_entry(args.task_id, {
        'run_at': start.isoformat(),
        'completed_at': end.isoformat(),
        'success': success,
        'output': output,
        'error': error,
    })
    
    return {
        'status': 'success',
        'message': f'Task {args.task_id} executed {"successfully" if success else "with errors"}',
        'data': {
            'success': success,
            'output': output,
            'error': error,
            'duration': (end - start).total_seconds()
        }
    }


def cmd_logs(args):
    """View recent execution logs for a task."""
    logs = get_task_logs(args.task_id)
    count = args.count or 10
    
    return {
        'status': 'success',
        'data': {
            'logs': logs[-count:]
        }
    }


def cmd_stats(args):
    """Show execution statistics."""
    tasks = load_tasks()
    hours = args.hours or 168  # Default to 1 week
    
    total_runs = sum(t.get('total_runs', 0) for t in tasks)
    total_success = sum(t.get('success_count', 0) for t in tasks)
    total_failure = sum(t.get('failure_count', 0) for t in tasks)
    
    success_rate = total_success / total_runs if total_runs > 0 else 0
    
    # Recent runs in the last N hours
    cutoff = datetime.now(pytz.UTC) - timedelta(hours=hours)
    recent_runs = []
    for task in tasks:
        logs = get_task_logs(task['id'])
        for log in logs:
            if datetime.fromisoformat(log['run_at']) > cutoff:
                recent_runs.append({
                    'task_id': task['id'],
                    'run_at': log['run_at'],
                    'success': log['success'],
                })
    
    return {
        'status': 'success',
        'data': {
            'total_tasks': len(tasks),
            'active_tasks': len([t for t in tasks if t['status'] == 'active']),
            'paused_tasks': len([t for t in tasks if t['status'] == 'paused']),
            'total_runs': total_runs,
            'recent_runs': len(recent_runs),
            'overall_success_rate': round(success_rate * 100, 2),
            'period_hours': hours,
        }
    }


def cmd_health(args):
    """Run overall system health check."""
    tasks = load_tasks()
    
    # Check for tasks with low success rates
    failed_tasks = [t for t in tasks if t.get('total_runs', 0) > 0 and 
                    (t.get('success_count', 0) / t['total_runs'] < 0.5)]
    
    # Check for stale logs
    stale_threshold = datetime.now(pytz.UTC) - timedelta(days=7)
    stale_count = 0
    
    # Check disk space
    disk_usage = subprocess.run(['df', '-h', DATA_DIR], capture_output=True, text=True)
    
    health_issues = []
    if failed_tasks:
        health_issues.append(f'{len(failed_tasks)} task(s) with low success rate')
    
    return {
        'status': 'healthy' if not health_issues else 'degraded',
        'message': 'All systems operational' if not health_issues else '; '.join(health_issues),
        'data': {
            'total_tasks': len(tasks),
            'active_tasks': len([t for t in tasks if t['status'] == 'active']),
            'failed_tasks': len(failed_tasks),
            'disk_usage': disk_usage.stdout.strip(),
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Claw Cron Manager')
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # List
    list_parser = subparsers.add_parser('list', help='List all cron tasks')
    list_parser.add_argument('--status', choices=['all', 'active', 'paused', 'failed'], default='all')
    
    # Show
    show_parser = subparsers.add_parser('show', help='Show task details')
    show_parser.add_argument('task_id', help='Task ID')
    
    # Add
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('name', help='Task name/ID')
    add_parser.add_argument('--command', required=True, help='Command to execute')
    add_parser.add_argument('--schedule', required=True, help='Schedule pattern')
    add_parser.add_argument('--timezone', default='UTC', help='Timezone')
    
    # Remove
    remove_parser = subparsers.add_parser('remove', help='Remove a task')
    remove_parser.add_argument('task_id', help='Task ID')
    
    # Pause
    pause_parser = subparsers.add_parser('pause', help='Pause a task')
    pause_parser.add_argument('task_id', help='Task ID')
    
    # Resume
    resume_parser = subparsers.add_parser('resume', help='Resume a paused task')
    resume_parser.add_argument('task_id', help='Task ID')
    
    # Run
    run_parser = subparsers.add_parser('run', help='Force run a task')
    run_parser.add_argument('task_id', help='Task ID')
    
    # Logs
    logs_parser = subparsers.add_parser('logs', help='View task logs')
    logs_parser.add_argument('task_id', help='Task ID')
    logs_parser.add_argument('--count', type=int, default=10, help='Number of recent logs')
    
    # Stats
    stats_parser = subparsers.add_parser('stats', help='Show execution statistics')
    stats_parser.add_argument('--hours', type=int, default=168, help='Number of hours to look back')
    
    # Health
    health_parser = subparsers.add_parser('health', help='System health check')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        sys.exit(1)
    
    init_dirs()
    
    # Dispatch to appropriate command
    commands = {
        'list': cmd_list,
        'show': cmd_show,
        'add': cmd_add,
        'remove': cmd_remove,
        'pause': cmd_pause,
        'resume': cmd_resume,
        'run': cmd_run,
        'logs': cmd_logs,
        'stats': cmd_stats,
        'health': cmd_health,
    }
    
    handler = commands.get(args.action)
    if handler:
        result = handler(args)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
