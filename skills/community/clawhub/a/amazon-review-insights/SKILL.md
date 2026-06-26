---
name: amazon-review-insights
description: Amazon product review intelligence analysis tool for global e-commerce sellers. Core capabilities:fetch Amazon reviews, AI-powered negative review analysis, quantify high-frequency issues, discover hidden negative feedback in 5-star reviews, generate improvement suggestions, track review trends, incremental updates.
metadata:
  openclaw:
    requires:
      env:
        - CUSTOMER_INSIGHTS_API_KEY
    dependencies:
      python:
        - requests>=2.28.0
---

# AstrMap Review Insights Skill

## Language

- Reply in **English** if user input is in English or non-Chinese (as this is the unified language)
- Reply in **中文** if user input is in Chinese

## Configuration

### API Key

All API calls require an API Key for authentication.

**Note**: The API endpoint is fixed at `https://api.astrmap.com` and is not configurable.

**Recommended**: Set the environment variable in `~/.zshrc` or `~/.bashrc`:

```bash
export CUSTOMER_INSIGHTS_API_KEY="your-api-key-here"
```

> To obtain an API Key: Download and install the AstrMap desktop client from https://www.astrmap.com/, log in, click **User Menu (bottom-left)** → **API Keys**, create and copy your API Key.

**Important**: If `CUSTOMER_INSIGHTS_API_KEY` is not set or no API Key is provided, **ask the user first**:
> "Please provide your AstrMap API Key (download at https://www.astrmap.com/, log in, click User Menu → API Keys to create one)"
>
> Then pass it via `--api-key` parameter for all subsequent commands.

**Security Notice**: This Skill sends the API Key to AstrMap servers (api.astrmap.com) for authentication. The API Key will not be used to access other services.

### Feature Tiers

| Feature | Requires Desktop Client | Requires API Key |
|---------|------------------------|-----------------|
| Query completed analysis results | No | Yes |
| Create collection-only task | Yes (online) | Yes |
| Create auto-analysis task | Yes (online) | Yes |
| Incremental fetch | Yes (online) | Yes |
| Manual trigger analysis | No | Yes |

> Tip: If you only need to query completed analysis results, you can use the API Key directly without downloading the desktop client.

### Desktop Client

Creating tasks requires the AstrMap desktop client running online.

**When device is offline** (`check_device` returns 1001 error):

1. **Ask the user**: "The desktop client is not running. Have you installed it?"
2. **If not installed**: Ask if you should help download, then guide through extraction and startup
3. **If installed but not running**: Prompt user to start the desktop client, then re-check online status

### Desktop Client Download & Installation

#### 1. Get Download Links

```bash
python scripts/api_client.py --action get_download_links
```

#### 2. Extraction Notes

> Important: Do not use Windows built-in extraction tools (may cause issues). Use 7-Zip, WPS Extraction, or similar tools instead.

#### 3. Startup Guide

**macOS**: Move the folder to "Applications" directory, right-click Astrmap.app → "Open", if blocked go to "System Settings → Privacy & Security → General" → "Still open".

**Windows**: Right-click "launch.vbs" → "Run with PowerShell" or double-click to start.

#### 4. Initial Setup

After launching:
1. Log in to your AstrMap account
2. Log in to your Amazon buyer account (do not use your seller account)
3. Ensure Amazon access is working

### Security & Verification

For detailed security verification, privacy risk statement, Amazon account security, and API Key safety guidelines, **read** `{baseDir}/references/security.md`.

### Dependency Installation

```bash
pip install -r requirements.txt
```

## Important Notes

### Points System
- **Create task (auto mode)**: Free review collection, AI analysis deducts points
- **Create task (collection-only mode)**: Free review collection, no point deduction
- **Incremental fetch**: Fetch latest reviews and re-analyze, deducts points
- **Query results**: View completed results, no point deduction

### Prerequisites (only for creating tasks)

1. AstrMap desktop client is logged in
2. Desktop client is logged in to Amazon buyer account
3. Amazon access is working

> Querying completed task results has no restrictions and can be called directly.

## Workflow

### Invocation

```bash
python scripts/api_client.py --action <action> [--params...]
```

### 1. Check Device Online

```bash
python scripts/api_client.py --action check_device --api-key "your-key"
```

Response: `{online: true, device_id: "xxx", status: "idle"}`

### 2. Create Task

> Note: Creating a task deducts points. Before executing, inform the user and wait for confirmation:
> "About to create task. Current points: {points}. This will deduct points. Continue?"

**Create Task Flow**:
1. `--action check_device` → Check device online status
2. `--action get_points` → Check account points
3. **Inform user of point consumption, wait for confirmation**
4. Confirm prerequisites, then `--action create_task --asin <ASIN> --site <site> [--is-auto false]`

**Run Mode**:
| Parameter | Description |
|-----------|-------------|
| `--is-auto true` (default) | Auto mode: automatically trigger AI analysis after collection |
| `--is-auto false` | Collection-only mode: stops at "pending analysis" status |

**Site Mapping**: US/CA/UK(English), DE(German), FR(French), IT(Italian), ES(Spanish), JP(Japanese)

**Command Examples**:
```bash
python scripts/api_client.py --action create_task --api-key "your-key" --asin "B09V3KXJPB" --site US
```

### 3. Poll Task Status

After submission, poll every **6 minutes**:

