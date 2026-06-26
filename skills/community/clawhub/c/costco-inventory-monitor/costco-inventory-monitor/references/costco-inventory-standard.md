# Costco Inventory Monitoring Standard

## 1) Scope

Track one or more Costco products across one or more ZIP codes and emit structured status snapshots.

## 2) Snapshot Schema

Each check should write one record per `product_id + zip_code` pair:

```json
{
  "timestamp_utc": "2026-04-02T00:00:00Z",
  "run_fingerprint": "run-xxxx",
  "product_id": "4000362984",
  "product_name": "TCL 55\" Q77K",
  "product_url": "https://www.costco.com/...",
  "zip_code": "03051",
  "availability": "in_stock",
  "delivery_message": "Estimated delivery in 3-5 business days",
  "source": "browser|api",
  "raw_excerpt": "optional status snippet"
}
```

## 3) Availability Taxonomy

- `in_stock`: purchasable now
- `limited_stock`: purchasable with constrained quantity
- `out_of_stock`: unavailable in current ZIP
- `unknown`: parsing failed or ambiguous signal

## 4) Cadence Policy

- Normal products: every 60 minutes
- High-demand products: every 15-30 minutes
- Spike/flash sale watch: every 3-10 minutes
- Overnight quiet window allowed, but keep at least one check every 6 hours

## 5) Fingerprint Policy

When polling every few minutes:

- default to `random` fingerprint per run;
- rotate request metadata safely (user-agent / session identifiers) in your runner;
- avoid generating one fingerprint per request inside the same run unless anti-bot pressure requires it.

Modes:

- `random`: new run fingerprint each execution
- `stable`: deterministic fingerprint from config payload
- `none`: disabled

## 6) Alert Rules

Trigger alert when:

1. `out_of_stock -> in_stock`
2. `unknown` persists for 3 consecutive checks
3. Product disappears or URL starts returning error pages

Deduplicate alerts inside a 30-minute suppression window.

## 7) Initial Rollout for User Example

Primary product: `4000362984` (TCL 55" Q77K TV).

Primary ZIPs:

- `03051` (Hudson, NH area)
- `97230` (Portland, OR area)

Recommended rollout:

1. Start with 5-minute checks for first 2 hours.
2. Then 15-minute checks for 24 hours.
3. If stable, downgrade to 30-60-minute checks.
4. Keep separate alert routing per ZIP for regional demand visibility.

## 8) Operational Notes

- Preserve raw response excerpts for parser debugging.
- Keep at least 14 days of snapshots for trend analysis.
- If automation endpoint changes, temporarily mark as `unknown` and fail open (do not infer `out_of_stock`).

## 9) Network Path & Proxy Baseline

When Costco edge returns Akamai deny pages (e.g., HTTP 403 with "You don't have permission"), treat this as a network-path incident, not inventory signal.

Recommended baseline:

- Primary path: `residential_proxy` (home broadband IPs) for high-frequency checks.
- Keep `direct` as fallback/diagnostic only.
- Prefer sticky session (`proxy_rotate_per_request=false` + fixed `proxy_session_id`) for multi-step page flow.
- Switch to rotation mode (`proxy_rotate_per_request=true`) if repeated CAPTCHA or deny pages occur on a sticky IP.

Incident handling for Akamai block:

1. Mark current snapshot `availability=unknown`.
2. Record `http_status`, deny-body excerpt, and active proxy metadata.
3. Retry through residential proxy path.
4. Only alert after 3 consecutive blocked checks (same product+ZIP) to avoid noisy alarms.
