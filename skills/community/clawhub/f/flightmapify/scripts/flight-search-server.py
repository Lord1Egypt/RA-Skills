#!/usr/bin/env python3
"""
Flight search server for FlightMapify skill.
Provides HTTP API endpoint for flight search using FlyAI CLI.
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse

# Add script directory to path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def run_flyai_flight_search(origin, destination, departure_date):
    """
    Run FlyAI CLI flight search command for single trip
    Search both direct and connecting flights to get all results
    """
    try:
        # Set FlyAI API key as environment variable
        env = os.environ.copy()
        
        # Explicitly set home directory for config access
        env['HOME'] = os.path.expanduser('~')
        
        # API key can be set via environment variable to avoid rate limiting
        # export FLYAI_API_KEY=your_api_key_here
        # If not set, try to read from config file
        user_api_key = env.get('FLYAI_API_KEY', '').strip()
        if not user_api_key:
            # Try to read from config file
            try:
                config_path = os.path.expanduser('~/.flyai/config.json')
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                        user_api_key = config_data.get('api-key', '')
            except Exception as e:
                logger.error(f"Failed to read FlyAI config: {e}")
        
        if user_api_key:
            # Use user's API key to avoid rate limiting
            api_key = user_api_key
            env['FLYAI_API_KEY'] = api_key
            env['FLYAI_API_TOKEN'] = api_key
            env['FLYAI_TOKEN'] = api_key
        else:
            # No user API key configured, FlyAI will use built-in default
            # Note: Built-in key may have rate limits
            api_key = ''
        
        all_flights = []
        
        # Search for direct flights (journey-type=1)
        cmd_direct = [
            'flyai', 'search-flight',
            '--origin', origin,
            '--destination', destination,
            '--dep-date', departure_date,
            '--journey-type', '1'
        ]
        
        logger.info(f"Running direct flight search: {' '.join(cmd_direct)}")
        
        result_direct = subprocess.run(
            cmd_direct,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30,
            env=env
        )
        
        if result_direct.returncode == 0:
            try:
                raw_data = json.loads(result_direct.stdout.strip())
                if raw_data.get('status') == 0 and raw_data.get('data') and raw_data['data'].get('itemList'):
                    direct_flights = parse_flight_data(raw_data['data']['itemList'])
                    all_flights.extend(direct_flights)
                    logger.info(f"Found {len(direct_flights)} direct flights")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse direct flight data JSON: {e}")
        
        # Search for connecting flights (journey-type=2)
        cmd_connecting = [
            'flyai', 'search-flight',
            '--origin', origin,
            '--destination', destination,
            '--dep-date', departure_date,
            '--journey-type', '2'
        ]
        
        logger.info(f"Running connecting flight search: {' '.join(cmd_connecting)}")
        
        result_connecting = subprocess.run(
            cmd_connecting,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30,
            env=env
        )
        
        if result_connecting.returncode == 0:
            try:
                raw_data = json.loads(result_connecting.stdout.strip())
                if raw_data.get('status') == 0 and raw_data.get('data') and raw_data['data'].get('itemList'):
                    connecting_flights = parse_flight_data(raw_data['data']['itemList'])
                    all_flights.extend(connecting_flights)
                    logger.info(f"Found {len(connecting_flights)} connecting flights")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse connecting flight data JSON: {e}")
        
        logger.info(f"Total flights found: {len(all_flights)}")
        return {'flights': all_flights}
        
    except subprocess.TimeoutExpired:
        logger.error("Flight search timed out")
        return {"error": "Flight search timed out"}
    except Exception as e:
        logger.error(f"Flight search error: {e}")
        return {"error": str(e)}

def parse_flight_data(item_list):
    """
    Parse flight data from FlyAI response
    """
    flights = []
    for item in item_list:
        if item.get('journeys') and len(item['journeys']) > 0:
            journey = item['journeys'][0]
            segments = journey.get('segments', [])
            if not segments:
                continue
            
            # For all flights, use first segment's departure and last segment's arrival
            first_segment = segments[0]
            last_segment = segments[-1]
            
            dep_city = first_segment.get('depCityName', '')
            dep_station = first_segment.get('depStationName', '')
            arr_city = last_segment.get('arrCityName', '')
            arr_station = last_segment.get('arrStationName', '')
            
            # Parse datetime strings
            dep_datetime = first_segment.get('depDateTime', '')
            arr_datetime = last_segment.get('arrDateTime', '')
            
            # Build flight number and airline info for display
            if len(segments) == 1:
                # Direct flight
                flight_number = first_segment.get('marketingTransportNo', '')
                airline = first_segment.get('marketingTransportName', '')
                journey_type = "直达"
            else:
                # Connecting flight - show all flight numbers
                flight_numbers = [seg.get('marketingTransportNo', '') for seg in segments if seg.get('marketingTransportNo')]
                airlines = [seg.get('marketingTransportName', '') for seg in segments if seg.get('marketingTransportName')]
                flight_number = ", ".join(flight_numbers)
                airline = ", ".join(airlines)
                journey_type = f"中转({len(segments)-1})"
            
            # Get coordinates based on cities (simplified)
            dep_coords = get_city_coordinates(dep_city)
            arr_coords = get_city_coordinates(arr_city)
            
            # Build route path with all segments for connecting flights
            route_path = []
            route_cities = []
            transfer_cities = []
            if len(segments) == 1:
                # Direct flight
                route_path = [
                    [dep_coords[0], dep_coords[1]],
                    [arr_coords[0], arr_coords[1]]
                ]
                route_cities = [dep_city, arr_city]
                transfer_cities = []
            else:
                # Connecting flight - build path through all segments
                route_path = [[dep_coords[0], dep_coords[1]]]  # Start point
                route_cities = [dep_city]
                for i, segment in enumerate(segments):
                    if i < len(segments) - 1:
                        # Add arrival city of this segment (which is departure of next)
                        transfer_city = segment.get('arrCityName', '')
                        transfer_coords = get_city_coordinates(transfer_city)
                        route_path.append([transfer_coords[0], transfer_coords[1]])
                        route_cities.append(transfer_city)
                        transfer_cities.append(transfer_city)
                route_path.append([arr_coords[0], arr_coords[1]])  # End point
                route_cities.append(arr_city)
            
            # Calculate total duration in hours and minutes
            total_duration_minutes = int(item.get('totalDuration', 0))
            duration_hours = total_duration_minutes // 60
            duration_minutes = total_duration_minutes % 60
            duration_str = f"{duration_hours}h{duration_minutes}m" if duration_hours > 0 else f"{duration_minutes}m"
            
            flight_info = {
                'flightNumber': flight_number,
                'airline': airline,
                'origin': f"{dep_city} {dep_station}",
                'destination': f"{arr_city} {arr_station}",
                'departureTime': dep_datetime.split(' ')[1] if ' ' in dep_datetime else dep_datetime,
                'arrivalTime': arr_datetime.split(' ')[1] if ' ' in arr_datetime else arr_datetime,
                'price': f"¥{item.get('ticketPrice', '')}",
                'priceValue': int(float(item.get('ticketPrice', 0))),
                'duration': duration_str,
                'durationMinutes': total_duration_minutes,
                'bookingUrl': item.get('jumpUrl', ''),
                'journeyType': journey_type,
                'departureLng': dep_coords[0],
                'departureLat': dep_coords[1],
                'arrivalLng': arr_coords[0],
                'arrivalLat': arr_coords[1],
                'routePath': route_path,
                'routeCities': route_cities,
                'transferCities': transfer_cities
            }
            logger.info(f"Parsed flight: {dep_city} -> {arr_city}, segments: {len(segments)}, type: {journey_type}")
            flights.append(flight_info)
    
    return flights

def get_city_coordinates(city_name):
    """Get approximate coordinates for major cities (Chinese and International)"""
    city_coords = {
        # Chinese cities
        '北京': ('116.4074', '39.9042'),
        '上海': ('121.4737', '31.2304'),
        '广州': ('113.2644', '23.1291'),
        '深圳': ('114.0579', '22.5431'),
        '杭州': ('120.1551', '30.2741'),
        '成都': ('104.0665', '30.5728'),
        '重庆': ('106.5516', '29.5630'),
        '西安': ('108.9480', '34.2632'),
        '武汉': ('114.3052', '30.5920'),
        '南京': ('118.7969', '32.0603'),
        '天津': ('117.1902', '39.1256'),
        '郑州': ('113.6654', '34.7579'),
        '长沙': ('112.9823', '28.1941'),
        '青岛': ('120.3826', '36.0671'),
        '大连': ('121.6147', '38.9140'),
        '厦门': ('118.0894', '24.4798'),
        '哈尔滨': ('126.6424', '45.7567'),
        '乌鲁木齐': ('87.6168', '43.8256'),
        '阿克苏': ('80.2500', '41.1667'),
        '哈密': ('93.5132', '42.8331'),
        '库尔勒': ('86.1452', '41.7617'),
        '兰州': ('103.8343', '36.0611'),
        '西宁': ('101.7782', '36.6171'),
        '银川': ('106.2309', '38.4872'),
        '呼和浩特': ('111.6708', '40.8414'),
        '贵阳': ('106.6302', '26.6470'),
        '昆明': ('102.7142', '25.0406'),
        '南宁': ('108.3665', '22.8170'),
        '海口': ('110.3310', '20.0444'),
        '三亚': ('109.5117', '18.2528'),
        '福州': ('119.2948', '26.0745'),
        '石家庄': ('114.5149', '38.0428'),
        '太原': ('112.5351', '37.8706'),
        '济南': ('117.0008', '36.6512'),
        '合肥': ('117.2272', '31.8206'),
        '南昌': ('115.8558', '28.6839'),
        '长春': ('125.3235', '43.8171'),
        '沈阳': ('123.4315', '41.8057'),
        '洛阳': ('112.4513', '34.6211'),
        '咸阳': ('108.7066', '34.3284'),
        
        # International cities
        '巴黎': ('2.3522', '48.8566'),
        '伦敦': ('-0.1276', '51.5074'),
        '纽约': ('-74.0060', '40.7128'),
        '东京': ('139.6917', '35.6895'),
        '首尔': ('126.9780', '37.5665'),
        '新加坡': ('103.8198', '1.3521'),
        '悉尼': ('151.2093', '-33.8688'),
        '迪拜': ('55.2708', '25.2048'),
        '曼谷': ('100.5018', '13.7563'),
        '香港': ('114.1694', '22.3193'),
        '澳门': ('113.5491', '22.1987'),
        '台北': ('121.5654', '25.0330'),
        '洛杉矶': ('-118.2437', '34.0522'),
        '旧金山': ('-122.4194', '37.7749'),
        '多伦多': ('-79.3832', '43.6532'),
        '温哥华': ('-123.1207', '49.2827'),
        '柏林': ('13.4050', '52.5200'),
        '罗马': ('12.4964', '41.9028'),
        '马德里': ('-3.7038', '40.4168'),
        '阿姆斯特丹': ('4.9041', '52.3676'),
        '苏黎世': ('8.5417', '47.3769'),
        '莫斯科': ('37.6173', '55.7558'),
        '伊斯坦布尔': ('28.9784', '41.0082'),
        '孟买': ('72.8777', '19.0760'),
        '新德里': ('77.2090', '28.6139'),
        '吉隆坡': ('101.6869', '3.1390'),
        '雅加达': ('106.8456', '-6.2088'),
        '马尼拉': ('120.9842', '14.5995'),
        '河内': ('105.8542', '21.0285'),
        '胡志明市': ('106.6297', '10.8231'),
    }
    
    # Return default coordinates if city not found
    return city_coords.get(city_name, ('116.4074', '39.9042'))

@app.route('/api/flight-search', methods=['GET'])
def flight_search():
    """
    Flight search API endpoint
    Query parameters:
    - origin: departure city/airport code
    - destination: arrival city/airport code  
    - departure-date: YYYY-MM-DD format
    """
    try:
        # Get raw query string - Flask automatically handles URL decoding
        origin = request.args.get('origin', '')
        destination = request.args.get('destination', '')
        departure_date = request.args.get('departure-date', '')
        
        # Flask's request.args already handles URL decoding properly
        # No additional decoding needed for UTF-8 characters
        
        # Validate required parameters
        if not origin or not destination or not departure_date:
            return jsonify({"error": "Missing required parameters: origin, destination, departure-date"}), 400
        
        # Validate date format
        try:
            datetime.strptime(departure_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        # Perform flight search (single trip only)
        flight_data = run_flyai_flight_search(origin, destination, departure_date)
        
        if "error" in flight_data:
            return jsonify(flight_data), 500
        
        return jsonify(flight_data)
        
    except Exception as e:
        logger.error(f"Flight search API error: {e}")
        return jsonify({"error": "Internal server error"}), 500

def is_port_in_use(port):
    """Check if a port is already in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_server(port=8791):
    """Start the flight search server"""
    if is_port_in_use(port):
        logger.info(f"Flight search server already running on port {port}")
        return True
    
    try:
        logger.info(f"Starting flight search server on port {port}")
        app.run(host='localhost', port=port, debug=False, use_reloader=False)
        return True
    except Exception as e:
        logger.error(f"Failed to start flight search server: {e}")
        return False

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Flight Search Server')
    parser.add_argument('--port', type=int, default=8791, help='Server port (default: 8791)')
    args = parser.parse_args()
    
    success = start_server(args.port)
    if not success:
        sys.exit(1)