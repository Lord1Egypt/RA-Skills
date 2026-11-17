import os
import sys
import requests
from bs4 import BeautifulSoup

"""Ebusy API client

This module provides a small helper class to log into an eBusy-based
booking system (see www.ebusy.de for examples, e.g. Tennis clubs in Germany) and fetch reservations for a
single court-module and date.

All **installation-specific** values (base URL, username, password,
module/court IDs, default date) are read from environment variables so
that no secrets or user-specific data live in the skill folder.

Expected environment variables:

- EBUSY_BASE_URL   e.g. "https://ktev.ebusy.de" or "https://medenhalle.ebusy.de"
- EBUSY_USERNAME   login username/email
- EBUSY_PASSWORD   login password
- EBUSY_COURT_ID   numeric eBusy court-module ID (e.g. 807 for KTEV, 1 for Medenhalle)
- EBUSY_FIRST_COURT_NO optional: base court number in that module (e.g. 2135)

These can be provided via:
- a .env file loaded by your environment/venv,
- export in your shell profile,
- or the OpenClaw gateway/agent env configuration.

The module can be used directly as a script:

    python ebusy_api.py 03/07/2026

which will print all reservations for the configured module/date.

"""


BASE_URL = os.getenv("EBUSY_BASE_URL", "https://medenhalle.ebusy.de")
USERNAME = os.getenv("EBUSY_USERNAME")
PASSWORD = os.getenv("EBUSY_PASSWORD")
COURT_ID = int(os.getenv("EBUSY_COURT_ID", "1"))
FIRST_COURT_NO = int(os.getenv("EBUSY_FIRST_COURT_NO", "1"))


