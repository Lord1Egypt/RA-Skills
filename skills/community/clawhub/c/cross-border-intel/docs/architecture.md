# Historical architecture reference

This document is kept as historical context for the local-first direction of `cross-border-intel`.

Some details remain useful for understanding the original migration goals, but the current source of truth for the runnable skill is the code in `lib/`, `scripts/`, and the overview in `SKILL.md`.

---

# cross-border-intel local-first architecture

## Overview

`cross-border-intel` should evolve from a thin shell that proxies a backend-owned product into a local-first OpenClaw application.

The backend remains the control plane for authentication, quota enforcement, third-party provider access, and optional AI summarization or delivery capabilities. The skill becomes the runtime plane that owns user-facing state inside each OpenClaw instance.

This architecture matches the intended product model:

- users add watchlist items conversationally inside OpenClaw chat
- users ask follow-up questions against previously collected reports and alerts
- users can schedule scans and report delivery from the instance itself
- vendor secrets stay off the instance
- the skill feels stateful even when backend APIs are temporarily unavailable

## Why the current model is not enough

The current `/intel/*` backend APIs own watchlists, snapshots, alerts, reports, config, and cron-driven workflows. The skill only triggers those backend workflows.

That design creates three product mismatches:

1. chat continuity lives in the wrong place
    - the backend stores business state, but the user interacts inside OpenClaw chat on a specific instance
    - follow-up questions should resolve against the instance-local history the user has already built

2. scheduling belongs to the instance
    - users expect report cadence and monitoring behavior to follow the OpenClaw instance they are using
    - backend cron jobs make the feature feel remote instead of native

3. the skill cannot act like an application
    - a shell wrapper around backend CRUD is not enough for local conversational ownership
    - the skill should be able to inspect, compare, summarize, and reason over locally persisted history

## Target split of responsibilities

### clawhost backend responsibilities

The backend remains responsible for capabilities that should stay centralized:

- authenticate gateway tokens and user tokens
- rate limiting and quota governance
- provider secret ownership
- provider calls to Keepa and TikHub
- optional notification delivery capabilities such as Telegram
- migration and backward compatibility for legacy backend-owned intel routes

The backend should trend toward capability endpoints instead of product-state endpoints.

Examples:

- fetch Amazon product data through Keepa
- fetch TikTok search results through TikHub
- optionally deliver alerts or reports through configured delivery providers

### skill responsibilities

The skill becomes the canonical owner of local application state:

- watchlists
- snapshots
- alerts
- reports
- schedules
- local workflow metadata
- chat-facing continuity and follow-up context

The skill should be able to perform the full product loop locally:

1. persist watchlist changes
2. fetch provider data from backend capability endpoints
3. store raw and normalized observations locally
4. compare new and previous observations
5. create alerts locally
6. generate reports locally
7. schedule the next run locally
8. answer chat questions from local state

## Runtime assumptions

OpenClaw gateway is started with instance-specific runtime information:

- `OPENCLAW_CONFIG_PATH=configPath`
- `OPENCLAW_STATE_DIR=clawDir`
- instance `.env` loaded from `clawDir/.env`

The skill should use these runtime guarantees.

### Configuration sources

The skill should resolve runtime data in this order:

1. `OPENCLAW_GATEWAY_TOKEN` if present
2. gateway token from `OPENCLAW_CONFIG_PATH` or `~/.openclaw/openclaw.json`
3. `OPENCLAW_STATE_DIR` for state ownership
4. `INTEL_API_URL` from instance `.env`

## Local storage model

The skill should own a SQLite database under the instance state directory.

Recommended path:

- `${OPENCLAW_STATE_DIR}/skills/cross-border-intel/local.sqlite3`

SQLite is a good fit because it is:

- local to the instance
- simple to back up and inspect
- strong enough for snapshots, alerts, reports, and schedules
- easy to query from shell-based tooling during the transition period

## Local data model

### `config`

Local preferences and feature flags.

Suggested contents:

- alert thresholds
- report preferences
- schedule preferences
- local feature enablement state
- optional delivery configuration references

### `watchlists`

Canonical local watchlist items.

Suggested fields:

- `id`
- `sourceType`
- `value`
- `domain`
- `isActive`
- `createdAt`
- `updatedAt`

### `amazon_snapshots`

