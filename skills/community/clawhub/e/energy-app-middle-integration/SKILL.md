---
name: energy-app-middle-integration
description: Use when integrating with the energy-app-middle BFF service - covers REST API endpoints, gRPC client setup, authentication headers, multi-tenancy, and downstream service dependencies for the changyuanfeilun energy platform.
---

# energy-app-middle Integration Guide

## Overview

`energy-app-middle` is a BFF + API aggregation layer for the distributed energy management platform. It exposes REST APIs to three client types (Owner / Provider / Platform) and orchestrates calls to IoT Core, IoT PaaS, IAM, algorithm services, and time-series databases.

## Quick Reference

| Client Type | Base Path | Audience |
|-------------|-----------|----------|
| Owner API | `/api/owner/*` | Energy asset owners |
| Provider API | `/api/provider/*` | Service providers |
| Platform API | `/platform-api/*` | Platform admins |
| gRPC Server | port `9090` | Internal services |
| Management | port `38081` | Actuator / metrics |

## 1. Key REST Endpoints

### Owner API (`/api/owner/`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/owner/der/control_record/{resourceId}` | DER control records (paginated) |
| GET/POST | `/api/owner/der/control_automation/{resourceId}` | DER automation settings |
| POST | `/api/owner/der/control_automation/{resourceId}/switch` | Toggle automation on/off |
| POST | `/api/owner/der/control_automation/{resourceId}/device` | Device automation properties |
| GET/POST | `/api/owner/project/price/{projectId}` | Electricity pricing |
| GET | `/api/owner/project/statistics/*` | Project electricity statistics |
| GET | `/api/owner/project/trend/*` | Project trend charts |
| GET/POST | `/api/owner/der/plan_prompt/*` | DER plan prompts |

### Provider API (`/api/provider/`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/provider/der/{resourceId}/billing_type` | Billing type (TOU/Market) |
| GET/POST | `/api/provider/der/{resourceId}/market_price_config` | Market price configs |

### Platform API (`/platform-api/`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/platform-api/market/config?marketCode={code}` | Market metric configurations |
| POST | `/platform-api/data` | Query market metric data |

## 2. Authentication & Headers

Token validation is delegated to IAM via gRPC. All requests must carry:

| Header | Description |
|--------|-------------|
| `X-ACCESS-TOKEN` | JWT token (validated by IAM) |
| `X-App` | App code |
| `X-Tenant` | Tenant code |
| `X-UID` | User UID (set by gateway) |
| `X-PUID` | Parent UID (for sub-accounts) |

All data is tenant-scoped — `tenantCode` is extracted from request context and applied to every query.

## 3. gRPC Integration (Internal Services)

### Dependency

```xml
<dependency>
    <groupId>com.feilun</groupId>
    <artifactId>energy-app-middle-grpc-interface</artifactId>
</dependency>
```

### Client Configuration

```yaml
grpc:
  client:
    energy-app-middle:
      address: dns:///energy-app-middle.${K8S_POD_NS}.svc.cluster.local:9090
      negotiationType: PLAINTEXT
      enableKeepAlive: true
```

## 4. Downstream Dependencies

| Service | Protocol | Purpose |
|---------|----------|---------|
| `iam` | gRPC | Token validation, authorization |
| `iot-core` | gRPC | Device management & queries |
| `iot-paas` | gRPC | Device grouping, batch tasks |
| `basic` | gRPC | Infrastructure services |
| `algorithm-der-power-forecast` | HTTP | PV power forecasting |
| `algorithm-dispatch` | HTTP | DR dispatch planning |
| `algorithm-bess-opt` | HTTP | Battery storage optimization |
| `algorithm-bid` | HTTP | VPP spot bidding |
| MySQL | JDBC | Transactional data |
| TDEngine | JDBC | Time-series device metrics |
| RisingWave | JDBC | Real-time metric aggregation |
| Apache Pulsar | Messaging | Device events, market data |
| PowerJob | HTTP | Distributed job scheduling |

## 5. Key DTOs

```
DerAutomationSettingsReq:
  dailyMaxImport/Export, dailyMinimalImport/Export (Double)
  maximumExportPower/ImportPower (Double)
  opportunityImportPrice/ExportPrice (Double)

DerControlRecordRes:
  resourceId, controlCode, status
  startTime, endTime, controlDate
  controlCurve (JSON array of power points)

MarketMetricDataReq:
  marketCode (AEMO_REGIONS: NSW1/QLD1/VIC1/SA1/TAS1)
  metrics (List<String>), targetId, startTime, endTime
```

## 6. Environment Variables

| Variable | Purpose |
|----------|---------|
| `K8S_POD_NS` | Kubernetes namespace (used in gRPC addresses) |
| `BIZ_NAME` | Business code (`energy-app-middle`) |
| `SPRING_PROFILES_ACTIVE` | Profile (`localdev` / `prod`) |
| `k8s.all.mysql.host/port` | MySQL connection |
| `k8s.eam.mysql.database` | MySQL database name |
| `k8s.all.tdengine.host` | TDEngine host |
| `k8s.all.risingwave.host/port` | RisingWave connection |
| `k8s.all.pulsar.service-url` | Pulsar broker URL |
| `k8s.all.powerjob.worker.server-address` | PowerJob server |

## 7. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `X-Tenant` header | Required for all requests — tenant isolation is enforced |
| Calling gRPC without `X-UID`/`X-PUID` | IoT PaaS interceptor requires both headers |
| Querying metrics without time range | TDEngine/RisingWave queries require `startTime` + `endTime` |
| Wrong `marketCode` | AEMO regions: `NSW1`, `QLD1`, `VIC1`, `SA1`, `TAS1` only |
