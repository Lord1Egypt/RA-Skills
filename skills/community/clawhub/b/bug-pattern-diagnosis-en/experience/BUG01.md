# BUG01: Intermittent Multi-Replica NPE — Stateful Business × Stateless Deployment × Dropped Identity Context

## Case Summary

A client sends a request with a valid token to an endpoint. Repeated requests succeed **roughly 50% of the time** and fail the rest with `errorCode: 10001, "service exception"`. The server runs multiple k8s replicas (Deployment + round-robin Service). The failing replica's logs contain a full NPE stack caused by `ChainContextHolder.getTokenPayload()` returning null, while the "entry replica" for the same request only has a one-line business error (no stack).

The root cause is the intersection of three layers:

1. **Application-layer stateful routing** (partition ownership)
2. **k8s stateless round-robin distribution**
3. **Internal forwarding protocol dropping the `x-token-payload` header**

**No single-layer fix can fully resolve this**, but fixing the protocol layer alone is sufficient.

---

## Symptom / Signature Checklist (for matching)

> When **4+** of these features are present, this case is a high-probability match. **2-3** features is still worth prioritizing this direction for investigation.

### Client-Side Phenomena

- [ ] Same token, same body, fired N times — success rate is **approximately `1/replicaCount`** or `(N-1)/N` (≈ 50% with 2 replicas)
- [ ] Failures return a business error code (e.g. 10001 / INTERNAL_SERVER_ERROR / "service exception") — not 401/403/timeout
- [ ] Single-replica local environment has **100% success** — cannot reproduce locally
- [ ] The error **looks like a token problem** ("unauthenticated / identity missing / user not found"), yet the client clearly sent a valid token

### Server-Side Log Features (MOST diagnostic!)

- [ ] A single client request leaves traces on **multiple replicas** in their logs (it should normally appear on just one)
- [ ] The different replicas' logs are **asymmetric in verbosity**:
  - Replica A: `ERROR` + full exception stack (NPE / ClassCastException / IllegalState against some low-level code)
  - Replica B: `ERROR` or `WARN` + a one-line short business error code, **no stack**
- [ ] On the replica that has a stack, the NPE points to code that **dereferences ThreadLocal / MDC / a context store** (e.g. `ChainContextHolder.getXxx()`, `RequestContextHolder.getXxx()`, `MDC.get()`)
- [ ] On the replica without a stack, the log looks like `response XXXX,XXX` (from RestTemplate/Feign handling an internal HTTP response)

### Deployment / Architecture Features

- [ ] Target service is a **k8s Deployment** with multiple replicas (not StatefulSet)
- [ ] The service uses **Kafka Consumer Groups** / **application-layer partition routing** / **in-memory cache with partition ownership**
- [ ] The code has `RestTemplate.exchange` / `Feign` calls that send HTTP **to this service's other pod IPs**
- [ ] There's some kind of "yellow pages table" (DB or Redis recording `partition → ip:port`)

### Code Features

- [ ] The receiver controller **directly dereferences** ThreadLocal/context (e.g. `ChainContextHolder.getTokenPayload().getAccount()`) without null-safety
- [ ] A "feign_token" / "system_token" literal placeholder exists for internal calls (e.g. `Authorization: Bearer feign_token`)
- [ ] Internal forwarding only sends `Authorization`, **missing** `x-token-payload` / `x-user-context` / `x-trace-id` etc.

### Key Log Fingerprints (directly greppable)

```text
# Replica A (receiver) — typical log
ERROR ... GlobalExceptionHandler - found system exception,null/<endpoint-path>
java.lang.NullPointerException: Cannot invoke "XxxPayload.getXxx()" because
    the return value of "XxxContextHolder.getPayload()" is null
    at <Controller>.<method>(<Controller>.java:NNN)

# Replica B (forwarder) — typical log
ERROR ... <Service> - <methodName> response <errorCode>,<errorMessage>
(that's it — no "at xxx.xxx" stack frames after it)
```