Normalized Amazon observations keyed by watchlist item.

Suggested fields:

- `id`
- `watchlistId`
- `asin`
- `title`
- `price`
- `currency`
- `bsr`
- `bsrCategory`
- `reviewCount`
- `rating`
- `seller`
- `imageUrl`
- `snapshotDate`
- `rawData`
- `createdAt`

### `tiktok_hits`

Normalized TikTok search results keyed by watchlist item or keyword.

Suggested fields:

- `id`
- `watchlistId`
- `keyword`
- `videoId`
- `authorName`
- `description`
- `playCount`
- `likeCount`
- `commentCount`
- `shareCount`
- `publishTime`
- `rawData`
- `createdAt`

### `alerts`

Locally detected alert events.

Suggested fields:

- `id`
- `watchlistId`
- `snapshotId`
- `type`
- `source`
- `title`
- `detail`
- `pushedAt`
- `createdAt`

### `reports`

Locally generated reports.

Suggested fields:

- `id`
- `reportType`
- `content`
- `periodStart`
- `periodEnd`
- `summarySource`
- `pushedAt`
- `createdAt`

### `jobs`

Local scheduling and lock state.

Suggested fields:

- `id`
- `jobType`
- `cadence`
- `enabled`
- `lastRunAt`
- `nextRunAt`
- `lockToken`
- `lockExpiresAt`
- `createdAt`
- `updatedAt`

## Backend capability design

The backend should gradually move from stateful `/intel/*` product APIs toward capability-oriented endpoints.

### Capability families

#### Provider fetch capabilities

These endpoints wrap vendor integrations and return normalized data without persisting user business state.

Examples:

- `POST /intel/capabilities/amazon/product`
- `POST /intel/capabilities/tiktok/search`

#### Optional delivery capabilities

These endpoints deliver already-generated local alerts or reports.

Examples:

- `POST /intel/capabilities/notifications/telegram`

## Primary chat workflows

### Watchlist management in chat

The user should be able to say:

- add this ASIN to my watchlist
- stop tracking this product
- show what I am watching

The skill should persist those changes immediately to the local SQLite database.

### Scan and compare

The user should be able to ask:

- scan my Amazon watchlist now
- what changed since yesterday

The skill should:

1. read local active watchlist items
2. call backend provider capability endpoints
3. store new snapshots locally
4. compare against previous snapshots
5. create local alerts
6. surface the result directly in chat

### Report generation and follow-up

The user should be able to ask:

- generate today’s report
- summarize the last week
- why did this report call out that product

The skill should generate and store the report locally, then answer follow-up questions from the same persisted dataset.

### Scheduling

The user should be able to say:

- run Amazon scans every morning
- send me a weekly summary on Friday

The skill should update local `jobs` state and own schedule execution from the instance.

## Migration strategy

### Short term

- keep existing backend `/intel/*` product routes available for compatibility
- add new capability endpoints alongside them
- stop building new skill behavior on top of backend-owned state
- make the skill bootstrap local SQLite immediately

### Medium term

- move watchlist ownership fully local
- move report and alert ownership fully local
- mark centralized cron workflows as legacy
- keep backend DB tables read-only or deprecated during transition

### Long term

- reduce `/intel/*` product routes to a small control-plane surface
- preserve only backend capabilities that need central secrets or governance
- make local chat and local scheduling the default operating model

## First vertical slice

The first useful proof of architecture should implement:

1. local SQLite bootstrap in the skill
2. local `config` and `watchlists`
3. backend Amazon product capability endpoint using Keepa
4. local Amazon scan flow that stores snapshots and alerts
5. local report generation

This slice is enough to prove that the skill can own the user experience while the backend stays responsible for secrets and governance.

## Compatibility notes

- legacy backend intel tables may remain temporarily for backward compatibility
- legacy cron endpoints may remain admin-only or transitional
- shell scripts may stay as operator tools during the migration, but they should wrap local-first logic rather than define the product boundary

## Verification goals

Successful implementation should demonstrate:

- the skill can read the gateway token from runtime config
- the skill creates a SQLite database under the instance state directory
- watchlists are owned locally
- Amazon snapshots are persisted locally
- alerts are generated locally from local comparisons
- reports are generated and stored locally
- backend vendor secrets remain backend-only
- follow-up questions can be answered from instance-local history