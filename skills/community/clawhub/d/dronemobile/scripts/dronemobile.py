#!/usr/bin/env python3
"""
DroneMobile vehicle control — OpenClaw skill script.
Usage: dronemobile.py <command>
Commands: start | stop | lock | unlock | trunk | status
"""
import os
import sys

try:
    from drone_mobile.client import DroneMobileClient
except ImportError:
    print("ERROR: drone_mobile not installed — run: pip install drone-mobile --break-system-packages")
    sys.exit(1)

COMMANDS = ["start", "stop", "lock", "unlock", "trunk", "status"]

def usage():
    print(f"Usage: dronemobile.py <{'|'.join(COMMANDS)}>")
    sys.exit(1)

if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    usage()

cmd = sys.argv[1]

email    = os.environ.get("DRONEMOBILE_EMAIL")
password = os.environ.get("DRONEMOBILE_PASSWORD")
device_key = os.environ.get("DRONEMOBILE_DEVICE_KEY")

if not email or not password:
    print("ERROR: DRONEMOBILE_EMAIL and DRONEMOBILE_PASSWORD must be set in environment")
    sys.exit(1)

def get_vehicle(client, device_key=None):
    vehicles = client.get_vehicles()
    if not vehicles:
        print("ERROR: No vehicles found on account")
        sys.exit(1)
    if device_key:
        for v in vehicles:
            dk = str(v.info.device_key) if hasattr(v, 'info') else str(getattr(v, 'device_key', ''))
            if dk == str(device_key):
                return v
        print(f"WARNING: Device key {device_key} not found — using first vehicle")
    return vehicles[0]

def parse_success(response):
    """Library bug workaround: check raw_data['command_success'] directly."""
    return response.raw_data.get("command_success", response.success)

def get_telemetry(raw):
    ctrl = raw.get("controller", {})
    temp = ctrl.get("current_temperature", "?")
    batt = raw.get("controller", {}).get("main_battery_voltage") or raw.get("main_battery_voltage", "?")
    engine = "on" if ctrl.get("engine_on") else "off"
    return temp, batt, engine

try:
    with DroneMobileClient(username=email, password=password) as client:
        vehicle = get_vehicle(client, device_key)

        if cmd == "status":
            # Use cached status already populated by get_vehicles()
            cached = getattr(vehicle, '_cached_status', None)
            raw = cached.raw_data if cached and hasattr(cached, 'raw_data') else {}
            last = raw.get("last_known_state", raw)
            ctrl = last.get("controller", {})
            temp = ctrl.get("current_temperature", "?")
            batt = ctrl.get("main_battery_voltage", "?")
            engine = "ON" if ctrl.get("engine_on") else "off"
            locked = "locked" if ctrl.get("armed") else "unlocked"
            door = "open" if ctrl.get("door_open") else "closed"
            hood = "open" if ctrl.get("hood_open") else "closed"
            mileage = last.get("mileage", raw.get("mileage", "?"))
            name = raw.get("vehicle_name", "Vehicle")
            print(f"🚗 {name} Status")
            print(f"   Engine: {engine} | Doors: {locked} | Battery: {batt}V | Temp: {temp}°C")
            print(f"   Door: {door} | Hood: {hood} | Mileage: {mileage} mi")
        else:
            method = getattr(vehicle, cmd)
            response = method()
            success = parse_success(response)
            temp, batt, engine = get_telemetry(response.raw_data)
            label = {
                "start": "🚀 Started",
                "stop":  "🛑 Stopped",
                "lock":  "🔒 Locked",
                "unlock":"🔓 Unlocked",
                "trunk": "🗃️ Trunk opened",
            }.get(cmd, cmd)
            if success:
                print(f"✅ {label} | Temp: {temp}°C | Battery: {batt}V | Engine: {engine}")
            else:
                print(f"❌ Command failed: {response.raw_data}")
                sys.exit(1)

except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
