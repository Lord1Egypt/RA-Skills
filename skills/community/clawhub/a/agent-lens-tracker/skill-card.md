## Description:

Track AI agent API calls, analyze token usage, and optimize costs for OpenAI, Anthropic, Google, and DeepSeek API usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument agent API calls, review token and cost reports, troubleshoot expensive models or prompts, and export local usage data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance pulls executable code from an unpinned external repository.

Mitigation: Review the repository before installing, use an isolated virtual environment, and prefer a pinned commit or verified release.

Risk: Tracing agent calls can store sensitive prompts or metadata in the local SQLite database.

Mitigation: Avoid tracing sensitive production data unless retention and cleanup practices are defined; use the documented clean command to remove old records.

Risk: Cost estimates may differ from actual billed costs because list prices and provider-specific formats can vary.

Mitigation: Treat reports as estimates and validate high-impact decisions against provider billing data and manually supplied token counts when needed.

## Reference(s):

- [Agent Lens ClawHub release](https://clawhub.ai/lrg913427-dot/skills/agent-lens-tracker)
- [lrg913427-dot publisher profile](https://clawhub.ai/user/lrg913427-dot)
- [Agent Lens install repository](https://github.com/lrg913427-dot/agent-lens.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cost-analysis guidance, token-counting snippets, CLI commands, and local data-retention recommendations.]

## Skill Version(s):

2.15.0 (source: server release metadata; artifact frontmatter reports 2.14.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
