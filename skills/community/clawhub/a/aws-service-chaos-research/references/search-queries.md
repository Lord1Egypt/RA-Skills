# Search Query Templates

Templates for documentation searches. Replace `{SERVICE}` with the actual AWS service
name (e.g., "Amazon RDS MySQL", "Amazon MSK", "Amazon ElastiCache Redis").

**IMPORTANT**: Execute all queries **one at a time, sequentially**. Do NOT run them in
parallel — the aws-knowledge-mcp-server has rate limits. Wait for each query to complete
before sending the next one.

## FIS-Enriched Path (Service Has Native FIS Actions)

Run **5 sequential searches** when FIS has native actions for the service:

### Query 1: Blogs & Best Practices

```
search_phrase: "{SERVICE} chaos engineering fault injection best practices"
topics: ["general"]
limit: 10
```

**Why**: Finds AWS Architecture Blog, DevOps Blog, Database Blog articles about
chaos testing for this service.

### Query 2: Official Docs & User Guides

```
search_phrase: "{SERVICE} high availability failover testing Multi-AZ"
topics: ["general"]
limit: 10
```

**Why**: Finds service user guide, HA/DR documentation pages.

### Query 3: API & CLI Reference

```
search_phrase: "{SERVICE} resilience testing AWS FIS"
topics: ["reference_documentation"]
limit: 10
```

**Why**: Finds FIS action reference, API reference, CLI reference pages.

### Query 4: Troubleshooting & Failure Modes

```
search_phrase: "{SERVICE} failover failure troubleshooting recovery"
topics: ["troubleshooting"]
limit: 10
```

**Why**: Finds repost.aws knowledge center, troubleshooting guides, known issues.

### Query 5: Well-Architected & Current Awareness

```
search_phrase: "{SERVICE} resilience reliability Well-Architected"
topics: ["general"]
limit: 10
```

**Why**: Finds Well-Architected reliability pillar, new features, Resilience Hub.

---

## Documentation-Only Path (No Native FIS Actions)

Run **6 sequential searches** when the service has no native FIS actions:

### Query 1: HA & Failover

```
search_phrase: "{SERVICE} high availability failover testing"
topics: ["general"]
limit: 10
```

**Why**: Finds HA architecture docs, failover procedures, Multi-AZ guides.

### Query 2: DR & Resilience

```
search_phrase: "{SERVICE} resilience disaster recovery Multi-AZ Multi-Region"
topics: ["general"]
limit: 10
```

**Why**: Finds DR strategy docs, cross-region replication, backup/restore.

### Query 3: Chaos & Fault Injection

```
search_phrase: "{SERVICE} chaos engineering fault injection testing"
topics: ["general"]
limit: 10
```

**Why**: Finds any chaos/FIS blog posts mentioning this service.

### Query 4: Best Practices & Reliability

```
search_phrase: "{SERVICE} best practices reliability availability"
topics: ["general"]
limit: 10
```

**Why**: Finds Well-Architected guidance, service-specific best practices.

### Query 5: Troubleshooting & Failure Modes

```
search_phrase: "{SERVICE} failure troubleshooting recovery error"
topics: ["troubleshooting"]
limit: 10
```

**Why**: Finds repost.aws knowledge center, known failure modes, recovery steps.

### Query 6: API & Configuration Reference

```
search_phrase: "{SERVICE} reboot failover replication configuration API"
topics: ["reference_documentation"]
limit: 10
```

**Why**: Finds API actions that can trigger failover/reboot, config parameters.

---

## Page Reading Priority

After searches complete, read the **top 3-5 most relevant pages** using
`aws___read_documentation` with `max_length: 8000`. Read pages **sequentially**
(one at a time).

### FIS-Enriched Path Priority:

1. **Service-specific chaos engineering / FIS blog post**
2. **Official HA / failover documentation page**
3. **Well-Architected guidance for this service**
4. **Troubleshooting / known failure mode pages**

### Documentation-Only Path Priority:

1. **Service HA/resilience overview page** — architecture, failure domains
2. **Failover/recovery documentation** — how the service handles failures
3. **Best practices page** — official recommendations for reliability
4. **Troubleshooting guide** — known failure modes and recovery procedures
5. **Any chaos/FIS blog post** mentioning this service

### Additional Discovery

After reading a key page, call `aws___recommend` on the most relevant page found to
discover related content that keyword search may miss (especially "New" and "Similar"
recommendations).

## FIS Scenario Library Pages (Always Fetch)

These pages are **always** fetched in Step 2 regardless of which path is taken:

```
Required reads:
  url: "https://docs.aws.amazon.com/fis/latest/userguide/scenario-library.html"
  max_length: 10000

  url: "https://docs.aws.amazon.com/fis/latest/userguide/scenario-library-scenarios.html"
  max_length: 10000
```

Detailed scenario pages (fetch based on relevance to target service):

| Scenario | URL |
|---|---|
| AZ Power Interruption | `https://docs.aws.amazon.com/fis/latest/userguide/az-availability-scenario.html` |
| AZ Application Slowdown | `https://docs.aws.amazon.com/fis/latest/userguide/az-application-slowdown-scenario.html` |
| Cross-AZ Traffic Slowdown | `https://docs.aws.amazon.com/fis/latest/userguide/cross-az-traffic-slowdown-scenario.html` |
| Cross-Region Connectivity | `https://docs.aws.amazon.com/fis/latest/userguide/cross-region-scenario.html` |

Supplementary pages (fetch if needed):

| Page | URL |
|---|---|
| FIS Actions Reference | `https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html` |
| FIS Document History | `https://docs.aws.amazon.com/fis/latest/userguide/doc-history.html` |

## Rate Limit Protection

If any MCP request returns a "Too many requests" error or any other transient error,
**retry up to 10 times** with a 5-second wait between retries. Only skip the request
and continue with the next one after all 10 retries have failed.
