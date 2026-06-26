#!/usr/bin/env python3
"""
parse_smart.py — Parse smartctl -a output into structured JSON.

Usage:
    # From scan_drives.py output:
    python3 scan_drives.py | python3 parse_smart.py

    # From a saved scan file:
    python3 parse_smart.py --input scan.json

    # Parse a single smartctl output file:
    python3 parse_smart.py --raw smartctl_output.txt

Output:
    JSON array of parsed drive health objects.
"""

import json
import re
import sys
import argparse
from pathlib import Path


# SATA/SSD key attributes to extract (attribute name, attribute ID)
SATA_KEY_ATTRIBUTES = {
    "1":   "Read_Error_Rate",
    "5":   "Reallocated_Sector_Ct",
    "7":   "Seek_Error_Rate",
    "9":   "Power_On_Hours",
    "10":  "Spin_Retry_Count",
    "184": "End-to-End_Error",
    "187": "Reported_Uncorrect",
    "188": "Command_Timeout",
    "196": "Reallocated_Event_Count",
    "197": "Current_Pending_Sector",
    "198": "Offline_Uncorrectable",
    "199": "UDMA_CRC_Error_Count",
    "231": "SSD_Life_Left",
    "232": "Available_Reservd_Space",
    "241": "Total_LBAs_Written",
}

# NVMe key fields
NVME_KEY_FIELDS = [
    "Critical Warning",
    "Temperature",
    "Available Spare",
    "Available Spare Threshold",
    "Percentage Used",
    "Power On Hours",
    "Unsafe Shutdowns",
    "Media and Data Integrity Errors",
    "Error Information Log Entries",
]

# Thresholds for health assessment
CRITICAL_NONZERO = {
    "Reallocated_Sector_Ct",
    "Current_Pending_Sector",
    "Offline_Uncorrectable",
    "Reported_Uncorrect",
    "End-to-End_Error",
    "Spin_Retry_Count",
}
WARNING_NONZERO = {
    "Command_Timeout",
    "UDMA_CRC_Error_Count",
    "Reallocated_Event_Count",
}
TEMP_WARNING_C = 50
TEMP_CRITICAL_C = 60
SSD_LIFE_WARNING = 20   # percent remaining
NVME_SPARE_WARNING = 20  # percent available spare
NVME_USED_WARNING = 80   # percentage used


def parse_device_info(text):
    """Extract device model, serial, firmware, capacity, form factor."""
    info = {}
    patterns = {
        "model": r"Device Model:\s+(.+)",
        "model_nvme": r"Model Number:\s+(.+)",
        "serial": r"Serial Number:\s+(.+)",
        "firmware": r"Firmware Version:\s+(.+)",
        "capacity": r"User Capacity:\s+(.+)",
        "rotation": r"Rotation Rate:\s+(.+)",
        "form_factor": r"Form Factor:\s+(.+)",
        "sata_version": r"SATA Version is:\s+(.+)",
        "transport": r"Transport protocol:\s+(.+)",
        "smart_support": r"SMART support is:\s+(.+)",
        "overall_health": r"SMART overall-health self-assessment test result:\s+(.+)",
    }
    for key, pattern in patterns.items():
        m = re.search(pattern, text)
        if m:
            val = m.group(1).strip()
            # Merge nvme model into model
            if key == "model_nvme" and "model" not in info:
                info["model"] = val
            elif key != "model_nvme":
                info[key] = val

    # Determine drive type
    if "NVMe" in text or "transport" in info:
        info["drive_type"] = "NVMe"
    elif "rotation" in info:
        rot = info["rotation"].lower()
        if "solid state" in rot or "0" == rot:
            info["drive_type"] = "SSD"
        else:
            info["drive_type"] = "HDD"
    else:
        info["drive_type"] = "Unknown"

    return info


