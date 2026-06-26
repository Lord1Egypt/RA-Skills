---
name: alibabacloud-sdk-client-initialization-for-golang
description: >
  Initialize and manage Alibaba Cloud SDK clients in Go. Covers sync.Once singleton, goroutine safety, endpoint vs region
  configuration, VPC endpoints, and debug mode. Use when the user creates Go SDK clients, configures endpoints, asks about
  goroutine safety, singleton patterns, or VPC endpoint setup in the Alibaba Cloud Go SDK.
version: 0.0.1-beta
---

# Client Initialization Best Practices (Go)

## Core Rules

- **Client is goroutine-safe** — safe to share across goroutines without additional synchronization.
- **Use singleton pattern** — do NOT create new client instances per request. Frequent client creation wastes resources.
- Prefer **explicit endpoint** over region-based endpoint resolution.

## Recommended Client Creation

```go
import (
    "os"
    "sync"

    openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
    ecs "github.com/alibabacloud-go/ecs-20140526/v3/client"
    "github.com/alibabacloud-go/tea/tea"
)

var (
    ecsClient     *ecs.Client
    ecsClientOnce sync.Once
)

func GetEcsClient() *ecs.Client {
    ecsClientOnce.Do(func() {
        config := &openapi.Config{
            AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
            AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
            Endpoint:        tea.String("ecs.cn-hangzhou.aliyuncs.com"),
        }
        var err error
        ecsClient, err = ecs.NewClient(config)
        if err != nil {
            panic(err)
        }
    })
    return ecsClient
}
```

## Endpoint Configuration

Priority: explicit `Endpoint` > region-based resolution via `RegionId`.

```go
// Preferred: explicit endpoint
config.Endpoint = tea.String("ecs.cn-hangzhou.aliyuncs.com")

// Alternative: SDK resolves endpoint from region
config.RegionId = tea.String("cn-hangzhou")
```

### VPC Endpoints

Use VPC endpoints when running inside Alibaba Cloud VPC:

```go
config.Endpoint = tea.String("ecs-vpc.cn-hangzhou.aliyuncs.com")
```

### File Upload APIs (Advance)

Set **both** `RegionId` and `Endpoint` to the same region for file upload APIs:

```go
config.RegionId = tea.String("cn-shanghai")
config.Endpoint = tea.String("objectdet.cn-shanghai.aliyuncs.com")
// VPC file upload authorization:
client.OpenPlatformEndpoint = tea.String("openplatform-vpc.cn-shanghai.aliyuncs.com")
client.EndpointType = tea.String("internal")
```

## SDK Components

| Component | Description |
|-----------|-------------|
| Core SDK (`darabonba-openapi`) | Generic calls, no product dependency |
| Product SDK (e.g., `ecs-20140526`) | Typed client, models, convenience methods |

## Debugging

Enable debug mode via environment variable to log all requests:

```bash
export DEBUG=tea
```
