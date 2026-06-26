#!/usr/bin/env python3
"""
AIKA GPS Integration Script
ดึงข้อมูล GPS จากระบบ AIKA สำหรับ OpenClaw

Usage: python aika_gps.py [command] [args]
Commands:
  location <device_id>     - Get current location
  nearest <lat> <lng>      - Find nearest technician  
  distance <device_id> <lat> <lng> - Calculate distance
"""

import json
import requests
import sys
import os
from datetime import datetime, timedelta
import math
from bs4 import BeautifulSoup

class AikaGPS:
    def __init__(self, config_path=None):
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), '../references/aika_config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.session = requests.Session()
        self.session.timeout = self.config['aika_settings']['timeout']
        self.last_login = None
        
    def login(self):
        """ล็อกอินเข้าระบบ AIKA"""
        if self.last_login and datetime.now() - self.last_login < timedelta(hours=1):
            return True
            
        # Demo mode - always return True for testing
        if self.config['authentication'].get('demo_mode', False):
            self.last_login = datetime.now()
            return True
            
        try:
            # Try main server first
            login_url = self.config['aika_settings']['server_url'] + self.config['aika_settings']['login_endpoint']
            
            auth_data = {
                'username': self.config['authentication']['username'],
                'password': self.config['authentication']['password']
            }
            
            response = self.session.post(login_url, data=auth_data)
            
            if response.status_code == 200:
                self.last_login = datetime.now()
                return True
            else:
                # Try alternative URL
                login_url = self.config['aika_settings']['alternative_url'] + "/login"
                response = self.session.post(login_url, data=auth_data)
                
                if response.status_code == 200:
                    self.last_login = datetime.now()
                    return True
                    
        except Exception as e:
            print(f"Login failed: {e}")
            
        return False
    
    def get_device_location(self, device_number):
        """ดึงตำแหน่งปัจจุบันของอุปกรณ์"""
        if not self.login():
            return None
            
        try:
            # Try to scrape from AIKA dashboard
            dashboard_url = f"{self.config['aika_settings']['server_url']}/dashboard"
            response = self.session.get(dashboard_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for device data in the page
                # This will need to be adjusted based on actual AIKA HTML structure
                device_elements = soup.find_all(attrs={'data-device': device_number})
                
                if device_elements:
                    device_data = device_elements[0]
                    
                    # Extract GPS coordinates - adjust selectors as needed
                    lat = self.extract_coordinate(device_data, 'latitude')
                    lng = self.extract_coordinate(device_data, 'longitude')
                    speed = self.extract_number(device_data, 'speed')
                    
                    if lat and lng:
                        return {
                            "device_id": f"OBD-{device_number[-5:]}",
                            "device_number": device_number,
                            "latitude": float(lat),
                            "longitude": float(lng), 
                            "speed": float(speed) if speed else 0,
                            "timestamp": datetime.now().isoformat(),
                            "address": self.reverse_geocode(lat, lng),
                            "status": "available" if speed is not None else "offline"
                        }
            
            # Fallback to alternative server
            alt_url = f"{self.config['aika_settings']['alternative_url']}/tracking/{device_number}"
            response = self.session.get(alt_url)
            
            if response.status_code == 200:
                # Try to parse JSON response if available
                try:
                    data = response.json()
                    if 'lat' in data and 'lng' in data:
                        return {
                            "device_id": data.get('device_id', f"OBD-{device_number[-5:]}"),
                            "device_number": device_number,
                            "latitude": float(data['lat']),
                            "longitude": float(data['lng']),
                            "speed": float(data.get('speed', 0)),
                            "timestamp": data.get('timestamp', datetime.now().isoformat()),
                            "address": data.get('address', 'Unknown'),
                            "status": "available"
                        }
                except:
                    # If not JSON, try HTML parsing
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Add specific parsing logic here
                    pass
                    
        except Exception as e:
            print(f"Error getting location for {device_number}: {e}")
            
        return None
    
    def extract_coordinate(self, element, coord_type):
        """Extract latitude or longitude from HTML element"""
        selectors = [
            f'[data-{coord_type}]',
            f'.{coord_type}',
            f'#{coord_type}',
            f'span:contains("{coord_type}")',
        ]
        
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found:
                    return found.get('data-' + coord_type) or found.text.strip()
            except:
                continue
        return None
    
    def extract_number(self, element, data_type):
        """Extract numeric data like speed"""
        selectors = [
            f'[data-{data_type}]',
            f'.{data_type}',
            f'#{data_type}',
        ]
        
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found:
                    value = found.get('data-' + data_type) or found.text.strip()
                    return ''.join(filter(str.isdigit, str(value)))
            except:
                continue
        return None
    
    def reverse_geocode(self, lat, lng):
        """Convert coordinates to address (basic implementation)"""
        try:
            # You could use Google Maps API here for real addresses
            return f"Lat: {lat}, Lng: {lng}"
        except:
            return "Unknown location"
    
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """คำนวณระยะทางระหว่าง 2 จุด (Haversine formula)"""
        R = 6371  # รัศมีโลกเป็นกิโลเมตร
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlng/2) * math.sin(dlng/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return round(distance, 2)
    
    def find_nearest_technician(self, customer_lat, customer_lng, required_skills=None):
        """หาช่างใกล้ที่สุด"""
        devices = self.config['devices']
        results = []
        
        for device_number, device_info in devices.items():
            # Check skills match
            if required_skills:
                has_skills = any(skill in device_info['skills'] for skill in required_skills)
                if not has_skills:
                    continue
                    
            location = self.get_device_location(device_number)
            if location and location['status'] == 'available':
                distance = self.calculate_distance(
                    customer_lat, customer_lng,
                    location['latitude'], location['longitude']
                )
                
                # Estimate ETA (average 40 km/h in city)
                eta_minutes = math.ceil((distance / 40) * 60)
                
                results.append({
                    "driver": device_info['driver'],
                    "device_number": device_number,
                    "distance": distance,
                    "eta_minutes": eta_minutes,
                    "skills": device_info['skills'],
                    "location": location
                })
        
        # Sort by distance
        results.sort(key=lambda x: x['distance'])
        return results

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    aika = AikaGPS()
    
    try:
        if command == "location" and len(sys.argv) >= 3:
            device_number = sys.argv[2]
            location = aika.get_device_location(device_number)
            
            if location:
                print(json.dumps(location, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"error": "Device not found or offline"}, ensure_ascii=False))
                
        elif command == "nearest" and len(sys.argv) >= 4:
            lat = float(sys.argv[2])
            lng = float(sys.argv[3])
            skills = sys.argv[4:] if len(sys.argv) > 4 else None
            
            results = aika.find_nearest_technician(lat, lng, skills)
            print(json.dumps(results, ensure_ascii=False, indent=2))
            
        elif command == "distance" and len(sys.argv) >= 5:
            device_number = sys.argv[2]
            target_lat = float(sys.argv[3])
            target_lng = float(sys.argv[4])
            
            location = aika.get_device_location(device_number)
            if location:
                distance = aika.calculate_distance(
                    location['latitude'], location['longitude'],
                    target_lat, target_lng
                )
                
                result = {
                    "device_number": device_number,
                    "driver": aika.config['devices'][device_number]['driver'],
                    "distance_km": distance,
                    "eta_minutes": math.ceil((distance / 40) * 60)
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"error": "Device not found"}, ensure_ascii=False))
        else:
            print(__doc__)
            
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    main()