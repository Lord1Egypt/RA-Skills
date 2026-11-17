## Description:

Reviews Feishu technical documents across literature surveys, solution walkthroughs, experimental designs, and external materials, then produces a structured review report and Feishu report artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tang-auuu](https://clawhub.ai/user/tang-auuu)

### License/Terms of Use:

MIT-0

## Use Case:

Teams reviewing technical, research, experimental-design, and external-facing documents use this skill to generate structured findings, severity-ranked issues, and Feishu report and summary documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu document read/write access and can create or overwrite report and summary documents.

Mitigation: Confirm the exact source documents, destination folder, summary-table token, and overwrite behavior before execution.

Risk: Review reports plus document and link metadata are stored in Feishu.

Mitigation: Treat generated reports and summary tables as sensitive workspace records and verify Feishu sharing and retention settings.

Risk: The external-material workflow references a separate material-review skill that is not bundled in this artifact.

Mitigation: Remove that dependency or vendor a reviewed copy before relying on the external-material workflow.

Risk: Security evidence marks the release as suspicious because some instructions are unsafe or under-scoped.

Mitigation: Review the source instructions and security scan results before installing or enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tang-auuu/skills/doc-review-auuu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown review report with Feishu document and summary-table outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu/lark-cli authorization and user confirmation of source documents, destination folder, summary-table token, and overwrite behavior.]

## Skill Version(s):

2.9.4 (source: server release evidence, artifact SKILL.md frontmatter, and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
