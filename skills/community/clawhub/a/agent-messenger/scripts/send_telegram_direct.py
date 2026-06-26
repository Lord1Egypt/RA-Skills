#!/usr/bin/env python3
"""
send_telegram_direct.py - Low-level Telegram API sender for agent messages
Bypasses OpenClaw chat resolution, uses bot tokens + user IDs directly
"""

import requests
import json
import sys
import argparse
from pathlib import Path

TELEGRAM_API = "https://api.telegram.org/bot"
CONFIG_FILE = Path("/data/.openclaw/openclaw.json")

def load_config():
    """Load openclaw.json"""
    with open(CONFIG_FILE) as f:
        return json.load(f)

def get_agent_info(config, agent_id):
    """Extract bot token and metadata for an agent"""
    # Find agent
    agent = next((a for a in config['agents']['list'] if a['id'] == agent_id), None)
    if not agent:
        return None
    
    # Find binding
    binding = next((b for b in config['bindings'] if b['agentId'] == agent_id), None)
    if not binding:
        return None
    
    account_id = binding['match'].get('accountId')
    bot_token = config['channels']['telegram']['accounts'][account_id]['botToken']
    
    return {
        'id': agent_id,
        'name': agent.get('name', agent_id),
        'emoji': agent.get('identity', {}).get('emoji', ''),
        'bot_token': bot_token
    }

def send_message(bot_token, user_id, message):
    """Send message via Telegram API"""
    url = f"{TELEGRAM_API}{bot_token}/sendMessage"
    payload = {
        'chat_id': user_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        result = response.json()
        return result.get('ok', False), result.get('description', result.get('error_code'))
    except requests.RequestException as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description='Send messages to OpenClaw agents via Telegram')
    parser.add_argument('message', help='Message to send')
    parser.add_argument('--agents', nargs='+', default=['all'], help='Agent IDs (default: all)')
    parser.add_argument('--user-id', default='8341113912', help='Telegram user ID')
    parser.add_argument('--format', default='{emoji} {name}: {message}', help='Message format')
    parser.add_argument('--vars', nargs='*', default=[], help='Template vars (key=value)')
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    
    # Parse agents
    if args.agents == ['all']:
        agent_ids = [a['id'] for a in config['agents']['list']]
    else:
        agent_ids = args.agents
    
    # Parse template variables
    template_vars = {}
    for var in args.vars:
        if '=' in var:
            key, val = var.split('=', 1)
            template_vars[key] = val
    
    # Apply template
    message = args.message
    for key, val in template_vars.items():
        message = message.replace(f'{{{{{key}}}}}', val)
    
    # Send to agents
    sent = 0
    failed = 0
    
    for agent_id in agent_ids:
        info = get_agent_info(config, agent_id)
        if not info:
            print(f"❌ {agent_id}: Not found in config")
            failed += 1
            continue
        
        # Format message
        formatted = args.format.format(
            emoji=info['emoji'],
            name=info['name'],
            message=message
        )
        
        # Send
        success, error = send_message(info['bot_token'], args.user_id, formatted)
        
        if success:
            print(f"✅ {agent_id} ({info['name']})")
            sent += 1
        else:
            print(f"❌ {agent_id}: {error}")
            failed += 1
    
    print(f"\n📊 Summary: {sent} sent, {failed} failed")
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
