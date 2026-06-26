VRM endpoints used

- Dashboard / installation: https://vrm.victronenergy.com/installation/<id>/dashboard
- API (token-based) — this script expects a personal API token. Common endpoints used:
  - /api/installations/<installationId>/latest (for latest measurements)
  - /api/installations/<installationId>/history?start=<iso>&end=<iso>&resolution=60 (hourly or per-minute depending on API availability)

Authentication: set VRM_API_KEY environment variable or pass --api-key to the script. The key must have read access to the installations.
