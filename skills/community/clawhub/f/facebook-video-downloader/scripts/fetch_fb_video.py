#!/usr/bin/env python3
"""
Facebook Video Downloader Script
Fetches video download links from savefbs.com
"""

import sys
import json
import requests
from urllib.parse import quote

def fetch_video_links(fb_url):
    """
    Fetch download links for a Facebook video
    
    Args:
        fb_url: Facebook video URL
        
    Returns:
        dict: Download links with quality options
    """
    
    # First, get the page to establish session
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://savefbs.com',
        'Referer': 'https://savefbs.com/',
        'Content-Type': 'application/json',
    }
    
    # Visit homepage first to get any cookies
    try:
        session.get('https://savefbs.com/', headers=headers, timeout=10)
    except:
        pass
    
    # API endpoint discovered from savefbs.com
    api_url = "https://savefbs.com/api/v1/aio/search"
    
    payload = {
        'vid': fb_url,
        'prefix': 'fb',
        'ex': '',
        'format': ''
    }
    
    try:
        response = session.post(api_url, json=payload, headers=headers, timeout=30)
        
        # Check if we got HTML error page
        content_type = response.headers.get('content-type', '')
        if 'text/html' in content_type:
            return {
                'success': False,
                'error': 'Server returned HTML instead of JSON. The API may require browser-based access.'
            }
        
        response.raise_for_status()
        data = response.json()
        
        # Parse the response - API returns code 0 for success
        if data.get('code') == 0:
            result = {
                'success': True,
                'title': data.get('data', {}).get('title', 'Facebook Video'),
                'thumbnail': data.get('data', {}).get('thumbnail'),
                'downloads': []
            }
            
            # Extract download links
            medias = data.get('data', {}).get('medias', [])
            for media in medias:
                result['downloads'].append({
                    'quality': media.get('quality', 'Unknown'),
                    'url': media.get('url'),
                    'extension': media.get('extension', 'mp4'),
                    'size': media.get('size', 'Unknown')
                })
            
            return result
        else:
            return {
                'success': False,
                'error': data.get('message', 'Failed to fetch video'),
                'code': data.get('code')
            }
            
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP error {e.response.status_code}: {e.response.reason}',
            'details': 'The server may be blocking automated requests. Try using a real Facebook video URL.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Network error: {str(e)}'
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'error': 'Invalid response from server (not JSON)'
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: fetch_fb_video.py <facebook_video_url>'
        }))
        sys.exit(1)
    
    fb_url = sys.argv[1]
    result = fetch_video_links(fb_url)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
