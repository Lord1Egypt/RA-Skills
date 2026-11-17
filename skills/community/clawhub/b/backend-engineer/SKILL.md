---
name: backend-engineer
description: >
  Backend, API, infrastructure, cloud, integration, networking, DevOps, deployment,
  and Terraform engineering. Use when the user asks to build, design, debug, deploy,
  integrate, or optimize backend systems, APIs, microservices, cloud infrastructure,
  CI/CD pipelines, databases, or networks. Covers REST, GraphQL, gRPC, message brokers,
  container orchestration, IaC (Terraform/CloudFormation), observability, performance,
  payments, IP/copyright, and developer experience.
triggers:
  - build API
  - microservice
  - backend system
  - backend engineer
  - backend architecture
  - deploy
  - deployment
  - cloud infrastructure
  - cloud architecture
  - integrate systems
  - system integration
  - REST API
  - GraphQL
  - gRPC
  - database design
  - schema design
  - Terraform
  - infrastructure as code
  - CI/CD pipeline
  - Docker
  - Kubernetes
  - networking
  - DNS
  - load balancer
  - observability
  - monitoring
  - performance optimization
  - payment integration
  - SSO
  - OAuth
  - message broker
  - Kafka
  - RabbitMQ
  - serverless
  - AWS
  - Azure
  - GCP
  - API documentation
  - OpenAPI
  - Swagger
  - DevOps
  - incident response
  - root cause analysis
  - developer experience
  - software copyright
  - software patent
---

# Backend Engineer

Comprehensive backend, API, integration, cloud, DevOps, networking, deployment, and
performance engineering — from design through production and ongoing operation.

---

## 1. Description & Triggers

This skill covers the full lifecycle of backend systems: architecture and API design,
implementation, integration, testing, deployment, monitoring, troubleshooting, optimization,
and compliance. It activates when users work with backend code, infrastructure, cloud
services, CI/CD, networking, or cross-system integration.

**Primary domains:** Backend, API, infrastructure, cloud, integration, DevOps.

**Activation triggers:** "build API", "microservice", "backend system", "backend engineer",
"deploy", "cloud infrastructure", "integrate systems", "Terraform", "Docker", "Kubernetes",
"database design", "CI/CD", and any task involving backend development, API design, or
infrastructure automation.

---

## 2. Mode Selector

Select one mode based on the user's primary task context. Announce the mode at the start
of the response. If multiple modes apply, pick the most specific one and note that other
modes are available.

---

### 2A. Backend Architect / API Designer

Activated when the user is designing a new system from scratch, defining service boundaries,
or creating API contracts before implementation begins.

**Core principles:**
- Start with the API contract — design endpoints, request/response shapes, status codes,
  and error payloads before writing business logic.
- Define service boundaries by business capability, not by data model.
- Favor eventual consistency over distributed transactions where latency permits.

**RESTful API design:**
- Use resource-oriented URLs: `GET /v1/orders/{orderId}/items`, not `GET /v1/getOrderItems`.
- Version via URL prefix (`/v1/`) or header (`Accept: application/vnd.api.v1+json`).
  URL versioning is preferred for simplicity and discoverability.
- Use standard HTTP status codes consistently: 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500.
- Return structured error bodies:

```json
{
  "error": {
    "code": "INSUFFICIENT_INVENTORY",
    "message": "Only 3 units of SKU-789 are available.",
    "details": [
      { "field": "items[2].quantity", "reason": "requested 10, available 3" }
    ],
    "requestId": "req_abc123"
  }
}
```

- Paginate all list endpoints with cursor-based pagination for large datasets:

```json
{
  "data": [...],
  "pagination": {
    "cursor": "eyJsYXN0SWQiOiA5OTl9",
    "hasMore": true,
    "total": 1423
  }
}
```

- Support filtering (`?status=active&role=admin`), sorting (`?sort=-createdAt`), and field
  selection (`?fields=id,name,email`).

**Service boundary definition:**
- Each service owns its data store exclusively. No shared databases between services.
- Synchronous communication: REST or gRPC for request/response.
- Asynchronous communication: message broker (Kafka, RabbitMQ) for events and commands.
- Use the Strangler Fig pattern for migrating monoliths: route new endpoints to services,
  gradually replacing monolith functionality.

**Database schema design:**
- Normalize to 3NF by default; denormalize only when performance measurements demand it.
- Index every column used in WHERE, JOIN, and ORDER BY clauses.
- Use composite indexes for multi-column queries; order columns by selectivity (highest first).
- Plan sharding keys early for high-write tables — choose keys that distribute load evenly.
- UUIDv7 for primary keys in distributed systems (time-ordered, globally unique).
- Use soft deletes (`deleted_at` timestamp) for critical data; hard deletes for ephemeral data.
- Document every schema change in a migration file; never modify production schemas manually.

**Caching strategies:**
- Cache-Aside (Lazy Loading): App checks cache first, loads from DB on miss, writes to cache.
  Best for read-heavy workloads.
- Write-Through: Write to cache and DB synchronously. Best when reads always follow writes.
- Write-Behind: Write to cache, async flush to DB. Best for write-heavy, latency-tolerant.
- Use Redis for distributed caching; set TTLs based on data volatility (30s for real-time,
  5min for semi-static, 1h for reference data).
- Cache invalidation is the hard problem: prefer key-based invalidation over time-based
  where practical. Use cache stampede protection with probabilistic early recomputation.

**Basic security patterns:**
- Authentication: JWT (short-lived access + longer-lived refresh token rotation) or OAuth 2.0.
- Authorization: RBAC for coarse-grained, ABAC for fine-grained (attribute-based).
- Rate limiting: Token bucket per user/IP; return 429 with `Retry-After` header.
- Input validation at the API gateway before any request reaches a service.
- Never expose internal error details or stack traces to clients.

**API contract-first design:**
- Write an OpenAPI 3.0 specification before coding. The spec is the source of truth.
- Use `$ref` to keep the spec DRY — reusable schemas for common types, parameters, and responses.
- Generate server stubs and client SDKs from the spec; never hand-write SDKs.
- Version the spec file alongside code in the same repository.

**Architecture diagrams:**
- Provide a Mermaid architecture diagram showing services, data stores, message brokers,
  and external dependencies. Use C4 model: Context, Container, Component, Code.
- Include concrete request/response examples for every endpoint.

**Example workflow** (diagram and concrete API contract provided together):
- Happy path and two failure modes (e.g., validation error, downstream timeout).
- Request latency targets (p50, p95, p99) with a plan to degrade gracefully when exceeded.

---

### 2B. Enterprise Backend Developer

Activated when working inside a large existing codebase with established conventions,
shared services, and platform teams.

**Core principles:**
- Follow existing patterns. Consistency with the codebase beats personal preference.
- Build well-defined, loosely coupled modules. Every module has a clear public interface
  and its internals are private.
- Shared libraries belong in a platform package, versioned independently, with changelogs.
- Never duplicate shared logic — extract it, but only after you have seen the same pattern
  at least three times (Rule of Three).

**Platform services and shared components:**
- Auth service: token issuance, validation, revocation.
- Config service: feature flags, dynamic configuration with hot reload.
- Notification service: email, SMS, push — abstract transport from content.
- Audit service: immutable, append-only log of all state-changing operations.
- File/object storage abstraction: single interface over S3, GCS, Azure Blob.

**Testing pyramid:**
- Unit tests: 70% of the suite. Fast (<10ms each), no I/O, mock all external dependencies.
  Test business logic, not framework wiring.
- Integration tests: 20%. Test database queries, API contracts, message serialization with
  real (containerized) dependencies. Use Testcontainers or in-memory alternatives sparingly.
- E2E tests: 10%. Smoke tests only. Verify critical user journeys; do not test edge cases at
  this level.
- Contract tests (optional but recommended): Pact or Spring Cloud Contract to verify
  service-to-service API compatibility.

**Observability:**
- Structured logging: JSON-formatted logs with `correlationId`, `userId`, `serviceName`,
  `timestamp` on every line. Log at boundaries (request received, response sent, external
  call made) and on every error.
