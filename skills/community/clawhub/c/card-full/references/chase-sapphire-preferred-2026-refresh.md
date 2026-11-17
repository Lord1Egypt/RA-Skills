# Chase Sapphire Preferred 2026 Refresh / Offer Extraction Note

Session learning from a Chase Sapphire Preferred full report (June 2026).

## What happened

- Chase issuer page was accessible, but simple HTML/text extraction rendered the welcome offer as: `Earn 75,000 strikethrough 100,000 points`.
- That ordering is ambiguous in plain text: it can look like 75K active and 100K crossed out, or vice versa.
- Browser visual inspection showed the actual rendering: **75,000 was struck through; 100,000 was active**.
- TPG had a same-day article confirming the 100K limited-time offer after $5,000 spend in 3 months.
- Upgraded Points metadata still showed 75K, likely stale after the refresh.

## Reusable rule

For card welcome offers with refreshed pages, crossed-out amounts, or `strikethrough` text:

1. Treat raw DOM/plain-text extraction as insufficient.
2. Verify visually with browser/screenshot tools when available.
3. Cross-check with an approved secondary source dated close to the query date.
4. If secondary sources conflict, favor issuer visual rendering + freshest approved source, and flag the conflict in Confidence Notes.

## Chase CSP 2026 refresh facts observed

- Active issuer offer: 100,000 Ultimate Rewards points after $5,000 spend in first 3 months.
- Struck-through prior offer: 75,000 points.
- Annual fee: $95.
- Notable refreshed benefits surfaced on issuer page:
  - $100 Chase Travel hotel credit each account anniversary year.
  - Up to $120 Global Entry / TSA PreCheck / NEXUS every 4 years.
  - Complimentary Apple TV for 12 months when activated by Dec 31, 2026.
  - DoorDash DashPass + $10/month promo through Dec 31, 2027.
  - 3x gas stations, EV charging, vacation homes at top brands.

## Confidence handling

If an approved secondary page lags the issuer refresh, do not hide it. State the conflict briefly, e.g. `Upgraded Points still showed 75K metadata; issuer visual page + TPG same-day report support 100K.`
