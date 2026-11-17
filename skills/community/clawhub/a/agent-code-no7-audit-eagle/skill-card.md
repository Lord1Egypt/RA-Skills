## Description:

Agent Code No.7 Audit Eagle supports Chinese-language financial statement analysis and audit assistance from user-provided financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monarchmio](https://clawhub.ai/user/monarchmio)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams, auditors, and agent builders use this skill to analyze balance sheets, income statements, and cash flow statements, identify anomalies, calculate ratios, and draft audit-oriented reports or workpaper templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial data submitted to an agent environment may include confidential or regulated information.

Mitigation: Use only financial data approved for the target agent environment and apply the organization's confidentiality controls before invoking the skill.

Risk: The skill's financial analysis and audit suggestions may be mistaken for a formal audit opinion or licensed professional judgment.

Mitigation: Treat outputs as advisory, preserve the skill's reference-only disclaimer, and require qualified professional review before relying on conclusions.

Risk: The artifact is written primarily in Chinese, which can reduce reviewability for non-Chinese users.

Mitigation: Request output in the user's preferred language and verify translated details before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monarchmio/skills/agent-code-no7-audit-eagle)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style financial analysis report with tables, risk notes, audit procedure suggestions, and workpaper templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language advisory audit support based on user-provided financial data; no code execution, persistence, credential access, or hidden data movement is indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
