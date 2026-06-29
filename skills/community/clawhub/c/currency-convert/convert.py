"""
Currency converter for OpenClaw skill.
Usage: python3 convert.py <from_currency> <to_currency> <amount>
Example: python3 convert.py USD PKR 100
"""

import sys
import json
import urllib.request
import os

if len(sys.argv) != 4:
        print("Error: Usage: convert.py <FROM> <TO> <AMOUNT")
        print("Example: convert.py USD PKR 100")
        sys.exit(1)

from_currency = sys.argv[1].upper().strip()
to_currency = sys.argv[2].upper().strip()

try:
        amount = float(sys.argv[3])
except ValueError:
        print(f"ERROR: Amount must be a number. Got: {sys.argv[3]}")
        sys.exit(1)

app_id = os.environ.get("OXR_APP_ID","")

if not app_id:
        print("ERROR: OXR_APP_ID environment variable not set.")
        print("Set it with: export OXR_APP_ID=your_app_id_here")
        sys.exit(1)

url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={from_currency},{to_currency}"

try:
        with urllib.request.urlopen(url, timeout = 10) as response:
                data = json.loads(response.read().decode())

except urllib.error.HTTPError as e:
        print(f"ERROR: API request failed with status {e.code}")

        if e.code == 401:
                print("Your App ID is invalid or expired.")
        sys.exit(1)

except Exception as e:
        print(f"ERROR: Could not reach API. {e}")
        sys.exit(1)

rates = data.get("rates", {})

if from_currency not in rates:
        print(f"ERROR: Unknown currency '{from_currency}'. Check the 3-letter code.")
        sys.exit(1)

if to_currency not in rates:
        print("ERROR: Unknown currency '{to_currency}'. Check the 3-letter code.")
        sys.exit(1)

rate = rates[to_currency] / rates[from_currency]
converted = amount * rate

print(f"FROM: {from_currency}")
print(f"TO: {to_currency}")
print(f"AMOUNT: {amount}")
print(f"RATE: {rate:.6f}")
print(f"RESULT: {converted:.2f}")
print(f"TIMESTAMP: {data.get('timestamp', 'unknown')}")
print(f"BASE: {data.get('base', 'USD')}")