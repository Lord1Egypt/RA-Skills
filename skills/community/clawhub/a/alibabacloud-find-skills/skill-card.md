## Description:

Helps agents search, browse, inspect, and when requested install Alibaba Cloud agent skills from the AgentExplorer catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover Alibaba Cloud skills by intent, keyword, or category, inspect matching skill details, and receive installation guidance only when they explicitly request installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may expose secrets, customer names, access keys, incident details, or internal identifiers.

Mitigation: Sanitize search phrases before use and avoid placing sensitive or private identifiers in AgentExplorer queries.

Risk: The documented installation path can add agent skills globally through unpinned npx commands while skipping confirmation.

Mitigation: Review selected skills before installation, prefer pinned and project-local installs, and use global non-interactive installation only when a persistent global agent change is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-find-skills)
- [AgentExplorer API Base URL](https://agentexplorer.aliyuncs.com)
- [AgentExplorer HTTP API Reference](references/agentexplorer-api.md)
- [Search Examples](references/search-examples.md)
- [Category Examples](references/category-examples.md)
- [Verification Methods](references/verification-method.md)
- [Curl Shell Compatibility Guide](references/curl-shell-compatibility.md)
- [Supported Agent Values for npx skills add](references/npx-skills-agents.md)
- [Acceptance Criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with result summaries, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AgentExplorer API request shapes, selected skill details, and installation commands when installation is requested.]

## Skill Version(s):

0.0.10 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
