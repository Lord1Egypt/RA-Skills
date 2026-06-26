---
name: task-status
description: Query task status from the AICNIC job management system. Use this skill when the user needs to check task status, retrieve job information, or mentions a jobId. It calls the http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId} API to fetch job details and extracts the jobState field from the response.
---

# Task Status Query

## Overview

This skill is used to query the status of a specific task in the AICNIC job management system.

## Usage

When the user needs to query a task status:

1. Obtain the `jobId` parameter provided by the user
2. Call the API to retrieve job information
3. Parse and return the value of the `jobState` field

## API Call

### Request Format

```
GET http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId}
```

### Curl Example

```bash
curl -X GET "http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId}" -H "accept: */*"
```

### Response Format

The API returns a JSON response:

```json
{
  "code": 0,
  "message": null,
  "data": {
    "id": 20452,
    "jobId": "15000",
    "jobState": "COMPLETED",
    ...
  }
}
```

## Parsing Rules

Extract the following fields from the API response:

| Field Path | Description |
|-----------|-------------|
| `data.jobState` | Task status (e.g., COMPLETED, RUNNING, PENDING, etc.) |
| `data.jobId` | Job ID |
| `data.jobName` | Job name |
| `data.startTime` | Start time |
| `data.endTime` | End time |

## Workflow

1. **Receive Parameter**: Get the jobId provided by the user
2. **Build URL**: `http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId}`
3. **Send Request**: Send a GET request using curl or an HTTP client
4. **Parse Response**: Parse the JSON response and extract the `data.jobState` field
5. **Return Result**: Display the task status to the user

## Example

### Query task status for jobId 15000

```bash
curl -X GET "http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/15000" -H "accept: */*"
```

Response:
```json
{
  "code": 0,
  "message": null,
  "data": {
    "jobId": "15000",
    "jobState": "COMPLETED",
    "endTime": "2024-12-09T09:30:10"
  }
}
```

Parsed Result: **Task status is COMPLETED**

## Common Task States

- `COMPLETED` - Completed
- `RUNNING` - Running
- `PENDING` - Pending
- `FAILED` - Failed
- `CANCELLED` - Cancelled
