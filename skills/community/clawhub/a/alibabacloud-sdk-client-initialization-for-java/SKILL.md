---
name: alibabacloud-sdk-client-initialization-for-java
description: >
  Initialize and manage Alibaba Cloud SDK clients in Java. Covers singleton pattern, thread safety, endpoint vs region
  configuration, VPC endpoints, sync vs async clients, and file upload APIs. Use when the user creates Java SDK clients,
  configures endpoints, asks about thread safety, singleton patterns, async calls, or VPC endpoint setup.
version: 0.0.2-beta
---

# Client Initialization Best Practices (Java)

## Core Rules

- **Client is thread-safe** — safe to share across threads without synchronization.
- **Use singleton pattern** — do NOT create new client instances per request. Frequent `new Client()` calls waste resources and hurt performance.
- Prefer **explicit endpoint** over region-based endpoint resolution.
- preview version

## Recommended Client Creation

```java
public class ClientFactory {
    private static volatile com.aliyun.ecs20140526.Client instance;

    public static com.aliyun.ecs20140526.Client getInstance() throws Exception {
        if (instance == null) {
            synchronized (ClientFactory.class) {
                if (instance == null) {
                    com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                        .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                        .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
                    config.setEndpoint("ecs.cn-hangzhou.aliyuncs.com");
                    instance = new com.aliyun.ecs20140526.Client(config);
                }
            }
        }
        return instance;
    }
}
```

## Endpoint Configuration

Priority: explicit `endpoint` > region-based resolution via `regionId`.

```java
// Preferred: explicit endpoint
config.setEndpoint("ecs.cn-hangzhou.aliyuncs.com");

// Alternative: SDK resolves endpoint from region
config.setRegionId("cn-hangzhou");
```

### VPC Endpoints

Use VPC endpoints when running inside Alibaba Cloud VPC (hybrid cloud, leased lines, multi-region):

```java
config.setEndpoint("ecs-vpc.cn-hangzhou.aliyuncs.com");
```

### File Upload APIs (Advance)

For file upload APIs (e.g., Visual Intelligence), set **both** `regionId` and `endpoint` to the same region. Otherwise you may see timeouts due to cross-region OSS access:

```java
config.setRegionId("cn-shanghai");
config.setEndpoint("objectdet.cn-shanghai.aliyuncs.com");
// For VPC file upload authorization:
client._openPlatformEndpoint = "openplatform-vpc.cn-shanghai.aliyuncs.com";
```

## Synchronous vs Asynchronous

| Mode | SDK Artifact | When to Use |
|------|-------------|-------------|
| Synchronous | `com.aliyun:{productCode}{version}` | Simple flows, low concurrency, easier debugging |
| Asynchronous | `com.aliyun:alibabacloud-{productCode}{version}` | High concurrency/throughput, non-blocking I/O |

Async example:

```java
AsyncClient client = AsyncClient.builder()
    .region("cn-hangzhou")
    .credentialsProvider(provider)
    .overrideConfiguration(ClientOverrideConfiguration.create()
        .setEndpointOverride("ecs.cn-chengdu.aliyuncs.com"))
    .build();

CompletableFuture<DescribeRegionsResponse> response = client.describeRegions(request);
response.thenAccept(resp -> System.out.println(new Gson().toJson(resp)))
    .exceptionally(throwable -> { System.out.println(throwable.getMessage()); return null; });
// Always close async client when done
client.close();
```
