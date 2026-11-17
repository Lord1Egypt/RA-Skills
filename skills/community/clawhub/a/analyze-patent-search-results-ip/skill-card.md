## Description:

Analyze validated patent-search artifacts at Stage 2/4 of a patent-landscape program to produce population-bounded trends, organization and technology distributions, competitor profiles, a branch-organized reviewed core patent index, transparent candidate-level value proxies, chart-ready data, and a self-contained statistical snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, and IP research teams use this skill after a validated patent search to turn Stage 1 search scope and candidate records into bounded statistical artifacts, reviewed core indexes, value proxy data, chart-ready aggregates, and a statistical HTML snapshot for downstream tagging and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stage 1 search files and generated patent-analysis artifacts may contain confidential project scope, portfolio, or strategy information.

Mitigation: Confirm PatSnap connector access and project confidentiality boundaries before use, and keep generated JSON, CSV, and HTML artifacts inside the authorized workspace.

Risk: Incomplete, capped, sampled, or semantically ambiguous connector data can make population statistics or organization rankings misleading.

Mitigation: Require documented population, date basis, family/unit definition, cutoff, count/cap state, and limitations in each output before treating results as decision evidence.

Risk: Patent status, citation, family breadth, and screening signals can be mistaken for legal conclusions, patent value, or product-roadmap certainty.

Mitigation: Label these fields as dated proxies or database signals, preserve null and uncertainty states, and route legal, valuation, or transaction conclusions to qualified review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/analyze-patent-search-results-ip)
- [PatSnap Skill Hub](https://open.patsnap.com/marketplace/skill-hub)
- [PatSnap MCP servers marketplace](https://open.patsnap.com/marketplace/mcp-servers)
- [Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Deep Patent Mining MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [Global Core Patent Database MCP](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, CSV, HTML, Guidance]

**Output Format:** [Structured JSON and CSV artifacts, a self-contained HTML statistical snapshot, and concise Markdown-style status and next-step guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves query version, connector operation, request, cutoff, population limits, family/unit definitions, proxy states, and limitations where available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
