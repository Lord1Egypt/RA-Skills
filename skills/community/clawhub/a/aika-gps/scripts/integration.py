#!/usr/bin/env python3
"""
AIKA GPS Integration for OpenClaw
ฟังก์ชันสำหรับให้ OpenClaw เรียกใช้งาน GPS
"""

import subprocess
import json
import os
import sys

class AikaGPSIntegration:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.aika_script = os.path.join(self.script_dir, 'aika_gps.py')
    
    def get_technician_location(self, technician_name):
        """ดึงตำแหน่งช่างจากชื่อ"""
        # Map ชื่อช่างเป็น Device Number
        technician_map = {
            'ช่างโต้': '7028888047',
            'โต้': '7028888047',
            'ช่างรุ่ง': 'TO_BE_ADDED',
            'รุ่ง': 'TO_BE_ADDED', 
            'ช่างเม่ง': 'TO_BE_ADDED',
            'เม่ง': 'TO_BE_ADDED'
        }
        
        device_number = technician_map.get(technician_name)
        if not device_number or device_number == 'TO_BE_ADDED':
            return {"error": f"ไม่พบข้อมูล GPS สำหรับ {technician_name}"}
        
        return self.run_aika_command(['location', device_number])
    
    def find_nearest_technician(self, customer_address, required_skills=None):
        """หาช่างใกล้ที่สุด"""
        # Convert address to coordinates (simplified)
        coordinates = self.address_to_coordinates(customer_address)
        if not coordinates:
            return {"error": "ไม่สามารถหาพิกัดของที่อยู่ได้"}
        
        cmd = ['nearest', str(coordinates['lat']), str(coordinates['lng'])]
        if required_skills:
            if isinstance(required_skills, str):
                required_skills = [required_skills]
            cmd.extend(required_skills)
        
        return self.run_aika_command(cmd)
    
    def calculate_distance_eta(self, technician_name, customer_address):
        """คำนวณระยะทางและเวลา"""
        coordinates = self.address_to_coordinates(customer_address)
        if not coordinates:
            return {"error": "ไม่สามารถหาพิกัดได้"}
        
        technician_map = {
            'ช่างโต้': '7028888047',
            'โต้': '7028888047',
        }
        
        device_number = technician_map.get(technician_name)
        if not device_number:
            return {"error": f"ไม่พบข้อมูลช่าง {technician_name}"}
        
        cmd = ['distance', device_number, str(coordinates['lat']), str(coordinates['lng'])]
        return self.run_aika_command(cmd)
    
    def run_aika_command(self, cmd_args):
        """รันคำสั่ง AIKA GPS script"""
        try:
            cmd = ['python', self.aika_script] + cmd_args
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"Command failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Integration error: {str(e)}"}
    
    def address_to_coordinates(self, address):
        """แปลงที่อยู่เป็นพิกัด (simplified mapping)"""
        # ข้อมูล mapping พื้นฐาน - จริงๆ ควรใช้ Google Maps API
        address_map = {
            'อบต.สระคู': {'lat': 16.4500, 'lng': 103.7000},
            'อบต.น้ำคำ': {'lat': 16.4200, 'lng': 103.6800},
            'อัยการจังหวัดร้อยเอ็ด': {'lat': 16.0500, 'lng': 103.6500},
            'ร้อยเอ็ด': {'lat': 16.0563, 'lng': 103.6531},
            'สุวรรณภูมิ': {'lat': 16.4500, 'lng': 103.7000}
        }
        
        # ค้นหาแบบ partial match
        for key, coords in address_map.items():
            if key.lower() in address.lower():
                return coords
        
        # Default fallback - ร้อยเอ็ด city center
        return {'lat': 16.0563, 'lng': 103.6531}

# Functions สำหรับ OpenClaw เรียกใช้โดยตรง
def aika_get_location(technician_name):
    """Get technician location for OpenClaw"""
    integration = AikaGPSIntegration()
    return integration.get_technician_location(technician_name)

def aika_find_nearest(customer_address, skills=None):
    """Find nearest technician for OpenClaw"""
    integration = AikaGPSIntegration()
    return integration.find_nearest_technician(customer_address, skills)

def aika_calculate_distance(technician_name, customer_address):
    """Calculate distance for OpenClaw"""
    integration = AikaGPSIntegration()
    return integration.calculate_distance_eta(technician_name, customer_address)

if __name__ == "__main__":
    # CLI interface
    if len(sys.argv) < 3:
        print("Usage: python integration.py [get_location|find_nearest|calculate_distance] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    integration = AikaGPSIntegration()
    
    if command == "get_location":
        result = integration.get_technician_location(sys.argv[2])
    elif command == "find_nearest":
        skills = sys.argv[3:] if len(sys.argv) > 3 else None
        result = integration.find_nearest_technician(sys.argv[2], skills)
    elif command == "calculate_distance":
        result = integration.calculate_distance_eta(sys.argv[2], sys.argv[3])
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))