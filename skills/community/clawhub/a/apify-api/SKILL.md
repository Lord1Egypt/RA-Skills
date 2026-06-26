---
name: apify
description: |
  Apify API integration with managed authentication. Run web scrapers, manage actors, datasets, key-value stores, and schedules.
  Use this skill when users want to interact with Apify - running web scraping actors, managing datasets, or scheduling tasks.
  Running actors consumes Apify compute units. Creating schedules and webhooks creates persistent resources that continue operating after the conversation ends.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: "🕷️"
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Apify

Access the Apify API with managed authentication. Run web scrapers and actors, manage datasets, key-value stores, request queues, schedules, and webhooks.

## Quick Start

```bash
# List your actors
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/apify/v2/acts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/apify/v2/
```

All endpoints documented below are accessed under this base URL. The gateway proxies requests to `api.apify.com` and automatically injects your API token. Only the endpoints listed in the API Reference section below are supported.

## Security & Permissions

- The Maton API key acts as a credential — treat it as a secret and do not expose it in client-side code or public repositories
- **Read operations** (GET) retrieve data from the connected Apify account
- **Write operations** (POST, PUT, DELETE) create, modify, or delete resources — confirm with the user before destructive actions
- **Actor runs** consume Apify compute units on the connected account — confirm before starting runs, especially on large inputs
- **Schedules and webhooks** are persistent resources that continue operating after the session ends — confirm before creating, and review existing ones before modification
- When multiple connections exist, always specify the `Maton-Connection` header to avoid acting on the wrong account

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Apify connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=apify&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'apify'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-04-07T21:20:16.974921Z",
    "last_updated_time": "2026-04-07T21:23:43.726795Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "apify",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete authentication setup.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Apify connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/apify/v2/acts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## API Reference

### User

#### Get Current User

```bash
GET /apify/v2/users/me
```

**Response:**
```json
{
  "data": {
    "id": "GgXk48GBlDInv62bA",
    "username": "my_username",
    "profile": {
      "name": "John Doe",
      "pictureUrl": "https://..."
    },
    "email": "john@example.com",
    "plan": {
      "id": "FREE",
      "description": "Free plan",
      "monthlyUsageCreditsUsd": 5
    },
    "createdAt": "2024-04-27T22:08:45.429Z"
  }
}
```

### Actors

#### List Actors

```bash
GET /apify/v2/acts
GET /apify/v2/acts?limit=10&offset=0
```

**Response:**
```json
{
  "data": {
    "total": 4,
    "count": 4,
    "offset": 0,
    "limit": 1000,
    "desc": false,
    "items": [
      {
        "id": "moJRLRc85AitArpNN",
        "name": "web-scraper",
        "username": "apify",
        "title": "Web Scraper",
        "createdAt": "2019-03-07T11:28:01.600Z",
        "modifiedAt": "2026-03-11T14:36:47.849Z",
        "stats": {
          "totalRuns": 2,
          "lastRunStartedAt": "2026-04-07T21:24:57.927Z"
        }
      }
    ]
  }
}
```

#### Get Actor

```bash
GET /apify/v2/acts/{actorId}
```

#### Run Actor

```bash
POST /apify/v2/acts/{actorId}/runs
Content-Type: application/json

{
  "startUrls": [{"url": "https://example.com"}],
  "maxRequestsPerCrawl": 10
}
```

**Response:**
```json
{
  "data": {
    "id": "mxA2b6luHFdcxBZuG",
    "actId": "moJRLRc85AitArpNN",
    "status": "RUNNING",
    "startedAt": "2026-04-07T21:24:57.927Z",
    "defaultKeyValueStoreId": "qP9EdMQrEqNcC2PzZ",
    "defaultDatasetId": "E9O7dXhrNxgA06o5k",
    "defaultRequestQueueId": "N3xb1qGmNzoxPNaAW"
  }
}
```

### Actor Runs

#### List Actor Runs

```bash
GET /apify/v2/actor-runs
GET /apify/v2/actor-runs?limit=10&desc=1
```

**Response:**
```json
{
  "data": {
    "total": 1,
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "items": [
      {
        "id": "mxA2b6luHFdcxBZuG",
        "actId": "moJRLRc85AitArpNN",
        "status": "SUCCEEDED",
        "startedAt": "2026-04-07T21:24:57.927Z",
        "finishedAt": "2026-04-07T21:25:08.086Z",
        "defaultDatasetId": "E9O7dXhrNxgA06o5k",
        "usageTotalUsd": 0.0037
      }
    ]
  }
}
```

#### Get Actor Run

```bash
GET /apify/v2/actor-runs/{runId}
```

