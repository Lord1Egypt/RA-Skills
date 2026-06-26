# AstrMap API Reference

## Overview

This document provides detailed documentation for all AstrMap API endpoints, request formats, response formats, and error codes.

## Authentication

All API requests require authentication in the HTTP header:

```
Authorization: Bearer {api_key}
Content-Type: application/json
```

> Note: API Key format is `sk_live_xxxxxxxxxxxxxxxx`

---

## Endpoint List

### 1. Device Status Check

**Endpoint**: `POST /api/v1/external/device/status`

Check if the device bound to the current API Key is online.

**Request Body**:
```json
{}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "online": true,
    "device_id": "device_xxx",
    "status": "idle"
  }
}
```

**Field Description**:
| Field | Type | Description |
|-------|------|-------------|
| online | bool | Whether device is online |
| device_id | string | Device ID |
| status | string | Device status (idle/busy) |

---

### 2. Create Task

**Endpoint**: `POST /api/v1/external/task/create`

Create a task and dispatch it to the device bound to the current account.

**Request Body**:
```json
{
  "platform": "amazon",
  "site": "US",
  "submit_content": "B09V3KXJPB",
  "is_auto": true
}
```

**Parameter Description**:
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| platform | No | amazon | Platform name |
| site | No | US | Site |
| submit_content | Yes | - | Input content, supports URL or ASIN |
| is_auto | No | true | Auto mode flag: true=auto analysis, false=collection only |

**Site Description**:
| site | Language |
|------|----------|
| US | English |
| CA | English |
| UK | English |
| DE | German |
| FR | French |
| IT | Italian |
| ES | Spanish |
| JP | Japanese |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "TSK_xxx",
    "name": "xxx",
    "status": "PENDING"
  }
}
```

---

### 3. Task Detail Query

**Endpoint**: `POST /api/v1/external/task/detail`

Query task details and status.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "TSK_xxx",
    "user_id": "user_xxx",
    "name": "Task name",
    "status": "SUCCESS",
    "platform": "amazon",
    "site": "US",
    "submit_content": "B09V3KXJPB",
    "parse_content": ["B09V3KXJPB"],
    "create_time": "2025-03-22 10:30:00",
    "update_time": "2025-03-22 10:35:00",
    "monitoring": false
  }
}
```

**Task Status Description**:
| Status | Description |
|--------|-------------|
| PENDING | Pending |
| DISPATCHING | Dispatching |
| COLLECTING | Collecting |
| PROCESSING | Processing |
| ANALYZING | Analyzing |
| SUCCESS | Completed |
| FAILED | Failed |
| CANCELLED | Cancelled |

---

### 4. Task List Query

**Endpoint**: `POST /api/v1/external/task/list`

Query task list.

**Request Body**:
```json
{
  "page": 1,
  "page_size": 20,
  "search_keyword": "B09",
  "filter_monitoring": false
}
```

**Parameter Description**:
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| page | No | 1 | Page number |
| page_size | No | 10 | Items per page |
| search_keyword | No | - | Search keyword |
| filter_monitoring | No | false | Filter monitoring tasks |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

---

### 4.1 Incremental Fetch

**Endpoint**: `POST /api/v1/external/task/incremental`

