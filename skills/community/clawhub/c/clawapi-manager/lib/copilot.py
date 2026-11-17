#!/usr/bin/env python3
"""
Copilot API Adapter
Handles quota queries and account management for Copilot
"""

import os
import sys
import json
import requests
from datetime import datetime

class CopilotAdapter:
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key or os.getenv('COPILOT_API_KEY')
        self.api_url = api_url or os.getenv('COPILOT_API_URL')
        
        if not self.api_key or not self.api_url:
            raise ValueError("COPILOT_API_KEY and COPILOT_API_URL must be set")
    
    def get_quota(self):
        """Query current quota usage"""
        try:
            headers = {
                'Authorization': f'token {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'{self.api_url}/api/quota',
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'provider': 'copilot',
                'status': 'ok',
                'quota': {
                    'used': data.get('usage', 0),
                    'total': data.get('quota', 0),
                    'remaining': data.get('quota', 0) - data.get('usage', 0),
                    'percentage': (data.get('usage', 0) / data.get('quota', 1)) * 100
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'provider': 'copilot',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_health(self):
        """Check API health status"""
        try:
            headers = {
                'Authorization': f'token {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'{self.api_url}/api/health',
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
            
        except:
            return False

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: copilot.py [quota|health]")
        sys.exit(1)
    
    command = sys.argv[1]
    adapter = CopilotAdapter()
    
    if command == 'quota':
        result = adapter.get_quota()
        print(json.dumps(result, indent=2))
    elif command == 'health':
        healthy = adapter.check_health()
        print(json.dumps({'healthy': healthy}))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