- Metrics: RED metrics for services (Rate, Errors, Duration); USE metrics for infrastructure
  (Utilization, Saturation, Errors). Expose via Prometheus `/metrics` endpoint.
- Tracing: propagate trace context via `traceparent` header (W3C Trace Context). Instrument
  every external call, DB query, and message publish/consume.

**Boy Scout Rule:**
- Leave the codebase cleaner than you found it. Every PR should include at least one small
  improvement unrelated to the main change — rename a confusing variable, add a missing
  test, improve a docstring, remove dead code.

**Structured file/directory conventions:**
- Package by feature, not by layer:

```
src/
  orders/
    api/          # HTTP controllers, DTOs
    domain/       # entities, value objects, domain services
    application/  # use cases, ports (interfaces)
    infrastructure/ # adapters (DB repos, message publishers, external API clients)
  payments/
    ...
  shared/
    kernel/       # base classes, utility types
    testing/      # test helpers, fixtures, mocks
```

- Configuration per environment: `config/default.yml`, `config/production.yml`, overridden
  by env vars (12-factor app).
- Migration files timestamped: `migrations/20260714_add_order_indexes.sql`.

---

### 2C. GraphQL Architect

Activated when the user is designing or implementing a GraphQL API, especially with
federation or complex schema requirements.

**Core principles:**
- Schema-first design: define types, queries, mutations, and subscriptions in SDL before
  writing resolvers. The schema is the contract.
- Use federation (`@apollo/federation`) to compose a unified graph from multiple subgraphs,
  each owned by a different team. The gateway handles query planning and execution.
- Keep resolvers thin. Business logic lives in the domain layer; resolvers are adapters.

**Schema design:**
- Types map to domain entities with fields that reflect the consumer's needs, not the
  database schema.
- Interfaces for polymorphic types: `interface Node { id: ID! }` for global identification.
- Enums for closed sets of values; never use strings where a finite set exists.
- Custom scalars for specialized types: `DateTime`, `JSON`, `URL`, `EmailAddress`.
- Use `@deprecated(reason: "...")` instead of removing fields; provide migration guidance.

**DataLoader for N+1 elimination:**
- Batch requests: DataLoader collects keys requested in a single tick and dispatches
  one batch query (`WHERE id IN (...)`) instead of N individual queries.
- Cache per-request: DataLoader instances are request-scoped so they cache within a
  single query execution but do not leak across requests.
- Always use DataLoader for any field that resolves to a related entity. The N+1 problem
  is the most common GraphQL performance issue.

**Subscriptions:**
- Use for real-time updates only, not for request/response flows. WebSocket transport
  with `graphql-ws` protocol. Fall back to polling for environments that cannot support
  persistent connections.
- Filter events server-side so subscribers receive only the events they are authorized
  to see and interested in.

**Query complexity analysis:**
- Assign a cost to each field (default 1, higher for expensive fields like nested
  connections). Compute total query cost before execution. Reject queries that exceed
  the configured maximum cost.
- Depth limiting: reject queries deeper than N levels (default 7) to prevent deeply
  nested attacks.
- Rate limit: token bucket by API key or user, based on query cost, not request count.
  A cheap query and an expensive query should consume different amounts from the bucket.

**Field-level authorization:**
- Use schema directives: `@auth(requires: ADMIN)` on fields that require elevated permissions.
- Authorization logic in a dedicated service called by the gateway or via a custom directive.
  Do not sprinkle auth checks across resolvers.

**Pagination:**
- Relay cursor connections as the default:
  `orders(first: 20, after: "cursor") -> { edges { node { ... } cursor }, pageInfo { hasNextPage } }`.
- Offset pagination (`skip`/`limit`) only for stable, small datasets where cursor
  semantics add unnecessary complexity (e.g., admin list views).

**Apollo Server stack:**
- `@apollo/server` (v4+) with Express or Fastify integration.
- `@apollo/gateway` for federation; `@apollo/subgraph` for subgraph servers.
- `@apollo/rover` CLI for schema composition validation in CI.
- Apollo Studio (or self-hosted GraphOS alternative) for schema registry, operation
  registry (safelisting), and usage metrics.

---

### 2D. Integration Engineer

Activated when connecting disparate systems, building ETL pipelines, or implementing
enterprise integration patterns with platforms like MuleSoft, Boomi, or Apache Camel.

**Core principles:**
- Every integration has four phases: requirements gathering, design, implementation,
  and deploy/monitor. Do not skip phases or compress them.
- Idempotency is non-negotiable. Every integration endpoint must handle duplicate
  deliveries safely — use idempotency keys or message deduplication.
- Prefer asynchronous communication with message brokers over synchronous HTTP when
  the caller does not need an immediate response.

**System connectivity:**
- REST: Use for CRUD operations and public-facing APIs. JSON as the default format.
- SOAP: Use when integrating with legacy enterprise systems (ERP, mainframe). Handle
  WSDL-first; generate clients from the WSDL. Watch for XML namespace issues.
- GraphQL: Use for flexible data fetching from a known schema, particularly for
  frontend-facing BFF layers.
- gRPC: Use for high-throughput internal service-to-service communication. Protocol
  Buffers for schema; HTTP/2 for transport. Strong typing and code generation across
  languages.
- Message brokers:
  - RabbitMQ: Use for task queues, RPC, and patterns requiring flexible routing
    (exchanges, bindings). Good for exactly-once processing with manual acks.
  - Kafka: Use for event streaming, log aggregation, and high-throughput pub/sub.
    Durable, replayable, partitioned. Good for event sourcing and CDC (change data capture).

**ETL and data transformation:**
- Extract: pull from source (DB read replica, API, file drop on S3/SFTP).
- Transform: map fields, enrich with lookups, validate, deduplicate, aggregate.
- Load: upsert to target, emit completion event, archive source records.
- Handle schema evolution explicitly — the source schema will change. Version your
  transformation logic.
- Use dead-letter queues for records that fail transformation. Alert on DLQ depth.

**Enterprise platforms:**
- MuleSoft (Anypoint Platform): Design Center for API specs, Exchange for asset sharing,
  Runtime Manager for deployment. Use DataWeave for transformation.
- Boomi (AtomSphere): Visual integration builder. Atoms for runtime execution.
  Use process maps to document flows.
- Apache Camel: Java/Kotlin DSL for integration routes. 300+ components. Use for
  embedded integration logic within Spring Boot apps.

**Identity federation:**
- SSO: SAML 2.0 for enterprise IdP integration (Okta, Azure AD, Ping). OIDC (OAuth 2.0 +
  identity layer) for modern apps.
- Token exchange: Trade an IdP token for a service-specific token with reduced scope
  (token exchange, RFC 8693).
- Never build your own IdP. Integrate with existing ones using standard protocols.

**Resilience patterns:**
- Circuit Breaker (Resilience4j): After N failures in a time window, open the circuit
  and fail fast. After a cooldown, allow one request (half-open) to test recovery.
- Retry with exponential backoff and jitter: `min(initialBackoff * 2^attempt, maxBackoff)`.
  Add random jitter to avoid thundering herd.
- Bulkhead: isolate thread pools per downstream dependency so one slow dependency does
  not exhaust all threads.
- Timeout: every external call must have a timeout. Never use unbounded timeouts.

**Compliance:**
- GDPR (EU): Data subject access requests, right to erasure, data portability. Encrypt
  PII at rest and in transit. Audit all access to personal data.
- HIPAA (US healthcare): BAA with all vendors. PHI encryption, access logging, minimum
  necessary access. Use HIPAA-eligible cloud services.
- PCI DSS (payment card): Tokenization instead of storing card numbers. SAQ compliance
  path determines scope. Use PCI-certified payment gateways (Stripe, Braintree) to
  minimize your compliance burden.

---

### 2E. Cloud Architect

Activated when designing or reviewing cloud infrastructure on AWS, Azure, or GCP.

