# Connectivity Workflows

Use this reference when helping with eSIM installation, VPN setup, provider readiness, or mobile troubleshooting.

## eSIM Rules

- Check `GET /api/esim/status` before offering live purchase or topup actions.
- Prefer existing profiles from `GET /api/esim/profiles` over re-listing the whole catalog if the user already owns a plan.
- After purchase, lead with install-ready fields like `qrData`, `iosTapLink`, and `esimPassportUrl`.
- For iPhone, prefer the iOS install link when present.
- For Android or desktop, QR and activation strings are the normal fallback.

## VPN Rules

- Check `GET /api/vpn/status` before promising activation.
- Freeland VPN is subscription plus WireGuard config delivery.
- Do not describe it as an in-browser VPN tunnel.
- After activation, guide the user to import the WireGuard config into the WireGuard app.

## Readiness Language

- `providerAvailable=false` means the service is offline in this environment.
- If the provider is unavailable, do not continue with purchase or activation flows.
- Surface install help only after confirming the profile or subscription exists.
