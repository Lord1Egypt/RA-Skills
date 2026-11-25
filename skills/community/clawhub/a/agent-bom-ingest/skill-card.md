## Description:

Validate and ingest operator-pushed agent-bom inventory JSON from AWS, Azure, GCP, Snowflake, CMDB, or endpoint collectors. Use when a user has canonical inventory JSON and wants local findings, graph, policy, provenance, or auditor-ready exports without giving agent-bom direct cloud credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operators use this skill to validate canonical inventory JSON produced by their own collectors, run local agent-bom analysis, and prepare findings, graphs, policy results, or auditor-ready exports without providing direct cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional vulnerability lookups contact OSV and GitHub Advisory services, and optional control-plane push sends inventory to the operator-specified destination.

Mitigation: Enable only the lookups needed, review the data sharing implications, and confirm the push destination and authentication method before pushing; keep API tokens out of chat and logs.

Risk: ClawScan coverage is incomplete because a referenced local path was not found.

Mitigation: Resolve and inspect the missing referenced file before relying on the benign scan verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/msaad00/skills/agent-bom-ingest)
- [agent-bom source repository (declared homepage/source link)](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown instructions with shell commands; agent-bom exports in JSON, SARIF, HTML, Markdown, CycloneDX, or SPDX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports are written to the operator-selected path.]

## Skill Version(s):

0.115.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