```bash
python scripts/api_client.py --action get_task_detail --api-key "your-key" --task-id "TSK_xxx"
```

**Status Flow**:

**Auto Mode** (`is_auto=true`): `PENDING` → `DISPATCHING` → `COLLECTING` → `PROCESSING` → `ANALYZING` → `SUCCESS/FAILED/CANCELLED`

**Collection-only Mode** (`is_auto=false`): `PENDING` → `DISPATCHING` → `COLLECTING` → `COLLECTED`

**Status Prompts**:

| Status | User Message |
|--------|-------------|
| PENDING | "Task submitted, waiting for scheduling..." |
| DISPATCHING | "Allocating device..." |
| COLLECTING | "Fetching Amazon review data, please wait (usually 20~120 seconds)" |
| PROCESSING | "Review data fetched, processing..." |
| ANALYZING | "Data processing complete, AI analyzing..." |
| SUCCESS | "Analysis complete! Fetching results..." |
| FAILED | "Task failed. Please check device status and network connection." |
| CANCELLED | "Task cancelled" |
| COLLECTED | "Collection complete! In pending analysis state." |

> If task does not complete after a long time (over 18 minutes), prompt user to check if desktop client is online.

### 4. Get Analysis Results

```bash
# AI Insights Summary
python scripts/api_client.py --action get_ai_insights --api-key "your-key" --task-id "TSK_xxx"
# Category-Tag Distribution
python scripts/api_client.py --action get_category_tag_distribution --api-key "your-key" --task-id "TSK_xxx"
# Basic Statistics
python scripts/api_client.py --action get_basic_statistics --api-key "your-key" --task-id "TSK_xxx"
# Negative Reviews List
python scripts/api_client.py --action get_negative_reviews --api-key "your-key" --task-id "TSK_xxx" --page 1 --page-size 20
```

> Note: Querying completed task results does not deduct points and has no prerequisites.

### 5. Incremental Fetch

> Note: Incremental fetch deducts points. Before executing, inform user and wait for confirmation.

**Incremental Fetch Flow**:
1. Check device and points
2. Inform user of point consumption, wait for confirmation
3. `--action create_incremental --task-id <task_id>`
4. Poll status (same as create task)

### 6. Manual Trigger Analysis (Collection-only Mode)

Tasks in collection-only mode (`is_auto=false`) stop at COLLECTED status, requiring manual AI analysis trigger:

```bash
python scripts/api_client.py --action trigger_analysis --api-key "your-key" --task-id "TSK_xxx"
```

Status flow: `COLLECTED` → `PROCESSING` → `ANALYZING` → `SUCCESS`

## All Available Actions

| action | Description | Required Parameters |
|--------|-------------|-------------------|
| get_download_links | Get desktop client download links | - |
| check_device | Check if device is online | - |
| create_task | Create task | --asin, --site |
| create_incremental | Incremental fetch | --task-id |
| trigger_analysis | Manual trigger analysis | --task-id |
| get_task_detail | Query task details | --task-id |
| get_task_list | Get task list | - |
| get_ai_insights | Get AI insights | --task-id |
| get_basic_statistics | Get basic statistics | --task-id |
| get_representative_reviews | Get representative reviews | --task-id |
| get_category_tag_distribution | Get category-tag distribution | --task-id |
| get_negative_reviews | Get negative reviews list | --task-id |
| get_trend | Get review trends | --task-id |
| get_related_comments | Get comments associated with tag/category | --task-id, --association-type |
| get_comments | Get raw comments | --task-id |
| get_comments_overview | Get comments overview | --task-id |
| get_points | Query points balance | - |

## Error Handling

| Error Code | Description | Handling |
|-----------|-------------|----------|
| 1001 | Device offline | Desktop client not running. Ask if installed; if not, provide download guide |
| 1002 | Insufficient points | Prompt user to recharge at https://www.astrmap.com/ |
| 2001 | Invalid API Key | Check if API Key is correct |
| 2002 | API Key disabled | Prompt user to create new API Key |
| 2003 | API Key expired | Prompt user to create new API Key |
| 2004 | Insufficient permissions | Check API Key permission configuration |
| 2005 | Request rate exceeded | Prompt user to retry later |
| InvalidTaskStatus | Task status is not COLLECTED | Only collection-only tasks with COLLECTED status can trigger analysis |

## Detailed API Documentation

For detailed API endpoint documentation, request parameters, and response formats, see [API Reference](references/api_reference.md).

## Usage Examples

### Scenario 1: Create New Task

```
User: Help me get and analyze reviews for B09V3KXJPB
AI Agent:
1. Check API Key → if not configured, ask user to provide
2. Check device and points
3. Inform point consumption, wait for confirmation
4. Create task
5. Poll status every 6 minutes, provide real-time progress
6. After analysis complete, get results
```

### Scenario 2: Collection-only Mode + Manual Trigger Analysis

```
User: Help me collect reviews only, don't analyze for now
AI Agent:
1. Check API Key and device
2. Create task with --is-auto false
3. Poll status until COLLECTED
4. After user confirms analysis, run trigger_analysis (API Key only, no desktop client required)
```

### Scenario 3: Query Completed Task

```
User: View analysis results for TSK_xxx
AI Agent:
1. Check API Key
2. Get analysis results directly (no device or prerequisites required)
```
