## Description:

Connect agents to Apple Health exports with MCP setup, schema validation, and privacy-safe analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect exported Apple Health CSV data to an MCP-compatible agent, validate available schemas, run bounded health-data queries, and preserve privacy and freshness caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Apple Health exports, MCP outputs, memory files, and query logs may expose private health information if shared or broadly accessible.

Mitigation: Keep exports and generated logs local with restricted filesystem access, avoid exposing raw rows unless explicitly requested, and treat files under ~/apple-health/ as sensitive.

Risk: The workflow can run mutable third-party MCP package code against sensitive health exports.

Mitigation: Prefer a pinned and reviewed @neiltron/apple-health-mcp package version, avoid automatic npx -y execution where possible, and restrict HEALTH_DATA_DIR to the intended export directory.

Risk: Stale Apple Health exports can produce misleading current-day or latest-trend summaries.

Mitigation: Record export freshness, disclose the date window used, and request a new export before claiming latest or current-day trends.

## Reference(s):

- [ClawHub Apple Health skill page](https://clawhub.ai/ivangdavila/skills/apple-health)
- [Apple Health skill homepage](https://clawic.com/skills/apple-health)
- [Apple Health MCP npm package](https://registry.npmjs.org/@neiltron%2Fapple-health-mcp)
- [healthkit-sync fallback skill](https://raw.githubusercontent.com/openclaw/skills/main/skills/mneves75/healthkit-sync/SKILL.md)
- [apple-watch fallback skill](https://raw.githubusercontent.com/openclaw/skills/main/skills/lainnet-42/apple-watch/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON configuration and SQL or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP setup steps, export validation checks, bounded query patterns, troubleshooting paths, and local memory templates; it does not provide live HealthKit access.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
