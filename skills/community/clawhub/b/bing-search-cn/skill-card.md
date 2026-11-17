## Description:

Uses Bing China to run web searches and fetch cleaned webpage text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dej4vu](https://clawhub.ai/user/dej4vu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search cn.bing.com and fetch public webpage text for Chinese-language research and browsing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webpage fetcher can request arbitrary URLs from the agent environment.

Mitigation: Run the skill only where private network destinations, localhost services, cloud metadata endpoints, and internal dashboards are blocked or allowlisted outside the skill.

Risk: Fetched web content may be large or untrusted.

Mitigation: Apply external response-size limits and review fetched content before using it in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dej4vu/skills/bing-search-cn)
- [Bing China](https://cn.bing.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON search results or fetched webpage text, with Markdown guidance for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and outbound access to cn.bing.com and requested public webpage URLs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
