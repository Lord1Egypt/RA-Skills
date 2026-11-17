#!/usr/bin/env python3
"""
Antigravity API Adapter
Handles quota queries and account management for Antigravity
"""

import os
import sys
import json
import requests
from datetime import datetime

class AntigravityAdapter:
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key or os.getenv('ANTIGRAVITY_API_KEY')
        self.api_url = api_url or os.getenv('ANTIGRAVITY_API_URL')
        
        if not self.api_key or not self.api_url:
            raise ValueError("ANTIGRAVITY_API_KEY and ANTIGRAVITY_API_URL must be set")
    
    def get_quota(self):
        """Query current quota usage"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'{self.api_url}/v1/quota',
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'provider': 'antigravity',
                'status': 'ok',
                'quota': {
                    'used': data.get('used', 0),
                    'total': data.get('total', 0),
                    'remaining': data.get('remaining', 0),
                    'percentage': (data.get('used', 0) / data.get('total', 1)) * 100
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'provider': 'antigravity',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_health(self):
        """Check API health status"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f'{self.api_url}/v1/health',
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
            
        except:
            return False

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: antigravity.py [quota|health]")
        sys.exit(1)
    
    command = sys.argv[1]
    adapter = AntigravityAdapter()
    
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