Create incremental fetch for completed tasks (SUCCESS/FAILED/CANCELLED), fetching new reviews since last fetch.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Parameter Description**:
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| task_id | Yes | - | Task ID, must be a completed task |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "TSK_xxx",
    "job_id": "JOB_xxx"
  }
}
```

**Error Codes**:
| Error Code | Description |
|------------|-------------|
| -1 | Task status is not completed. Only completed tasks can do incremental fetch |

**Use Cases**:
- Task completed some time ago, need to update with latest review data
- Difference from creating a new task: input is the existing ASIN (no need to re-enter), automatically fetches incremental data
- Incremental fetch triggers full fetch + analysis process, analysis deducts points

---

### 4.2 Manual Trigger Analysis

**Endpoint**: `POST /api/v1/external/task/{task_id}/trigger-analysis`

Manually trigger AI analysis for collection-only tasks. Applicable for tasks with `is_auto=false` that stopped at COLLECTED status after collection.

**Parameter Description**:
| Parameter | Required | Description |
|-----------|----------|-------------|
| task_id | Yes | Task ID, task status must be COLLECTED |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

**Status Flow After Trigger**: `COLLECTED` → `PROCESSING` → `ANALYZING` → `SUCCESS`

**Error Codes**:
| Error Code | Description |
|------------|-------------|
| InvalidTaskStatus | Task status is not COLLECTED, cannot trigger analysis |

---

### 4.3 Desktop Client Download Config

**Endpoint**: `GET /download-config.json`

This is a public config file for getting desktop client download links.

**Response**:
```json
{
  "version": "1.0.0",
  "last_updated": "2026-04-27T14:31:08.795719Z",
  "downloads": {
    "macos": {
      "name_zh": "macOS Version",
      "name_en": "macOS Version",
      "url": "<actual download URL>",
      "version": "1.0.0",
      "size": "156MB",
      "requirements": {
        "min_version": "10.15",
        "recommended_memory": "8GB",
        "disk_space": "500MB"
      }
    },
    "windows": {
      "name_zh": "Windows Version",
      "name_en": "Windows Version",
      "url": "<actual download URL>",
      "version": "1.0.0",
      "size": "142MB",
      "requirements": {
        "min_version": "10",
        "recommended_memory": "8GB",
        "disk_space": "500MB"
      }
    }
  }
}
```

---

### 5. AI Insights Query

**Endpoint**: `POST /api/v1/external/analysis/insights`

Get AI insights summary.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "executive_summary": [...],
    "key_problems": [...],
    "improvement_recommendations": [...],
    "priority_ranking": {},
    "insights_version": "1.0",
    "last_analyzed_at": "2025-03-22 10:35:00"
  }
}
```

---

### 6. Tag Distribution Query

**Endpoint**: `POST /api/v1/external/analysis/tags`

Get tag distribution statistics.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "tag_categories": [
      {
        "category": "product",
        "category_name": "Product Quality",
        "tags": [
          {"tag": "Workmanship issue", "polarity": "negative", "count": 15}
        ],
        "total_count": 20
      }
    ]
  }
}
```

---

### 7. Issue Dimension Statistics Query

**Endpoint**: `POST /api/v1/external/analysis/issue-statistics`

Get issue dimension statistics (product, service, experience three-dimensional model).

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "product_count": 10,
    "product_rate": "6.7%",
    "service_count": 8,
    "service_rate": "5.3%",
    "experience_count": 5,
    "experience_rate": "3.3%"
  }
}
```

---

### 8. Top Issues Distribution Query

**Endpoint**: `POST /api/v1/external/analysis/top-issues`

Get TopN issue distribution across dimensions.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "top_issue_distribution": {
      "product": [...],
      "service": [...],
      "experience": [...]
    }
  }
}
```

---

### 9. Basic Statistics Query

**Endpoint**: `POST /api/v1/external/analysis/statistics`

Get basic statistics.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total_comments": 150,
    "negative_comments": 23,
    "negative_rate": "15%",
    "product_count": 10,
    "product_rate": "6.7%",
    "service_count": 8,
    "service_rate": "5.3%",
    "experience_count": 5,
    "experience_rate": "3.3%",
    "last_analyzed_at": "2025-03-22 10:35"
  }
}
```

---

### 10. Negative Reviews List Query

**Endpoint**: `POST /api/v1/external/analysis/negative-reviews`

Get negative reviews list.

**Request Body**:
```json
{
  "task_id": "TSK_xxx",
  "page": 1,
  "page_size": 20
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": "comment_xxx",
        "content": "Shipping took forever!",
        "rating": 1,
        "date": "2025-03-15",
        "tags": ["Shipping issue", "Slow delivery"]
      }
    ],
    "total": 23,
    "page": 1,
    "page_size": 20
  }
}
```

---

### 11. Review Trend Query

**Endpoint**: `POST /api/v1/external/analysis/trend`

Get review trend data.

**Request Body**:
```json
{
  "task_id": "TSK_xxx",
  "filter_data": "30",
  "filter_product": "all"
}
```

