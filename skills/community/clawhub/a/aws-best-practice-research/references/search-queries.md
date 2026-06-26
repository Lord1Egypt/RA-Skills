# Search Query Templates

Templates for the 5 sequential documentation searches. Replace `{SERVICE}` with the
actual AWS service name (e.g., "ElastiCache Redis", "Amazon RDS MySQL", "Amazon MSK").

**IMPORTANT**: Execute all queries **one at a time, sequentially**. Do NOT run them in
parallel — the aws-knowledge-mcp-server has rate limits. Wait for each query to complete
before sending the next one.

## Query 1: Official Best Practices + HA/DR

```
search_phrase: "{SERVICE} best practices high availability disaster recovery"
topics: ["general"]
limit: 10
```

**Why**: Finds the service's own best-practice documentation, resilience pages,
and HA/DR configuration guides.

## Query 2: Well-Architected Lens

```
search_phrase: "{SERVICE} Well-Architected reliability resilience best practices"
topics: ["general"]
limit: 10
```

**Why**: Finds the service-specific Well-Architected Lens (if one exists), which is
the single most comprehensive source of best practices organized by pillar.

## Query 3: Replication / Failover / Backup Details

```
search_phrase: "{SERVICE} replication multi-AZ failover cluster mode backup"
topics: ["reference_documentation", "troubleshooting"]
limit: 10
```

**Why**: Finds detailed configuration documentation for HA mechanisms, including
replication setup, failover behavior, backup/restore procedures.

## Query 4: Security Configuration

```
search_phrase: "{SERVICE} security encryption authentication access control"
topics: ["general"]
limit: 10
```

**Why**: Finds encryption (at-rest, in-transit), authentication mechanisms (IAM, RBAC,
native auth), network security (VPC, security groups, subnet groups), and compliance info.

## Query 5: Well-Architected Security

```
search_phrase: "{SERVICE} Well-Architected security best practices"
topics: ["general"]
limit: 10
```

**Why**: Finds security-specific Well-Architected recommendations, supplementing
Query 4 with framework-level security pillar guidance.

---

## Page Reading Priority

After the 5 searches complete, identify and read key pages in this priority order:

1. **Well-Architected Lens pages** (Reliability, Security, PE, OE pillars) — highest value
2. **Official best practices page** — service-native recommendations
3. **Resilience / disaster recovery page** — specific HA/DR mechanics
4. **Replication / configuration reference** — detailed setup parameters

Read up to 5 pages **sequentially** (one at a time) with `max_length: 15000` each.
Wait for each page read to complete before starting the next one.

## Additional Searches (if initial results are thin)

For services with less documentation, run additional targeted searches:

```
Extra 1: "{SERVICE} monitoring CloudWatch metrics alerts"
  topics: ["reference_documentation"]

Extra 2: "{SERVICE} scaling auto scaling capacity planning"
  topics: ["general", "reference_documentation"]

Extra 3: "{SERVICE} maintenance upgrade patching version"
  topics: ["reference_documentation"]
```
