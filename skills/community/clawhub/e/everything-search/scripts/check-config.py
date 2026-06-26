#!/usr/bin/env python3
"""
Configuration check script.

Verifies Everything HTTP Server is properly configured and running.
"""

import sys
import os
import socket
import urllib.request

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import check_connection


def check_process():
    """Check if Everything process is running."""
    print("[1/4] Checking Everything process...")
    
    try:
        import subprocess
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Everything.exe"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "Everything.exe" in result.stdout:
            print("   ✓ Everything is running")
            return True
        else:
            print("   ✗ Everything is NOT running")
            return False
    except Exception as e:
        print(f"   ? Unable to check: {e}")
        return None


def check_port():
    """Check if port 2853 is listening."""
    print("[2/4] Checking port 2853...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('127.0.0.1', 2853))
        sock.close()
        
        if result == 0:
            print("   ✓ Port 2853 is OPEN")
            return True
        else:
            print("   ✗ Port 2853 is CLOSED")
            return False
    except Exception as e:
        print(f"   ? Error checking port: {e}")
        return False


def check_http():
    """Check if HTTP server is responding."""
    print("[3/4] Checking HTTP server...")
    
    try:
        req = urllib.request.Request('http://127.0.0.1:2853/')
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print("   ✓ HTTP server is responding (Status: 200)")
                return True
            else:
                print(f"   ✗ HTTP server returned status: {response.status}")
                return False
    except Exception as e:
        print(f"   ✗ HTTP server error: {e}")
        return False


def check_api():
    """Check if search API is working."""
    print("[4/4] Checking search API...")
    
    try:
        url = 'http://127.0.0.1:2853/?search=test&json=1'
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            import json
            data = json.loads(response.read().decode())
            
            if "totalResults" in data:
                print(f"   ✓ Search API is working (test query returned {data['totalResults']} results)")
                return True
            else:
                print(f"   ✗ Invalid API response")
                return False
    except Exception as e:
        print(f"   ✗ API error: {e}")
        return False


def main():
    print("=" * 60)
    print("Everything Configuration Check")
    print("=" * 60)
    print()
    
    # Run all checks
    process_ok = check_process()
    port_ok = check_port()
    http_ok = check_http()
    api_ok = check_api()
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    checks = [
        ("Everything process", process_ok),
        ("Port 2853", port_ok),
        ("HTTP server", http_ok),
        ("Search API", api_ok),
    ]
    
    all_ok = True
    for name, ok in checks:
        if ok is True:
            print(f"   ✓ {name}")
        elif ok is False:
            print(f"   ✗ {name}")
            all_ok = False
        else:
            print(f"   ? {name} (unknown)")
    
    print()
    
    if all_ok:
        print("✅ Everything is properly configured!")
        return 0
    else:
        print("❌ Configuration issues detected!")
        print()
        print("Troubleshooting:")
        print("1. Make sure Everything is running")
        print("2. Open Everything → Ctrl+P → HTTP Server")
        print("3. Check 'Enable HTTP server' is checked")
        print("4. Set port to 2853")
        print("5. Click OK and restart Everything")
        return 1


if __name__ == "__main__":
    sys.exit(main())