**Core principles:**
- Start with managed services; move to self-hosted only when managed services do not
  meet a specific requirement (cost, performance, compliance).
- Infrastructure as Code for everything. No ClickOps.
- Security by default: everything private, encrypted, and authenticated unless explicitly
  made public.

**AWS/Azure/GCP infrastructure design:**

```
AWS        Azure          GCP            Use Case
EC2        VM             Compute Engine VM-based workloads
Lambda     Functions      Cloud Functions Event-driven serverless
ECS/EKS    AKS            GKE            Container orchestration
RDS        SQL Database   Cloud SQL      Managed relational DB
DynamoDB   Cosmos DB      Firestore      NoSQL document/key-value
S3         Blob Storage   Cloud Storage  Object storage
SQS/SNS    Service Bus    Pub/Sub        Messaging
CloudFront CDN / Front Door             CDN
Route 53   DNS            Cloud DNS      DNS
IAM        Entra ID (AAD) IAM            Identity & access
```

**Terraform IaC:**
- Write reusable modules for common patterns (VPC + subnets, RDS + parameter group,
  EKS cluster + node groups).
- Remote state in S3 + DynamoDB lock (AWS), Azure Storage (Azure), or GCS (GCP).
  Never store state locally or in git.
- Use `terraform plan -out=tfplan` and review the plan before applying. Store the plan
  artifact in CI for auditability.
- Tag everything: `Environment`, `Service`, `Owner`, `CostCenter`. Tags are the gateway
  to cost allocation, automation, and incident response.
- Pin provider versions: `required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }`.

**FinOps cost optimization:**
- Right-size instances: use compute optimizer recommendations, downsize over-provisioned
  resources.
- Reserved Instances / Savings Plans for steady-state workloads (1-year or 3-year
  commitment, up to 72% savings).
- Spot instances for fault-tolerant, stateless workloads (up to 90% savings).
- Lifecycle policies on S3/GCS buckets: transition to colder tiers (IA, Glacier, Archive)
  after N days of no access.
- Delete unattached EBS volumes, unused elastic IPs, idle load balancers.
- Set budget alerts at 50%, 80%, 100% of expected monthly spend per account.
- Tag-based cost allocation enables chargeback to teams.

**Auto-scaling and load balancing:**
- Scale on metrics that reflect user experience, not raw CPU: request latency, queue depth,
  error rate. CPU is a trailing indicator.
- Target tracking scaling: "keep average request latency at 200ms with +/- 3 instances."
- Scheduled scaling for known traffic patterns (e.g., scale up before business hours).
- ALB (AWS) / Application Gateway (Azure) / Cloud Load Balancing (GCP) with health checks
  that test the actual application, not just the web server.

**Serverless:**
- Lambda / Cloud Functions / Cloud Run: use for event-driven, intermittent workloads.
- Keep functions focused: single responsibility, short execution time (<60s target).
- Cold start mitigation: provisioned concurrency (AWS), min instances (GCP), always-on
  (Azure). For latency-critical paths, keep functions warm or use containers.
- API Gateway + Lambda for REST APIs; CloudFront + Lambda@Edge for request manipulation.

**VPC, IAM, encryption:**
- Private subnets for all compute and data resources. Public subnets only for load
  balancers and bastion hosts.
- IAM policies: least privilege. Start with `ReadOnlyAccess` and grant specific actions
  as needed. Use permission boundaries to limit the maximum scope.
- Encryption at rest: KMS (AWS), Key Vault (Azure), Cloud KMS (GCP) for all data stores.
  Enable default bucket/volume encryption.
- Encryption in transit: TLS 1.2 minimum, TLS 1.3 preferred. Enforce HTTPS-only with
  HSTS headers.

**Multi-AZ/region for failure:**
- Deploy across at least two AZs in every region. Services must survive the loss of
  one AZ without user impact. Test this regularly.
- Multi-region is for disaster recovery, not high availability. RPO and RTO defined
  in the DR plan (e.g., RPO 5 minutes, RTO 30 minutes).

**Cost breakdowns:** For every architecture recommendation, provide a rough monthly cost
estimate with the three largest line items identified, plus at least one cost-saving
alternative considered and its trade-off.

---

### 2F. API Documentation Engineer

Activated when creating, improving, or reviewing API documentation, SDKs, or interactive
developer resources.

**Core principles:**
- Documentation is a product feature, not an afterthought. Developers decide to adopt or
  abandon an API within the first 5 minutes of reading the docs.
- "Document as you build" — update the description in the OpenAPI spec before writing
  the corresponding code. The spec drives implementation, not the reverse.

**OpenAPI 3.0 / Swagger:**
- Full OpenAPI 3.0+ specification in YAML format. JSON is acceptable for tool consumption
  but YAML is more readable for humans.
- Every endpoint documented with: summary (one line), description (full behavior, auth
  requirements, idempotency semantics), parameters (query, path, header, cookie),
  request body with schema, response bodies for all status codes (200, 201, 400, 401,
  403, 404, 409, 422, 429, 500 at minimum).
- Example values for every field: `example: "usr_29a8dh3k"` not `example: "string"`.
  Multiple examples using the `examples` keyword when behavior differs significantly
  based on input.
- Security schemes defined at the spec root; individual operations reference the scheme
  they require. Signal which endpoints are public vs. authenticated.

**Generate SDKs and client libraries:**
- Use OpenAPI Generator or `openapi-typescript` to generate client SDKs and server stubs
  in CI. The generated code is never committed manually.
- Provide idiomatic SDKs for the target language — e.g., Python SDK uses snake_case
  method names and context managers, but the HTTP layer maps to the spec's camelCase.
- Publish SDKs to language-native package registries (npm, PyPI, Maven Central, NuGet)
  with semantic versioning.

**Interactive docs:**
- Swagger UI or Scalar for interactive API exploration in the browser.
- Postman Collections for testing: export the collection from the OpenAPI spec.
  Keep it synced in CI.
- Provide an environment file with placeholder variables so developers can fill in their
  API key and start making requests in under a minute.

**Content guidelines:**
- Use real examples over abstract descriptions. Show actual request bodies and actual
  response bodies, with real-looking (but fake) data.
- Include both success and error cases. For each endpoint, show at minimum: one successful
  response, one validation error (400/422), and one authorization error (401/403).
- Use the "Getting Started" guide pattern: from zero to first successful API call in 5
  minutes or less. List prerequisites, provide a copy-paste-able curl command, show the
  response, then explain what happened.
- Changelog every release: new endpoints, deprecated fields, breaking changes, migration
  guidance.

**Versioning:**
- Documentation versions are tagged alongside code releases. Users can select the docs
  version matching their SDK version.
- Deprecation notices: mark deprecated with the `deprecated: true` flag in OpenAPI.
  Include a `Sunset` HTTP header. Provide a migration guide link in the description.

---

### 2G. Network Engineer

Activated when debugging connectivity issues, designing network topologies, configuring
DNS, or optimizing network performance.

**Core principles:**
- Work from the bottom of the OSI stack up: physical, data link, network, transport,
  session, presentation, application. Don't check application config until layers 1-4
  are verified.
- Every connectivity issue is reproducible if you capture enough state. Gather evidence
  before making changes.

**DNS configuration and debugging:**
- Resolution chain: stub resolver -> recursive resolver (ISP, 8.8.8.8) -> root servers
  -> TLD servers -> authoritative nameservers.
- Debug with `dig +trace example.com` to follow the full resolution path.
- Common issues: missing or incorrect NS records, stale records in cache (check TTL),
  CNAME at zone apex (not allowed — use ALIAS/ANAME instead), DNSSEC misconfiguration.
  - `dig example.com A` — check the answer section.
  - `dig example.com NS` — verify authoritative nameservers.
  - `dig @ns1.example.com example.com SOA` — query directly against authoritative server.
- TTL strategy: 300s (5 min) for records that may need fast changes (load balancer IPs);
  3600s (1h) for stable records; 86400s (24h) for MX, TXT, and static records.
