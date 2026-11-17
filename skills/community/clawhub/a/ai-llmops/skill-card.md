## Description:

A Chinese-language LLMOps playbook for managing AI model and asset lifecycles, including asset inventories, model cards, versioning, launch and retirement workflows, drift monitoring, cost governance, and local checklist generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

AI platform, engineering, operations, and finance teams use this skill to structure AI asset inventories, registration records, lifecycle controls, drift checks, and cost governance practices. Agents can also use its local toolkit guidance to produce checklists, model-card templates, lifecycle review points, drift monitoring notes, and cost governance lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Most documentation and CLI output are Chinese-language materials.

Mitigation: Use reviewers who can assess Chinese-language governance guidance before relying on the outputs in production workflows.

Risk: The security audit contains stale copy-paste references to a different toolkit name.

Mitigation: Treat the server-resolved security summary as authoritative and review future audit text for naming consistency.

Risk: Verification scripts can overwrite files under the package's own verify directory.

Mitigation: Run verification scripts from a disposable copy or version-controlled workspace when preserving generated verification artifacts matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-llmops)
- [01 Asset Inventory](references/01-资产全景与台账.md)
- [02 Model Cards and Registration](references/02-模型卡与注册.md)
- [03 Version Management](references/03-版本管理.md)
- [04 Launch and Retirement Management](references/04-上线下线管理.md)
- [05 Drift Monitoring](references/05-漂移监控.md)
- [06 Cost Governance](references/06-成本治理.md)
- [07 Governance Processes](references/07-治理制度与流程.md)
- [08 FAQ](references/08-FAQ.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional local shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language guidance; local toolkit outputs checklist-style text to standard output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
