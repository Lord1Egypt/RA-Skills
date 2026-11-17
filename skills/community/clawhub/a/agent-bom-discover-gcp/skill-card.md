## Description:

Discover GCP-hosted AI agent and MCP-relevant assets from the operator's environment, emit canonical agent-bom inventory JSON, and scan it without giving agent-bom long-lived GCP credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud security engineers use this skill to inventory AI and workload resources in operator-approved GCP projects, producing schema-valid agent-bom inventory JSON for optional local scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious: its partial scan found a referenced local Python path missing from the bundle and references to credential paths.

Mitigation: Before installing, verify the missing Python example from a source you trust and review the skill's credential use and the permissions granted.

Risk: The skill makes authenticated read-only calls to inventory resources in the configured GCP project.

Mitigation: Use only operator-approved projects and scoped read-only credentials; keep private keys and tokens out of chat, and choose the inventory output path yourself.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/msaad00/skills/agent-bom-discover-gcp)
- [agent-bom project homepage](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions and canonical JSON inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory is written to an operator-selected path; discovery is read-only, and scanning is optional.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
