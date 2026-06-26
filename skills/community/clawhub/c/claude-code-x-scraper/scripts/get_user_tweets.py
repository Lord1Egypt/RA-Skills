#!/usr/bin/env python3
"""
Get user tweets by username
Convenience wrapper around x_api_client.py
"""

import sys
import json
from x_api_client import XAPIClient


def get_user_tweets(username, max_results=10, exclude_replies=False, exclude_retweets=False):
    """
    Get tweets for a user by username
    
    Args:
        username: X username (with or without @)
        max_results: Number of tweets to fetch (5-100)
        exclude_replies: Exclude reply tweets
        exclude_retweets: Exclude retweets
    
    Returns:
        List of tweet dicts with text, created_at, public_metrics
    """
    client = XAPIClient()
    
    # First get user ID from username
    user_data = client.get_user_by_username(username)
    if 'data' not in user_data:
        raise Exception(f"User not found: {username}")
    
    user_id = user_data['data']['id']
    user_info = user_data['data']
    
    # Get tweets
    tweets_data = client.get_user_tweets(
        user_id, 
        max_results=max_results,
        exclude_replies=exclude_replies,
        exclude_retweets=exclude_retweets
    )
    
    # Format output
    result = {
        'user': {
            'id': user_info['id'],
            'username': user_info['username'],
            'name': user_info.get('name', ''),
            'description': user_info.get('description', ''),
            'verified': user_info.get('verified', False),
            'public_metrics': user_info.get('public_metrics', {})
        },
        'tweets': tweets_data.get('data', []),
        'meta': tweets_data.get('meta', {})
    }
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: get_user_tweets.py <username> [count] [--no-replies] [--no-retweets]")
        sys.exit(1)
    
    username = sys.argv[1].lstrip('@')
    
    # Parse arguments
    count = 10
    no_replies = False
    no_retweets = False
    
    for arg in sys.argv[2:]:
        if arg.isdigit():
            count = int(arg)
        elif arg == '--no-replies':
            no_replies = True
        elif arg == '--no-retweets':
            no_retweets = True
    
    try:
        result = get_user_tweets(username, count, no_replies, no_retweets)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
