# Configuration Guide

## Website List

The `gx_websites.json` file contains the platform URLs organized by category. Edit this file to:

1. Add new platforms
2. Remove outdated platforms
3. Add your own account credentials (in the `auth_required` section)

## Adding Credentials

For platforms that require login, add entries under `auth_required.sites`:

```json
{
  "name": "Platform Name",
  "url": "https://example.com/login",
  "account": "your_username",
  "password": "your_password",
  "note": "Optional note"
}
```

## Scanning Script

The main script `gx_bidding_monitor.py` uses OpenClaw's browser tool for scanning. It requires:

- Python 3.8+
- `httpx`, `beautifulsoup4`, `lxml`
- OpenClaw gateway with browser (Chrome/Chromium)

## Platform Maintenance

- Government websites occasionally restructure URLs
- Check platform accessibility periodically
- Update `gx_websites.json` when URLs change
- Some platforms require periodic re-login to maintain session
