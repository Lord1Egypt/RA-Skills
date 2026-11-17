## Description:

Search Google or Bing with easyserp, keep source links, and recover pending requests. Use for structured web search, repeatable queries, or domain-scoped results; use easybrSearch or another browser research workflow for broader cross-site/media discovery and page reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers can use this skill to run repeatable Google or Bing searches, including domain-scoped queries, and give agents structured results with source links. It also helps recover the status of searches that are still pending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rated this release suspicious with medium confidence because its MCP setup uses an unpinned package; some artifact behavior was only partially inspected.

Mitigation: Before installing, consider whether you trust the package source and verify and pin the exact version used by the MCP integration. Some behavior remains unassessed.

## Reference(s):

- [API and recovery reference](references/api-and-recovery.md)
- [Integration and installation guide](references/integrations.md)
- [Service console](https://serp.skyvora.cc)
- [ClawHub release page](https://clawhub.ai/xxjrq/skills/easyserp)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured Google or Bing search results with source links, returned as JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are candidates and do not establish that linked pages were opened or verified; pending requests retain recovery identifiers.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
