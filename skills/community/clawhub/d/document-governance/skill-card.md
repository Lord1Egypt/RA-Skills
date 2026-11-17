## Description:

工程文档治理元技能，帮助 AI 编程项目按文档意图选择类型、分层记录，并路由到相应的编写、评审或治理流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

AI coding agents and developers use this skill to classify engineering documentation tasks, select suitable document types and record layers, and route work to writing, review, or governance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting outdated documentation could remove useful records.

Mitigation: Archive outdated documents first, and warn and obtain confirmation before deletion.

Risk: Two referenced local paths were unavailable during scanning, leaving evidence about related behavior incomplete.

Mitigation: Check those paths and review the relevant guidance before relying on it.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/zengfr/document-governance-skills/tree/main/document-governance)
- [ClawHub skill page](https://clawhub.ai/zengfr/skills/document-governance)
- [Three-layer model](artifact/references/three-layer-model.md)
- [Core document types](artifact/references/core-doc-types.md)
- [As-is vs. to-be guidance](artifact/references/as-is-vs-to-be.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Concise text guidance with document type, layer, and workflow recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
