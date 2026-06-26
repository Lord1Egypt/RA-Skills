---
name: edge-computing
description: Deep edge computing workflow—what runs at edge vs origin, caching, KV and data locality, security, limits, and latency validation. Use when deploying to CDN/edge workers (Cloudflare Workers, Lambda@Edge, Vercel Edge, etc.).
---

# Edge Computing

Edge runtimes move logic closer to users—with **strict CPU/time limits**, **different APIs** than full Node, and **tenant isolation** requirements.

## When to Offer This Workflow

**Trigger conditions:**

- Auth, redirects, or personalization at the CDN layer
- HTML rewriting, A/B assignment, or bot mitigation at the edge
- Global latency SLOs for read-heavy paths

**Initial offer:**

Use **six stages**: (1) workload fit, (2) edge vs origin split, (3) data & state, (4) security & tenancy, (5) limits & cost, (6) testing & rollout). Confirm platform (Workers, Lambda@Edge, Fastly Compute, etc.).

---

## Stage 1: Workload Fit

**Goal:** Prefer short, CPU-light, request-scoped work—not long jobs or huge body buffering.

**Exit condition:** Explicit list of what remains on origin (heavy SSR, large uploads).

---

## Stage 2: Edge vs Origin Split

**Goal:** Document what runs where: geo headers, redirects, cache key logic, A/B bucketing, partial HTML injection.

### Practices

- Cache `Vary` and cookie behavior documented to avoid wrong personalization leakage

---

## Stage 3: Data & State

**Goal:** If using edge KV/Durable Objects/regional stores, state consistency (eventual vs strong) and rate of round-trips to origin.

---

## Stage 4: Security & Tenancy

**Goal:** Validate JWT/session at edge; isolate tenants; never embed secrets in deploy bundles visible to clients.

---

## Stage 5: Limits & Cost

**Goal:** Wall-clock CPU limits, request size caps, egress pricing; graceful degradation or fallback to origin.

---

## Stage 6: Testing & Rollout

**Goal:** Canary per region/PoP; synthetics from multiple locations; compare p95 vs origin-only path.

---

## Final Review Checklist

- [ ] Workload fits edge constraints
- [ ] Edge vs origin responsibilities documented
- [ ] State/consistency strategy clear
- [ ] Multi-tenant security reviewed
- [ ] Limits, cost, fallback documented
- [ ] Multi-region validation performed

## Tips for Effective Guidance

- Edge runtimes differ from full Node—verify available APIs (fs, streams, crypto).
- Read platform-specific cold-start and isolate model docs.

## Handling Deviations

- Hybrid: edge for headers/cache only; heavy compute stays on origin.
