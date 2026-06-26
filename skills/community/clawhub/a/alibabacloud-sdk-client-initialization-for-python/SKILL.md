---
name: alibabacloud-sdk-client-initialization-for-python
description: >
  Initialize and manage Alibaba Cloud SDK clients in Python. Covers singleton pattern, thread safety, endpoint vs region
  configuration, VPC endpoints, async mode, and file upload APIs. Use when the user creates SDK clients, configures
  endpoints, asks about thread safety, singleton patterns, async calls, or VPC endpoint setup in the Python SDK.
version: 0.0.1-beta
---

# Client Initialization Best Practices (Python)

## Core Rules

- **Client is thread-safe** — safe to share across threads without additional locking.
- **Use singleton pattern** — do NOT create new client instances per request. Frequent client creation wastes resources.
- Prefer **explicit endpoint** over region-based endpoint resolution.

## Recommended Client Creation

```python
import os
from threading import Lock
from alibabacloud_tea_openapi.models import Config
from alibabacloud_ecs20140526.client import Client as EcsClient

_client = None
_lock = Lock()

def get_ecs_client() -> EcsClient:
    global _client
    if _client is None:
        with _lock:
            if _client is None:
                config = Config(
                    access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
                    access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
                    endpoint='ecs.cn-hangzhou.aliyuncs.com',
                )
                _client = EcsClient(config)
    return _client
```

## Endpoint Configuration

Priority: explicit `endpoint` > region-based resolution via `region_id`.

```python
# Preferred: explicit endpoint
config = Config(endpoint='ecs.cn-hangzhou.aliyuncs.com')

# Alternative: SDK resolves endpoint from region
config = Config(region_id='cn-hangzhou')
```

### VPC Endpoints

Use VPC endpoints when running inside Alibaba Cloud VPC:

```python
config = Config(endpoint='ecs-vpc.cn-hangzhou.aliyuncs.com')
```

### File Upload APIs (Advance)

Set **both** `region_id` and `endpoint` to the same region. Optionally set `open_platform_endpoint` and `endpoint_type` for VPC:

```python
config = Config(
    region_id='cn-shanghai',
    endpoint='objectdet.cn-shanghai.aliyuncs.com',
    open_platform_endpoint='openplatform-vpc.cn-shanghai.aliyuncs.com',
    endpoint_type='internal',
)
```

## SDK Components

| Component | Install Command |
|-----------|----------------|
| Core SDK | `pip install alibabacloud-tea-openapi` |
| Product SDK | `pip install alibabacloud_ecs20140526` (example) |

## Async Mode

Python SDK supports async calls via `_async` method suffix:

```python
import asyncio
from alibabacloud_ecs20140526.client import Client
from alibabacloud_ecs20140526.models import DescribeImagesRequest
from alibabacloud_tea_openapi.models import Config

async def main():
    config = Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        endpoint='ecs-cn-hangzhou.aliyuncs.com',
    )
    client = Client(config)
    request = DescribeImagesRequest(region_id='cn-hangzhou')
    response = await client.describe_images_async(request)
    return response

asyncio.run(main())
```
