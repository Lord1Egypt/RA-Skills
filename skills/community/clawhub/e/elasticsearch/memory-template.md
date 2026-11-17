# Memory Template — Elasticsearch

Create `~/Clawic/data/elasticsearch/memory.md` with this structure:

```markdown
# Elasticsearch Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Cluster
<!-- Nodes and roles, version, deployment, license tier, tiers in use -->

## Workload
<!-- Entity search, logs, metrics, vector, or mixed -->
<!-- Index and alias naming already in use, ILM policies, data streams -->

## Pain Points
<!-- Incidents hit, recurring errors, mappings known to be wrong -->

## Preferences
<!-- Review gates before destructive or structural changes -->
<!-- Explanation depth: request bodies only vs full walkthrough -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their cluster and workload |
| `complete` | Know their setup well enough to skip discovery |
