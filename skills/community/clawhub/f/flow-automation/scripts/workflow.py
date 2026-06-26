#!/usr/bin/env python3
"""
Automation Workflow Runner
Executes YAML-defined workflows with triggers and actions
"""

import argparse
import os
import sys
import time
import yaml
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
import ssl

try:
    import requests
except ImportError:
    requests = None


def load_yaml(path):
    """Load workflow YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def load_env(path):
    """Load environment variables from file."""
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip()


def interpolate(template, context):
    """Simple template interpolation."""
    result = template
    for key, val in context.items():
        result = result.replace(f'{{{{{key}}}}}', str(val))
    return result


def get_nested(data, path):
    """Get nested value from dict using dot notation."""
    keys = path.replace('.', '.').split('.')
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k, {})
        elif isinstance(data, list):
            try:
                data = data[int(k)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return data


def execute_http(action, context):
    """Execute HTTP request."""
    config = action.get('config', {})
    url = interpolate(config.get('url', ''), context)
    method = config.get('method', 'GET').upper()
    headers = config.get('headers', {})
    
    # Interpolate headers
    headers = {k: interpolate(v, context) for k, v in headers.items()}
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = Request(url, headers=headers, method=method)
        
        # Handle request body
        if 'body' in config:
            req.data = interpolate(config['body'], context).encode()
            
        with urlopen(req, timeout=30, context=ctx) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
            try:
                return json.loads(body)
            except:
                return {'raw': body}
    except URLError as e:
        return {'error': str(e)}


def execute_telegram(action, context):
    """Send Telegram message."""
    config = action.get('config', {})
    message = interpolate(config.get('message', ''), context)
    chat_id = interpolate(config.get('chat_id', ''), context)
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        return {'error': 'TELEGRAM_BOT_TOKEN not set'}
    
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = Request(url, data=json.dumps(data).encode(), 
                  headers={'Content-Type': 'application/json'})
    
    try:
        with urlopen(req, context=ctx) as resp:
            return json.loads(resp.read())
    except URLError as e:
        return {'error': str(e)}


def execute_transform(action, context):
    """Transform data using template."""
    config = action.get('config', {})
    template = config.get('template', '')
    return interpolate(template, context)


def execute_action(action, context):
    """Execute a single action."""
    action_type = action.get('type', '').lower()
    name = action.get('name', action_type)
    
    if action_type == 'http':
        result = execute_http(action, context)
    elif action_type == 'telegram':
        result = execute_telegram(action, context)
    elif action_type == 'transform':
        result = execute_transform(action, context)
    elif action_type == 'log':
        msg = interpolate(action.get('config', {}).get('message', ''), context)
        print(f"[LOG] {msg}")
        result = {'logged': msg}
    else:
        result = {'error': f'Unknown action type: {action_type}'}
    
    context[f'{name}_result'] = result
    return result


def run_workflow(workflow_path, env_file=None, verbose=False):
    """Run a workflow once."""
    if env_file:
        load_env(env_file)
    
    workflow = load_yaml(workflow_path)
    name = workflow.get('name', 'unnamed')
    
    print(f"[{datetime.now().isoformat()}] Running workflow: {name}")
    
    context = {
        'env': os.environ,
        'workflow': workflow
    }
    
    # Execute actions in order
    for action in workflow.get('actions', []):
        if verbose:
            print(f"  Executing: {action.get('name', 'unnamed')}")
        result = execute_action(action, context)
        if verbose:
            print(f"    Result: {str(result)[:100]}")
    
    print(f"[{datetime.now().isoformat()}] Workflow complete: {name}")
    return context


def parse_cron(cron_str):
    """Parse simple cron expression."""
    # Very simplified - supports: "minute hour * * *"
    parts = cron_str.split()
    if len(parts) >= 5:
        return {
            'minute': parts[0],
            'hour': parts[1],
            'day': parts[2],
            'month': parts[3],
            'weekday': parts[4]
        }
    return None


def run_daemon(workflow_path, env_file=None, verbose=False):
    """Run workflow as daemon with scheduling."""
    workflow = load_yaml(workflow_path)
    trigger = workflow.get('trigger', {})
    trigger_type = trigger.get('type', 'schedule')
    
    if trigger_type != 'schedule':
        print(f"Only schedule trigger supported in daemon mode")
        return
    
    cron_str = trigger.get('cron', '0 * * * *')
    print(f"Starting daemon with schedule: {cron_str}")
    
    while True:
        now = datetime.now()
        # Simple check - in production use proper cron library
        print(f"[{now.isoformat()}] Waiting...")
        time.sleep(60)  # Check every minute
        run_workflow(workflow_path, env_file, verbose)


def main():
    parser = argparse.ArgumentParser(description='Automation Workflow Runner')
    parser.add_argument('--file', required=True, help='Workflow YAML file')
    parser.add_argument('--run-once', action='store_true', help='Run once and exit')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--env', help='Environment variables file')
    parser.add_argument('-v', '--verbose', action='store_true')
    
    args = parser.parse_args()
    
    if args.daemon:
        run_daemon(args.file, args.env, args.verbose)
    else:
        run_workflow(args.file, args.env, args.verbose)


if __name__ == '__main__':
    main()
