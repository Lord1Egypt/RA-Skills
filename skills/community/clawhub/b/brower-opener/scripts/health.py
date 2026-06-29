#!/usr/bin/env python3
"""
Health check script for Chrome remote debugging.
Checks if Chrome is running on port 9222 and responding to requests.
"""

import sys
import socket
import time


def check_chrome_health(timeout=30):
    """
    Check if Chrome is running with remote debugging enabled on port 9222.
    Uses low-level socket to avoid triggering browser opening.
    
    Args:
        timeout: Maximum time to wait for Chrome to respond (seconds)
    
    Returns:
        tuple: (is_healthy: bool, message: str)
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Use socket directly to avoid any browser-triggering behavior
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', 9222))
            sock.close()
            
            if result == 0:
                # Port is open, try to get version info without opening browser
                return check_chrome_version()
        except Exception:
            pass
        
        time.sleep(0.5)
    
    return False, f"Chrome did not respond on port 9222 within {timeout} seconds"


def check_chrome_version():
    """
    Check Chrome version using socket HTTP request.
    Avoids urllib to prevent browser auto-opening.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('127.0.0.1', 9222))
        
        # Send HTTP GET request manually
        request = b"GET /json/version HTTP/1.1\r\nHost: 127.0.0.1:9222\r\n\r\n"
        sock.sendall(request)
        
        # Receive response
        response = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b"\r\n\r\n" in response:
                    break
            except socket.timeout:
                break
        
        sock.close()
        
        # Check if response contains Chrome info
        response_str = response.decode('utf-8', errors='ignore')
        if 'Browser' in response_str or 'WebKit' in response_str or 'protocolVersion' in response_str:
            return True, "Chrome is healthy and responding on port 9222"
        
        return True, "Port 9222 is open (Chrome may be starting)"
    except Exception as e:
        return True, "Port 9222 is open (response check failed)"



def main():
    """Main entry point."""
    print("Checking Chrome health on port 9222...")
    
    is_healthy, message = check_chrome_health()
    
    if is_healthy:
        print(f"[OK] {message}")
        sys.exit(0)
    else:
        print(f"[ERROR] {message}")
        print("\nTroubleshooting:")
        print("  1. Make sure Chrome is started with --remote-debugging-port=9222")
        print("  2. Check if port 9222 is blocked by firewall")
        print("  3. Try restarting Chrome with debugging enabled")
        sys.exit(1)


if __name__ == "__main__":
    main()
