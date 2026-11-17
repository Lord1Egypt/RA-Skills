# Bill Query Catalog

This table lists common high-priority paths. It is **not a closed allowlist**. Start with the smallest bill query that can answer the question. Every concrete product Action run by this Skill must include the global flag `--invoke-source ctyun-analyze-billing`. Local `ctyun-cli bill <Action> --help` is the source of truth for Action behavior, flags, pagination, and response fields.

| Intent | Preferred Action | Required flags | Optional filters | Pagination | Notes |
| --- | --- | --- | --- | --- | --- |
| Consumption, refund, adjustment summary | `QueryMonthlyBillSummary` | `billingCycleId` | `contractId` | No | Start here for overall spend. |
| Product cycle analysis | `QueryProductCycleBill` | `billingCycleId`, `pageNo`, `pageSize` | `billMode`, `billType`, `contractId`, `groupByonDay`, `isZeroFileter`, `offset`, `payMethod`, `productCode`, `projectId`, `resourceId` | Yes | Use for product-level costs. |
| Resource cycle analysis | `QueryResourceCycleBill` | `billingCycleId`, `pageNo`, `pageSize` | `billMode`, `billType`, `contractId`, `groupByonDay`, `isZeroFileter`, `offset`, `payMethod`, `productCode`, `projectId`, `resourceId` | Yes | Use for resource-level costs. |
| Resource detail analysis | `QueryResourceDetailBill` | `billingCycleId`, `pageNo`, `pageSize` | `billMode`, `billType`, `contractId`, `isZeroFileter`, `offset`, `payMethod`, `productCode`, `projectId`, `resourceId` | Yes | Apply a bill-derived resource filter when possible. |
| Usage cycle analysis | `QueryUsageCycleBill` | `accountId`, `billingCycleId`, `pageNo`, `pageSize`, `userId` | `billMode`, `billType`, `contractId`, `groupByonDay`, `isZeroFileter`, `offset`, `payMethod`, `productCode`, `projectId`, `resourceId` | Yes | Recheck local help for identity flags. |
| Usage detail analysis | `QueryUsageDetailBill` | `billingCycleId`, `pageNo`, `pageSize` | `billMode`, `billType`, `contractId`, `isZeroFileter`, `offset`, `payMethod`, `productCode`, `projectId`, `resourceId` | Yes | Use only when the question needs usage detail. |
| On-demand transaction analysis | `QueryQueryBillOnDemandFee` | `billingCycleId` | `billType`, `contractId`, `hasTotal`, `masterOrderId`, `pageNo`, `pageSize`, `payMethod`, `productCode`, `projectId` | When the API returns a total | Check the response before assuming pagination. |

For an Action not in this table, run:

```text
ctyun-cli bill --help
ctyun-cli bill <Action> --help
```

Use it only after confirming that it is read-only and the scope is approved. Stop when its behavior or change risk is unclear.
