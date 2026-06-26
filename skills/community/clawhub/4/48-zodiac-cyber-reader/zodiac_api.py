import sys
import urllib.request
import urllib.parse
import json

# ==========================================
# 48 Zodiac API Client (Zero-Dependency & Secure)
# ==========================================
BASE_URL = "https://zodiac-48-api.712991518.workers.dev/api"

def get_zone(sign: str):
    """Fetch single 48-Zodiac zone detailing."""
    url = f"{BASE_URL}/zone?sign={urllib.parse.quote(sign, safe='')}"
    req = urllib.request.Request(url, headers={'User-Agent': 'ClawHub-Skill/1.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode('utf-8')

def get_pairing(sign1: str, sign2: str):
    """Fetch pairing details between two signs."""
    url = (
        f"{BASE_URL}/pairing?sign1={urllib.parse.quote(sign1, safe='')}"
        f"&sign2={urllib.parse.quote(sign2, safe='')}"
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'ClawHub-Skill/1.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python zodiac_api.py [zone|pairing] [args...]")
        sys.exit(1)
        
    action = sys.argv[1]
    
    if action == "zone":
        print(get_zone(sys.argv[2]))
    elif action == "pairing" and len(sys.argv) >= 4:
        print(get_pairing(sys.argv[2], sys.argv[3]))
    else:
        print(json.dumps({"error": "Invalid arguments."}))
