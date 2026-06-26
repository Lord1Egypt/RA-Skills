---
kind: local-app | website
name: Target Name
app_id: com.example.app
domain: example.com
aliases: [Alias 1, Alias 2]
updated: YYYY-MM-DD
---

## Platform traits
- Facts about the target platform, UI model, login dependency, loading style, or execution constraints.

## Successful paths
- [YYYY-MM-DD] Preferred path: exact validated action chain.
- [YYYY-MM-DD] Alternate path: when the preferred one does not apply.

## Preconditions
- What must already be true before starting.

## Verification
- How to confirm success using the strongest available signal.

## Unstable or failed paths
- [YYYY-MM-DD] What failed or is not recommended, and why.

## Recommended default
- The default route to try first next time.

## Notes for future runs
- Extra target-specific observations worth reusing.
