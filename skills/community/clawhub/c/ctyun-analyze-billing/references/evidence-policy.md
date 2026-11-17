# Billing Evidence Policy

- **P0 bill data:** `bill` responses are the main source for charges that already happened.
- **P1 resource check:** use it to confirm identity and current context. It cannot replace or disprove a past bill.
- **P2 extra data:** use usage, monitoring, specs, or prices only when P0/P1 is not enough or the user asks. Missing monitoring data does not mean zero usage. Current prices do not change billed amounts.

If P0 and resource data disagree, the **bill API is the source of truth**. Report the difference. Do not change the bill fact.

Build every resource query from bill fields: `productCode`/`resourceType`/`serviceTag` → `resourceId` or `realResourceId` → `regionId`, `projectId`, period/order → the most specific read-only detail Action. Check flags with local help. Do not scan all products, regions, or accounts. A permission error does not mean the resource did not exist. A missing resource may be historical.

Check pagination. If pages are missing, use `Partial data` and do not claim a full check. Keep separate money fields and different usage units separate. For a calculation over complete visible data, state its inputs, scope, basis, and difference. Otherwise use `Partial data` or `Cannot determine`.
