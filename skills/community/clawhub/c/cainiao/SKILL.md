---
name: cainiao
description: Use Cainiao Network (菜鸟物流) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.
version: 1.0.0
tags: logistics, shipping, cainiao, aggregation, cross-border, china
---

# Cainiao Network (菜鸟物流)

## Overview

Use this skill to help users with common Cainiao tasks such as tracking shipments, understanding service levels, estimating timing or fees, and preparing to send a parcel.

## Usage Scenarios

### Scenario 1: Track a Cainiao-managed cross-border shipment
**User input:** "我在淘宝海淘的包裹，菜鸟单号 CN1234567890 到哪了？"
**Expected output:** Show consolidated tracking information for the cross-border shipment, including the outbound leg (China warehouse → departure), international transit, customs clearance status (e.g., "清关中"), and domestic delivery leg (最后一公里). Explain Cainiao's role as the logistics aggregator across multiple carriers.

### Scenario 2: Find a Cainiao Station (菜鸟驿站) for pickup
**User input:** "我的快递放到菜鸟驿站了，怎么查取件码？"
**Expected output:** Guide the user on retrieving the pickup code via the Cainiao app, Taobao app, or SMS notification. Explain what to do if they missed the notification (check order details, contact station) and typical Cainiao Station operating hours.

### Scenario 3: Estimate Cainiao shipping for cross-border e-commerce
**User input:** "从中国寄到美国，走菜鸟的国际物流，5公斤大概多少钱，多久到？"
**Expected output:** Provide an estimate covering Cainiao's cross-border logistics options: Cainiao Super Economy (海运/空运), Cainiao Standard (空运), and Cainiao Express (优先). Compare transit times (10-30 days depending on service), pricing tiers, and customs implications. Note that Cainiao aggregates from multiple carriers so specific tracking may involve handoffs.
### Scenario 4: 菜鸟裹裹查所有包裹
**User input:** "帮我看看我最近一周的菜鸟裹裹包裹列表，有没有一个从义乌发过来的到了驿站还没取？"
**Expected output:** 列出用户菜鸟账号下近7天的所有在途/待取/已签收包裹。根据描述筛选出义乌发出的包裹，查看其最新物流状态。如果已到达驿站，提醒用户取件码和驿站位置（如兔喜超市、妈妈驿站等），以及超期保管规则。

## Local Persistence

When the local CLI/runtime code is used, this skill may create and persist local data under:

- `~/.openclaw/data/cainiao/cainiao.db`
  - stores query history
  - stores shipment-subscription records
  - may store saved address records if those commands are implemented/used
- `~/.openclaw/data/cainiao/secure/`
  - stores encrypted local files used by the privacy/storage helper
- `~/.openclaw/data/cainiao/secure/.key`
  - stores a local encryption key file with mode `600`
- `~/.openclaw/data/cainiao/privacy_export.json`
  - may be created when the user runs privacy export

Only use persistence when it is necessary for the user's requested workflow. If the user asks about privacy, disclose these paths clearly.

## Privacy Controls

The local CLI supports privacy operations:

- `privacy info` — show local storage paths and stored-file info
- `privacy clear` — clear local SQLite history/subscription data and encrypted local files
- `privacy export` — export local storage metadata to `privacy_export.json`

## Workflow

1. Determine the user's goal:
   - track an existing shipment
   - estimate fee or delivery time
   - compare service types
   - find a nearby outlet or pickup point (Cainiao Station)
   - prepare shipment details
   - review or clear local history/subscriptions/privacy data
2. Ask for only the missing essentials, such as tracking number, route, package size, or urgency.
3. Give the most practical answer first.
4. If exact fee or timing cannot be confirmed, provide a cautious estimate and state assumptions.
5. If the task uses local runtime features that persist data, mention that local history/subscription/privacy files may be created under `~/.openclaw/data/cainiao/`.
6. Do not claim to complete real shipping actions unless live tools are available and confirmed.
