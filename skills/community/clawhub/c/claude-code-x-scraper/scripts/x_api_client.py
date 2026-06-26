#!/usr/bin/env python3
"""
X (Twitter) API Client for Claude Code
Handles authentication and API calls to X (Twitter) API v2
"""

import os
import sys
import json
import urllib.request
import urllib.error
from urllib.parse import urlencode, quote
from pathlib import Path


class XAPIClient:
    """X API v2 Client"""
    
    BASE_URL = "https://api.twitter.com/2"
    
    def __init__(self, bearer_token=None, credentials_path=None):
        """
        Initialize X API client
        
        Args:
            bearer_token: X API Bearer token (optional if credentials_path provided)
            credentials_path: Path to credentials file (optional)
        """
        self.bearer_token = bearer_token or self._load_bearer_token(credentials_path)
        if not self.bearer_token:
            raise ValueError("Bearer token required. Set X_BEARER_TOKEN env var or provide credentials_path")
    
    def _load_bearer_token(self, credentials_path):
        """Load bearer token from credentials file or environment"""
        # Try environment first
        token = os.getenv('X_BEARER_TOKEN')
        if token:
            # Remove 'Bearer ' prefix if present
            return token.replace('Bearer ', '')
        
        # Try credentials file
        if not credentials_path:
            # Default locations
            possible_paths = [
                Path.home() / '.openclaw' / 'credentials' / 'x_api_tokens.env',
                Path.home() / '.openclaw' / 'credentials' / 'x_credentials.env',
            ]
            for path in possible_paths:
                if path.exists():
                    credentials_path = path
                    break
        
        if credentials_path and Path(credentials_path).exists():
            with open(credentials_path, 'r') as f:
                for line in f:
                    if line.startswith('X_BEARER_TOKEN='):
                        token = line.strip().split('=', 1)[1]
                        return token.replace('Bearer ', '')
        
        return None
    
    def _make_request(self, endpoint, params=None):
        """Make authenticated request to X API"""
        url = f"{self.BASE_URL}{endpoint}"
        if params:
            url += "?" + urlencode(params, quote_via=quote)
        
        # Add Cloudflare Markdown for Agents support
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'text/markdown, text/html, application/json, */*;q=0.8'
        }
        
        request = urllib.request.Request(url, headers=headers)
        
        # Setup proxy handler if HTTPS_PROXY is set
        proxy_handler = None
        https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')
        if https_proxy:
            proxy_handler = urllib.request.ProxyHandler({'https': https_proxy, 'http': https_proxy})
        
        try:
            if proxy_handler:
                opener = urllib.request.build_opener(proxy_handler)
                with opener.open(request) as response:
                    return json.loads(response.read().decode('utf-8'))
            else:
                with urllib.request.urlopen(request) as response:
                    return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                raise Exception(f"X API Error: {error_json.get('title', 'Unknown error')} - {error_json.get('detail', error_body)}")
            except json.JSONDecodeError:
                raise Exception(f"X API Error {e.code}: {error_body}")
    
    def get_user_by_username(self, username):
        """Get user information by username"""
        username = username.lstrip('@')
        endpoint = f"/users/by/username/{username}"
        params = {
            'user.fields': 'created_at,description,public_metrics,verified,verified_type,profile_image_url'
        }
        return self._make_request(endpoint, params)
    
    def get_user_tweets(self, user_id, max_results=10, exclude_replies=False, exclude_retweets=False):
        """
        Get tweets from a user
        
        Args:
            user_id: X user ID
            max_results: Number of tweets to retrieve (5-100, default 10)
            exclude_replies: Whether to exclude replies
            exclude_retweets: Whether to exclude retweets
        """
        endpoint = f"/users/{user_id}/tweets"
        params = {
            'max_results': min(max(max_results, 5), 100),
            'tweet.fields': 'created_at,author_id,public_metrics,source,lang',
            'expansions': 'author_id'
        }
        
        # Build exclude parameter
        excludes = []
        if exclude_replies:
            excludes.append('replies')
        if exclude_retweets:
            excludes.append('retweets')
        if excludes:
            params['exclude'] = ','.join(excludes)
        
        return self._make_request(endpoint, params)
    
    def get_tweet(self, tweet_id):
        """Get a specific tweet by ID"""
        endpoint = f"/tweets/{tweet_id}"
        params = {
            'tweet.fields': 'created_at,author_id,public_metrics,source,lang,entities'
        }
        return self._make_request(endpoint, params)
    
    def search_recent_tweets(self, query, max_results=10):
        """
        Search recent tweets (last 7 days)
        Note: Requires Elevated or Academic access level
        
        Args:
            query: Search query string
            max_results: Number of tweets to retrieve (10-100, default 10)
        """
        endpoint = "/tweets/search/recent"
        params = {
            'query': query,
            'max_results': min(max(max_results, 10), 100),
            'tweet.fields': 'created_at,author_id,public_metrics,lang'
        }
        return self._make_request(endpoint, params)


def main():
    """CLI interface for X API Client"""
    if len(sys.argv) < 2:
        print("Usage: x_api_client.py <command> [args...]")
        print("Commands:")
        print("  user <username>           - Get user info")
        print("  tweets <user_id> [count]  - Get user tweets")
        print("  tweet <tweet_id>          - Get specific tweet")
        print("  search <query> [count]    - Search recent tweets")
        sys.exit(1)
    
    command = sys.argv[1]
    client = XAPIClient()
    
    try:
        if command == 'user':
            if len(sys.argv) < 3:
                print("Usage: x_api_client.py user <username>")
                sys.exit(1)
            result = client.get_user_by_username(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'tweets':
            if len(sys.argv) < 3:
                print("Usage: x_api_client.py tweets <user_id> [count]")
                sys.exit(1)
            user_id = sys.argv[2]
            count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            result = client.get_user_tweets(user_id, max_results=count)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'tweet':
            if len(sys.argv) < 3:
                print("Usage: x_api_client.py tweet <tweet_id>")
                sys.exit(1)
            result = client.get_tweet(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'search':
            if len(sys.argv) < 3:
                print("Usage: x_api_client.py search <query> [count]")
                sys.exit(1)
            query = sys.argv[2]
            count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            result = client.search_recent_tweets(query, max_results=count)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
