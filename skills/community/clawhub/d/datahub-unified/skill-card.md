## Description:

DataHub Unified Data Layer helps agents retrieve financial market, filing, announcement, macroeconomic, research, and investor-relations data across 14 sources through a publish-subscribe interface with routing, caching, and quick helper functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial research teams use this skill to help an agent configure and call a local DataHub implementation for quotes, financial statements, announcements, macroeconomic series, natural-language financial queries, and multi-source validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a separately configured local DataHub implementation.

Mitigation: Confirm the configured DataHub code path is trusted before installing or using the skill.

Risk: Some providers require API keys or cookies for financial data access.

Mitigation: Configure provider credentials only when needed and keep secrets out of prompts, shared logs, and generated examples.

Risk: Financial data requests may trigger outbound queries to configured providers.

Mitigation: Use explicit user requests for data fetching and review configured sources before automated or batch use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/datahub-unified)
- [Skill source: SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill output guides an agent to use configured local DataHub code and provider credentials when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
