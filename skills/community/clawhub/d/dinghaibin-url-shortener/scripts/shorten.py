#!/usr/bin/env python3
"""
URL Shortener - Create short URLs with custom aliases and tracking
"""

import argparse
import hashlib
import json
import os
import random
import string
import sys
from pathlib import Path


DATA_FILE = Path.home() / '.url_shortener.json'


def load_data():
    """Load saved URLs from file."""
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {'urls': {}, 'counter': 0}


def save_data(data):
    """Save URLs to file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def generate_short_code(length=6):
    """Generate a random short code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def shorten_url(url, alias=None):
    """Create a short URL."""
    data = load_data()
    
    # Use alias if provided
    if alias:
        if alias in data['urls']:
            print(f"Error: Alias '{alias}' already exists")
            return None
        short_code = alias
    else:
        # Generate unique code
        while True:
            short_code = generate_short_code()
            if short_code not in data['urls']:
                break
    
    # Store URL
    data['urls'][short_code] = {
        'url': url,
        'clicks': 0,
        'created': str(Path(__file__).stat().st_ctime)
    }
    save_data(data)
    
    return short_code


def list_urls():
    """List all saved URLs."""
    data = load_data()
    
    if not data['urls']:
        print("No URLs saved")
        return
    
    print("\n=== Saved URLs ===")
    for alias, info in data['urls'].items():
        print(f"{alias}: {info['url']}")
        print(f"  Clicks: {info['clicks']}")


def show_stats(alias):
    """Show statistics for a URL."""
    data = load_data()
    
    if alias not in data['urls']:
        print(f"Error: Alias '{alias}' not found")
        return 1
    
    info = data['urls'][alias]
    print(f"\n=== Stats for {alias} ===")
    print(f"URL: {info['url']}")
    print(f"Clicks: {info['clicks']}")
    print(f"Created: {info['created']}")
    return 0


def generate_qr(url, output_file=None):
    """Generate QR code for URL."""
    try:
        import qrcode
        img = qrcode.make(url)
        
        if output_file:
            img.save(output_file)
            print(f"QR code saved to: {output_file}")
        else:
            # Save with default name
            default = 'qrcode.png'
            img.save(default)
            print(f"QR code saved to: {default}")
        
        return 0
    except ImportError:
        print("Error: qrcode not installed. Run: pip install qrcode[pil]")
        return 1
    except Exception as e:
        print(f"Error generating QR: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='URL Shortener')
    parser.add_argument('url', nargs='?', help='URL to shorten')
    parser.add_argument('--alias', help='Custom short alias')
    parser.add_argument('--qr', action='store_true', help='Generate QR code')
    parser.add_argument('--qr-file', help='Save QR code to file')
    parser.add_argument('--list', action='store_true', help='List saved URLs')
    parser.add_argument('--stats', help='Show stats for alias')
    
    args = parser.parse_args()
    
    # List URLs
    if args.list:
        list_urls()
        return 0
    
    # Show stats
    if args.stats:
        return show_stats(args.stats)
    
    # Need URL for other operations
    if not args.url:
        parser.print_help()
        return 1
    
    # Validate URL
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Create short URL
    short_code = shorten_url(url, args.alias)
    if short_code:
        print(f"Short URL: {short_code}")
        
        # Generate QR if requested
        if args.qr or args.qr_file:
            qr_file = args.qr_file or 'qrcode.png'
            generate_qr(url, qr_file)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