**Parameter Description**:
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| task_id | Yes | - | Task ID |
| filter_data | No | 30 | Data range (30/60/all) |
| filter_product | No | all | Product filter |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "trend_reviews": {
      "source": [["Date", "Total reviews", "Negative reviews"], ["2025-03-01", 50, 8]]
    }
  }
}
```

---

### 12. Raw Comments Overview Query

**Endpoint**: `POST /api/v1/external/analysis/comments-overview`

Get raw comments overview/statistics.

**Request Body**:
```json
{
  "task_id": "TSK_xxx"
}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total_reviews": 150,
    "avg_rating": 4.2,
    "verified_count": 120,
    "image_count": 30,
    "video_count": 5
  }
}
```

---

### 13. Raw Comments Query

**Endpoint**: `POST /api/v1/external/analysis/comments`

Get raw comments list.

**Request Body**:
```json
{
  "task_id": "TSK_xxx",
  "page": 1,
  "page_size": 20,
  "filter_star": "all",
  "filter_verified": "all"
}
```

**Parameter Description**:
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| task_id | Yes | - | Task ID |
| page | No | 1 | Page number |
| page_size | No | 20 | Items per page |
| filter_star | No | all | Rating filter (1-5/all) |
| filter_verified | No | all | Filter verified reviews |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [...],
    "total": 150,
    "page": 1,
    "page_size": 20
  }
}
```

---

### 14. Get Related Comments

**Endpoint**: `POST /api/v1/external/analysis/related-comments`

Get comments associated with specific tags or issues for drill-down analysis.

**Request Body**:
```json
{
  "task_id": "TSK_xxx",
  "association_type": "tag",
  "normalized_tag": "Shipping issue",
  "category": "service",
  "page": 1,
  "page_size": 20
}
```

**Parameter Description**:
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| task_id | Yes | - | Task ID |
| association_type | Yes | - | Association type: `tag` or `issue` |
| normalized_tag | No | - | Normalized tag name (when association_type=tag) |
| category | No | - | Tag category (when association_type=tag) |
| dimension | No | - | Issue dimension (when association_type=issue) |
| issue_type | No | - | Issue type (when association_type=issue) |
| page | No | 1 | Page number |
| page_size | No | 20 | Items per page |

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [...],
    "total": 50,
    "association_type": "tag",
    "task_id": "TSK_xxx"
  }
}
```

---

### 15. Points Balance Query

**Endpoint**: `POST /api/v1/external/account/points`

Query current account remaining points.

**Request Body**:
```json
{}
```

**Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "available_points": 1000
  }
}
```

---

## Error Codes

| Error Code | Description | Detailed Description |
|-----------|-------------|---------------------|
| 0 | Success | - |
| -1 | Server internal error | Server internal exception |
| 1001 | Device offline | Desktop client not logged in or device offline |
| 1002 | Insufficient points | Account points insufficient for operation |
| 2001 | Invalid API Key | Key does not exist or has expired |
| 2002 | API Key disabled | User actively disabled |
| 2003 | API Key expired | Time exceeds expires_at setting |
| 2004 | Insufficient permissions | Missing corresponding operation permissions |
| 2005 | Request rate exceeded | Default 100 times/minute |
| InvalidTaskStatus | Task status does not allow this operation | Only collection-only tasks with COLLECTED status can trigger analysis |

---

## Rate Limits

- Default limit: 100 requests/minute
- Exceeding limit returns error code 2005 with `Retry-After` header

---

## FAQ

### Points System

- **Create task (auto mode)**: Free Amazon review collection, AI analysis deducts account points
- **Create task (collection-only mode)**: Free Amazon review collection, no point deduction
- **Incremental fetch**: Fetch latest reviews and re-analyze, deducts points
- **Query results**: View completed task analysis results, no point deduction, no prerequisites

### Prerequisites (only for creating tasks)

Before creating a task, ensure the following conditions are met:

1. AstrMap desktop client is logged in
2. Desktop client is logged in to Amazon buyer account
3. Ensure Amazon access is working

### Error Handling
1. Device offline (1001): Check if desktop client is logged in
2. Insufficient points (1002): Prompt user to recharge points
3. Invalid API Key (2001): Check if API Key is correct
