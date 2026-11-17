# AIXBT crypto research

Reviewed 2026-09-05 against the [official MCP guide](https://docs.aixbt.tech/developers/mcp), [API v3 overview](https://docs.aixbt.tech/developers/v3) and [current OpenAPI contract](https://api.aixbt.tech/v3/openapi.yaml). Use this reference for narrative discovery and project events; use other providers for missing price, liquidity or protocol state with explicit attribution.

## Access

| Surface | Address | Credential carrier |
| --- | --- | --- |
| Native Streamable HTTP MCP | `https://api.aixbt.tech/mcp` | `Authorization: Bearer` with the user's API key for unattended clients; interactive clients can complete OAuth |
| REST API v3 | `https://api.aixbt.tech/v3` | `x-api-key` header for protected reads |

The current Topic list and detail are public. Other resources require access; a public Topic read does not verify paid entitlement. MCP initialization and `tools/list` work without signing in. Review the discovered schemas and expose only task-relevant research reads; never derive an allowlist from this document alone. In Hermes use native `mcp_servers` remote configuration, the selected profile's secret environment and its supported header expansion. Confirm variable resolution without showing the key. Do not embed credentials in skills, generated artifacts, URLs or shell arguments, or add a proxy merely to translate native HTTP.

REST uses `{data, meta}` envelopes and cursor pagination through `meta.nextCursor`; stop at the task's result/page budget. `GET /v3/me` describes entitlement and history limits: inspect only when authorized and keep credential/account fields out of reports. HTTP 401/403 requires resolving access; 429 requires bounded backoff. A payment-required response grants no authority to pay, sign or enable another provider.

## Research sequence

1. State the subject and period; for an unspecified recent update use the past 24 hours. Resolve crypto projects using exact identities. Filter to the crypto universe when supported; do not substitute an identically named stock or company.
2. For broad narratives, inspect current Topics, then search Intel with the user's constraints. For a named asset, resolve its Project and recent Intel. Use vocabulary to validate chain/category filters, and Project IDs for deeper reads. A project's leaderboard presence must not decide whether to search its Intel.
3. Follow relevant Topic reports for synthesis and Intel for underlying events. Bound depth and pagination to the question. Do not mistake a current Topic board for complete historical coverage.
4. Inspect supporting links and corrections. Verify material unsupported claims with the relevant protocol, issuer or chain source. Several posts repeating one announcement are one underlying source. Report contradictions and omissions; an official-source flag is a lead, not proof of the economic claim.
5. For missing market metrics, resolve the returned identifiers into the appropriate data provider. Preserve the separate source, units and timestamp. Never invent a price, yield or contract address from narrative sentiment.

These procedures are informed by the [official research workflow](https://docs.aixbt.tech/developers/skill); this pack does not redistribute that skill or require it as a dependency.

## Interpretation and output

The provider's research workflow describes `trend` as a 0–100 forecast score, not raw mentions or an investment return. The v3 contract limits comparability to the same `meta.versions.trendModel`; `trendDelta.value` is the score-point change over its window, not a percentage. Missing history means an unknown delta. Prefer explaining concrete changes over displaying scores or leaderboard ranks as investment quality.

Keep retrieval time separate from `detectedAt`, `reinforcedAt` and report publication/revision times. The current contract defines `activity.eventTime` as claimed event time. Deprecated `activity.occurredAt` is a publication/detection timestamp: do not label it when the event happened. A recently reinforced old event is not necessarily new news. A detection timestamp is not the event time. One uncited observation, or a project-tagged item whose canonical chain is metadata rather than event location, is a lead that needs a primary dated source before it supports a catalyst thesis. Two differently worded searches that return nothing do not prove a claim false; they bound coverage.

Lead with what changed and why the evidence supports it. Link primary sources where available, distinguish inference from observations, and state stale, thin or permission-limited coverage. A shortlist remains research; it does not authorize allocation, execution, alert creation or ongoing monitoring. The API also advertises alert writes; this read-only workflow does not enable them. A successful connection proves neither protected research reads nor complete market coverage.
