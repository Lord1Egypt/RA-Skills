Contact Map Skill (contact-map-bm)

This skill contains a simple Python script to generate an interactive HTML map of your Odoo contacts.

Usage:
  cd ~/.openclaw/workspace/skills/contact-map-bm
  python3 scripts/generate_map.py

Notes:
- The script respects Nominatim usage (1 request/sec). Generating for many contacts may take several minutes.
- The script writes to: ~/.openclaw/workspace/odoo_contacts_germany_map.html
- You can create a .env in this folder with ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD to avoid relying on shell env.

If you want this skill to be the default handler when you ask "show contacts on map", I can register it as the builtin handler in OpenClaw (requires config changes).