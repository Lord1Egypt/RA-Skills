## Description:

Discovers AWS-hosted AI agents and workloads, writes canonical inventory JSON, and can optionally scan that inventory with agent-bom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud security teams use this skill to inventory AWS-hosted AI agents and related workloads as canonical JSON. They can optionally scan the inventory with agent-bom when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports medium confidence and two missing referenced paths, leaving some checks incomplete.

Mitigation: Complete the missing reference checks before relying on the benign verdict.

Risk: The inventory can include sensitive AWS account and workload metadata.

Mitigation: Use an approved read-only AWS role and store the inventory only at an operator-approved path.

## Reference(s):

- [agent-bom repository](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Canonical inventory JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Written to an operator-selected path; scanning and export are optional and operator-directed.]

## Skill Version(s):

0.115.6 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