### Exclusion Criteria (Negative Signals)

- **100% failure on a single replica** → NOT this case; it's a plain code bug
- **All replicas show full stacks** → NOT this case; no cross-replica chain
- **Token actually expired** (logs contain `token expired` / `invalid signature`) → NOT this case
- **Failures concentrate within minutes of scale events / deploys** → Possibly Kafka rebalance transient issue, not this case

---

## Detailed Explanation / Root Cause Chain

### The Three-Layer Decomposition

| Layer | What it is | Is it a bug on its own? |
|---|---|---|
| **Code layer** | Some business endpoint's service has partition routing logic: `MonitorCacheMgr.send(tbCode)` hashes `tbCode` to find the partition owner pod; non-owners forward over internal HTTP to the owner | Not a bug (legitimate design for stateful business) |
| **Deployment layer** | k8s Deployment with 2+ replicas; Service uses round-robin to distribute external traffic. Replicas have 50/50 hit rate regardless of business routing | Not a bug (standard k8s usage) |
| **Protocol layer** | Internal forwarding only carries `Authorization: Bearer feign_token` (literal placeholder); **does not carry `x-token-payload`**. Receiver's `AuthInterceptor` only honors `x-token-payload`; if missing, `ChainContextHolder.TokenPayload = null` | **This is the actual bug** |

### Request "Fission" Flow

The client sees 1 request; the server actually processes 2 HTTP calls:

```text
Client ──► Request #1 ──► k8s Service (round-robin)
                            │
                 50%        │         50%
            ┌───────────────┴───────────────┐
            ▼                               ▼
       Pod A (owner of tbCode)        Pod B (NOT owner)
       ──────────────────              ──────────────────
       1. AuthInterceptor              1. AuthInterceptor
          parses x-token-payload ✓       parses x-token-payload ✓
       2. Controller reads account ✓   2. Controller reads account ✓
       3. send() — I am the owner      3. send() — owner is Pod A
          → local call()                  → initiates Request #2 to Pod A
       4. business logic executes          │
       5. Returns ApiResponse(0) ✅        │ ❌ drops x-token-payload
                                           ▼
                                      Pod A as receiver:
                                      5. AuthInterceptor can't find
                                         x-token-payload
                                         → ChainContextHolder = null
                                      6. Controller dereferences .getAccount()
                                         💥 NPE
                                      7. GlobalExceptionHandler catches
                                         → logs full NPE stack (log ①)
                                         → returns ApiResponse(10001)
                                           ▲
                                           │ HTTP 200 + body{errorCode:10001}
                                           │
                                      Pod B receives response:
                                      8. errorCode != 0
                                         log.error("...response 10001,service exception")
                                         (log ②, one line, no stack)
                                      9. throw ServiceException
                                         → returns ApiResponse(10001) to client
```

### Why the Failure Is Intermittent

k8s Service round-robin picks the target replica for each request independently of token content:

- Lucky — hits the owner directly → no forwarding → 100% success
- Unlucky — hits a non-owner → forwarding triggered → dropped header → NPE → failure

### Why the Logs Are Asymmetric

Spring's `GlobalExceptionHandler` categorizes exceptions into two classes:

| Exception type | Semantics | Log level | Stack printed |
|---|---|---|---|
| `SystemException` / uncaught `Throwable` | Unexpected system error (NPE, SQL fault, etc.) | `ERROR` | ✅ Full stack |
| `ServiceException` / business exception | Business rule violation (expected error) | `WARN` or `ERROR` | ❌ No stack |

- **Pod A** (receiver): Actual NPE → SystemException path → **stack present**
- **Pod B** (forwarder): Just wraps `errorCode` into `ServiceException` → business exception path → **no stack**

### Why "Login Is Stateless" Doesn't Save You

The common confusion:

