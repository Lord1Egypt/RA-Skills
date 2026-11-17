## Description:

Discover AWS-hosted AI agent and MCP-relevant assets from the operator's environment, emit canonical agent-bom inventory JSON, and optionally scan it when the operator requests a scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud operators use this skill to inventory AI agents and workloads in their AWS environment with operator-controlled, read-only credentials. They can stop after generating a canonical inventory or explicitly request a local scan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because a local reference could not be resolved.

Mitigation: Review the unresolved reference and inspect the skill before installing.

## Reference(s):

- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Canonical inventory JSON file and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory is written to an operator-selected path; scanning and export are optional operator-directed steps.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