class EbusyAPI:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    def login(self, username: str, password: str) -> bool:
        """Log into the eBusy instance using CSRF token + session.

        Returns True on success, False otherwise.
        """
        login_page = self.session.get(f"{self.base_url}/login")
        login_page.raise_for_status()

        soup = BeautifulSoup(login_page.text, "html.parser")
        csrf_el = soup.find("input", {"name": "_csrf"})
        if not csrf_el or not csrf_el.get("value"):
            raise RuntimeError("Could not find CSRF token on login page")

        csrf_token = csrf_el["value"]

        login_data = {
            "username": username,
            "password": password,
            "_csrf": csrf_token,
            "remember-me": "on",
        }

        response = self.session.post(
            f"{self.base_url}/login",
            data=login_data,
            headers={"Accept": "application/xml, text/xml"},
        )

        return response.ok

    def get_reservations(self, court_id: int | None = None, date: str | None = None) -> dict:
        """Fetch reservations JSON for a given court-module and date.

        - court_id: eBusy court-module id (falls None → default COURT_ID)
        - date: string in format MM/DD/YYYY as used by eBusy (e.g. "03/07/2026").
        """
        court_id = court_id or COURT_ID
        if not date:
            raise ValueError("date must be provided (MM/DD/YYYY)")

        url = f"{self.base_url}/court-module/{court_id}"
        params = {"currentDate": date}
        headers = {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = self.session.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


def _ensure_env_vars() -> None:
    missing = []
    for key in ("EBUSY_BASE_URL", "EBUSY_USERNAME", "EBUSY_PASSWORD", "EBUSY_COURT_ID"):
        if not os.getenv(key):
            missing.append(key)
    if missing:
        raise RuntimeError(
            "Missing required environment variables for eBusy access: " + ", ".join(missing)
        )


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ebusy_api.py MM/DD/YYYY [start_hour start_min end_hour end_min]", file=sys.stderr)
        raise SystemExit(1)

    date = sys.argv[1]
    _ensure_env_vars()

    # Parse time window if provided
    start_hour, start_min, end_hour, end_min = None, None, None, None
    if len(sys.argv) == 6:
        try:
            start_hour = int(sys.argv[2])
            start_min = int(sys.argv[3])
            end_hour = int(sys.argv[4])
            end_min = int(sys.argv[5])
        except ValueError:
            print("Invalid time window parameters", file=sys.stderr)
            raise SystemExit(1)

    api = EbusyAPI()
    if not api.login(USERNAME, PASSWORD):
        print("Login failed", file=sys.stderr)
        raise SystemExit(1)

    data = api.get_reservations(date=date)
    reservations = data.get("reservations", [])
    
    # Filter reservations for the specified time window
    if start_hour is not None:
        filtered_reservations = []
        for r in reservations:
            try:
                res_start = int(r["fromTime"][:2])
                res_end = int(r["toTime"][:2])
                if not (res_end <= start_hour or res_start >= end_hour):
                    filtered_reservations.append(r)
            except (ValueError, KeyError):
                continue
    else:
        filtered_reservations = reservations
    
    sorted_reservations = sorted(
        filtered_reservations, key=lambda r: (r["court"], r["fromTime"])
    )

    # Check total courts
    total_courts = 6  # Default, will be adjusted based on FIRST_COURT_NO
    try:
        # Try to get total courts from environment or use a reasonable default
        total_courts = int(os.getenv("EBUSY_TOTAL_COURTS", "6"))
    except ValueError:
        pass

    # Build availability structure
    court_status = {}
    for i in range(1, total_courts + 1):
        court_status[f"Platz {i}"] = {"available": True, "bookings": []}

    # Mark unavailable courts based on reservations
    for r in sorted_reservations:
        try:
            court_num = r["court"]
            court_index = court_num - FIRST_COURT_NO + 1
            if 1 <= court_index <= total_courts:
                court_name = f"Platz {court_index}"
                court_status[court_name]["available"] = False
                court_status[court_name]["bookings"].append({
                    "from": r["fromTime"],
                    "to": r["toTime"],
                    "text": r["text"]
                })
        except (KeyError, ValueError):
            continue

    # Calculate availability
    available_count = sum(1 for status in court_status.values() if status["available"])
    unavailable_count = total_courts - available_count

    # Output results
    import json
    result = {
        "date": date,
        "time_window": f"{start_hour:02d}:{start_min:02d}-{end_hour:02d}:{end_min:02d}" if start_hour else "All day",
        "total_courts": total_courts,
        "available_courts": available_count,
        "unavailable_courts": unavailable_count,
        "available": [{"name": name, "available": info["available"], "bookings": info["bookings"]} 
                      for name, info in sorted(court_status.items())],
        "unavailable": [{"name": name, "bookings": info["bookings"]} 
                        for name, info in court_status.items() if not info["available"]],
        "status": "success"
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


def check() -> None:
    """Check availability for a specific date and time window.
    
    Usage: python ebusy_api.py check MM/DD/YYYY start_hour start_min end_hour end_min
    """
    import sys
    
    if len(sys.argv) < 7 or sys.argv[1] != "check":
        print("Usage: python ebusy_api.py check MM/DD/YYYY start_hour start_min end_hour end_min", file=sys.stderr)
        raise SystemExit(1)
    
    # Extract parameters
    date = sys.argv[2]
    try:
        start_hour = int(sys.argv[3])
        start_min = int(sys.argv[4])
        end_hour = int(sys.argv[5])
        end_min = int(sys.argv[6])
    except ValueError:
        print("Invalid time parameters", file=sys.stderr)
        raise SystemExit(1)
    
    _ensure_env_vars()
    
    api = EbusyAPI()
    if not api.login(USERNAME, PASSWORD):
        print("Login failed", file=sys.stderr)
        raise SystemExit(1)
    
    data = api.get_reservations(date=date)
    reservations = data.get("reservations", [])
    
    # Filter reservations for the specified time window
    filtered_reservations = []
    for r in reservations:
        try:
            res_start = int(r["fromTime"][:2])
            res_end = int(r["toTime"][:2])
            if not (res_end <= start_hour or res_start >= end_hour):
                filtered_reservations.append(r)
        except (ValueError, KeyError):
            continue
    
    # Build court status
    total_courts = 6  # Default
    try:
        total_courts = int(os.getenv("EBUSY_TOTAL_COURTS", "6"))
    except ValueError:
        pass
    
    court_status = {}
    for i in range(1, total_courts + 1):
        court_status[f"Platz {i}"] = {"available": True, "bookings": []}
    
    # Mark unavailable courts
    for r in filtered_reservations:
        try:
            court_num = r["court"]
            court_index = court_num - FIRST_COURT_NO + 1
            if 1 <= court_index <= total_courts:
                court_name = f"Platz {court_index}"
                court_status[court_name]["available"] = False
                court_status[court_name]["bookings"].append({
                    "from": r["fromTime"],
                    "to": r["toTime"],
                    "text": r["text"]
                })
        except (KeyError, ValueError):
            continue
    
    # Calculate availability
    available_count = sum(1 for status in court_status.values() if status["available"])
    unavailable_count = total_courts - available_count
    
    # Output results
    import json
    result = {
        "date": date,
        "time_window": f"{start_hour:02d}:{start_min:02d}-{end_hour:02d}:{end_min:02d}",
        "total_courts": total_courts,
        "available_courts": available_count,
        "unavailable_courts": unavailable_count,
        "available": [{"name": name, "available": info["available"], "bookings": info["bookings"]} 
                      for name, info in sorted(court_status.items())],
        "unavailable": [{"name": name, "bookings": info["bookings"]} 
                        for name, info in court_status.items() if not info["available"]],
        "status": "success"
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # Check if 'check' command is used
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    else:
        main()
