# EMR Serverless Application Management Guide

## Overview

EMR Serverless applications are the top-level resource for running Spark and Hive jobs without managing infrastructure.
An application must be in `STARTED` state before job runs can be submitted.

## Available Operations

All operations are available via `@tool` functions in `scripts/on_serverless/emr_serverless_cli.py`.

### 1. List Applications

List all EMR Serverless applications, optionally filtered by state.

```python
list_applications(states=["STARTED", "CREATED"])
```

**Parameters:**
- `states` (optional): Filter by state. Valid values: `CREATING`, `CREATED`, `STARTING`, `STARTED`, `STOPPING`, `STOPPED`, `TERMINATED`.

**Returns:** List of application dicts with keys: `id`, `name`, `state`, `type`, `release_label`, `created_at`, `updated_at`, `architecture`.

### 2. Get Application Details

```python
get_application(application_id="00abcdef12345678")
```

**Parameters:**
- `application_id` (required): The EMR Serverless application ID.

**Returns:** Detailed dict with additional keys: `state_details`, `auto_start_configuration`, `auto_stop_configuration`, `network_configuration`.

### 3. Start Application

Pre-initializes the application so job submissions start faster.

```python
start_application(application_id="00abcdef12345678")
```

**Returns:** `{"application_id": "...", "status": "start_requested"}`

### 4. Stop Application

Releases all resources associated with the application.

```python
stop_application(application_id="00abcdef12345678")
```

**Returns:** `{"application_id": "...", "status": "stop_requested"}`

## Application States

```
CREATING → CREATED → STARTING → STARTED → STOPPING → STOPPED → TERMINATED
```

- `CREATED` / `STOPPED`: Application exists but is not running. Jobs will trigger auto-start if configured.
- `STARTED`: Application is ready to accept job runs.

## Configuration

- `AWS_REGION`: AWS region (default: `us-east-1`)
- `EMR_SERVERLESS_APP_ID`: Default application ID (optional, can be passed per-call)
- AWS credentials via boto3 default chain
