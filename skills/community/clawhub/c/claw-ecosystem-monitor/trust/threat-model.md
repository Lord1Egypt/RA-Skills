# Threat Model

## Assets

- Source-quality decisions.
- Generated metadata snapshots.
- Public persona reputation.
- Future product trust surface.

## Threats

| Threat | Mitigation |
|---|---|
| Scraping disallowed or rate-limited surfaces | Use official APIs and stop on 403/429/robots changes. |
| Accidental content mirroring | Store metadata, hashes, timestamps, short summaries, and links only. |
| Secret leakage | Default no-secret operation; no `.env` reads; no header persistence. |
| False claims in reports | Include source URL and request timestamp for every signal. |
| Platform policy drift | Re-check `source_quality.yaml` before public release and weekly thereafter. |
| Reputation damage from AI-assisted PRs | E1 requires repo policy review, disclosure, tests, and human-owned final submission. |
| Premature payment integration | No payment code, hosted API, checkout, invoice flow, or donation link in this free skill. |

## Residual Risk

Public metadata terms can change. Any warning, 403, 429, DMCA, or platform complaint pauses the relevant source until reviewed.
