---
name: contact-map-bm
description: Generate an interactive Germany map of Odoo contacts (click markers to open the record in Odoo).
metadata: {"openclaw":{"emoji":"🗺️","requires":{"env":["ODOO_URL","ODOO_DB","ODOO_USERNAME","ODOO_PASSWORD"]},"primaryEnv":"ODOO_PASSWORD","triggers":["show contacts on map","contacts map","map contacts","contact map","show my contacts on a map"]}}
---

# Contact Map (contact-map-bm)

This skill generates an interactive HTML map (Leaflet) with your Odoo contacts geocoded and shown as clickable markers that open the corresponding res.partner record in Odoo.

Features
- Reads contacts from Odoo via XML-RPC (res.partner).
- Attempts to reuse coordinate fields if present (common x_*/lat/longitude fields).
- Geocodes addresses via Nominatim when coordinates are missing (one request/sec respectful usage).
- Produces HTML at: ${workspace}/odoo_contacts_germany_map.html
- Popups include contact name, address, email, phone and a link "Open in Odoo".

Requirements
- Environment variables: ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD (or ODOO_API_KEY).
- Internet access for Nominatim geocoding (optional if your contacts have coordinates).

Usage
- From the skill folder:
  python3 scripts/generate_map.py            # Generate map for Germany (default)
  python3 scripts/generate_map.py --city Hamburg   # Generate map filtered to a city

Integration
- The skill declares trigger phrases so OpenClaw can surface it when you ask to see contacts on a map. If you want this to be the *default* handler for that UI action, I can enable the builtin mapping in OpenClaw config (requires confirmation).

Security
- Do not commit ODOO passwords or API keys. The script reads the environment first and falls back to a local .env in the skill folder if present.

Files
- scripts/generate_map.py — main generator script.

