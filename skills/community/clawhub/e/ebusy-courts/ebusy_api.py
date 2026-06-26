import os
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
        print("Usage: python ebusy_api.py MM/DD/YYYY", file=sys.stderr)
        raise SystemExit(1)

    date = sys.argv[1]
    _ensure_env_vars()

    api = EbusyAPI()
    if not api.login(USERNAME, PASSWORD):
        print("Login failed", file=sys.stderr)
        raise SystemExit(1)

    data = api.get_reservations(date=date)
    reservations = data.get("reservations", [])
    sorted_reservations = sorted(
        reservations, key=lambda r: (r["court"], r["fromTime"])
    )

    for r in sorted_reservations:
        court_index = r["court"] - FIRST_COURT_NO + 1
        print(
            f"Reservierung Platz {court_index}: {r['fromTime']} - {r['toTime']} von {r['text']}"
        )


if __name__ == "__main__":
    main()
