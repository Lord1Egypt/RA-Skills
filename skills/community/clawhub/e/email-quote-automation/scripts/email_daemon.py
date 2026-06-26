#!/usr/bin/env python3
"""
Scheduled background service for periodic email checking
定时检查邮件后台服务
"""

import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))

import config
from email_check import main as check_once

def main():
    interval_minutes = config.SCHEDULE_CONFIG['check_interval_minutes']
    interval_seconds = interval_minutes * 60
    
    print(f"Starting scheduled email checking service, interval = {interval_minutes} minutes")
    print(f"Storage directory: {config.STORAGE_CONFIG['base_path']}")
    print("Press Ctrl+C to stop service")
    print()
    
    try:
        while True:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting check...")
            try:
                check_once()
            except Exception as e:
                print(f"Error during check: {e}")
            
            print(f"Next check in {interval_minutes} minutes...\n")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nService stopped")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