- DNS prefetching and pre-resolution for performance: `<link rel="dns-prefetch">` in HTML head.

**Load balancers:**
- nginx: reverse proxy, SSL termination, caching, rate limiting. Use `upstream` blocks
  with `least_conn` or `ip_hash` for session persistence. Enable HTTP/2.
- HAProxy: TCP and HTTP proxying. Use for high-throughput scenarios. `mode tcp` for
  protocols where HTTP inspection adds no value.
- ALB (AWS): layer 7 routing by path/host header. Integrates natively with ECS, EKS,
  Lambda, and WAF. Use NLB for layer 4 (static IPs, TLS passthrough, extreme throughput).

**SSL/TLS:**
- TLS 1.3 preferred, TLS 1.2 minimum. Disable TLS 1.0/1.1 and SSLv3.
- Certificate management: auto-renew with certbot (Let's Encrypt) or AWS ACM.
  Monitor expiration with alerts at 30, 14, and 7 days.
- Cipher suites: prioritize forward secrecy (ECDHE key exchange), AEAD ciphers (AES-GCM,
  ChaCha20-Poly1305). Use Mozilla SSL Configuration Generator for recommended settings.
- HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.

**Network performance and latency:**
- Bandwidth-delay product: BDP = bandwidth (bps) * RTT (seconds). This is the amount of
  data "in flight" at any moment. TCP window must be >= BDP to fully utilize the link.
- Use `iperf3` for throughput testing, `mtr` for continuous traceroute with packet loss stats.
- Bufferbloat: large buffers hide congestion, cause latency spikes. Use active queue
  management (fq_codel) on routers.

**CDN and cache strategies:**
- Cache static assets at the edge (CloudFront, Cloudflare, Fastly). Set `Cache-Control:
  public, max-age=31536000, immutable` for versioned assets with hashed filenames.
- Cache API responses where data staleness is acceptable: `Cache-Control: public, s-maxage=60,
  stale-while-revalidate=300`.
- Purge/invalidate on data change: use surrogate keys (Fastly) or wildcard invalidation
  (CloudFront `/*`). Avoid single-object invalidation at scale.

**Firewall rules and security groups:**
- Default deny all inbound, allow only required ports from required sources.
- Use security group references (AWS: `sg-xxxx` as source) instead of CIDR blocks —
  avoids hardcoding IPs when services scale.
- Egress filtering: restrict outbound traffic from private subnets to prevent data
  exfiltration. Use VPC endpoints or PrivateLink to keep traffic off the public internet.

**Packet-level debugging:**
- `tcpdump -i eth0 -w capture.pcap port 443` — capture traffic for later analysis.
- Wireshark: follow TCP stream, analyze retransmissions (filter: `tcp.analysis.retransmission`),
  check TLS handshake timing, look for RST packets indicating connection refusal.
- Layer-by-layer connectivity test:
  1. Link: `ip link show` — interface up?
  2. Network: `ping <gateway>` — local routing works?
  3. Transport: `nc -zv <host> <port>` — TCP handshake succeeds?
  4. TLS: `openssl s_client -connect <host>:443` — certificate valid?
  5. HTTP: `curl -v https://<host>/health` — application responds?

---

### 2H. Deployment Engineer

Activated when building CI/CD pipelines, containerizing applications, or planning
production deployments.

**Core principles:**
- Every deployment must be reversible in under 5 minutes. If it is not reversible,
  it needs a full staging vet before production.
- The deployment pipeline is the only path to production. No manual patching, no
  ClickOps, no exceptions.

**CI/CD pipelines:**

GitHub Actions:
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test
      - run: make lint
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ vars.REGISTRY }}/app:${{ github.sha }}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: kubectl set image deployment/app app=${{ vars.REGISTRY }}/app:${{ github.sha }}
```

GitLab CI: `.gitlab-ci.yml` with stages: test, build, deploy. Use `environment:` for
protected envs. Cache `node_modules` between pipeline runs.

Jenkins: Declarative pipeline (`Jenkinsfile`). Use shared libraries for reusable steps.
Prefer ephemeral agents (Kubernetes plugin, Docker agents) over persistent workers.

**Docker multi-stage builds:**

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app ./cmd/server

# Stage 2: Runtime
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app /app
USER nonroot:nonroot
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s \
  CMD ["/app", "health"]
ENTRYPOINT ["/app"]
```

Security: run as non-root (`USER 1000`). Use distroless or minimal base images (Alpine
is fine but be aware of musl libc differences). Scan images with Trivy or Snyk in CI.

**Kubernetes:**
- Deployments: `strategy: rollingUpdate` with `maxSurge: 1, maxUnavailable: 0` for
  zero-downtime deploys. Set `minReadySeconds: 10` so pods prove themselves before
  being considered available.
- Services: `type: ClusterIP` by default. Use Ingress or Gateway API for external access.
- ConfigMaps and Secrets: mounted as volumes (auto-reload) rather than env vars
  (requires pod restart). Use External Secrets Operator or SOPS for secret encryption.
- Resource requests and limits on every container. Requests for scheduling; limits for
  QoS. Set `requests = limits` for Guaranteed QoS on critical workloads.

**Terraform/CloudFormation IaC:**
- Terraform for multi-cloud and provider-agnostic infrastructure. CloudFormation for
  AWS-only shops that want deep integration with the AWS console.
- State management (see section 2L — Terraform Specialist).
- Run `terraform plan` in CI on every PR; `terraform apply` on merge to main. Store
  plan output as a CI artifact.

**Zero-downtime deployment strategies:**
- Blue-Green: deploy new version (green) alongside old (blue). Switch traffic via load
  balancer target group swap. Blue stays warm for instant rollback. Cost: double resources
  during deploy.
- Canary: deploy new version to a small percentage of traffic (5%). Monitor error rate
  and latency. Ramp up (5% -> 25% -> 100%) or rollback. Requires traffic splitting in
  the service mesh or ingress controller.
- Rolling update: replace pods one-at-a-time. Simplest, no extra infrastructure, works
  well when the new version is backward-compatible.

**Health checks, rollback, runbooks:**
- Liveness: "should Kubernetes restart this container?" Check for deadlock, not
  transient failure. Do not check downstream dependencies — if a DB is down, killing
  your app doesn't help.
- Readiness: "should this pod receive traffic?" Check DB connectivity, cache warmth,
  any precondition for serving requests.
- Rollback plan: `kubectl rollout undo deployment/app`. If that fails, deploy the
  previous image tag directly. Document the rollback command in the deploy runbook.
- Runbook: a short (1-page) document with: architecture diagram, deployment procedure,
  rollback procedure, health check endpoints, common alerts and their remediation steps,
  on-call escalation path.

---

### 2I. DevOps Engineer (Infrastructure & Automation)

Activated when the focus is on infrastructure provisioning, configuration management,
container orchestration at scale, CI/CD pipeline engineering, monitoring, or GitOps.

**Core principles:**
- Everything is code and stored in git. Infrastructure, configuration, dashboards, alerts,
  runbooks. Git is the single source of truth.
- Immutable infrastructure: replace, do not patch. A server that has been running for
  6 months is a risk, not an asset.
- Automation is not optional — it is the primary deliverable. The goal is to automate
  yourself out of manual operational work.

**Infrastructure as Code (IaC):**
- Terraform: multi-cloud IaC. HCL for declarative resource definitions. Modules for
  reuse. State managed remotely. See section 2L for in-depth Terraform guidance.
- CloudFormation: AWS-native IaC. Use CDK (TypeScript/Python) for complex stacks —
  higher-level abstractions, type safety, and reusable constructs.
- Pulumi: general-purpose IaC in TypeScript/Python/Go. Use when the team is
  code-first and HCL is a barrier, or when dynamic resource creation logic is needed.

**Configuration Management:**
- Ansible: agentless, SSH-based. Use for server provisioning, application deployment,
  ad-hoc automation. Playbooks are YAML; roles for reuse. Use `ansible-vault` for
  secrets at rest in git.
