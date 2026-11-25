## Description:

Discover Azure-hosted AI agent and MCP-relevant assets from the operator's environment, emit canonical agent-bom inventory JSON, and scan it without giving agent-bom long-lived Azure credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud platform, security, and AI infrastructure teams use this skill to inventory Azure-hosted AI and agent workloads as canonical agent-bom JSON, then optionally scan that inventory when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because the referenced Azure adapter was unavailable for assessment.

Mitigation: Review the adapter before installation and use only approved Azure subscriptions with read-only identities.

Risk: Discovery uses the operator's existing Azure identity to read Azure resource and service metadata.

Mitigation: Use an approved read-only identity, keep secrets and tokens out of prompts, and write inventory only to a path you choose.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/msaad00/skills/agent-bom-discover-azure)
- [agent-bom project](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [Canonical agent-bom inventory JSON, with optional scan findings JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes inventory to an operator-selected path; scanning is optional and only runs when requested.]

## Skill Version(s):

0.115.6 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
