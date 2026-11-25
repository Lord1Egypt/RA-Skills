---
name: checkly-monitors
description: Create health and infrastructure monitors including heartbeat, TCP, DNS, ICMP, URL, gRPC, SSL, and traceroute monitors. Use for uptime monitoring, service availability, TLS certificate validation, gRPC health or behavior checks, network path diagnostics, DNS validation, and infrastructure health without browser code. Triggers on heartbeat, TCP monitor, DNS monitor, ICMP monitor, ping monitor, URL monitor, gRPC monitor, SSL monitor, certificate expiry, traceroute, health check, uptime monitoring.
---

# checkly monitors

Health and infrastructure checks without browser code execution.

Retired `me-south-1` (Bahrain) is invalid in monitor locations and inherited defaults. Remove or replace it before validation, testing or deployment.

## Monitor types

| Monitor | Use case | Checks |
|---------|----------|--------|
| **Heartbeat** | Periodic ping expected | Inbound webhook calls |
| **TCP** | Port connectivity | Socket connection |
| **DNS** | Domain resolution | DNS records |
| **ICMP** | Host reachability | ICMP echo |
| **URL** | HTTP availability | Status code only |
| **gRPC** | gRPC service health or unary behavior | Status, health, response, metadata, latency |
| **SSL** | Certificate and TLS posture | Expiry, trust, hostname, protocol, cipher, key |
| **Traceroute** | Network path diagnostics | Latency, hop count, packet loss |

## Structured monitor intent

`TcpMonitor`, `DnsMonitor`, `IcmpMonitor`, `UrlMonitor`, and `GrpcMonitor` accept structured `intent` for durable root-cause-analysis and check-repair guidance. `HeartbeatMonitor`, `SslMonitor`, and `TracerouteMonitor` do not expose it.

```typescript
new UrlMonitor('dashboard-url', {
  name: 'Dashboard URL',
  request: {
    url: 'https://example.com/dashboard',
  },
  intent: {
    goal: 'Verify that the dashboard remains publicly reachable.',
    constraints: [
      {
        type: 'REQUIRED_OUTCOME',
        statement: 'The dashboard returns a successful HTTP response.',
      },
      {
        type: 'MUST_PRESERVE',
        statement: 'Keep the production hostname in the monitored URL.',
      },
    ],
  },
})
```

Intent supplements executable monitor assertions; it does not replace them. Provide an object to set or update intent; omit it or set `intent: null` to have none. Both omission and `null` clear any web-authored intent on deployment. `goal` is required and limited to 2,000 trimmed characters. Constraints use exact uppercase types `REQUIRED_OUTCOME` or `MUST_PRESERVE`, with at most 20 of each type and 1,000 trimmed characters per statement.

## Heartbeat monitors

Expect periodic pings from your application.

```typescript
import { HeartbeatMonitor } from 'checkly/constructs'

new HeartbeatMonitor('app-heartbeat', {
  name: 'App Heartbeat',
  period: 300,
  periodUnit: 'seconds',
  grace: 60,
  graceUnit: 'seconds',
})
```

Your application pings the generated heartbeat URL:

```bash
curl -X POST https://ping.checklyhq.com/heartbeats/{YOUR_ID}
```

## TCP monitors

Check TCP port connectivity.

```typescript
import { TcpMonitor } from 'checkly/constructs'

new TcpMonitor('database-tcp', {
  name: 'Database TCP Check',
  request: { hostname: 'db.example.com', port: 5432 },
  frequency: 5,
})
```

## DNS monitors

Validate DNS records.

```typescript
import { DnsMonitor, DnsAssertionBuilder } from 'checkly/constructs'

new DnsMonitor('dns-check', {
  name: 'DNS A Record',
  request: {
    query: 'example.com',
    recordType: 'A',
    assertions: [DnsAssertionBuilder.jsonAnswer('$.Answer[0].data').equals('93.184.216.34')],
  },
})
```

Use `recordType: 'HTTPS'` when validating HTTPS/SVCB-style service-binding records (RFC 9460):

```typescript
new DnsMonitor('https-dns-check', {
  name: 'DNS HTTPS Record',
  request: {
    query: 'example.com',
    recordType: 'HTTPS',
    assertions: [DnsAssertionBuilder.textAnswer().contains('alpn')],
  },
})
```

## URL monitors

Check simple HTTP availability.

```typescript
import { UrlMonitor } from 'checkly/constructs'

new UrlMonitor('url-check', {
  name: 'Homepage URL Check',
  request: {
    url: 'https://example.com',
  },
})
```

## gRPC monitors

Use `GrpcMonitor` for a unary method (`BEHAVIOR`) or the standard gRPC health-check service (`HEALTH`). The request `url` is a hostname without a scheme.