def parse_sata_attributes(text):
    """Parse SMART attribute table from SATA/SSD drives."""
    attributes = {}
    # Table header pattern followed by rows:
    # ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
    in_table = False
    for line in text.splitlines():
        if "ID# ATTRIBUTE_NAME" in line or "ATTRIBUTE_NAME" in line:
            in_table = True
            continue
        if in_table:
            # End of table on blank line
            if not line.strip():
                in_table = False
                continue
            # Parse attribute row
            # Example: "  5 Reallocated_Sector_Ct   0x0032   100   100   000    Old_age   Always       -       0"
            m = re.match(
                r'\s*(\d+)\s+(\S+)\s+\S+\s+(\d+)\s+(\d+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+([\d+]+)',
                line
            )
            if m:
                attr_id = m.group(1)
                attr_name = m.group(2)
                value = int(m.group(3))
                worst = int(m.group(4))
                thresh = int(m.group(5))
                raw_value = m.group(6)
                # Try to parse raw as int
                try:
                    raw_int = int(raw_value)
                except ValueError:
                    raw_int = None

                attributes[attr_name] = {
                    "id": attr_id,
                    "value": value,
                    "worst": worst,
                    "threshold": thresh,
                    "raw_value": raw_value,
                    "raw_int": raw_int,
                    "failing": value <= thresh and thresh > 0,
                }

    return attributes


def parse_nvme_attributes(text):
    """Parse NVMe SMART/Health Information log."""
    attributes = {}
    in_section = False
    for line in text.splitlines():
        if "SMART/Health Information" in line or "NVMe Log" in line:
            in_section = True
            continue
        if in_section:
            if not line.strip():
                continue
            # Key: value lines
            m = re.match(r'^(.*?):\s+(.+)$', line.strip())
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                attributes[key] = val
            # End section on next header
            elif line.startswith("===") or line.startswith("---"):
                break

    return attributes


def parse_temperature(text, attributes, drive_type):
    """Extract temperature in Celsius."""
    # Try from attributes first
    for attr_name in ("Temperature_Celsius", "Airflow_Temperature_Cel", "Drive_Temperature"):
        if attr_name in attributes:
            raw = attributes[attr_name].get("raw_int")
            if raw is not None:
                # Raw value for temp sometimes has extra bytes; mask lower byte
                return raw & 0xFF

    # NVMe temperature field
    if drive_type == "NVMe" and isinstance(attributes, dict):
        temp_val = attributes.get("Temperature")
        if temp_val:
            m = re.search(r'(\d+)', str(temp_val))
            if m:
                return int(m.group(1))

    # Fallback: grep from text
    m = re.search(r'Temperature[^:]*:\s+(\d+)\s+Celsius', text)
    if m:
        return int(m.group(1))

    return None


def assess_sata_health(attributes, temperature, device_info):
    """Return (status, flags) where status is 'Good'/'Warning'/'Critical'."""
    flags = []
    status = "Good"

    for attr_name in CRITICAL_NONZERO:
        if attr_name in attributes:
            raw = attributes[attr_name].get("raw_int", 0) or 0
            if raw > 0:
                flags.append({
                    "level": "Critical",
                    "attribute": attr_name,
                    "raw_value": raw,
                    "message": f"{attr_name.replace('_', ' ')} = {raw} (should be 0)"
                })
                status = "Critical"
            # Also check if value is at or below threshold
            if attributes[attr_name].get("failing"):
                flags.append({
                    "level": "Critical",
                    "attribute": attr_name,
                    "message": f"{attr_name} below failure threshold"
                })
                status = "Critical"

    for attr_name in WARNING_NONZERO:
        if attr_name in attributes:
            raw = attributes[attr_name].get("raw_int", 0) or 0
            if raw > 0:
                flags.append({
                    "level": "Warning",
                    "attribute": attr_name,
                    "raw_value": raw,
                    "message": f"{attr_name.replace('_', ' ')} = {raw}"
                })
                if status == "Good":
                    status = "Warning"

    # SSD life remaining
    for attr_name in ("SSD_Life_Left", "Wear_Leveling_Count", "Media_Wearout_Indicator"):
        if attr_name in attributes:
            val = attributes[attr_name].get("value", 100)
            if val <= SSD_LIFE_WARNING:
                flags.append({
                    "level": "Critical" if val <= 5 else "Warning",
                    "attribute": attr_name,
                    "value": val,
                    "message": f"SSD life remaining: {val}%"
                })
                status = "Critical" if (val <= 5 and status != "Critical") else status
                if status == "Good":
                    status = "Warning"

    # Temperature
    if temperature is not None:
        if temperature >= TEMP_CRITICAL_C:
            flags.append({
                "level": "Critical",
                "attribute": "Temperature",
                "value": temperature,
                "message": f"Temperature critical: {temperature}°C (threshold: {TEMP_CRITICAL_C}°C)"
            })
            status = "Critical"
        elif temperature >= TEMP_WARNING_C:
            flags.append({
                "level": "Warning",
                "attribute": "Temperature",
                "value": temperature,
                "message": f"Temperature elevated: {temperature}°C (threshold: {TEMP_WARNING_C}°C)"
            })
            if status == "Good":
                status = "Warning"

    return status, flags