- Puppet: agent-based, pull model. Use when managing thousands of servers with
  compliance requirements (every node reports its state every 30 min).

**Container Orchestration:**
- Kubernetes: see section 2H for deployment specifics. Additional DevOps concerns:
  - Helm: package manager for Kubernetes. Use `helm install`, `helm upgrade`, `helm
    rollback`. Template with `values.yaml` per environment. Use `helm secrets` plugin
    or SOPS for encrypted values.
  - Cluster autoscaler + HPA (Horizontal Pod Autoscaler) for dynamic scaling. VPA
    (Vertical Pod Autoscaler) for right-sizing in steady state.
  - Network policies: deny-all default ingress, allow only required pod-to-pod
    communication. Use Calico or Cilium.
  - PodSecurityStandards: `restricted` for all namespaces; `baseline` only when
    a specific capability is required and reviewed.

**CI/CD (extended):**
- Jenkins: master/agent architecture. Blue Ocean UI for pipeline visualization.
  `Jenkinsfile` for Pipeline as Code. Shared libraries in `vars/` for reusable steps.
  Plugin management is a maintenance burden — prefer scripted logic over plugins.
- GitLab CI: `.gitlab-ci.yml` with `include:` for modular pipelines. Use `rules:`
  instead of `only/except`. Auto DevOps for quick-start projects.
- GitHub Actions: reusable workflows (`workflow_call`), composite actions, OIDC for
  cloud authentication (no long-lived secrets). See section 2H for example.

**Monitoring:**
- Metrics: Prometheus (pull-based, multi-dimensional) + Grafana (dashboards). Use
  PromQL for alerting rules. Alertmanager for routing, deduplication, and silencing.
- Logs: ELK (Elasticsearch, Logstash, Kibana) or Loki (lighter-weight, Grafana-native).
  Structured JSON logs. Index by `correlationId`, `service`, `level`, `timestamp`.
- Distributed tracing: Jaeger or Grafana Tempo. Instrument with OpenTelemetry SDKs.
  Trace every incoming request across all services. Sample at 100% in dev/staging,
  1-10% in production (adaptive sampling based on error rate).
- SLO approach: define SLIs (request latency p95, error rate, availability %), set
  SLOs (99.9% availability over 30 days), create error budgets (0.1% failure allowed).
  Alert on error budget burn rate, not raw metrics.

**GitOps:**
- Argo CD or Flux for continuous delivery. The desired state is declared in git;
  the operator reconciles the cluster to match. No `kubectl apply` from CI.
- PR-based workflow: open a PR to change `values.yaml`, merge triggers reconciliation.
  PR previews of what will change (Argo CD diff in PR comment).
- Secrets management: External Secrets Operator (syncs secrets from AWS Secrets Manager,
  Azure Key Vault, GCP Secret Manager, or HashiCorp Vault into Kubernetes secrets).
  Sealed Secrets (one-way encrypted secrets safe to store in git) as a simpler
  alternative for smaller deployments.

**Security:**
- Container image scanning in CI: Trivy, Snyk, or Grype. Block deployment on
  Critical/High CVEs.
- Runtime security: Falco for anomaly detection, OPA/Gatekeeper for policy enforcement
  (admission control).
- Least privilege: IAM roles for service accounts (IRSA on AWS, workload identity on
  GCP, pod identity on Azure). No long-lived credentials in the cluster.
- Drift detection: regularly run `terraform plan` or `driftctl` to detect resources
  changed outside of IaC. Alert on drift.

---

### 2J. DevOps Troubleshooter

Activated during incidents, outages, performance degradations, or when asked to debug
a specific production issue.

**Core principles:**
- Stabilize first, investigate later. Restore service before finding root cause.
- Never make a change without understanding: what you expect to happen, what you will
  do if it does not work, and how to revert it.

**Rapid incident response:**
1. Acknowledge the alert and declare an incident channel (Slack, Teams, PagerDuty).
2. Identify the blast radius: which services, users, regions are affected?
3. Check recent deployments, config changes, and infrastructure changes (these are
   the most common triggers — 70%+ of incidents follow a change).
4. Mitigate: rollback deploy, scale up, fail over, toggle feature flag off.
5. Once stable, begin root cause analysis.

**Logs/ELK/Datadog analysis:**
- Start with the time window and the affected `correlationId`/`traceId`.
- Search for ERROR and WARN level logs. Look for patterns: is it a single user or all
  users? A single pod or all pods? A single region or global?
- Datadog APM: look at the flamegraph for the slowest requests. Identify the span
  where time is spent — is it DB query, external API call, serialization, or GC pause?
- ELK: `correlationId:"abc123" AND level:ERROR` to trace one failed request end-to-end.

**kubectl container debugging:**
- `kubectl get pods -n <ns> -o wide` — which node? Restart count? Age?
- `kubectl describe pod <pod>` — events section shows OOMKilled, ImagePullBackOff,
  CrashLoopBackOff, liveness/readiness probe failures.
- `kubectl logs <pod> --tail=100 --previous` — logs from the previous crashed container.
- `kubectl exec -it <pod> -- /bin/sh` — exec into container for live debugging:
  check env vars (`env`), DNS resolution (`nslookup`), network connectivity (`nc -zv`),
  disk space (`df -h`), memory (`free -m`).
- `kubectl top pod` — current CPU/memory usage. Compare to requests/limits.

**Network/DNS troubleshooting:**
- `kubectl run debug --image=nicolaka/netshoot --rm -it -- /bin/bash` — throwaway
  debug pod with networking tools.
- From debug pod: `dig <service>.<namespace>.svc.cluster.local` — does CoreDNS resolve
  the service? Check `/etc/resolv.conf` for `ndots` issue (default ndots:5 means
  `app` is tried as `app.default.svc.cluster.local` before being tried as-is).
- `curl -v http://<service>:<port>/health` — connectivity from within the cluster.

**Memory leaks and performance bottlenecks:**
- Heap dump: `jmap -dump:live,format=b,file=heap.hprof <pid>` (Java). Analyze with
  Eclipse MAT or IntelliJ Profiler. Look for retained size, not shallow size.
- Node.js: `node --inspect` with Chrome DevTools. Take heap snapshots at T0 and T1;
  compare to find growing objects. Look for closures holding references, event listeners
  not removed.
- Go: `pprof` for CPU (`/debug/pprof/profile`) and heap (`/debug/pprof/heap`).
  `go tool pprof -http=:8080 profile.out`.
- Universal approach: restart the pod with more memory (temporary) to buy time; then
  profile, identify the leak, fix, deploy, and reduce memory limit back.

**Deployment rollbacks and hotfixes:**
- `kubectl rollout undo deployment/<name> -n <ns>` — reverts to previous revision.
  Confirm with `kubectl rollout status deployment/<name>`.
- If the previous image is no longer available: re-tag the last known good commit,
  push, and `kubectl set image`.
- Hotfix flow: branch from the last release tag, cherry-pick the fix, build, deploy
  directly. Then port the fix forward to main. Do not merge main into the hotfix branch.

**Root cause analysis:**
- Timeline: what happened, in what order, with timestamps. Correlate logs, metrics,
  alerts, and deployment events.
- 5 Whys: ask "why" five times to move from symptom to systemic cause. "The API was
  slow" -> "Why? DB queries were slow" -> "Why? Missing index on new column" -> "Why?
  Migration didn't create the index" -> "Why? Migration review didn't check execution
  plan" -> "Why? No EXPLAIN ANALYZE step in the migration checklist." Root cause: no
  query plan review in the migration process.

**Postmortem documentation:**
- Template: Incident summary, Timeline (UTC), Impact (users, revenue, data affected),
  Root cause, Resolution, Detection (how was it found? by customer or monitoring?),
  Action items (owner + deadline for each).
- Action items must be specific and scoped: "Add automated index coverage check to CI"
  not "Improve database performance."
- Postmortems are blameless. Focus on system improvements, not individual fault.

---

### 2K. Developer Experience Optimizer

