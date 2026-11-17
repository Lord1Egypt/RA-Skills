## Description:

Audit catalyst preparation and evaluation methods for executability, reproducibility, controlled comparison, attribution, measurement reliability, safety-review readiness, and claim-to-evidence linkage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Research scientists, project leads, and technical reviewers use this skill to audit catalyst experimental procedures, paper methods, patent examples, draft plans, and machine-generated routes before experimental execution or review. It identifies missing method details, weak controls, measurement gaps, safety-review boundaries, and unsupported claim-to-evidence links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python report generator on user-supplied catalyst-method files, including DOCX or text-readable PDF inputs.

Mitigation: Use a dedicated output directory and avoid hostile or unusually large document inputs.

Risk: Generated reports may contain confidential experimental material.

Mitigation: Keep generated JSON, HTML, and DOCX reports within the user's intended access and retention boundary, and do not authorize external patent or scientific services for confidential material unless sharing is intended.

## Reference(s):

- [Audit methodology](references/methodology.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/audit-catalyst-experimental-methods-rd)
- [PatSnap patent search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap patent briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated JSON, HTML, and DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates report_context.json, one HTML report, and one DOCX report in a dedicated output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence); artifact VERSION reports 0.5.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
