## Description:

Crypto Research Interactive Framework provides interactive crypto deep research with human-AI collaboration for project, sector, market, tokenomics, technology, quality, content, image-prompt, and brainstorming workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kudodefi](https://clawhub.ai/user/kudodefi)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts use this skill to structure crypto research, route requests to focused workflows, collaborate through checkpoints, and produce local research outputs or content drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional MCP setup may encourage unpinned package execution or API-key-in-URL configuration.

Mitigation: Pin package versions, store secrets in environment variables, review MCP server provenance, and run optional MCP servers in a constrained environment.

Risk: The skill reads public sources and writes local crypto research reports, so users may rely on incomplete or time-sensitive information.

Mitigation: Use collaborative checkpoints, review cited sources and dates, and validate material findings before acting on research outputs.

## Reference(s):

- [CRIF README](README.md)
- [Security and Permissions](SECURITY.md)
- [License](LICENSE.md)
- [Orchestrator](references/core/orchestrator.md)
- [Core Configuration](references/core/core-config.md)
- [MCP Server Reference](references/core/mcp-servers.md)
- [Research Methodology](references/guides/research-methodology.md)
- [Output Standards](references/guides/output-standards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, research briefs, content drafts, image prompts, local workspace files, and optional setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated through selected workflows and may include checkpoint prompts for human review.]

## Skill Version(s):

0.1.1 (source: SKILL.md framework version and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
