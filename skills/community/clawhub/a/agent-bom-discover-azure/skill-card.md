## Description:

Discovers Azure-hosted AI and MCP-relevant assets and produces canonical agent-bom inventory JSON for optional scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud security engineers use this skill to inventory Azure AI and agentic workloads through approved, read-only Azure access, then optionally scan the resulting inventory with agent-bom.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure discovery uses the operator's Azure identity, and the security review has medium confidence with incomplete analysis because a referenced local path could not be resolved.

Mitigation: Use only approved subscriptions with read-only access, and review the unresolved local-path issue before running.

Risk: The workflow writes Azure inventory to a path chosen by the operator.

Mitigation: Choose a protected operator-controlled path and review the inventory before sharing it.

## Reference(s):

- [agent-bom project homepage](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Canonical inventory JSON file and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to an operator-selected path; scanning is optional and requires an explicit request.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