**Response:**
```json
{
  "data": {
    "id": "mxA2b6luHFdcxBZuG",
    "actId": "moJRLRc85AitArpNN",
    "status": "SUCCEEDED",
    "statusMessage": "Finished! Total 1 requests: 1 succeeded, 0 failed.",
    "startedAt": "2026-04-07T21:24:57.927Z",
    "finishedAt": "2026-04-07T21:25:08.086Z",
    "stats": {
      "durationMillis": 10009,
      "runTimeSecs": 10.009,
      "computeUnits": 0.011,
      "memAvgBytes": 254919122,
      "cpuAvgUsage": 14.67
    },
    "defaultKeyValueStoreId": "qP9EdMQrEqNcC2PzZ",
    "defaultDatasetId": "E9O7dXhrNxgA06o5k",
    "defaultRequestQueueId": "N3xb1qGmNzoxPNaAW"
  }
}
```

#### Abort Actor Run

```bash
POST /apify/v2/actor-runs/{runId}/abort
```

#### Resurrect Actor Run

```bash
POST /apify/v2/actor-runs/{runId}/resurrect
```

### Actor Tasks

#### List Actor Tasks

```bash
GET /apify/v2/actor-tasks
```

#### Get Actor Task

```bash
GET /apify/v2/actor-tasks/{taskId}
```

#### Create Actor Task

```bash
POST /apify/v2/actor-tasks
Content-Type: application/json

{
  "actId": "moJRLRc85AitArpNN",
  "name": "my-scraping-task",
  "options": {
    "build": "latest",
    "memoryMbytes": 1024,
    "timeoutSecs": 300
  },
  "input": {
    "startUrls": [{"url": "https://example.com"}]
  }
}
```

#### Run Actor Task

```bash
POST /apify/v2/actor-tasks/{taskId}/runs
```

#### Update Actor Task

```bash
PUT /apify/v2/actor-tasks/{taskId}
Content-Type: application/json

{
  "name": "updated-task-name"
}
```

#### Delete Actor Task

```bash
DELETE /apify/v2/actor-tasks/{taskId}
```

### Datasets

#### List Datasets

```bash
GET /apify/v2/datasets
```

#### Get Dataset

```bash
GET /apify/v2/datasets/{datasetId}
```

#### Create Dataset

```bash
POST /apify/v2/datasets
Content-Type: application/json

{
  "name": "my-dataset"
}
```

#### Get Dataset Items

```bash
GET /apify/v2/datasets/{datasetId}/items
GET /apify/v2/datasets/{datasetId}/items?format=json&limit=100
```

**Response:**
```json
[
  {
    "title": "Example Domain",
    "url": "https://example.com",
    "#debug": {
      "requestId": "zYk68OuvhfdFudP",
      "statusCode": 200
    }
  }
]
```

#### Push Items to Dataset

```bash
POST /apify/v2/datasets/{datasetId}/items
Content-Type: application/json

[
  {"title": "Item 1", "url": "https://example1.com"},
  {"title": "Item 2", "url": "https://example2.com"}
]
```

#### Delete Dataset

```bash
DELETE /apify/v2/datasets/{datasetId}
```

### Key-Value Stores

#### List Key-Value Stores

```bash
GET /apify/v2/key-value-stores
```

#### Get Key-Value Store

```bash
GET /apify/v2/key-value-stores/{storeId}
```

**Response:**
```json
{
  "data": {
    "id": "qP9EdMQrEqNcC2PzZ",
    "name": null,
    "userId": "GgXk48GBlDInv62bA",
    "createdAt": "2026-04-07T21:24:57.930Z",
    "stats": {
      "readCount": 2,
      "writeCount": 6,
      "storageBytes": 2018
    }
  }
}
```

#### Create Key-Value Store

```bash
POST /apify/v2/key-value-stores
Content-Type: application/json

{
  "name": "my-store"
}
```

#### List Keys

```bash
GET /apify/v2/key-value-stores/{storeId}/keys
```

#### Get Record

```bash
GET /apify/v2/key-value-stores/{storeId}/records/{key}
```

#### Put Record

```bash
PUT /apify/v2/key-value-stores/{storeId}/records/{key}
Content-Type: application/json

{"data": "value"}
```

#### Delete Record

```bash
DELETE /apify/v2/key-value-stores/{storeId}/records/{key}
```

#### Delete Key-Value Store

```bash
DELETE /apify/v2/key-value-stores/{storeId}
```

### Request Queues

#### List Request Queues

```bash
GET /apify/v2/request-queues
```

#### Get Request Queue

```bash
GET /apify/v2/request-queues/{queueId}
```

#### Create Request Queue

```bash
POST /apify/v2/request-queues
Content-Type: application/json

{
  "name": "my-queue"
}
```

#### Add Request to Queue

