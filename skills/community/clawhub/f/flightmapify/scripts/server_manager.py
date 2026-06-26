#!/usr/bin/env python3
"""
Server manager for FlightMapify skill.
Manages flight search server with proper port conflict resolution.
"""

import os
import sys
import subprocess
import socket
import time

class ServerManager:
    """Manages flight search server for FlightMapify"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
    def is_port_in_use(self, port: int) -> bool:
        """Check if a port is already in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def find_available_port(self, start_port: int, max_attempts: int = 10) -> int:
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            if not self.is_port_in_use(port):
                return port
        raise RuntimeError(f"No available ports found near {start_port}")
    
    def start_flight_server_if_needed(self, default_port: int = 8791) -> tuple[bool, int]:
        """
        Start flight search server if not already running.
        Returns (success: bool, actual_port: int)
        """
        script_path = os.path.join(self.script_dir, "flight-search-server.py")
        if not os.path.exists(script_path):
            print(f"Warning: Flight search script not found at {script_path}", file=sys.stderr)
            return False, default_port
        
        # Find available port
        try:
            actual_port = self.find_available_port(default_port)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return False, default_port
        
        # Check if server is already running on this port
        if self.is_port_in_use(actual_port):
            # Verify it's actually our server by testing the endpoint
            try:
                import urllib.request
                test_url = f"http://localhost:{actual_port}/api/flight-search?origin=test&destination=test&departure-date=2024-01-01"
                urllib.request.urlopen(test_url, timeout=2)
                print(f"✅ Flight search server already running on port {actual_port}")
                return True, actual_port
            except:
                print(f"Port {actual_port} is occupied by another process", file=sys.stderr)
                return False, default_port
        
        try:
            # Load environment variables from .env file
            env = os.environ.copy()
            env_path = os.path.join(os.path.dirname(self.script_dir), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            if key.startswith('export '):
                                key = key[7:]
                            env[key] = value
            
            # Start the server with environment variables
            cmd = [sys.executable, script_path, str(actual_port)]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp,
                env=env
            )
            
            # Wait for server to start
            time.sleep(1.5)
            
            if process.poll() is None:
                print(f"✅ Started flight search server on port {actual_port}")
                return True, actual_port
            else:
                print(f"❌ Failed to start flight search server on port {actual_port}", file=sys.stderr)
                return False, default_port
                
        except Exception as e:
            print(f"❌ Error starting flight search server: {e}", file=sys.stderr)
            return False, default_port

def main():
    """Test function"""
    manager = ServerManager()
    success, port = manager.start_flight_server_if_needed()
    
    print(f"\nFlight Server Status: {'✅ Running' if success else '❌ Failed'} on port {port}")

if __name__ == '__main__':
    main()