def assess_nvme_health(attributes, temperature):
    """Return (status, flags) for NVMe drives."""
    flags = []
    status = "Good"

    # Critical Warning byte
    crit = attributes.get("Critical Warning", "0x00")
    try:
        crit_int = int(crit, 16) if crit.startswith("0x") else int(crit)
    except (ValueError, AttributeError):
        crit_int = 0
    if crit_int != 0:
        flags.append({
            "level": "Critical",
            "attribute": "Critical Warning",
            "value": crit,
            "message": f"NVMe Critical Warning flags set: {crit}"
        })
        status = "Critical"

    # Available Spare
    spare = attributes.get("Available Spare", "100%")
    m = re.search(r'(\d+)', str(spare))
    if m:
        spare_pct = int(m.group(1))
        spare_thresh_str = attributes.get("Available Spare Threshold", "10%")
        m2 = re.search(r'(\d+)', str(spare_thresh_str))
        spare_thresh = int(m2.group(1)) if m2 else 10
        if spare_pct <= spare_thresh:
            flags.append({
                "level": "Critical",
                "attribute": "Available Spare",
                "value": spare_pct,
                "message": f"Available spare {spare_pct}% at or below threshold {spare_thresh}%"
            })
            status = "Critical"
        elif spare_pct <= NVME_SPARE_WARNING:
            flags.append({
                "level": "Warning",
                "attribute": "Available Spare",
                "value": spare_pct,
                "message": f"Available spare low: {spare_pct}%"
            })
            if status == "Good":
                status = "Warning"

    # Percentage Used
    used = attributes.get("Percentage Used", "0%")
    m = re.search(r'(\d+)', str(used))
    if m:
        used_pct = int(m.group(1))
        if used_pct >= 100:
            flags.append({
                "level": "Critical",
                "attribute": "Percentage Used",
                "value": used_pct,
                "message": f"NVMe endurance exhausted: {used_pct}% used"
            })
            status = "Critical"
        elif used_pct >= NVME_USED_WARNING:
            flags.append({
                "level": "Warning",
                "attribute": "Percentage Used",
                "value": used_pct,
                "message": f"NVMe heavily used: {used_pct}%"
            })
            if status == "Good":
                status = "Warning"

    # Media errors
    media_errs = attributes.get("Media and Data Integrity Errors", "0")
    m = re.search(r'(\d+)', str(media_errs))
    if m and int(m.group(1)) > 0:
        flags.append({
            "level": "Critical",
            "attribute": "Media and Data Integrity Errors",
            "value": int(m.group(1)),
            "message": f"Media errors detected: {media_errs}"
        })
        status = "Critical"

    # Unsafe shutdowns (warning only; can be high on laptops)
    unsafe = attributes.get("Unsafe Shutdowns", "0")
    m = re.search(r'(\d+)', str(unsafe))
    if m:
        unsafe_int = int(m.group(1))
        if unsafe_int > 100:
            flags.append({
                "level": "Warning",
                "attribute": "Unsafe Shutdowns",
                "value": unsafe_int,
                "message": f"High unsafe shutdown count: {unsafe_int}"
            })
            if status == "Good":
                status = "Warning"

    # Temperature
    if temperature is not None:
        if temperature >= TEMP_CRITICAL_C:
            flags.append({
                "level": "Critical",
                "attribute": "Temperature",
                "value": temperature,
                "message": f"Temperature critical: {temperature}°C"
            })
            status = "Critical"
        elif temperature >= TEMP_WARNING_C:
            flags.append({
                "level": "Warning",
                "attribute": "Temperature",
                "value": temperature,
                "message": f"Temperature elevated: {temperature}°C"
            })
            if status == "Good":
                status = "Warning"

    return status, flags


