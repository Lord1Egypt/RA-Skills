# Delivery Verification

Before delivery, confirm:

- The report states an observation or research date.
- Each material factual claim has a directly supporting source URL nearby.
- Volatile product, pricing, hiring, and review evidence includes its observation date.
- Facts, inferences, recommendations, and unknowns are visibly distinguished.
- Major findings include a confidence level and rationale.
- `Not found publicly` has not been rewritten as `absent`.
- Vendors are compared with equivalent scope, dates, geography, units, and workload.
- Failed, inaccessible, contradictory, and missing sources are disclosed.
- Review or listing samples are deduplicated and their size and bias are stated.
- Recommendations trace back to findings and are prioritized for the user's decision.

Run `python3 scripts/verify_report.py <report.md>` for the minimum structural gate. Passing the script does not prove that citations support the claims; inspect that relationship manually.
