## Description:

Trending/new/changed MCP servers and live x402 services via a freshness-ranked, liveness-probed index with an x402-paid change-data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foomworks](https://clawhub.ai/user/foomworks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Fresh Feeds to find, rank, and verify MCP servers and discover live x402-payable services without crawling raw registries manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 endpoints can spend funds when a wallet or x402 handler retries payment-required requests.

Mitigation: Use free preview and health endpoints first, and configure strict per-call and session wallet limits before enabling paid requests.

Risk: Registry quality scores and liveness probes are point-in-time service signals, not guarantees that a listed MCP server or x402 service remains safe or available.

Mitigation: Verify a server or service immediately before relying on it, and review returned trust signals before deployment.

## Reference(s):

- [Fresh Feeds service](https://fresh-feeds.foomworks.workers.dev)
- [Fresh Feeds MCP endpoint](https://fresh-feeds.foomworks.workers.dev/mcp)
- [ClawHub skill page](https://clawhub.ai/foomworks/skills/fresh-feeds)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint URLs and inline curl commands; service responses are machine-readable JSON except for the SVG badge endpoint.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some full-data endpoints are x402-paid; preview, health, and ETag checks support lower-cost discovery.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
