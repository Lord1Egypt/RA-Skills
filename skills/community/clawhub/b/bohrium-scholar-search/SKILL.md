---
name: bohrium-scholar-search
description: "Search scholars and fetch scholar profile via open.bohrium.com. Use when: user asks to find/search/look up a scholar, researcher, or academic by name, affiliation, or research direction; or asks about a specific researcher's publications, citations, h-index, education, work experience, or research profile. NOT for: paper/patent content search (use bohrium-paper-search), knowledge base management, or file operations."
---

# SKILL: Bohrium Scholar Search & Profile

## Overview

Query scholar information via the Bohrium OpenAPI gateway (`open.bohrium.com`). Provides two core endpoints:

| Endpoint | Method | Path | Purpose |
|----------|--------|------|---------|
| Scholar Search | POST | `/openapi/v1/paper-server/scholar/search` | Search scholars by name / affiliation / research tags |
| Scholar Info | GET | `/openapi/v1/paper-server/scholar/info?scholarId=xxx` | Fetch the full profile by `scholarId` |

**Typical workflow:** Given a scholar name → search candidates → pick the target `scholarId` → fetch the full profile (papers, citations, h-index, research directions, education/work history).

**No CLI support** — all operations use the HTTP API.

## Authentication

`ACCESS_KEY` is read from the OpenClaw config `~/.openclaw/openclaw.json`:

```json
"bohrium-scholar-search": {
  "enabled": true,
  "apiKey": "YOUR_ACCESS_KEY",
  "env": {
    "ACCESS_KEY": "YOUR_ACCESS_KEY"
  }
}
```

OpenClaw automatically injects `env.ACCESS_KEY` into the runtime environment.

### Runtime Resolution

```
Read os.environ["ACCESS_KEY"]
  ├─ Non-empty → use directly
  └─ Empty     → prompt the user:
                 "ACCESS_KEY is not configured in OpenClaw. Please set
                  bohrium-scholar-search.env.ACCESS_KEY in ~/.openclaw/openclaw.json
                  with the AccessKey obtained from the user settings page at
                  https://bohrium.dp.tech, then restart the OpenClaw session."
```

**Important:** Do not persist the AccessKey in any other file or hardcode it into source; always inject it through the OpenClaw environment.

### Error Handling

If the API returns `Invalid AccessKey` (code 2000) or HTTP 401:
1. The key configured in OpenClaw is invalid or expired.
2. Prompt the user: "Your AccessKey is invalid. Please update `bohrium-scholar-search.env.ACCESS_KEY` in `~/.openclaw/openclaw.json` and restart the OpenClaw session."

## Common Code Template

```python
import os, requests

AK = os.environ.get("ACCESS_KEY", "")
if not AK:
    raise RuntimeError(
        "ACCESS_KEY not found. Please configure it in ~/.openclaw/openclaw.json "
        "under bohrium-scholar-search.env.ACCESS_KEY."
    )

BASE = "https://open.bohrium.com/openapi/v1/paper-server"
HEADERS_JSON = {"accessKey": AK, "Content-Type": "application/json"}
HEADERS = {"accessKey": AK}
```

---

## Standard Workflow

```
User asks about a scholar
  │
  ├─ Known scholarId → call Scholar Info directly
  └─ Unknown scholarId → call Scholar Search first
       └─ Pick items[].scholarId from the response → call Scholar Info
```

---

## Scholar Search

### Basic Search

```python
r = requests.post(f"{BASE}/scholar/search", headers=HEADERS_JSON, json={
    "name": "Yann LeCun",
    "page": 1,
    "pageSize": 5
})
data = r.json()
for item in data["data"]["items"]:
    print(f"[{item['scholarId']}] {item.get('nameEn','')} / {item.get('nameZh','')}")
    print(f"  Org: {item.get('scholarOrgNameEn','')}")
    print(f"  Papers: {item.get('paperNums',0)}, Citations: {item.get('citationNums',0)}, h-index: {item.get('hIndex',0)}")
```

