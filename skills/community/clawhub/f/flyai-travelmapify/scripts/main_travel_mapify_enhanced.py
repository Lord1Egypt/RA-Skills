#!/usr/bin/env python3
"""
Enhanced main entry point for Travel Mapify skill.
Supports both image input (OCR extraction) and direct text input (comma-separated locations).
Automatically starts HTTP server and hotel search server when generating maps.
"""

import os
import sys
import json
import argparse
import subprocess
import socket
import time
from typing import List, Dict

# Import configuration module
try:
    from .config import WORKSPACE_DIR, SKILL_DIR, FLYAI_EXECUTABLE, DEFAULT_HTTP_PORT, DEFAULT_HOTEL_PORT, DEFAULT_PROXY_URL
    from .city_detector import get_default_city_for_locations
except ImportError:
    # Fallback if running as standalone script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, SCRIPT_DIR)
    from config import WORKSPACE_DIR, SKILL_DIR, FLYAI_EXECUTABLE, DEFAULT_HTTP_PORT, DEFAULT_HOTEL_PORT, DEFAULT_PROXY_URL
    from city_detector import get_default_city_for_locations

# Script directories (loaded from config module)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def ensure_required_servers_running():
    """Ensure Amap proxy and hotel search servers are running using the dedicated script"""
    ensure_script = os.path.join(SCRIPT_DIR, "ensure_servers_running.py")
    
    if not os.path.exists(ensure_script):
        print(f"Error: Server management script not found at {ensure_script}", file=sys.stderr)
        return False, None
    
    try:
        cmd = [sys.executable, ensure_script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Required servers (Amap proxy + Hotel search) are running")
            # Return success and the configured hotel port
            return True, DEFAULT_HOTEL_PORT
        else:
            print(f"❌ Failed to start required servers:\n{result.stderr}")
            return False, None
            
    except Exception as e:
        print(f"Error running server management script: {e}", file=sys.stderr)
        return False, None

def start_http_server(port=DEFAULT_HTTP_PORT, max_retries=3):
    """Start HTTP server in background with port conflict resolution"""
    current_port = port
    
    for attempt in range(max_retries):
        if is_port_in_use(current_port):
            if attempt == 0:
                print(f"Port {current_port} is in use, checking if it's our HTTP server...")
                # Check if it's actually our server by testing the connection
                try:
                    import urllib.request
                    urllib.request.urlopen(f"http://localhost:{current_port}", timeout=2)
                    print(f"HTTP server already running on port {current_port}")
                    return True, current_port
                except:
                    print(f"Port {current_port} is occupied by another process")
            
            if attempt < max_retries - 1:
                current_port += 1
                print(f"Trying alternative port {current_port}...")
                continue
            else:
                print(f"All ports {port}-{current_port} are occupied. Please free a port or specify a different one.")
                return False, None
        
        try:
            # Start HTTP server in background
            cmd = [sys.executable, "-m", "http.server", str(current_port)]
            http_process = subprocess.Popen(
                cmd,
                cwd=WORKSPACE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp  # Create new process group
            )
            
            # Wait a moment for server to start
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

def parse_text_locations(text_input: str) -> List[Dict]:
    """
    Parse comma-separated location names into POI format
    """
    if not text_input.strip():
        return []
    
    # Split by commas and clean up whitespace
    location_names = [name.strip() for name in text_input.split(',') if name.strip()]
    
    pois = []
    for i, name in enumerate(location_names):
        pois.append({
            'name': name,
            'confidence': 1.0,  # High confidence for direct user input
            'source': 'text_input'
        })
    
    return pois, location_names



def process_text_input(text_input: str, output_json: str):
    """
    Process direct text input of location names
    Returns tuple: (success: bool, location_names: List[str])
    """
    try:
        pois, location_names = parse_text_locations(text_input)
        
        if not pois:
            print("Error: No valid locations found in text input", file=sys.stderr)
            return False, []
        
        # Save to JSON file
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(pois, f, ensure_ascii=False, indent=2)
        
        print(f"Processed {len(pois)} locations from text input")
        return True, location_names
        
    except Exception as e:
        print(f"Error processing text input: {e}", file=sys.stderr)
        return False, []

def generate_map_with_optimized_template(input_json, output_html):
    """Generate map using generic template with unique map ID isolation"""
    try:
        # Use generic template with unique ID generator (primary)
        generate_script = os.path.join(SCRIPT_DIR, 'generate_from_optimized_template.py')
        
        if not os.path.exists(generate_script):
            print(f"Error: Generic template generator not found", file=sys.stderr)
            return False
        
        cmd = [sys.executable, generate_script, input_json, output_html]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Map generation failed: {result.stderr}", file=sys.stderr)
            return False
        
        print(f"Map generated successfully: {output_html}")
        return True
        
    except Exception as e:
        print(f"Error generating map: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Travel Mapify - Create interactive travel maps')
    parser.add_argument('--locations', '-l', required=True, help='Comma-separated location names (direct text input)')
    parser.add_argument('--output-html', '-o', required=True, help='Output HTML file for the travel map')
    parser.add_argument('--city', default='上海', help='Default city for geocoding (default: 上海)')
    parser.add_argument('--proxy-url', default=DEFAULT_PROXY_URL, 
                       help=f'Amap API proxy URL (default: {DEFAULT_PROXY_URL})')
    parser.add_argument('--http-port', type=int, default=DEFAULT_HTTP_PORT, help=f'HTTP server port (default: {DEFAULT_HTTP_PORT})')
    parser.add_argument('--hotel-port', type=int, default=DEFAULT_HOTEL_PORT, help=f'Hotel search server port (default: {DEFAULT_HOTEL_PORT})')
    
    args = parser.parse_args()
    
    # Create temporary JSON file for POIs (in scripts directory to avoid workspace clutter)
    temp_json_basename = os.path.basename(args.output_html).replace('.html', '_pois.json')
    temp_json = os.path.join(SCRIPT_DIR, temp_json_basename)
    
    # Ensure output HTML file is in workspace directory for HTTP server access
    if not os.path.isabs(args.output_html) and '/' not in args.output_html and '\\' not in args.output_html:
        # If output is just a filename (no path), put it in workspace
        final_output_html = os.path.join(WORKSPACE_DIR, args.output_html)
    else:
        final_output_html = args.output_html
    
    # Process text input
    temp_poi_file = temp_json + '.raw_pois.json'
    location_names = []
    
    print(f"Processing text locations: {args.locations}")
    success, location_names = process_text_input(args.locations, temp_poi_file)
    if not success:
        sys.exit(1)
    
    # Auto-detect city from location names if user didn't specify one
    if args.city == '上海':  # Only auto-detect if using default
        detected_city = get_default_city_for_locations(location_names, fallback_city=args.city)
        if detected_city != args.city:
            print(f"Auto-detected city: {detected_city} (from locations: {', '.join(location_names)})")
            final_city = detected_city
        else:
            final_city = args.city
    else:
        final_city = args.city
    
    # Ensure required servers are running BEFORE geocoding/POI search
    print("\nEnsuring required servers are running before POI search...")
    servers_success, actual_hotel_port = ensure_required_servers_running()
    if not servers_success:
        print("Warning: Could not start required servers, geocoding may fail", file=sys.stderr)
    
    # Now geocode the extracted POIs
    print("Geocoding POIs...")
    geocode_script = os.path.join(SCRIPT_DIR, 'geocode_locations.py')
    
    if not os.path.exists(geocode_script):
        print(f"Error: Geocoding script not found: {geocode_script}", file=sys.stderr)
        sys.exit(1)
    
    # Run geocoding
    cmd = [
        sys.executable, geocode_script, temp_poi_file,
        '--output', temp_json,
        '--city', final_city,
        '--proxy-url', args.proxy_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Geocoding failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print("Geocoding completed successfully")
    
    # Clean up temporary raw POI file
    try:
        os.remove(temp_poi_file)
    except:
        pass
    
    # Generate map using optimized template
    print("Generating travel map with optimized template...")
    if not generate_map_with_optimized_template(temp_json, final_output_html):
        sys.exit(1)
    
    # Clean up temporary JSON file
    try:
        os.remove(temp_json)
    except:
        pass
    
    # Start HTTP server (Amap proxy and hotel servers already started before geocoding)
    print("\nStarting HTTP server...")
    http_success, actual_http_port = start_http_server(args.http_port)
    hotel_success = True  # Already ensured before geocoding
    
    # If hotel server started successfully, update the HTML file with the correct port
    # Update HTML file with correct hotel port if needed
    if hotel_success and os.path.exists(final_output_html):
        try:
            with open(final_output_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Replace placeholder with actual hotel port
            updated_html = html_content.replace('HOTEL_SEARCH_PORT_PLACEHOLDER', str(actual_hotel_port))
            
            with open(final_output_html, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"✅ Updated HTML file with hotel server port: {actual_hotel_port}")
        except Exception as e:
            print(f"Warning: Could not update HTML file with correct port: {e}")
    
    if http_success and hotel_success:
        print(f"\n✅ Travel map ready!")
        print(f"🔗 Access your map at: http://localhost:{args.http_port}/{os.path.basename(final_output_html)}")
        print(f"🏨 Hotel search functionality: ACTIVE (port {actual_hotel_port})")
        print(f"🚀 All servers running successfully!")
    else:
        print(f"\n⚠️  Travel map generated but some servers may not be running")
        print(f"🔗 Manual access: http://localhost:{args.http_port}/{os.path.basename(final_output_html)}")
        if not http_success:
            print(f"❌ HTTP server failed to start - please start manually")
        if not hotel_success:
            print(f"❌ Hotel search server failed to start - hotel search may not work")

if __name__ == '__main__':
    main()