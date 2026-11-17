## Description:

Map all credentials your OpenClaw agent can access. Scans env vars, config, memory, skills, MCP servers, git history. Generates exposure report with risk scoring. Activate when user says "credential audit", "exposure map", "security audit", or "what can my agent access".

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use the skill to audit which credentials and agent configuration their OpenClaw environment exposes. It summarizes credential-like findings, exposure risks, and ways to reduce access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit searches broad credential-bearing sources, including environment variables, configuration, memory, MCP settings, skills, and Git history.

Mitigation: Choose the narrowest scan scope that answers the audit and review access to each selected source before running.

Risk: The security review reports partial scan coverage, degraded static analyzers, a missing state file, and Git history coverage limited to the first 50 commits.

Mitigation: Treat results as incomplete where coverage is limited and verify high-impact sources separately.

Risk: The saved report contains credential previews and source locations that may be sensitive.

Mitigation: Keep the report private and review it before sharing; the skill documents masked previews and restricted file permissions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thomaszhou22/skills/credential-exposure-map)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Configuration guidance]

**Output Format:** [Markdown audit summary and JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk-ranked findings with masked credential previews and source locations, plus exposure-reduction recommendations.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
