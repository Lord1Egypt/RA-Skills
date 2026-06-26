# KNOWLEDGE_MAP.md — Confidence Overlay

> Optional Advanced overlay.
> Track what the agent knows, how reliable it seems, and when it was last verified.
> Prefer coarse bands over fake precision.

---

## Domain Confidence

| Domain | Confidence | Sources | Last Verified | Notes |
|---|---|---|---|---|
| _Example: User preferences_ | 🟢 | `USER.md`, `MEMORY.md` | YYYY-MM-DD | _High confidence, frequently verified_ |
| _Example: Project X_ | 🟡 | `memory/bank/project-x.md` | YYYY-MM-DD | _Useful but only partially current_ |
| _Example: Vendor policy details_ | 🔴 | `memory/bank/vendors.md` | YYYY-MM-DD | _Needs re-check before acting_ |

## Known Gaps

| Gap | Times Hit | Last Hit | Suggested Action |
|---|---:|---|---|
| _Example: API rate limits_ | 2 | YYYY-MM-DD | _Research and document_ |

## Notes

- `Last Verified` matters more than pseudo-precise scoring.
- Only raise confidence when supported by successful use or fresh evidence.
- If uncertain, mark the domain conservatively or tag related proposals `[NEEDS_REVIEW]`.