```typescript
import { GrpcAssertionBuilder, GrpcMonitor } from 'checkly/constructs'

new GrpcMonitor('grpc-health', {
  name: 'gRPC Health',
  degradedResponseTime: 3000,
  maxResponseTime: 10000,
  request: {
    url: 'grpc.example.com',
    port: 50051,
    grpcConfig: {
      mode: 'HEALTH',
      tls: true,
      service: 'my.package.Service',
    },
    assertions: [
      GrpcAssertionBuilder.statusCode().equals(0),
      GrpcAssertionBuilder.healthCheckStatus().equals('SERVING'),
      GrpcAssertionBuilder.responseTime().lessThan(5000),
    ],
  },
})
```

- In `HEALTH` mode, optionally set `grpcConfig.service`; omit it to query overall server health.
- In protobuf `BEHAVIOR` mode, set `grpcConfig.method` and use `serviceDefinition: 'REFLECTION'` or `'PROTO_FILE'`. For FlatBuffers, use `encoding: 'FLATBUFFERS'` and base64-encoded compiled schema `bfbsContent`; omit `serviceDefinition` and `protoContent`. FlatBuffers is not allowed in `HEALTH` mode.
- `healthCheckStatus().equals()` and `.notEquals()` accept `UNKNOWN`, `SERVING`, `NOT_SERVING`, or `SERVICE_UNKNOWN` (or raw enum values `0`-`3`). Use the builder: it emits the numeric wire target required by the runner.
- In `BEHAVIOR` mode, use `responseMessage('$.path')`, `textBody()`, or `responseMetadata('header-name')` assertions as appropriate.
- Do not add `storeResponseBody` to the request; it is no longer part of `GrpcRequest`.

## SSL monitors

Use `SslMonitor` to validate certificate expiry, chain trust, hostname verification, TLS version, cipher suite, key size, signature algorithm, fingerprints, and OCSP stapling. The request `hostname` has no scheme.

```typescript
import {
  CipherSuite,
  SslAssertionBuilder,
  SslMonitor,
  TlsVersion,
} from 'checkly/constructs'

new SslMonitor('tls-certificate', {
  name: 'TLS Certificate',
  degradedResponseTime: 3000,
  maxResponseTime: 10000,
  request: {
    hostname: 'example.com',
    port: 443,
    ipFamily: 'IPv4',
    sslConfig: {
      alertDaysBeforeExpiry: 30,
      skipChainValidation: false,
    },
    assertions: [
      SslAssertionBuilder.certificate('daysUntilExpiry').greaterThan(30),
      SslAssertionBuilder.certificate('selfSigned').equals(false),
      SslAssertionBuilder.connection('chainTrusted').equals(true),
      SslAssertionBuilder.connection('hostnameVerified').equals(true),
      SslAssertionBuilder.connection('tlsVersion').equals(TlsVersion.TLS1_3),
      SslAssertionBuilder.connection('cipherSuite').equals(CipherSuite.TLS_AES_256_GCM_SHA384),
      SslAssertionBuilder.responseTime().lessThan(1000),
    ],
  },
})
```

- Response-time thresholds are top-level monitor properties and measure TLS handshake time.
- Put certificate settings under `request.sslConfig`.
- For mutual TLS, set `clientCertificateMode: 'explicit'` and `sslClientCertificateId` under `sslConfig`; never embed certificate secrets in a check file.
- SSL assertions are property-scoped. Use `certificate('<property>')` for certificate facts and `connection('<property>')` for connection and handshake facts; migration warning: source-specific builders such as `certExpiresInDays()` and `tlsVersion()` are obsolete.
- Certificate properties include `daysUntilExpiry`, `keySizeBits`, `subjectCN`, `issuerCN`, `serialNumber`, `fingerprintSha256`, `issuerFingerprintSha256`, `keyAlgorithm`, `signatureAlgorithm`, `sans`, `selfSigned`, and `isCA`.
- Connection properties include `tlsVersion`, `cipherSuite`, `hostnameVerified`, `chainTrusted`, `ocspStapled`, `ocspStatus`, and `resolvedIp`.
- The supported operator depends on the property. Numeric properties support equality and greater/less-than comparisons; booleans support `equals`; strings generally support equality and, where applicable, `contains`/`notContains`.
- Use `responseTime()` for TLS response time, `jsonResponse('$.path')` for structured result fields, and `textResponse()` (optionally with an extraction regex) for serialized result text.
- Use the exported `TlsVersion`, `CipherSuite`, and `SignatureAlgorithm` constants to avoid invalid assertion values.

## Traceroute monitors

