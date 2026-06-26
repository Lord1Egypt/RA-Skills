---
name: apify-actors
description: Run Apify Actors, manage tasks, inspect datasets and key-value stores, and review usage via the Apify API. Use this skill when users want to automate web scraping workflows, manage data pipelines, or coordinate Apify actor runs from chat.
---

# Apify

![Apify](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/apify-dark.svg)

Access Apify via the Apify API with managed API key authentication. Run Actors, manage tasks, inspect datasets and stores, and review logs or usage from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apify-actors) for hosted connection flows and credentials so you do not need to configure Apify API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Apify |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Apify |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    Apify API      │
│   (User Chat)   │     │   (API Key)  │     │   (Actors)       │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Apify      │                       │
          │                       │  4. Secure Proxy       │
          │                       │  5. API Requests        │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  Apify   │
    │  File    │           │ Auth     │           │ Console  │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Apify again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Apify tools
clawlink_list_tools --integration apify

# Search for a specific tool
clawlink_search_tools --query "actor" --integration apify
```

## Authentication

All Apify tool calls are authenticated automatically by ClawLink using the user's connected Apify API credentials.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every Apify API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=apify and connect Apify.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `apify` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration apify
```

**Response:** Returns the live tool catalog for Apify.

### Reconnect

If Apify tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=apify
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration apify`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Apify is connected.
2. Call `clawlink_list_tools --integration apify` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `apify`.
5. If no Apify tools appear, direct the user to https://claw-link.dev/dashboard?add=apify.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List actors → Get dataset items → Return data   │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute actor run                                │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer inspecting Actors, tasks, datasets, stores, queues, schedules, logs, and usage before launching new runs.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Tool Reference

### Actors& Versions

| Tool | Description | Mode |
|------|-------------|------|
| `apify_acts_get` | List all Actors for the user | Read |
| `apify_get_actor` | Get Actor details by ID | Read |
| `apify_act_versions_get` | List versions of an Actor | Read |
| `apify_act_version_get` | Get a specific Actor version | Read |
| `apify_create_actor` | Create a new Actor | Write |
| `apify_delete_actor` | Delete an Actor | Write |

### Actor Runs

| Tool | Description | Mode |
|------|-------------|------|
| `apify_run_actor` | Run an Actor asynchronously | Write |
| `apify_run_actor_sync` | Run an Actor synchronously | Write |
| `apify_get_actor_last_run_dataset_items` | Get dataset items from last Actor run | Read |
| `apify_get_list_of_runs` | List runs for an Actor | Read |
| `apify_get_log` | Get log for an Actor run | Read |
| `apify_actor_run_abort_post` | Abort a running Actor | Write |
| `apify_actor_run_delete` | Delete a finished Actor run | Write |

### Tasks

| Tool | Description | Mode |
|------|-------------|------|
| `apify_get_list_of_tasks` | List all tasks | Read |
| `apify_actor_task_get` | Get task details | Read |
| `apify_actor_task_run_sync_get` | Run a task synchronously | Write |
| `apify_create_task` | Create a new task | Write |
| `apify_actor_task_delete` | Delete a task | Write |

### Datasets

| Tool | Description | Mode |
|------|-------------|------|
| `apify_datasets_get` | List all datasets | Read |
| `apify_dataset_get` | Get dataset metadata | Read |
| `apify_get_dataset_items` | Get items from a dataset | Read |
| `apify_store_data_in_dataset` | Store data in a dataset | Write |
| `apify_dataset_delete` | Delete a dataset | Write |

### Key-Value Stores

| Tool | Description | Mode |
|------|-------------|------|
| `apify_key_value_stores_get` | List key-value stores | Read |
| `apify_key_value_store_get` | Get key-value store metadata | Read |
| `apify_get_key_value_record` | Get a record from a store | Read |
| `apify_store_data_in_key_value_store` | Store data in a key-value store | Write |
| `apify_key_value_store_delete` | Delete a key-value store | Write |

### Request Queues

| Tool | Description | Mode |
|------|-------------|------|
| `apify_request_queues_get` | List request queues | Read |
| `apify_request_queue_get` | Get queue metadata | Read |
| `apify_request_queue_requests_get` | List requests in a queue | Read |
| `apify_request_queue_requests_post` | Add a request to a queue | Write |
| `apify_request_queue_delete` | Delete a request queue | Write |

### Schedules

| Tool | Description | Mode |
|------|-------------|------|
| `apify_schedules_get` | List all schedules | Read |
| `apify_schedule_get` | Get schedule details | Read |
| `apify_schedules_post` | Create a new schedule | Write |
| `apify_schedule_delete` | Delete a schedule | Write |

## Code Examples

### List Actors

```bash
clawlink_call_tool --tool "apify_acts_get" \
  --params '{
    "my": 1
  }'
```

### Run an Actor synchronously

```bash
clawlink_call_tool --tool "apify_run_actor_sync" \
  --params '{
    "actor_id": "apify/web-scraper",
    "input": {
      "startUrls": [{"url": "https://example.com"}]
    }
  }'
```

### Get dataset items

```bash
clawlink_call_tool --tool "apify_get_dataset_items" \
  --params '{
    "dataset_id": "YOUR_DATASET_ID",
    "limit": 100
  }'
```

### Create a task

```bash
clawlink_call_tool --tool "apify_create_task" \
  --params '{
    "actor_id": "apify/web-scraper",
    "name": "My Scraper Task",
    "input": {
      "startUrls": [{"url": "https://example.com"}]
    }
  }'
```

## Security & Permissions

- Access is scoped to the connected Apify account's data and Actor runs.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting Actors, datasets, queues, schedules) are marked as high-impact and must be confirmed.
- Running Actors incurs compute costs; confirm before launching runs.
- Synchronous Actor runs timeout after 300 seconds; prefer async runs for large datasets.

## Notes

- Actor IDs use the format `username/actor-name` or just `actor-name` for public Actors.
- For datasets larger than 1000 items, use pagination (offset/limit) to retrieve in batches.
- Logs are limited to the trailing 5 million characters.
- Synchronous runs are best for quick scrapes; longer jobs should use async runs.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration apify`. |
| Missing connection | Apify is not connected. Direct the user to https://claw-link.dev/dashboard?add=apify. |
| `Actor not found` | The Actor ID does not exist or is not accessible. |
| `Run timeout` | Synchronous run exceeded 300 seconds. Use async run instead. |
| `Dataset empty` | The dataset has no items or the run is still in progress. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `apify`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Apify API Documentation](https://docs.apify.com/api/v2)
- [Apify Platform](https://apify.com/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apify-actors
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apify-actors)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
