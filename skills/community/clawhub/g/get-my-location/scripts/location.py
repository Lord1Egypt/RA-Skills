#!/usr/bin/env python3
"""
Get My Location - IP geolocation with multi-source fallback.
Each source retries up to MAX_RETRIES times before moving to the next.
No API key required for any source.

Usage:
  python location.py            # Get current IP location
  python location.py <ip>       # Query specific IP
  python location.py --json     # Output raw JSON
  python location.py <ip> --json
"""

import sys
import json
import time
import io

# Fix Windows console encoding
if sys.stdout.encoding and 'gbk' in sys.stdout.encoding.lower():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding and 'gbk' in sys.stderr.encoding.lower():
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote

MAX_RETRIES = 3
TIMEOUT = 10


def http_get(url, timeout=TIMEOUT):
    """Simple HTTP GET, returns string or raises."""
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    req = Request(url, headers={"User-Agent": ua, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        return data.decode("utf-8", errors="replace")


def retry(func, label):
    """Call func up to MAX_RETRIES times. Return result or None."""
    for i in range(1, MAX_RETRIES + 1):
        try:
            result = func()
            if result and isinstance(result, dict):
                return result
        except Exception as e:
            msg = str(e)[:120]
            print(f"  [{label}] retry {i}/{MAX_RETRIES}: {msg}", file=sys.stderr)
            if i < MAX_RETRIES:
                time.sleep(1)
    return None


# ── Source 1: freegeoip.app (redirects to api.ipbase.com) ──

def try_freegeoip(ip=None):
    url = "https://freegeoip.app/json/" if ip is None else f"https://freegeoip.app/json/{ip}"
    def _do():
        raw = http_get(url)
        data = json.loads(raw)
        if data.get("ip") or data.get("country_code"):
            data["_source"] = "freegeoip.app"
            return data
        return None
    return retry(_do, "freegeoip.app")


# ── Source 2: api.ipbase.com ──

def try_ipbase(ip=None):
    url = "https://api.ipbase.com/v1/json/" if ip is None else f"https://api.ipbase.com/v1/json/{ip}"
    def _do():
        raw = http_get(url)
        data = json.loads(raw)
        if data.get("ip") or data.get("country_code"):
            data["_source"] = "api.ipbase.com"
            return data
        return None
    return retry(_do, "api.ipbase.com")


# ── Source 3: ip-api.com (no key, 45/min) ──

def try_ip_api(ip=None):
    url = "http://ip-api.com/json/" if ip is None else f"http://ip-api.com/json/{quote(ip)}"
    def _do():
        raw = http_get(url)
        data = json.loads(raw)
        if data.get("status") == "success":
            # Normalize to common format
            data["_source"] = "ip-api.com"
            data["country_name"] = data.get("country", "")
            data["region_name"] = data.get("regionName", "")
            data["city"] = data.get("city", "")
            data["latitude"] = data.get("lat", 0)
            data["longitude"] = data.get("lon", 0)
            data["zip_code"] = data.get("zip", "")
            data["time_zone"] = data.get("timezone", "")
            return data
        return None
    return retry(_do, "ip-api.com")


# ── Output ──

def format_location(data):
    """Pretty formatted Chinese location info."""
    ip = data.get("ip", "")
    country = data.get("country_name", data.get("country", ""))
    region = data.get("region_name", data.get("region", ""))
    city = data.get("city", "")
    lat = data.get("latitude", 0)
    lon = data.get("longitude", 0)
    zipcode = data.get("zip_code", data.get("zip", ""))
    tz = data.get("time_zone", data.get("timezone", ""))
    source = data.get("_source", "unknown")

    lines = []
    lines.append("📍 你的位置信息")
    lines.append(f"  IP 地址: {ip}")
    if country:
        lines.append(f"  国家:   {country}")
    if region:
        lines.append(f"  省份:   {region}")
    if city:
        lines.append(f"  城市:   {city}")
    if zipcode:
        lines.append(f"  邮编:   {zipcode}")
    if lat and lon:
        lines.append(f"  坐标:   {lat:.6f}, {lon:.6f}")
    if tz:
        lines.append(f"  时区:   {tz}")
    lines.append(f"  数据源: {source}")
    return "\n".join(lines)


def main():
    ip = None
    json_mode = False

    for arg in sys.argv[1:]:
        if arg == "--json":
            json_mode = True
        elif arg.startswith("-"):
            print(f"Unknown option: {arg}", file=sys.stderr)
            sys.exit(1)
        else:
            ip = arg

    # Run fallback chain
    result = try_freegeoip(ip)
    if not result:
        result = try_ipbase(ip)
    if not result:
        result = try_ip_api(ip)

    if result:
        if json_mode:
            # Clean internal fields for JSON output
            out = {k: v for k, v in result.items() if not k.startswith("_")}
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            output = format_location(result)
            print(output)
        sys.exit(0)
    else:
        print("❌ 所有数据源都无法获取位置信息", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