Use `TracerouteMonitor` for path latency, hop-count, and packet-loss diagnostics. The request `url` is a hostname without a scheme or port.

Response-time limits measure final-hop average round-trip latency: defaults are 500 ms degraded and 1000 ms failed. Validation compares effective values even when only one is set: degraded above 1000 requires an explicit maximum; a positive maximum below 500 requires an explicit degraded limit. `maxResponseTime: 0` disables failure on latency and lets the degraded limit apply alone. Equal limits leave no degraded state. These defaults match what deployed monitors with unset limits already use.

```typescript
import {
  TracerouteAssertionBuilder,
  TracerouteMonitor,
} from 'checkly/constructs'

new TracerouteMonitor('network-path', {
  name: 'Network Path',
  degradedResponseTime: 500,
  maxResponseTime: 1000,
  request: {
    url: 'example.com',
    protocol: 'TCP',
    port: 443,
    maxHops: 30,
    maxUnknownHops: 15,
    ptrLookup: true,
    assertions: [
      TracerouteAssertionBuilder.responseTime('avg').lessThan(1000),
      TracerouteAssertionBuilder.hopCount().lessThan(20),
      TracerouteAssertionBuilder.packetLoss().lessThan(10),
    ],
  },
})
```

- `protocol` accepts `TCP` (default), `UDP`, `ICMP`, or `SCTP`. If `port` is omitted, the backend defaults to 443 for TCP and 33434 for UDP/SCTP; omit `port` for ICMP.
- `responseTime()` accepts `avg` (default), `min`, `max`, or `stdDev`.
- `hopCount()` and `packetLoss()` do not take a property.

## Response-time validation

Constructs send effective default limits explicitly; omitted values continue to match backend defaults. Defaults in milliseconds (degraded / maximum) are API 5000 / 20000, URL and TCP 3000 / 5000, DNS 500 / 1000, gRPC 10000 / 20000, SSL 3000 / 10000, and traceroute 500 / 1000. These are defaults, not the validation ceilings below.

For `IcmpMonitor`, `degradedPacketLossThreshold` defaults to 10 and `maxPacketLossThreshold` to 20 (percent). Effective degraded must be at most effective maximum: setting only degraded above 20 fails, as does setting only maximum below 10. Set both explicitly for a different valid pair; explicit zero is preserved.

`degradedResponseTime` and `maxResponseTime` are top-level monitor properties. They control degraded/failing check states and are separate from response-time assertions inside `request.assertions`.

The CLI applies these standard client-side ceilings when the authenticated account does not advertise extended response-time limits:

| Monitor | Standard ceiling |
|---------|------------------|
| TCP | 5 seconds |
| DNS | 5 seconds |
| URL | 30 seconds |
| gRPC | 180 seconds |
| SSL | 30 seconds |
| Traceroute | 30 seconds |

For accounts with extended limits, the CLI skips the fixed ceiling and lets the Checkly API enforce the account-specific limit. Do not assume the entitlement is present: validate with `npx checkly test` against the target account. Older or self-hosted APIs that do not expose account feature flags keep the standard ceilings.

Ordering diagnostics depend on the construct, independently of those ceilings:

| Construct | Client-side ordering comparison |
|---|---|
| `ApiCheck`, `UrlMonitor`, `TcpMonitor`, `DnsMonitor` | Compare only when both response-time thresholds are explicit. |
| `GrpcMonitor`, `SslMonitor` | Also compare explicit degraded against an omitted maximum (20000 / 10000 ms respectively); an omitted degraded is not compared against explicit maximum. |
| `TracerouteMonitor` | Compare both effective response-time thresholds, including either omitted default (500 / 1000 ms); maximum zero disables latency failure. |
| `IcmpMonitor` | Compare both effective packet-loss thresholds, including either omitted default (10 / 20 percent). |

Thus only `degradedResponseTime: 8000` on `UrlMonitor`, or only `degradedResponseTime: 25000` on `ApiCheck`, produces no response-time ordering diagnostic; synthesis still sends the omitted maximum as 5000 / 20000 ms. This does not establish total project validity or live API acceptance. Prefer setting both thresholds to an ordered pair rather than relying on this validation gap.

## Validate and deploy

```bash
npx checkly test
npx checkly deploy
```

`retryStrategy`, `runParallel`, and higher frequencies are plan-gated for uptime monitors. Confirm the account's `UPTIME_CHECKS_*` entitlements before adding them; omit unavailable properties.

## Related skills

- See `checkly-checks` for API and browser checks plus deployed result inspection
- See `checkly-groups` for organizing monitors
- See `checkly-test` for local and Checkly-runtime validation
- See `checkly-deploy` for deployment safety
