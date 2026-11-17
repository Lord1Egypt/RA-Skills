---
name: boxem
description: "Boxem MCP — Amazon seller tools, analytics, repricing, listings, Lua code execution, knowledge base, and background jobs via the Boxem platform."
metadata:
  title: "Boxem"
  version: "1.0.0"
  mcp:
    url: "https://new.boxem.com/backend/mcp"
    transport: "sse"
---

# Boxem MCP

Connect to the **Boxem** MCP server for Amazon seller tools, analytics, code execution, and more.

## Server URL

```
https://new.boxem.com/backend/mcp
```

Transport: SSE (Server-Sent Events)

## Setup

### With mcporter

```bash
mcporter config add boxem --url https://new.boxem.com/backend/mcp
mcporter list boxem --schema
```

### Direct MCP connection

Add to your MCP client config:

```json
{
  "boxem": {
    "url": "https://new.boxem.com/backend/mcp",
    "transport": "sse"
  }
}
```

## Available Tools

### Amazon Product Data

- **amazonProductsCatalog** — Get product name and sales rank for ASINs.
- **amazonUngateProducts** — Check listing restrictions and get ungate URLs.
- **getBoxemSellersAmazonItemAnalyticsBySku** — Item analytics by SKU for repricing decisions.
- **repriceAmazonItems** — Change item prices. ⚠️ Not currently implemented.
- **createAmazonListings** — Create new Amazon listings.

### Analytics

- **dailyAnalyticsStats** — Daily stats by date range (up to 30 days per call).

### Code Execution

- **executeCode** — Execute Lua code. Can fetch websites via `fetch()`. Times out after 30s.
- **executeLuaFile** — Execute a Lua file by path.

### HTTP & Web

- **httpRequest** — GET/POST/PUT/DELETE requests through a proxy.

### Background Jobs

- **createIntervalJob** — Create recurring background AI jobs with tool access.
- **listIntervalJobs** — List active interval jobs with IDs and token usage.
- **deleteIntervalJobs** — Delete interval jobs by UUID.

### Notifications

- **sendEmail** — Send email notifications (also in-app).
- **boxemConfetti** — Trigger confetti animation for logged-in users.

### Knowledge Base

- **knowledge** — Index of knowledge files about FBA, WFS, e-commerce, Boxem, and selling advice.
- **knowledgeLookupWithFileIndex** — Look up a specific knowledge file by index.

### Suppliers

- **getBoxemSuppliers** — List the seller's suppliers.

### Memory

- **memory** — Persistent file-based memory for user preferences and context across conversations.
