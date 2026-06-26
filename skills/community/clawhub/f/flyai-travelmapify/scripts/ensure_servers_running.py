#!/usr/bin/env python3
"""
Ensure required servers (Amap proxy and Hotel search) are running for flyai-travelmapify.
This script forcefully starts both servers if they're not already running.
"""

import os
import sys
import subprocess
import socket
import time
import signal
from pathlib import Path

# Server configuration - using the correct ports as confirmed
AMAP_PROXY_PORT = 8769
HOTEL_SERVER_PORT = 8780

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Force kill any process running on the specified port"""
    try:
        # Find process using the port
        result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            pid = result.stdout.strip()
            print(f"Killing existing process on port {port} (PID: {pid})")
            os.kill(int(pid), signal.SIGTERM)
            time.sleep(1)
            # Force kill if still running
            if is_port_in_use(port):
                os.kill(int(pid), signal.SIGKILL)
                time.sleep(1)
    except Exception as e:
        print(f"Warning: Could not kill process on port {port}: {e}")

def start_amap_proxy():
    """Start Amap proxy server forcefully"""
    print("Starting Amap proxy server...")
    
    # Kill any existing process on port 8769
    kill_process_on_port(AMAP_PROXY_PORT)
    
    # Start Amap proxy from skill directory
    proxy_script = Path(__file__).parent / "amap-proxy.js"
    if not proxy_script.exists():
        print(f"Error: Amap proxy script not found at {proxy_script}")
        return False
    
    try:
        cmd = ['node', str(proxy_script)]
        proxy_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp
        )
        
        # Wait for server to start
        time.sleep(2)
        
        if is_port_in_use(AMAP_PROXY_PORT):
            print(f"✅ Amap proxy server started successfully on port {AMAP_PROXY_PORT}")
            return True
        else:
            print(f"❌ Failed to start Amap proxy server on port {AMAP_PROXY_PORT}")
            return False
            
    except Exception as e:
        print(f"Error starting Amap proxy server: {e}")
        return False

def start_hotel_server():
    """Start hotel search server forcefully"""
    print("Starting hotel search server...")
    
    # Kill any existing process on port 8780
    kill_process_on_port(HOTEL_SERVER_PORT)
    
    # Start hotel search server
    hotel_script = Path("~/.openclaw/workspace/skills/flyai-travelmapify/scripts/hotel-search-server.py").expanduser()
    if not hotel_script.exists():
        print(f"Error: Hotel search server script not found at {hotel_script}")
        return False
    
    try:
        cmd = [sys.executable, str(hotel_script), str(HOTEL_SERVER_PORT)]
        hotel_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp
        )
        
        # Wait for server to start
        time.sleep(2)
        
        if is_port_in_use(HOTEL_SERVER_PORT):
            print(f"✅ Hotel search server started successfully on port {HOTEL_SERVER_PORT}")
            return True
        else:
            print(f"❌ Failed to start hotel search server on port {HOTEL_SERVER_PORT}")
            return False
            
    except Exception as e:
        print(f"Error starting hotel search server: {e}")
        return False

def main():
    print("🔧 Ensuring required servers are running for flyai-travelmapify...")
    print(f"   Amap Proxy Port: {AMAP_PROXY_PORT}")
    print(f"   Hotel Server Port: {HOTEL_SERVER_PORT}")
    print()
    
    # Check current status
    amap_running = is_port_in_use(AMAP_PROXY_PORT)
    hotel_running = is_port_in_use(HOTEL_SERVER_PORT)
    
    if amap_running and hotel_running:
        print("✅ Both servers are already running!")
        return True
    
    # Start missing servers
    success = True
    
    if not amap_running:
        success &= start_amap_proxy()
    else:
        print(f"✅ Amap proxy server already running on port {AMAP_PROXY_PORT}")
    
    if not hotel_running:
        success &= start_hotel_server()
    else:
        print(f"✅ Hotel search server already running on port {HOTEL_SERVER_PORT}")
    
    if success:
        print("\n🚀 All required servers are now running!")
        return True
    else:
        print("\n❌ Some servers failed to start. Please check the logs above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)