- **Auth layer (JWT token) is indeed stateless** — every pod can independently decode the token
- **Business layer is heavily stateful** — because:
  1. Kafka Consumer Group protocol: one partition can only be consumed by one consumer in the group → pods bind tightly to partitions
  2. High-frequency device data must aggregate in memory (thousands per second, Redis can't absorb it)
  3. Aggregate data lives only in the pod consuming that partition → queries must route to the owner

So the project has to hand-roll application-layer routing (partition yellow pages + pod-to-pod HTTP forwarding) on top of stateless k8s deployment — and this forwarding protocol is exactly where bugs breed.

---

## Diagnostic Methodology

### Core Techniques Used

| Technique | Purpose | When to use |
|---|---|---|
| **Quantified reproduction** | Fire 100 requests in a row, tally the success rate; confirm deterministic vs intermittent | Required first step |
| **Replica-count comparison** | Match success rate against `1/N`; directly points at inter-replica inconsistency | Immediately when intermittency is observed |
| **Cross-replica log correlation** | Pull logs from all replicas by traceId / time window, view **side by side** | When internal call chains are suspected |
| **Source vs deployed-binary diff** | `javap -c -p` the deployed jar, diff against local source | When wrong-version deployment is suspected |
| **Context-propagation lifecycle diagram** | Mark every cross-thread/process/instance boundary and audit each for compensation | When context loss is suspected |
| **Header packet capture** | `tcpdump` / print `getHeaderNames()` at the receiver | When header transfer is suspected |
| **Sibling code comparison** | Find 5-10 similar implementations in the project; diff the bug vs the healthy ones | When multiple similar implementations exist |

### Diagnostic Steps (in order)

#### 1. Quantify the Symptom (10 min)

```bash
# Fire 100 identical requests (replace URL, token, body)
for i in $(seq 1 100); do
  curl -s -X POST "$URL" -H "Authorization: $TOKEN" -d "$BODY" \
    | jq -r '.errorCode' | head -1
done | sort | uniq -c
```

Read the success rate:
- 100% / 0% → NOT this case; take a different path
- **≈ 50% (2 replicas) / ≈ 33% (3 replicas) / ... → strong signal of this case**

#### 2. Confirm Replica Topology (5 min)

```bash
kubectl get deploy <service-name> -o json | jq '.spec.replicas'
kubectl get pods -l app=<service-name>
```

- replicaCount > 1 with ordinary ClusterIP/LoadBalancer Service → "multi-replica round-robin" condition satisfied

#### 3. Cross-Replica Log Correlation (30 min)

```bash
# Tail every replica in parallel, prefix each line with the pod name
for pod in $(kubectl get pods -l app=<service> -o name); do
  kubectl logs -f "$pod" --tail=100 | sed "s/^/[$pod] /" &
done
wait
```

Fire one failing request and observe:
- Does the log appear **simultaneously** on multiple replicas?
- Is **verbosity asymmetric** between replicas?

Both present → strongly consistent with this case type.

#### 4. Localize the Code (30 min)

- Find the file/line pointed to by the NPE stack in the "has-stack" replica
- Find the `log.error("...response XXX,XXX")` call site in the "no-stack" replica
- Inspect the `restTemplate.exchange` / `Feign` method surrounding that logging
- Check the URL — is it in the form `http://<dynamic-ip>:<port>/...` (pod-to-pod direct)?
- Inspect the Headers — missing `x-token-payload` / `x-user-context`?

#### 5. Confirm Protocol Mismatch (15 min)

- Capture the full header list of a request as it passes through the Gateway
- Capture the headers added during internal forwarding
- Diff the two and identify what's missing
- Trace the receiver's `AuthInterceptor` / `@PreAuthorize` / context-parsing code to confirm which headers it depends on

**The difference set is exactly the header list to fix.**

---

## Remediation Plan

### Root-Cause Fix (P0, required)

**Propagate identity context headers in the outbound internal HTTP call.** Reference implementation:

```java
private Integer invokeRemoteDeviceOpt(JsonNode node, NodePartition nodePartition, RestTemplate restTemplate) {
    String newUrl = String.format("http://%s:%s/rest/v1/access/device/product/services",
            nodePartition.getIp(), nodePartition.getPort());
    HttpHeaders headers = new HttpHeaders();
    headers.add("Authorization", RequestHeaderConstant.HTTP_FEIGN_TOKEN_BEARER.getValue());
    headers.add("Content-Type", "application/json");
    headers.add("Accept", "application/json");

    // Core fix: propagate the identity context
    TokenPayload tokenPayload = ChainContextHolder.getTokenPayload();
    if (tokenPayload != null) {
        TokenContext tokenContext = TokenContext.builder().payload(tokenPayload).build();
        headers.add(RequestHeaderConstant.HTTP_TOKEN_PAYLOAD_HEADER.getValue(),
                JSONUtil.INSTANCE.toJson(tokenContext));
    } else {
        log.warn("invokeRemoteDeviceOpt missing TokenPayload, forward to {} without x-token-payload", newUrl);
    }
    ChainContext ctx = ChainContextHolder.get();
    if (ctx != null) {
        if (StringUtils.isNotBlank(ctx.getRemoteIp())) {
            headers.add(RequestHeaderConstant.HTTP_REMOTE_IP_HEADER.getValue(), ctx.getRemoteIp());
        }
        if (StringUtils.isNotBlank(ctx.getLocale())) {
            headers.add(RequestHeaderConstant.HTTP_LANGUAGE.getValue(), ctx.getLocale());
        }
    }
    // ... subsequent restTemplate.exchange remains unchanged
}
```

**Key**: Serialization must match the Gateway entry point exactly (e.g. both use `JSONUtil.INSTANCE.toJson(TokenContext)`), otherwise the receiver's deserialization will fail.

### Safety Net (P1, recommended)

**Make receiver-side ThreadLocal dereferences null-safe:**

```java
@PostMapping(value = "/rest/v1/access/device/product/services")
public ApiResponse<Integer> innerDeviceOptRequest(@RequestBody JsonNode jsonNode) {
    String tbCode = ChainContextHolder.getTbCode();
    TokenPayload payload = ChainContextHolder.getTokenPayload();
    String account = payload != null ? payload.getAccount() : null;
    String tid = payload != null ? payload.getTid() : null;
    // ...
}
```

Defensive value: if a future caller also forgets to propagate headers, the process won't crash — it will merely degrade to `account=null`.

### Hardening (P2, long-term)

- **Extract a common utility** `forwardHeadersBuilder()` to unify the "internal HTTP forwarding" header assembly so nobody forgets again
- **Remove dead code**: scan for "intended to handle internal calls but with broken logic" (e.g. `url.startsWith("/inner/") && url.equals("feign_token")` — always false)
- **Separate URL namespace**: long-term, route external APIs and internal forwards to **different URL prefixes**; let the receiver pull identity from the body explicitly rather than relying on headers. Existing `/inner/rest/...` pattern is a good reference

---

## Prevention Checklist

### When writing "outbound HTTP calls"

- [ ] Does this call **cross a network boundary**? (Even pod-to-pod within the same service counts)
- [ ] Does the receiver depend on `ThreadLocal` / `MDC` / context storage?
- [ ] Did I explicitly propagate identity headers (`x-token-payload` / `x-user-context`), traceId, MDC?
- [ ] Is the header set **identical** to what's injected at the service entry point (Gateway / AuthFilter)?
- [ ] When context is null, is the degradation strategy clear (log.warn + continue vs throw)?

### When writing "inbound Controllers"

- [ ] Which callers will hit this endpoint? External? Other services? My own pods?
- [ ] Can every caller guarantee to supply the headers I depend on?
- [ ] Before dereferencing `ContextHolder.getXxx().getYyy()`, is the worst case NPE-safe?
- [ ] Better yet, should I use **explicit parameters** + `@Validated` and avoid ThreadLocal dependencies entirely?

### When reviewing stateful services

- [ ] Does the app have hidden state (session / partition ownership / in-memory cache)?
- [ ] Is it deployed as Deployment or StatefulSet? Does it match the business semantics?
- [ ] Does internal routing fully propagate all required context?
- [ ] In a **multi-replica environment**, can the same business key produce 100 repeated requests to test for failure?

### Deployment stage

- [ ] Is the source version ↔ deployed version verifiable? (image tag, git commit hash)
- [ ] During gray releases, does a canary pod run first?
- [ ] For stateful service upgrades, has cross-version internal-call compatibility been tested?

---

## Playbook for Similar Intermittent Bugs

When you hear vague reports like "occasional NPE / occasional 500 / occasional 403", walk through:

### Step 1: Quantify the Reproduction (10 min)

Fire N requests and compute the success rate:
- 100% / 0% → skip to Step 5 (deterministic bug path)
- Any other ratio → continue

### Step 2: Check Replica Count (5 min)

`kubectl get deploy` — how many replicas?
- Success rate ≈ `1/N` or `(N-1)/N`? → inter-replica inconsistency
- Can a single replica reproduce it? If not → **strongly indicates this case type**

### Step 3: Cross-Replica Log Correlation (30 min)

- Fire one failing request while tailing logs from all replicas
- Look for "same request leaves traces on multiple replicas + asymmetric verbosity"
- Identify the code locations for both "replica with stack" and "replica without stack"

### Step 4: Source vs Deployed Diff (15 min)

- Pull the jar from a live pod and decompile the critical classes
- Diff against local source
- Any difference is a major lead (suspect wrong-version deployment first)

### Step 5: Draw the Context Propagation Chain (30 min)

- Mark every cross-thread / cross-process / cross-instance boundary
- Check every boundary for an explicit pack → unpack mechanism
- Validate with packet capture or header-printing at the receiver

### Step 6: Sibling Code Comparison (15 min)

- Find 5-10 code sites doing similar things
- Diff the buggy code vs the healthy ones

### Step 7: Minimal Reproduction + Test Fixation (1 hour)

- Build a "minimum replica count + minimum precondition" repro case
- **Turn it into an integration test** to prevent regression

---

## References

### Relevant File Paths (project: cuavcloudservice)

- Root-cause fix site: `CuavCloudApplyService/CuavCloudService/.../application/device/DeviceService.java` (`invokeRemoteDeviceOpt`)
- NPE crash site: `CuavCloudApplyService/CuavCloudService/.../api/device/DeviceAccessController.java:313`
- Context definitions: `cuavcloudcbb/.../context/ChainContextHolder.java`, `ChainContext.java`
- Header constants: `cuavcloudcbb/.../constant/RequestHeaderConstant.java`
- Gateway injection points: `cuavcloudservice/.../gateway/filter/AuthorizationFilter.java` (lines 133/274/338/345)
- Receiver parsing: `cuavcloudcbb/.../authentication/application/interceptor/AuthInterceptor.java`
- Partition routing: `CuavCloudService/.../domain/cache/MonitorCacheMgr.java` (`send`), `domain/merchmant/NodePartitionMgr.java`
- Partition mapping store: `t_kafka_partition` (DB) + `access.partition.cache.v4.{id}` (Redis)

### Key Concepts

- JWT stateless authentication
- Kafka Consumer Group partition assignment
- k8s Deployment vs StatefulSet
- ThreadLocal lost across network boundaries
- Asymmetric `GlobalExceptionHandler` treatment of SystemException vs ServiceException

### One-Liner Summary

> **When k8s's stateless deployment philosophy clashes with application-layer stateful business logic, internal pod-to-pod HTTP forwarding drops `x-token-payload`, and replica round-robin turns the bug into Schrödinger's cat. The two pods each hold half the evidence (stack on the receiver, business error on the forwarder); only cross-pod log correlation reveals the full chain.**