```bash
POST /apify/v2/request-queues/{queueId}/requests
Content-Type: application/json

{
  "url": "https://example.com",
  "uniqueKey": "example-key"
}
```

#### Delete Request Queue

```bash
DELETE /apify/v2/request-queues/{queueId}
```

### Schedules

#### List Schedules

```bash
GET /apify/v2/schedules
```

#### Get Schedule

```bash
GET /apify/v2/schedules/{scheduleId}
```

#### Create Schedule

```bash
POST /apify/v2/schedules
Content-Type: application/json

{
  "name": "daily-scrape",
  "cronExpression": "0 0 * * *",
  "isEnabled": true,
  "actions": [
    {
      "type": "RUN_ACTOR_TASK",
      "actorTaskId": "task123"
    }
  ]
}
```

#### Update Schedule

```bash
PUT /apify/v2/schedules/{scheduleId}
Content-Type: application/json

{
  "isEnabled": false
}
```

#### Delete Schedule

```bash
DELETE /apify/v2/schedules/{scheduleId}
```

### Webhooks

#### List Webhooks

```bash
GET /apify/v2/webhooks
```

#### Get Webhook

```bash
GET /apify/v2/webhooks/{webhookId}
```

#### Create Webhook

```bash
POST /apify/v2/webhooks
Content-Type: application/json

{
  "eventTypes": ["ACTOR.RUN.SUCCEEDED"],
  "requestUrl": "https://example.com/webhook",
  "condition": {
    "actorId": "moJRLRc85AitArpNN"
  }
}
```

#### Update Webhook

```bash
PUT /apify/v2/webhooks/{webhookId}
Content-Type: application/json

{
  "isAdHoc": false
}
```

#### Delete Webhook

```bash
DELETE /apify/v2/webhooks/{webhookId}
```

## Pagination

Apify uses offset-based pagination:

```bash
GET /apify/v2/acts?limit=10&offset=20&desc=1
```

**Parameters:**
- `limit` - Maximum items per response (default: 1000)
- `offset` - Number of items to skip
- `desc` - Set to `1` for descending order (newest first)

**Response includes:**
```json
{
  "data": {
    "total": 100,
    "count": 10,
    "offset": 20,
    "limit": 10,
    "desc": true,
    "items": [...]
  }
}
```

For key-value stores, use key-based pagination:
```bash
GET /apify/v2/key-value-stores/{storeId}/keys?limit=100&exclusiveStartKey=lastKey
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/apify/v2/acts',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.data.items);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/apify/v2/actor-runs',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10, 'desc': 1}
)
runs = response.json()['data']['items']
```

### Run Actor and Get Results

```python
import os
import requests
import time

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Run an actor
run_resp = requests.post(
    'https://gateway.maton.ai/apify/v2/acts/apify~web-scraper/runs',
    headers=headers,
    json={
        'startUrls': [{'url': 'https://example.com'}],
        'maxRequestsPerCrawl': 10
    }
)
run = run_resp.json()['data']
run_id = run['id']
dataset_id = run['defaultDatasetId']

# Wait for completion
while True:
    status_resp = requests.get(
        f'https://gateway.maton.ai/apify/v2/actor-runs/{run_id}',
        headers=headers
    )
    status = status_resp.json()['data']['status']
    if status in ['SUCCEEDED', 'FAILED', 'ABORTED']:
        break
    time.sleep(5)

# Get results
items_resp = requests.get(
    f'https://gateway.maton.ai/apify/v2/datasets/{dataset_id}/items',
    headers=headers
)
results = items_resp.json()
print(f'Scraped {len(results)} items')
```

## Notes

- Actor IDs can be specified as `{username}~{actorName}` (e.g., `apify~web-scraper`) or by ID
- Run statuses: `READY`, `RUNNING`, `SUCCEEDED`, `FAILED`, `ABORTING`, `ABORTED`, `TIMING-OUT`, `TIMED-OUT`
- Dataset items can be retrieved in various formats: `json`, `jsonl`, `csv`, `xlsx`, `xml`, `rss`
- Key-value store records can store any content type
- Schedule cron expressions follow standard cron format
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly in some shells

## Rate Limits

| Scope | Limit |
|-------|-------|
| Global | 250,000 requests/minute |
| Default per-resource | 60 requests/second |
| Key-Value Store CRUD | 200 requests/second |
| Dataset & Queue operations | 400 requests/second |

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Apify connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 429 | Rate limited (use exponential backoff) |
| 4xx/5xx | Passthrough error from Apify API |

## Resources

- [Apify API Reference](https://docs.apify.com/api/v2)
- [Apify Actors Documentation](https://docs.apify.com/actors)
- [Apify Storage Documentation](https://docs.apify.com/storage)
- [Apify Schedules Documentation](https://docs.apify.com/schedules)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
