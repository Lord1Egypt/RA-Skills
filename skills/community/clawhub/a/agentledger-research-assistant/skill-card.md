## Description:

Structured web research framework for AI agents. Teaches your agent to conduct multi-source research, synthesize findings into actionable briefs, maintain a research library, and track evolving topics over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

External users and developers use this skill to guide agents through structured web research, source evaluation, synthesis, saved research briefs, and ongoing topic monitoring for market research, competitor analysis, topic deep-dives, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to create and maintain persistent research folders and monitoring files in a workspace.

Mitigation: Install it only where persistent research files are intended, and periodically review generated research directories for relevance and sensitive content.

Risk: Topic monitoring and heartbeat or cron integration can create recurring agent behavior.

Mitigation: Enable monitoring only with explicit refresh rules, bounded topics, and non-sensitive subject matter.

Risk: Generated reports may include a default third-party branded footer.

Mitigation: Review or remove the branded footer before using reports in contexts where attribution or branding matters.

## Reference(s):

- [Research Assistant on ClawHub](https://clawhub.ai/clawdssen/skills/agentledger-research-assistant)
- [Research Assistant Advanced Patterns](references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown research briefs, research library indexes, monitoring notes, templates, and agent instruction snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update research/README.md, research/briefs/, research/monitoring/, templates, source networks, chains, and research quality logs.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
