## Description:

合同卫士 — AI合同审查助手，识别风险条款、提取关键信息、追踪到期日

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review Chinese-language contract files, identify risky clauses, extract parties, amounts and dates, track expirations, archive contract metadata, compare contract versions, and generate structured review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local scripts read contract files and can persist contract metadata on disk.

Mitigation: Use a private CG_DATA_DIR with restrictive permissions and treat generated reports, diffs, excerpts, and local paths as sensitive.

Risk: Contract review output may be incomplete or legally incorrect.

Mitigation: Use reports as decision support only and have important contracts reviewed by qualified legal counsel.

Risk: Untrusted filenames or JSON values may increase local handling risk.

Mitigation: Avoid untrusted filenames and JSON input values when archiving, reviewing, or comparing contracts.

## Reference(s):

- [合同卫士 README](assets/README.md)
- [合同风险条款清单](references/risk-checklist.md)
- [合同模板库](references/contract-templates.md)
- [ClawHub skill page](https://clawhub.ai/hanjing5024064/skills/contract-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown reports with tables, risk summaries, local command examples, and JSON-backed command results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive contract excerpts, names, contact details, contract terms, and local file paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