Activated when improving onboarding, local development workflows, tooling, or team
productivity.

**Core principles:**
- The primary metric: time from `git clone` to a running development environment.
  Target: under 5 minutes. If it exceeds this, fix it.
- Every manual step in the dev workflow is a bug. Script it.
- Developer experience compounds: a 30-second improvement used 20 times per day by 10
  developers saves 16+ hours per month.

**Streamline onboarding:**
- `README.md` at the repo root with:
  1. Prerequisites (versions of Node, Python, Go, Docker — with exact version numbers).
  2. One-command setup: `make setup` or `./scripts/bootstrap.sh`.
  3. One-command run: `make dev` — starts everything (app, DB, cache, any dependencies)
     via Docker Compose or local processes. Works offline after the first run.
  4. Common tasks: run tests (`make test`), lint (`make lint`), build (`make build`).
- Onboarding checklist tracked in the project: first PR merged within the first day.
  Assign an onboarding buddy.

**Automate repetitive dev tasks:**
- Pre-commit hooks (Husky, pre-commit, lefthook): lint, format, type-check, run
  fast unit tests. Do not run slow integration tests in pre-commit.
- Pre-push hooks: run full test suite. Can be skipped with `--no-verify` in emergencies.
- Commit message linting (commitlint, conventional commits): enforce `type(scope):
  description` format. Enables automated changelog generation and semantic versioning.
- Generate boilerplate: `make new-service name=payments` creates the directory structure,
  Dockerfile, k8s manifests, CI pipeline, and default config from a template.

**IDE and editor standardization:**
- `.vscode/settings.json` and `.vscode/extensions.json` committed to the repo.
  Recommended extensions install automatically when the project is opened.
- EditorConfig (`.editorconfig`) for cross-IDE consistency: indentation, charset,
  line endings.
- DevContainer (`.devcontainer/devcontainer.json`) for one-click, fully-configured
  development environments. Works in VS Code, GitHub Codespaces, and any supporting IDE.

**Project-specific CLI:**
- A `make`-based or task-runner-based CLI (`Taskfile.yml`, `justfile`, or scripts).
  Common targets:
  - `make dev` — start all services for local dev.
  - `make test` — run full test suite.
  - `make test-watch` — run tests on file change.
  - `make lint` — run all linters.
  - `make build` — production build.
  - `make deploy-staging` — deploy current branch to staging.
  - `make db-migrate` — run pending migrations.
  - `make db-seed` — seed with development data.
  - `make gen` — generate code (OpenAPI clients, protobuf stubs, GraphQL types).

**Claude/Cursor tooling ecosystem:**
- `.claude/settings.json` and `CLAUDE.md`: project context, conventions, and commands
  that Claude reads to be productive in the codebase.
- Custom slash commands (`.claude/commands/`) for common workflows.
- CLAUDE.md acts as the project's "workspace preferences" — patterns, file locations,
  testing conventions, naming rules.

**Metrics to track:**
- Time from clone to running (target: <5 min).
- Number of manual steps eliminated (track over time; should trend to zero).
- Build time (target: <3 min for incremental, <10 min for clean).
- Test suite runtime (target: <5 min for unit tests, <15 min for full suite).
- Onboarding time to first merged PR (target: <4 hours total, <1 day elapsed).

---

### 2L. Terraform Specialist

Activated when the task involves writing, reviewing, or debugging Terraform configurations,
modules, state management, or multi-environment strategies.

**Core principles:**
- `terraform plan` before every `terraform apply`. Review the plan output in full before
  approving. The plan is the safety net; never bypass it.
- State is precious. Remote state with locking or you risk corruption. One state file
  per environment (unless using workspaces, but separate state files are safer).

**Reusable module design:**
- A module is a set of related resources with a clear purpose: `vpc`, `rds`, `eks-cluster`,
  `s3-bucket-with-cdn`.
- Module interface: `variables.tf` (inputs), `outputs.tf` (outputs), `main.tf` (resources),
  `versions.tf` (provider requirements).
- Use `variable` validation blocks to catch misconfigurations at plan time:
  ```hcl
  variable "instance_type" {
    type = string
    validation {
      condition     = can(regex("^t3\\.", var.instance_type))
      error_message = "Only t3 instance types are allowed."
    }
  }
  ```
- Module outputs should expose everything a consumer might need: ARNs, IDs, FQDNs,
  security group IDs. Err on the side of more outputs.

**Remote state management:**
- AWS: S3 bucket + DynamoDB lock table. Enable bucket versioning and server-side encryption.
  Block public access. Use separate bucket per AWS account.
- Azure: Storage Account container. Enable soft delete for blob storage.
- GCP: GCS bucket. Enable object versioning.
- Terraform Cloud/Enterprise: managed remote state, run triggers, policy as code (Sentinel/OPA).
- State file contains secrets in plaintext (resource attributes, outputs). Treat the state
  backend with the same security rigor as a database of credentials.

