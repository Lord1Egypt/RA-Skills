#!/usr/bin/env python3
"""
FlightMapify - Create interactive flight route maps with real-time flight search.
"""

import os
import sys
import json
import argparse
import subprocess
import socket
import time
from typing import List, Dict

def get_workspace_dir():
    """
    Dynamically determine the OpenClaw workspace directory.
    Tries multiple methods to find the correct workspace.
    """
    # Method 1: Check if we're running within OpenClaw context
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    workspace_candidate = os.path.dirname(skill_dir)
    
    # Check if this looks like a valid OpenClaw workspace
    if os.path.exists(os.path.join(workspace_candidate, "AGENTS.md")) or os.path.exists(os.path.join(workspace_candidate, "SOUL.md")):
        return workspace_candidate
    
    # Method 2: Check OPENCLAW_WORKSPACE environment variable
    env_workspace = os.environ.get('OPENCLAW_WORKSPACE')
    if env_workspace and os.path.exists(env_workspace):
        return env_workspace
    
    # Method 3: Check typical OpenClaw workspace locations
    home = os.path.expanduser("~")
    typical_workspaces = [
        os.path.join(home, ".openclaw", "workspace"),
        os.path.join(home, "openclaw", "workspace"),
        os.path.join(home, "Documents", "openclaw", "workspace")
    ]
    
    for candidate in typical_workspaces:
        if os.path.exists(candidate) and os.path.exists(os.path.join(candidate, "AGENTS.md")):
            return candidate
    
    # Method 4: Use current working directory as fallback
    return os.getcwd()

# Script directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = get_workspace_dir()

