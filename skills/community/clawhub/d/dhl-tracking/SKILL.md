---
name: dhl-tracking
description: Track DHL parcels in Germany via the dhl.de API. Use when a user asks to track a DHL package, check delivery status, monitor a shipment, or wants notifications about a DHL Sendungsnummer. Works with standard DHL parcel tracking numbers (00340...). No API key required.
---

# DHL Tracking

Track DHL parcels via the `dhl.de` internal API endpoint using simple HTTP requests.

## Important: Why this skill exists

DHL's tracking website (`dhl.de/sendungsverfolgung`) is a JavaScript SPA protected by Akamai Bot Manager. The SPA renders tracking data client-side after passing bot checks — headless browsers (even with stealth patches) fail due to TLS fingerprinting.

**The solution:** A simple `curl` to `www.dhl.de/int-verfolgen/data/search` with minimal headers returns full tracking JSON. No auth, no cookies, no JS needed.

## Quick Usage

### Bash (one-liner)
```bash
bash scripts/dhl_track.sh TRACKING_NUMBER
```

### Python (formatted output)
```bash
python3 scripts/dhl_track.py TRACKING_NUMBER
```

### Direct curl
```bash
curl -s 'https://www.dhl.de/int-verfolgen/data/search?piececode=TRACKING_NUMBER&language=de' \
  -H 'Accept: application/json' -H 'User-Agent: Mozilla/5.0'
```

## Response Structure

```
sendungen[0].sendungsdetails.sendungsverlauf:
  .status              → Current status text (German)
  .fortschritt         → Progress (0-5)
  .maximalFortschritt  → Always 5
  .events[]            → Array of {datum, status, ruecksendung}

sendungen[0].sendungsdetails.zustellung:
  .zustellzeitfensterVon/Bis → Delivery window

sendungen[0].sendungsdetails.istZugestellt → boolean
```

### Progress values
- **0-1**: Label created / picked up
- **2**: In transit
- **3**: In recipient's region
- **4**: Out for delivery (loaded onto delivery vehicle)
- **5**: Delivered

## Monitoring Pattern

To monitor a package and notify when close to delivery:

1. Run `python3 scripts/dhl_track.py TRACKING_NUMBER` periodically (cron, every 30 min)
2. Parse `fortschritt` from stderr JSON output
3. Notify user when `fortschritt >= 4` (out for delivery)

## What does NOT work (and why this skill exists)

- **`web_fetch` on dhl.de** → only gets static HTML shell, no tracking data (JS SPA)
- **Headless Chrome on dhl.de** → Akamai blocks internal API via TLS fingerprinting (returns 404)
- **Stealth patches** (fake UA, hide webdriver, fake plugins) → still detected by TLS/JA3 fingerprint
- **`nolp.dhl.de` legacy endpoint** → now also protected by Akamai (returns 500)
- **DHL public API (`api-eu.dhl.com`)** → requires API key registration
- **Third-party trackers** (17track, parcelsapp) → often delayed or incomplete for DE parcels

## Notes

- Works for German DHL Paket numbers (typically `0034...`)
- Language: `language=de` (German) or `language=en` (English)
- Be reasonable with polling (max once per minute)
- If the API starts returning 404/HTML, the Akamai protection may have expanded — try varying the User-Agent or adding a `Referer: https://www.dhl.de/` header
