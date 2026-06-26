#!/usr/bin/env python3
"""
Boat Daily Email Report Generator
Fetches live Victron VRM API data and generates a formatted HTML email
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path
import sys

# Configuration
# ⚠️ IMPORTANT: Replace these with your own values!
# Get your VRM API token from: https://vrm.victronenergy.com/access-tokens
VRM_TOKEN = os.environ.get("VRM_TOKEN", "YOUR_VRM_API_TOKEN_HERE")
VRM_BASE = "https://vrmapi.victronenergy.com/v2"

# Example installations - REPLACE WITH YOUR OWN
# Find your installation ID in the VRM URL: https://vrm.victronenergy.com/installation/YOUR_ID/dashboard
INSTALLATIONS = {
    "boat1": {
        "id": 123456,              # Your first boat's installation ID
        "name": "My Boat 1",       # Custom name for emails
        "batteryInstance": 279,    # SmartShunt instance (usually 279)
        "hasGateway": True,
        "gateway": "Cerbo GX (v3.70)",
    },
    "boat2": {
        "id": 654321,              # Your second boat's installation ID
        "name": "My Boat 2",
        "batteryInstance": 279,
        "hasGateway": True,
        "gateway": "Cerbo GX (v3.70)",
    }
}

def get_headers():
    return {
        "X-Authorization": f"Token {VRM_TOKEN}",
        "Accept": "application/json"
    }

def fetch_battery_data(installation_id, instance):
    """Fetch battery data from BatterySummary widget"""
    try:
        url = f"{VRM_BASE}/installations/{installation_id}/widgets/BatterySummary/latest?instance={instance}"
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        
        data = response.json()
        records = data.get("records", {}).get("data", {})
        
        return {
            "soc": records.get("51", {}).get("valueFloat", 0),
            "voltage": records.get("47", {}).get("valueFloat", 0),
            "current": records.get("49", {}).get("valueFloat", 0),
            "temp": records.get("115", {}).get("valueFloat", None),
        }
    except Exception as e:
        print(f"Error fetching battery data: {e}", file=sys.stderr)
        return None

def fetch_diagnostics(installation_id):
    """Fetch diagnostics for solar and inverter data"""
    try:
        url = f"{VRM_BASE}/installations/{installation_id}/diagnostics"
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        
        return response.json().get("records", [])
    except Exception as e:
        print(f"Error fetching diagnostics: {e}", file=sys.stderr)
        return []

def fetch_alarms(installation_id):
    """Fetch active alarms"""
    try:
        url = f"{VRM_BASE}/installations/{installation_id}/alarms?limit=10"
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        
        data = response.json()
        alarms = []
        
        for alarm in data.get("alarms", []):
            alarms.append({
                "name": alarm.get("meta_info", {}).get("name", "Unknown"),
                "attribute": alarm.get("meta_info", {}).get("dataAttribute", "Unknown"),
                "active": alarm.get("active", [False, False])[1]
            })
        
        # Get gateway info from devices
        devices = data.get("devices", [])
        gateway_info = None
        for device in devices:
            if device.get("idDeviceType") == 0:  # Gateway
                seconds_ago = device.get("secondsAgo", 0)
                if seconds_ago < 60:
                    gateway_info = f"{seconds_ago}s ago"
                elif seconds_ago < 3600:
                    gateway_info = f"{seconds_ago // 60}m ago"
                else:
                    gateway_info = f"{seconds_ago // 3600}h ago"
        
        return {
            "alarms": alarms,
            "gateway_last_seen": gateway_info or "unknown"
        }
    except Exception as e:
        print(f"Error fetching alarms: {e}", file=sys.stderr)
        return {"alarms": [], "gateway_last_seen": "unknown"}

def extract_solar_data(diagnostics):
    """Extract solar charger data from diagnostics"""
    solar_data = {}
    
    for record in diagnostics:
        if record.get("Device") != "Solar Charger":
            continue
        
        code = record.get("code", "")
        value = record.get("formattedValue", "")
        
        if code == "PVP":  # PV Power
            solar_data["power"] = value.replace(" W", "").strip() + " W"
        elif code == "YT":  # Yield today
            solar_data["yieldToday"] = value
        elif code == "MCPT":  # Max charge power today
            solar_data["maxChargePower"] = value
        elif code == "PVV":  # PV Voltage
            solar_data["pvVoltage"] = value
        elif code == "ScI":  # Charger current
            solar_data["chargerCurrent"] = value
    
    # Set defaults if not found
    if "power" not in solar_data:
        solar_data["power"] = "0 W"
    if "yieldToday" not in solar_data:
        solar_data["yieldToday"] = "0 kWh"
    if "maxChargePower" not in solar_data:
        solar_data["maxChargePower"] = "0 W"
    if "pvVoltage" not in solar_data:
        solar_data["pvVoltage"] = "0 V"
    
    return solar_data

def extract_inverter_data(diagnostics):
    """Extract inverter/AC data from diagnostics"""
    inverter_data = {"status": "AC In"}
    
    for record in diagnostics:
        if record.get("Device") != "VE.Bus System":
            continue
        
        code = record.get("code", "")
        value = record.get("formattedValue", "")
        
        # Look for AC input status
        if code in ["IV1", "IV2"] or "input" in code.lower():
            inverter_data["status"] = value
    
    return inverter_data

def generate_report(data):
    """Generate HTML email with populated data"""
    # Load bundled template
    template_path = Path(__file__).parent / "boat-email-template.html"
    
    if not template_path.exists():
        print(f"Error: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)
    
    template_content = template_path.read_text()
    
    # Replace placeholders
    html = template_content
    html = html.replace("{{date}}", datetime.now().strftime("%B %d, %Y"))
    
    # Example boat 1 data
    boat1_data = data.get("boat1", {})
    html = html.replace("{{boat1.battery.soc}}", f"{boat1_data.get('battery', {}).get('soc', 0):.1f}")
    html = html.replace("{{boat1.battery.voltage}}", f"{boat1_data.get('battery', {}).get('voltage', 0):.2f}")
    html = html.replace("{{boat1.battery.current}}", f"{boat1_data.get('battery', {}).get('current', 0):.2f}")
    html = html.replace("{{boat1.solar.power}}", boat1_data.get("solar", {}).get("power", "0 W"))
    html = html.replace("{{boat1.solar.yieldToday}}", boat1_data.get("solar", {}).get("yieldToday", "0 kWh"))
    html = html.replace("{{boat1.solar.maxChargePower}}", boat1_data.get("solar", {}).get("maxChargePower", "0 W"))
    html = html.replace("{{boat1.solar.pvVoltage}}", boat1_data.get("solar", {}).get("pvVoltage", "0 V"))
    html = html.replace("{{boat1.gateway.lastSeen}}", boat1_data.get("gateway", {}).get("lastSeen", "unknown"))
    
    # Example boat 2 data
    boat2_data = data.get("boat2", {})
    html = html.replace("{{boat2.battery.soc}}", f"{boat2_data.get('battery', {}).get('soc', 0):.1f}")
    html = html.replace("{{boat2.battery.voltage}}", f"{boat2_data.get('battery', {}).get('voltage', 0):.2f}")
    html = html.replace("{{boat2.battery.current}}", f"{boat2_data.get('battery', {}).get('current', 0):.2f}")
    html = html.replace("{{boat2.acInput.status}}", boat2_data.get("acInput", {}).get("status", "unknown"))
    html = html.replace("{{boat2.gateway.lastSeen}}", boat2_data.get("gateway", {}).get("lastSeen", "unknown"))
    
    # Handle alarms
    import re
    if pg_data["alarms"]["alarms"]:
        alarms_html = ""
        for alarm in pg_data["alarms"]["alarms"]:
            alarms_html += f'<div class="alarm-item"><strong>{alarm["name"]}</strong><br/>{alarm["attribute"]}</div>'
        
        # Remove template tags and insert actual alarm content
        html = re.sub(r'<div class="section-title">🚨 Active Alarms</div>\s*<div class="alarm-box">\s*{{#if pegasus\.alarms}}.*?{{#each pegasus\.alarms}}<div class="alarm-item"><strong>{{this\.name}}</strong><br/>{{this\.attribute}}</div>{{/each}}.*?{{/if}}\s*</div>',
                     f'<div class="section-title">🚨 Active Alarms</div>\n<div class="alarm-box">\n{alarms_html}\n</div>',
                     html, flags=re.DOTALL)
    else:
        # Remove alarms section if no alarms
        html = re.sub(r'<div class="section-title">🚨 Active Alarms</div>.*?</div>\n\s*<div class="section-title">🔌 Hardware</div>', 
                     '<div class="section-title">🔌 Hardware</div>',
                     html, flags=re.DOTALL)
    
    return html

def main():
    print("🚤 Fetching boat power system data...", file=sys.stderr)
    
    report_data = {}
    
    # Fetch data for all configured installations
    for boat_key, config in INSTALLATIONS.items():
        boat_id = config["id"]
        boat_name = config["name"]
        battery_instance = config["batteryInstance"]
        
        print(f"  {boat_name} ({boat_id})...", file=sys.stderr)
        
        battery = fetch_battery_data(boat_id, battery_instance)
        diagnostics = fetch_diagnostics(boat_id)
        alarms = fetch_alarms(boat_id)
        
        report_data[boat_key] = {
            "battery": battery or {"soc": 0, "voltage": 0, "current": 0, "temp": None},
            "solar": extract_solar_data(diagnostics),
            "acInput": extract_inverter_data(diagnostics),
            "alarms": {"alarms": alarms["alarms"]},
            "gateway": {"lastSeen": alarms["gateway_last_seen"]},
        }
    
    # Generate HTML report
    print("📧 Generating email...", file=sys.stderr)
    html = generate_report(report_data)
    
    # Save to file
    output_path = Path("/home/jeanclaude/.openclaw/workspace/skills/boat-daily-check/out/boat-daily-email.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    
    print(f"✅ Email generated: {output_path}", file=sys.stderr)
    
    # Output JSON for further processing
    report_data["timestamp"] = datetime.now().isoformat()
    report_data["emailPath"] = str(output_path)
    print(json.dumps(report_data, indent=2))

if __name__ == "__main__":
    main()