def parse_drive(device, smartctl_text):
    """Parse a single drive's smartctl output into a structured dict."""
    device_info = parse_device_info(smartctl_text)
    drive_type = device_info.get("drive_type", "Unknown")

    if drive_type == "NVMe":
        attributes = parse_nvme_attributes(smartctl_text)
        temperature = parse_temperature(smartctl_text, attributes, drive_type)
        status, flags = assess_nvme_health(attributes, temperature)
    else:
        attributes = parse_sata_attributes(smartctl_text)
        temperature = parse_temperature(smartctl_text, attributes, drive_type)
        status, flags = assess_sata_health(attributes, temperature, device_info)

    # Extract Power On Hours
    power_on_hours = None
    if drive_type == "NVMe":
        poh = attributes.get("Power On Hours", "")
        m = re.search(r'([\d,]+)', str(poh))
        if m:
            power_on_hours = int(m.group(1).replace(",", ""))
    else:
        if "Power_On_Hours" in attributes:
            power_on_hours = attributes["Power_On_Hours"].get("raw_int")
        # Some drives use Power_On_Hours_and_Minutes
        elif "Power_On_Hours_and_Minutes" in attributes:
            raw = attributes["Power_On_Hours_and_Minutes"].get("raw_int", 0)
            if raw:
                power_on_hours = raw >> 16  # high 16 bits = hours

    # Overall health from smartctl summary line
    overall = device_info.get("overall_health", "").upper()
    if "FAILED" in overall and status != "Critical":
        status = "Critical"
        flags.append({
            "level": "Critical",
            "attribute": "overall_health",
            "message": f"SMART self-assessment: {device_info.get('overall_health')}"
        })

    return {
        "device": device,
        "model": device_info.get("model", "Unknown"),
        "serial": device_info.get("serial", "Unknown"),
        "firmware": device_info.get("firmware"),
        "capacity": device_info.get("capacity"),
        "drive_type": drive_type,
        "rotation": device_info.get("rotation"),
        "smart_overall": device_info.get("overall_health"),
        "temperature_c": temperature,
        "power_on_hours": power_on_hours,
        "health_status": status,
        "flags": flags,
        "attributes": attributes,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse smartctl output to structured JSON")
    parser.add_argument("--input", help="Path to scan_drives.py JSON output file")
    parser.add_argument("--raw", help="Path to raw smartctl -a text output for a single device")
    parser.add_argument("--device", help="Device name for --raw input (e.g. /dev/disk0)")
    args = parser.parse_args()

    results = []

    if args.raw:
        # Single raw smartctl text file
        text = Path(args.raw).read_text()
        device = args.device or args.raw
        results.append(parse_drive(device, text))

    elif args.input:
        scan_data = json.loads(Path(args.input).read_text())
        for entry in scan_data.get("scan_results", []):
            device = entry.get("device", "unknown")
            if "error" in entry:
                results.append({
                    "device": device,
                    "error": entry["error"],
                    "health_status": "Unknown",
                    "flags": []
                })
            elif "smartctl_output" in entry:
                results.append(parse_drive(device, entry["smartctl_output"]))

    else:
        # Read from stdin (piped from scan_drives.py)
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            print(json.dumps({"error": "No input provided"}, indent=2))
            sys.exit(1)
        try:
            scan_data = json.loads(stdin_data)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON input: {e}"}, indent=2))
            sys.exit(1)

        for entry in scan_data.get("scan_results", []):
            device = entry.get("device", "unknown")
            if "error" in entry:
                results.append({
                    "device": device,
                    "error": entry.get("error"),
                    "hint": entry.get("hint"),
                    "health_status": "Unknown",
                    "flags": []
                })
            elif "smartctl_output" in entry:
                results.append(parse_drive(device, entry["smartctl_output"]))

    import json as _json
    print(_json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