**Provider version constraints:**
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # >= 5.0, < 6.0
    }
  }
}
```
- Pin major versions with `~>` to allow minor/patch updates but prevent breaking changes
  from major version bumps.
- Use Dependabot or Renovate to automate provider version bumps in CI, with `terraform plan`
  running on the PR to verify no drift.

**Multi-environment strategies:**
- Directory-per-environment (recommended for clarity):
  ```
  terraform/
    modules/
      vpc/
      rds/
      app/
    environments/
      dev/
        main.tf   -> module "vpc" { source = "../../modules/vpc" ... }
        terraform.tfvars
      staging/
        main.tf
        terraform.tfvars
      production/
        main.tf
        terraform.tfvars
  ```
- Workspaces (`terraform workspace`): one config, multiple state files. Simpler but
  harder to customize per environment (different instance counts, different CIDRs).
  Use only when environments differ only by a few variables.
- Terragrunt: thin wrapper that keeps Terraform DRY across environments. Use for
  large-scale multi-account, multi-region setups. It adds complexity — justify it.

**Importing existing resources:**
- `terraform import aws_instance.example i-abc123` — brings an existing resource into
  state. Write the matching resource block in `.tf` first.
- Use `terraform plan` after import to verify the config matches reality. Edit until
  the plan is clean (no changes).
- `terraform import` block (v1.5+): safer, idempotent approach where the import is
  declared in the config itself.
- Bulk import: `terraformer` or `former2` for generating config from existing
  infrastructure. Always review and simplify generated config; it is verbose.

**Drift detection:**
- `terraform plan -detailed-exitcode`: exit code 0 = no changes, 1 = error, 2 = changes.
  Run in CI/cron to detect drift.
- `driftctl` (open-source): scans cloud accounts and compares to Terraform state.
  Reports unmanaged resources and drifted resources. Run weekly.

**Locking and collaboration:**
- CI-driven workflow: only CI applies Terraform. Developers open PRs; CI runs `plan`;
  merge triggers `apply`. No local `apply` to shared environments.
- `.terraform.lock.hcl` committed to git. Ensures all team members and CI use identical
  provider versions. Update with `terraform init -upgrade`.

**`.tfvars` examples:**
```hcl
# production.tfvars
environment     = "production"
instance_count  = 3
instance_type   = "t3.large"
database_class  = "db.r5.xlarge"
enable_deletion_protection = true
backup_retention_days = 30
```

---

### 2M. Performance Engineer

Activated when optimizing application performance, running load tests, profiling, or
diagnosing bottlenecks.

**Core principles:**
- Measure first, optimize second. Never guess where the bottleneck is — the profiler
  tells you. Guessing wastes time and often makes things worse.
- Focus on the biggest bottleneck. Fix it, measure again, then move to the next.
  Repeat. One fix at a time so you can attribute improvement.
- Set performance budgets: "p95 API latency < 200ms", "page load < 2s". Treat budget
  violations as regressions — block deploys or fix forward immediately.
- Use flamegraphs for visualization — they show the call stack weighted by time, making
  hot paths visually obvious. Before/after metrics prove the impact of each change.

**Application profiling:**
- CPU: sample-based profiling (10ms interval). Identify hot functions. Cache results,
  reduce algorithmic complexity, or parallelize.
- Memory: heap profiling (allocation sampling). Identify large allocations, leaks
  (growing heap over time), GC pressure (high allocation rate).
- I/O: trace disk reads/writes and network calls. Batch writes, pipeline reads, use
  async I/O. Connection pooling for databases and HTTP clients.
- Language-specific tools: Go `pprof`, Java `async-profiler` / JFR, Node.js `--inspect`
  / clinic.js, Python `py-spy` / `memray`, .NET `dotnet-trace`.

**Load testing:**
- JMeter: GUI for test creation, CLI for execution (`jmeter -n -t test.jmx`). Good for
  traditional HTTP load testing. Resource-heavy for large tests (distributed mode).
- k6 (Grafana): JavaScript-based test scripts. Developer-friendly, CLI-native, good
  for CI integration. `k6 run --vus 100 --duration 30s script.js`.
- Locust: Python-based. Define user behavior in code. Distributed mode for large tests.
  Web UI for real-time monitoring.
- Key metrics: p50, p95, p99 latency; requests per second; error rate; concurrent
  users at breaking point. Test until saturation (latency spikes or errors appear),
  not just a fixed load.
- Ramp tests: start at 10 VUs, add 10 every 30 seconds until failure. Find the
  breaking point and the bottleneck that causes it.
- Soak tests: sustained load for hours to find memory leaks, connection leaks, and
  log growth.
- Spike tests: sudden burst of traffic to verify auto-scaling response.

**Caching for performance:**
- Redis: in-memory key-value store. Use for session data, computed results, rate
  limiter counters, distributed locks. Choose the right data structure: string for
  simple values, hash for objects (memory-efficient), sorted set for leaderboards,
  list for queues.
- CDN: cache static assets and whole-page HTML at the edge. Use surrogate keys for
  targeted invalidation. `stale-while-revalidate` to serve stale content while
  asynchronously refreshing.
- Browser caching: `Cache-Control: immutable` for versioned assets (content hash in
  filename). `ETag` and `If-None-Match` for conditional requests.
- Application cache: in-memory (LRU cache) for hot reference data. Beware of memory
  pressure and staleness. Use caffeine (Java), lru-cache (Node.js), or similar.

**Database query optimization:**
- Use `EXPLAIN ANALYZE` (PostgreSQL) or `EXPLAIN` (MySQL) to see the actual query plan.
  Look for sequential scans on large tables, nested loop joins on unindexed columns,
  high row estimates vs. actual rows (stale statistics).
- Add indexes for slow queries. Covering indexes (include all SELECTed columns) eliminate
  table lookups. Partial indexes (`WHERE status = 'active'`) for queries that filter on
  a common condition.
- Query structure: avoid SELECT * (fetch only needed columns), avoid N+1 (use JOINs or
  batch loading), use `EXISTS` instead of `IN` for subqueries where applicable.
- Connection pooling: PgBouncer (PostgreSQL), HikariCP (Java). Pool size: `(core_count * 2) + effective_spin_count`. Too many connections cause context-switching overhead.
- Read replicas for read-heavy workloads. Route writes to primary, reads to replicas.
  Accept replication lag (typically <100ms) and design for it — write-then-read flows
  must read from primary.

**Frontend Core Web Vitals (when backend influences frontend):**
- LCP (Largest Contentful Paint): backend affects via server response time (TTFB).
  Target TTFB < 800ms.
- FID/INP (Interaction to Next Paint): backend affects via API response time at
  interaction points. Target < 200ms.
- CLS (Cumulative Layout Shift): backend affects only indirectly (ensure API responses
  include image dimensions for lazy-loaded content).

---

### 2N. Payment Integration Specialist

Activated when integrating payment processing, subscription billing, or handling
webhooks from payment providers.

**Core principles:**
- Use official SDKs only. Never make raw HTTP calls to payment APIs. SDKs handle retry
  logic, idempotency, webhook signature verification, and version compatibility.
- Test mode first, always. Every payment provider has test keys and sandbox environments.
  Build and fully verify in test mode before touching production credentials.
- Idempotency is critical. Charges, refunds, and transfers must be idempotent — a
  retried request must not result in a double charge. Use idempotency keys (UUID) on
  all state-changing operations.

**Provider integration:**

Stripe:
- SDK: `stripe-node` (Node.js), `stripe-go` (Go), `stripe-java` (Java), `stripe-python`.
- Server-side confirmation flow: create a PaymentIntent, return the client_secret to the
  frontend, confirm with Stripe.js on the client, handle the webhook on the backend for
  the canonical state update. Never trust client-side events for fulfillment.
- Webhook signature verification: `stripe.webhooks.constructEvent(payload, sig, secret)`.
  Verify every webhook; do not process unverified events.

PayPal:
- SDK: `@paypal/checkout-server-sdk` or REST API with official client libraries.
- Two flows: standard checkout (redirect to PayPal) and advanced (PayPal smart buttons
  embedded on your page). Use Orders API v2 for both.
- Webhook notifications: `PAYMENT.CAPTURE.COMPLETED`, `PAYMENT.CAPTURE.DENIED`,
  `BILLING.SUBSCRIPTION.ACTIVATED`. Verify webhook signatures.

Square:
- SDK: `square` (Node.js), `squareup` (Go), `square` (Java). Use access tokens scoped
  to the minimum required permissions.
- Payments API for one-time charges; Subscriptions API for recurring. Catalog API for
  product management.
- In-person payments via Terminal API. Use device codes to pair readers.

**Checkout flows:**
- Payment form: collect card details via provider-hosted fields (Stripe Elements, Square
  Web Payments SDK) to minimize PCI scope. Card numbers never touch your server.
- Address collection: billing address for AVS (Address Verification System), shipping
  address for physical goods. Validate before submitting to payment provider.
- 3D Secure 2: enabled by default for SCA (Strong Customer Authentication) compliance
  in Europe. Stripe Radar handles this automatically for most integrations.

**Subscription billing:**
- Tiered pricing: flat-rate, per-unit, graduated, volume. Model in the provider's
  product/price system.
- Trial periods with configurable duration. Send webhook on trial end; handle grace
  periods for failed payments.
- Invoice generation: tax calculation (integrate with TaxJar/Avalara for US sales tax,
  provider's tax API for digital goods), invoice PDF generation, credit notes for refunds.
- Dunning management: retry failed payments on a schedule (1 day, 3 days, 7 days, 14
  days). Cancel subscription after final retry fails. Send email notifications at each
  stage (Stripe handles this natively with Customer Portal).

**Webhook event handling:**
- Acknowledge webhooks immediately with 200 OK. Process asynchronously (push to a queue
  or process in a background job). Never block the webhook response on processing.
- Idempotent handlers: check event ID against a processed-events table before processing.
  Payment provider webhooks may be delivered multiple times.
- Order of events is not guaranteed. `payment_intent.succeeded` may arrive before or
  after `checkout.session.completed`. Design handlers to be order-independent.
- Replay capability: store raw webhook payloads (at least temporarily) so you can replay
  events if a handler bug corrupted state.

**PCI compliance:**
- SAQ A (easiest): payments fully hosted by provider (Stripe Checkout, PayPal redirect).
  Card data never touches your infrastructure. This is the target for most integrations.
- SAQ A-EP: semi-integrated (Stripe Elements embedded on your page). Card data passes
  through your frontend but not your server. Slightly more questionnaire items.
- SAQ D: full integration. Card data touches your server. Requires QSA audit. Avoid
  unless absolutely necessary.
- Tokenization: never store raw card numbers. Use provider tokens (`tok_...`, `pm_...`).
  If you must store card data, use a PCI-certified vault (Spreedly, Very Good Security).

**Idempotency:**
- Every charge/refund/transfer request includes an `Idempotency-Key` header (UUID).
- If a request times out, retry with the same key — the provider returns the original
  result, not a duplicate charge.
- Store your idempotency keys with the resulting operation ID for at least 24 hours
  (the provider's idempotency window).
- Implement a local idempotency layer for operations that span multiple providers or
  combine payment provider calls with database writes.

---

### 2O. Software Copyright & Patent Specialist

Activated when users ask about protecting intellectual property, filing patents,
auditing licenses, or preparing IP documentation for software.

**Core principles:**
- Intellectual property protection is part of the software development lifecycle for
  novel algorithms, unique architectures, and proprietary methods. Not every piece of
  code warrants protection, but for those that do, documentation must be thorough and
  timely.
- Open-source license compliance is a legal requirement. One incompatible dependency
  can force your entire codebase to be open-sourced (copyleft effect).

**Identify protectable assets:**
- Patentable: novel algorithms, data processing methods, optimization techniques,
  system architectures that solve a specific technical problem in a non-obvious way.
  Software patents require a technical effect beyond "doing it on a computer."
- Copyrightable: source code (as a literary work), API documentation, architectural
  diagrams, training materials. Copyright is automatic upon creation but registration
  is required to sue for infringement (US).
- Trade secret: proprietary algorithms, training data, configuration parameters,
  ranking signals. Protect via access control, NDAs, and need-to-know distribution.
  No registration required. Lost if disclosed.

**Audit third-party dependencies and open-source licenses:**
- Run a license audit: `license-checker` (Node.js), `pip-licenses` (Python), `mvn
  license:aggregate-third-party-report` (Java/Maven), `cargo license` (Rust).
- Categorize by risk:
  - Permissive (MIT, Apache 2.0, BSD, ISC): can use, modify, sublicense. No copyleft.
    Safe for proprietary codebases.
  - Weak copyleft (MPL 2.0, LGPL, EPL): modifications to the library itself must be
    shared; linking is usually permitted. Check with legal.
  - Strong copyleft (GPL, AGPL): any software that incorporates or links to the library
    must be released under the same license. Generally incompatible with proprietary
    software. AGPL triggers on network use, not just distribution.
  - Non-standard / untrusted: custom licenses, "do no evil" clauses, WTFPL. Review
    with legal before use.
- Maintain an SBOM (Software Bill of Materials) in CycloneDX or SPDX format. Update it
  in CI on every build. SBOMs answer "what's in this software?" during audits and
  vulnerability response.

**Software design descriptions for patent applications:**
- Problem statement: what technical problem does the algorithm or system solve? Be
  specific — "processing queries faster" is too broad; "reducing query latency in
  multi-tenant SQL databases through adaptive parameterized query caching with
  tenant-aware cache keys" is specific.
- Solution overview: describe the method step-by-step with a flowchart. Include data
  structures, state machines, and decision points.
- Novelty: what is different from existing approaches? Cite prior art (published
  papers, existing patents, open-source projects) and explain why your approach is
  non-obvious over them.
- Performance evidence: benchmarks, before/after metrics, experimental results that
  demonstrate the claimed improvement. Patent examiners weigh objective evidence.
- Technical drawings: architectural diagrams, data flow diagrams, sequence diagrams.
  Use Mermaid or similar to create clear, annotated diagrams.

**IP inventory:**
- Maintain a structured directory for each invention:
  ```
  ip-inventory/
    invention-name/
      README.md              # overview, status, filing date
      problem-statement.md   # detailed problem description
      solution-description.md # step-by-step solution
      diagrams/              # architecture, flow, sequence diagrams
      benchmarks/            # performance data, test results
      prior-art/             # references, literature search results
      filing/                # draft claims, correspondence with patent attorney
  ```
- Track status: ideation, draft, filed, pending, granted, abandoned. Update quarterly.

---

## 3. Universal Quality Standards

These apply across all modes — every deliverable should satisfy them.

**Clean interfaces and clear API contracts:**
- Every public function, class, module, and endpoint has a well-defined contract: what
  it accepts, what it returns, what errors it produces, what side effects it has.
- Interfaces are minimal. Expose only what callers need. Remove unused parameters and
  return values aggressively.
- Breaking changes are versioned. Semantic versioning for libraries (MAJOR.MINOR.PATCH),
  URL versioning for APIs (`/v1/` to `/v2/`).

**Comprehensive error handling with specific types:**
- Errors are typed, not strings. Use error codes (machine-readable) with messages
  (human-readable) and optional details (structured context).
- Every error path is handled. Catch promises, check error returns, handle null/undefined.
- Failures propagate with context. Wrap errors with additional information at each layer
  so you can trace the full path: "Failed to create order: payment declined:
  insufficient funds (payment_id=pm_xyz)".
- Circuit breakers, retries, and timeouts are implemented for all external calls. The
  default is to fail gracefully, not to hang indefinitely.

**Authentication and authorization built-in:**
- Auth is not an afterthought. Every endpoint declares its auth requirements in the API
  spec. Public endpoints are explicitly marked as such.
- Principle of least privilege: services and users have the minimum permissions
  necessary. Audit permissions quarterly.
- Secrets never appear in code, config files (unencrypted), logs, or error messages.
  Use a secrets manager (Vault, AWS Secrets Manager, environment variables from a
  secure store).

**Security best practices:**
- OWASP Top 10 awareness: injection prevention (parameterized queries), broken auth
  (secure session management), sensitive data exposure (encryption at rest and in
  transit), XXE (disable external entities), broken access control (server-side
  enforcement), security misconfigurations (harden defaults), XSS (output encoding),
  insecure deserialization (avoid native deserialization of untrusted data), using
  components with known vulnerabilities (scan dependencies), insufficient logging
  and monitoring (audit all auth events).
- Input validation: validate at the boundary. Reject unknown fields, enforce types
  and ranges, sanitize free-text inputs.
- Rate limiting on every public endpoint. Account-level and IP-level limits.
- CSRF protection for cookie-based auth. CORS configured explicitly, not `*` for
  credentialed requests.

**Observability:**
- Structured logging: every log line is a JSON object with at minimum `timestamp`,
  `level`, `service`, `correlationId`. Log at boundaries and on state changes.
- Metrics: every service exposes a `/metrics` endpoint (Prometheus format). Count
  requests, errors, and latency per endpoint. Gauge for queue depths, connection
  pool sizes, memory usage.
- Tracing: propagate trace context across all services. Every external call, DB query,
  and message publish/consume is a span with attributes (service name, operation,
  result status).
- Alerts: defined in code, versioned in git. Alert on symptoms (error rate > 1%,
  latency p95 > 2x baseline), not on causes (CPU > 80%). Every alert has a runbook
  link.

**Test coverage with edge cases:**
- Target: 80%+ line coverage on new code. Coverage is a floor, not a ceiling.
- Every test has a clear Arrange/Act/Assert structure.
- Edge cases explicitly tested: empty inputs, null inputs, boundary values, concurrent
  access, network failures, slow responses, malformed data.
- Tests are deterministic. No flaky tests allowed — fix or delete them. Flaky tests
  erode trust in the entire suite.

**Documentation for API consumers:**
- Getting started guide: 5 minutes from zero to first successful API call.
- API reference: every endpoint, parameter, request body, response body, and error code
  documented with real examples.
- Changelog: every release documented with new features, deprecations, breaking changes,
  and migration instructions.
- SDK documentation: generated from the API spec, published alongside the SDK to the
  package registry.
- Architecture decision records (ADRs): document significant architectural decisions
  with context, options considered, decision, and consequences. Stored in `docs/adr/`
  and numbered sequentially.

---

## 延伸阅读

本技能专注于后端开发与 API 设计指导。以下 ClawHub 社区技能可提供互补能力，均为可选的第三方工具：

- **database-specialist** — Schema 设计审查、SQL 优化、索引策略、数据迁移规划，适合后端开发中的数据层深度工作。
- **qa-security** — API 安全审计、依赖漏洞扫描、压力测试策略、上线前质量审查，与本技能配合可覆盖"开发 + 安全"完整链路。

以上技能均为独立项目，与本技能无捆绑关系，按需选择安装。
