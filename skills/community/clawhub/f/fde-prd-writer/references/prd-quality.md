# FDE PRD quality gate

Check item by item. Any "no" should be fixed, or listed in `[to be confirmed]` and the downstream skills and decisions it blocks should be explained.

| Check items | Passing standards |
|---|---|
| Upstream Complete | There is #1 questionable evidence vs. #2 POC deed source; the gap is not disguised as fact. |
| POC Boundaries | Have the scope of this issue, clearly do not do anything, and "this POC does not prove anything". |
| Complete behavior | Key requirements cover triggers, preconditions, main process, rules and exceptions/boundaries. |
| Data and Permissions | When it comes to data, integration or sensitive operations, sources, permissions, verification, failure handling and Mock boundaries can be determined. |
| Acceptable | AC can be observed and judged, avoiding subjective expressions such as "good experience" and "support". |
| Testable | Test or demo scenarios for every important AC mapping; high-risk paths cover failures and permissions. |
| Available for handover | The minimum inputs for #4, #5, #6, and #7 have been written into "Downstream Handover" respectively. |
| Decision-making | Risks, dependencies, assumptions, items to be confirmed have impact, owner or next step. |
