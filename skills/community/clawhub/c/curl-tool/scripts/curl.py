#!/usr/bin/env python3
"""Curl Tool - Simple HTTP requests."""

import argparse
import base64
import json
import sys
import urllib.request
import urllib.parse
import urllib.error


def make_request(
    url: str,
    method: str = 'GET',
    data: str = None,
    headers: dict = None,
    user: str = None,
    output: str = None,
    include_headers: bool = False,
    silent: bool = False
) -> bool:
    """Make HTTP request."""
    if headers is None:
        headers = {}
    
    # Build request
    if data and method == 'GET':
        method = 'POST'
    
    req = urllib.request.Request(url, method=method)
    
    # Add headers
    for key, value in headers.items():
        req.add_header(key, value)
    
    # Add data
    if data:
        if isinstance(data, dict):
            data = json.dumps(data)
            if 'Content-Type' not in headers:
                req.add_header('Content-Type', 'application/json')
        req.data = data.encode('utf-8')
    
    # Basic auth
    if user:
        if ':' in user:
            username, password = user.split(':', 1)
        else:
            username, password = user, ''
        credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()
        req.add_header('Authorization', f'Basic {credentials}')
    
    try:
        # Make request
        response = urllib.request.urlopen(req, timeout=30)
        
        # Read response
        body = response.read().decode('utf-8')
        
        # Output
        if output:
            with open(output, 'w') as f:
                f.write(body)
            if not silent:
                print(f"Saved to: {output}")
        else:
            if include_headers:
                print(f"HTTP/1.1 {response.status} {response.reason}")
                for key, value in response.headers.items():
                    print(f"{key}: {value}")
                print()
            print(body)
        
        return True
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        if hasattr(e, 'read'):
            body = e.read().decode('utf-8', errors='replace')
            print(body, file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Simple HTTP client')
    parser.add_argument('url', help='URL to request')
    parser.add_argument('-X', '--method', default='GET', help='HTTP method')
    parser.add_argument('-d', '--data', help='Request body')
    parser.add_argument('-H', '--header', action='append', dest='headers', help='HTTP headers')
    parser.add_argument('-o', '--output', help='Save to file')
    parser.add_argument('-u', '--user', help='Basic auth (user:password)')
    parser.add_argument('-i', '--include', action='store_true', help='Include headers')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent')
    parser.add_argument('--json', dest='json_data', nargs='?', const='{}', help='Send as JSON')
    
    args = parser.parse_args()
    
    # Parse headers
    headers = {}
    if args.headers:
        for h in args.headers:
            if ':' in h:
                key, value = h.split(':', 1)
                headers[key.strip()] = value.strip()
    
    # Parse data
    data = None
    if args.data:
        data = args.data
    
    # Handle JSON data
    if args.json_data is not None:
        headers['Content-Type'] = 'application/json'
        if args.json_data:
            try:
                data = json.loads(args.json_data)
            except:
                data = args.json_data
    
    make_request(
        url=args.url,
        method=args.method,
        data=data,
        headers=headers,
        user=args.user,
        output=args.output,
        include_headers=args.include,
        silent=args.silent
    )


if __name__ == '__main__':
    main()