### Search with Filters

```python
r = requests.post(f"{BASE}/scholar/search", headers=HEADERS_JSON, json={
    "name": "Zhang San",
    "school": "Tsinghua University",
    "affiliation": "Tsinghua University",
    "tags": "machine learning",
    "page": 1,
    "pageSize": 10
})
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Scholar name keyword (1–99 chars) |
| `school` | string | No | School / institution |
| `tags` | string | No | Research interest tag |
| `affiliation` | string | No | Affiliation (English) |
| `affiliationZh` | string | No | Affiliation (Chinese) |
| `page` | int | No | Page number, default 1 |
| `pageSize` | int | No | Page size, default 10 |

### Key Response Fields

`data.items[]` array, each item contains:

| Field | Description |
|-------|-------------|
| `scholarId` | Unique scholar ID, required by the info endpoint |
| `nameEn` / `nameZh` | English / Chinese name |
| `paperNums` | Publication count |
| `citationNums` | Citation count |
| `hIndex` | h-index |
| `scholarOrgNameEn` / `scholarOrgNameZh` | Affiliation name (EN/ZH) |
| `isHighCited` | Highly-cited scholar flag |

---

## Scholar Info

Fetch the full profile using the `scholarId` returned by the search endpoint:

```python
r = requests.get(
    f"{BASE}/scholar/info",
    headers=HEADERS,
    params={"scholarId": scholar_id}
)
info = r.json()["data"]
print(info.get("nameEn"), "|", info.get("nameZh"))
print("Research:", info.get("researchDirection"))
print("Education:", info.get("educationBackgroundZh") or info.get("educationBackground"))
print("Work:", info.get("workExperienceZh") or info.get("workExperience"))
```

### Additional Response Fields

In addition to the fields returned by search:

| Field | Description |
|-------|-------------|
| `researchDirection` | Array of research directions |
| `educationBackground` / `educationBackgroundZh` | Education history (EN/ZH) |
| `workExperience` / `workExperienceZh` | Work experience (EN/ZH) |

---

## Presentation Guidelines

Format the API response into a user-friendly summary that highlights:

- **Name**: `nameEn` / `nameZh`
- **Affiliation**: `scholarOrgNameEn` / `scholarOrgNameZh`
- **Metrics**: `paperNums` / `citationNums` / `hIndex`
- **Highly cited**: `isHighCited`
- **Research directions**: `researchDirection`
- **Education**: prefer `educationBackgroundZh`, fall back to `educationBackground`
- **Work experience**: prefer `workExperienceZh`, fall back to `workExperience`

If multiple candidates are returned, first present a summary table for the user to choose, then fetch the full profile.

---

## curl Examples

```bash
AK="$ACCESS_KEY"
BASE="https://open.bohrium.com/openapi/v1/paper-server"

# Step 1: Scholar search
curl -s -X POST "$BASE/scholar/search" \
  -H "accessKey: $AK" \
  -H "Content-Type: application/json" \
  -d '{"name":"Yann LeCun","page":1,"pageSize":3}'

# Step 2: Fetch profile
curl -s "$BASE/scholar/info?scholarId=RETURNED_ID" \
  -H "accessKey: $AK"
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ACCESS_KEY` is empty | OpenClaw did not inject the env var | Verify `bohrium-scholar-search.env.ACCESS_KEY` in `~/.openclaw/openclaw.json` |
| `Invalid AccessKey` / 401 | Key expired or incorrect | Update the AccessKey in `~/.openclaw/openclaw.json` and restart the session |
| Empty search result | 1) A 24-char no-space string is treated as an internal ID; 2) upstream per-user rate limiting | Use a natural name rather than an ID; retry later |
| Info endpoint parameter error | Missing `scholarId` | Call the search endpoint first and take `data.items[].scholarId` |
| `name` length error | Out of 1–99 chars | Shorten the name keyword |
