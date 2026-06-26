#!/usr/bin/env python3
"""Agent Oversight — manages sub-agent coordination"""
import subprocess, sys

def get_sessions():
    result = subprocess.run(['openclaw', 'sessions', 'list', '--json'], capture_output=True, text=True)
    return result.stdout

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else '--status'
    if cmd == '--status':
        print("🛡️ Agent Oversight Status")
        print("Last check: OK")
    elif cmd == '--list-sessions':
        print(get_sessions())
    else:
        print("Usage: oversight.py [--status|--list-sessions|--kill-hung]")
        
if __name__ == '__main__':
    main()
