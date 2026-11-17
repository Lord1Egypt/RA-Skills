# Input and channel mapping

Build a source-to-canonical field map before analysis. Keep original column names and record every transformation.

## Canonical entities

- Transaction: order, trade, booking, invoice, subscription event, or project event.
- Line item: product, service, SKU, package, add-on, or resource.
- Customer: customer, buyer, member, account, lead, or platform-scoped anonymous user.
- Channel: POS, mini-program, Meituan, Youzan, Eleme, Douyin, marketplace, walk-in, direct sales, or another source.
- Location or resource: store, venue, room, court, class, staff member, warehouse, or service point.

Map at least: primary key, event time, status, quantity, list amount, customer-paid amount, refund, merchant discount, platform discount, delivery charge, commission, service fee, settlement, cost, tax, customer key, product or service key, channel, store, and fulfillment type when available.

## Meituan

- Treat Meituan customer identifiers as platform-scoped. Do not claim cross-channel identity.
- Separate merchant discounts from platform-funded discounts.
- Distinguish customer payment, platform fees, delivery charges, refunds, and merchant settlement.
- Delivery charges collected for a rider or platform are not merchant revenue unless the export explicitly defines them that way.
- Use stable encrypted buyer identifiers for new and returning analysis only when they are consistent across the selected period. Otherwise show order behavior without customer claims.

## Youzan

- Map trade, order, payment, refund, buyer, member, source, sales channel, store, and settlement exports separately when needed.
- Prefer stable buyer or member IDs to display names and phone fragments.
- Distinguish paid amount from settlement and recognize partial refunds at the correct grain.
- A member and a buyer can be different identity scopes; merge only with an explicit relation.

## Mini-program, POS, and service-provider systems

- Preserve the originating system and store. A mobile number, openid, unionid, membership ID, and POS customer ID are different keys until a verified mapping joins them.
- For mini-program orders, distinguish payment channel from order channel.
- For POS, handle anonymous walk-in orders separately from identified members.
- For SaaS exports, inspect whether the report is order-level, item-level, settlement-level, or daily aggregate before joining.

## Multiple files and databases

- Detect duplicate exports and overlapping date windows before unioning.
- Aggregate line items before joining to order-level tables when a join would multiply revenue.
- In SQLite, inspect table schemas and row counts first, then trace keys with small samples.
- Preserve cancellations, refunds, and reversals long enough to reconcile final totals.

## Identity and coverage

Calculate identifiable customer coverage as identified valid transactions divided by eligible transactions. Restrict frequency, new and returning, and retention metrics to the valid identity scope. Display the scope in plain language near the chart when it affects interpretation.