def ensure_flight_search_server_running(port=8791):
    """Ensure flight search server is running using unified server manager"""
    try:
        # Add scripts directory to path for imports
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        if SCRIPT_DIR not in sys.path:
            sys.path.insert(0, SCRIPT_DIR)
        from server_manager import ServerManager
        manager = ServerManager()
        success, actual_port = manager.start_flight_server_if_needed(port)
        return success, actual_port
    except Exception as e:
        print(f"❌ Error in server management: {e}", file=sys.stderr)
        return False, port

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill the process using the specified port"""
    try:
        # Find the process using the port
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"Killing process {pid} on port {port}...")
                    subprocess.run(['kill', '-9', pid], capture_output=True)
            return True
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")
    return False

def start_http_server(port=9000, max_retries=3):
    """Start HTTP server in background with port conflict resolution"""
    current_port = port
    
    for attempt in range(max_retries):
        if is_port_in_use(current_port):
            if attempt == 0:
                print(f"Port {current_port} is in use, checking if it's our HTTP server...")
                try:
                    import urllib.request
                    urllib.request.urlopen(f"http://localhost:{current_port}", timeout=2)
                    print(f"HTTP server already running on port {current_port}")
                    return True, current_port
                except:
                    print(f"Port {current_port} is occupied by another process, killing it...")
                    if kill_process_on_port(current_port):
                        print(f"Successfully killed process on port {current_port}")
                        time.sleep(1)  # Wait for port to be released
                        continue  # Retry with the same port
                    else:
                        print(f"Failed to kill process on port {current_port}")
            
            if attempt < max_retries - 1:
                current_port += 1
                print(f"Trying alternative port {current_port}...")
                continue
            else:
                print(f"All ports {port}-{current_port} are occupied. Please free a port or specify a different one.")
                return False, None
        
        try:
            cmd = [sys.executable, "-m", "http.server", str(current_port)]
            # Ensure HTTP server runs from workspace directory (dynamic detection)
            http_process = subprocess.Popen(
                cmd,
                cwd=WORKSPACE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )
            time.sleep(1)
            if http_process.poll() is None:
                print(f"HTTP server started successfully on http://localhost:{current_port}")
                return True, current_port
            else:
                print(f"Failed to start HTTP server on port {current_port}")
                if attempt < max_retries - 1:
                    current_port += 1
                    continue
                else:
                    return False, None
                    
        except Exception as e:
            print(f"Error starting HTTP server on port {current_port}: {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                current_port += 1
                continue
            else:
                return False, None
    
    return False, None

def generate_flight_map(origin, destination, travel_date, output_html, flight_port):
    """Generate flight map HTML file"""
    try:
        # Read template
        template_path = os.path.join(SCRIPT_DIR, '../assets/templates/flight-map-template.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace placeholders
        html_content = template_content.replace('ORIGIN_PLACEHOLDER', origin)
        html_content = html_content.replace('DESTINATION_PLACEHOLDER', destination)
        html_content = html_content.replace('DATE_PLACEHOLDER', travel_date)
        html_content = html_content.replace('FLIGHT_SEARCH_PORT_PLACEHOLDER', str(flight_port))
        
        # Handle Amap API key - use default if not provided
        amap_api_key = os.environ.get('AMAP_API_KEY', '88628414733cf2ccb7ce2f94cfd680ef')
        html_content = html_content.replace('AMAP_API_KEY_PLACEHOLDER', amap_api_key)
        
        # Ensure output is in workspace directory (dynamic detection)
        if not os.path.isabs(output_html):
            # If output is just a filename or relative path, put it in workspace
            final_output_html = os.path.join(WORKSPACE_DIR, os.path.basename(output_html))
        else:
            final_output_html = output_html
        
        # Verify workspace directory exists
        if not os.path.exists(WORKSPACE_DIR):
            os.makedirs(WORKSPACE_DIR, exist_ok=True)
        
        # Write HTML file
        with open(final_output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Flight map generated: {final_output_html}")
        print(f"📁 Workspace directory: {WORKSPACE_DIR}")
        return True, final_output_html
        
    except Exception as e:
        print(f"❌ Error generating flight map: {e}", file=sys.stderr)
        return False, None

def main():
    parser = argparse.ArgumentParser(description='FlightMapify - Create interactive flight route maps')
    parser.add_argument('--origin', '-o', required=False, default='', help='Departure city (e.g., "北京")')
    parser.add_argument('--destination', '-d', required=False, default='', help='Arrival city (e.g., "上海")')
    parser.add_argument('--date', '-t', required=False, default='', help='Travel date in YYYY-MM-DD format')
    parser.add_argument('--output', '-f', required=False, default='flight-map.html', help='Output HTML file name')
    parser.add_argument('--port', '-p', type=int, default=9000, help='HTTP server port (default: 9000)')
    parser.add_argument('--flight-port', type=int, default=8791, help='Flight search server port (default: 8791)')
    
    args = parser.parse_args()
    
    # Validate date format if provided
    if args.date:
        try:
            from datetime import datetime
            datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD format.", file=sys.stderr)
            sys.exit(1)
    
    # Start flight search server
    print("🚀 Starting flight search server...")
    flight_success, actual_flight_port = ensure_flight_search_server_running(args.flight_port)
    
    # Generate flight map
    print("🗺️  Generating flight map...")
    success, output_file = generate_flight_map(args.origin, args.destination, args.date, args.output, actual_flight_port)
    if not success:
        sys.exit(1)
    
    # Verify file accessibility
    if not output_file.startswith(WORKSPACE_DIR):
        print(f"⚠️  Warning: Output file may not be accessible via HTTP server")
        print(f"   File: {output_file}")
        print(f"   Workspace: {WORKSPACE_DIR}")
    
    # Start HTTP server
    print("📡 Starting HTTP server...")
    http_success, actual_http_port = start_http_server(args.port)
    
    if http_success and flight_success:
        print(f"\n✅ Flight map ready!")
        print(f"🔗 Access your flight map at: http://localhost:{actual_http_port}/{os.path.basename(output_file)}")
        print(f"✈️  Flight search functionality: ACTIVE (port {actual_flight_port})")
        if args.origin and args.destination and args.date:
            print(f"\n💡 Usage tips:")
            print(f"   - Enter '{args.origin}' in the departure field")
            print(f"   - Enter '{args.destination}' in the arrival field") 
            print(f"   - Select {args.date} as your travel date")
            print(f"   - Click '搜航班' to search for available flights")
        else:
            print(f"\n💡 Usage tips:")
            print(f"   - Enter any departure city in the departure field")
            print(f"   - Enter any destination city in the arrival field") 
            print(f"   - Select your travel date")
            print(f"   - Click '搜航班' to search for available flights")
    else:
        print(f"\n⚠️  Flight map generated but some servers may not be running")
        print(f"🔗 Manual access: http://localhost:{args.port}/{os.path.basename(output_file)}")

if __name__ == '__main__':
    main()