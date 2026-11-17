# Worked Example

Input REST operations:

```text
GET /orders?store_id&from&to -> orders[]
GET /stores -> stores[]
```

Ingest records `ListOrders` as a read fact candidate with one row per `orders[]` element and
`ListStores` as a read dimension lookup. Review asks the user to approve Order grain, Store business
key, amount unit/additivity, time field, and route requirements; every decision cites its operation
schema.

Approved OKF emits a Sales fact, Store dimension, Revenue metric, and two API Endpoint references.
The fact links store_id to Store, amount to Revenue, and every field to its endpoint citation.
Repository YAML emits the same semantics as one catalog plus shared Store dimension and Sales model
ontology.

Verification checks that Order grain is falsifiable, Store is reused rather than duplicated, Revenue
declares currency and additivity, routes require store/time context, links resolve, and no
undocumented response field appears. Any missing money basis returns to review rather than guessing.
