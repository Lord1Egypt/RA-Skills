## Description:

帮招聘 HR 快速汇总面试反馈、生成候选人推进话术、整理 Offer 材料并回写跟进记录。 / Help recruiting teams debrief interviews, draft candidate follow-ups, prepare offer materials, and update trackers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashley-aihr](https://clawhub.ai/user/ashley-aihr)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HRBPs, and hiring teams use this skill to turn messy interview feedback, JD and resume inputs, and offer-prep details into recruiting decisions, candidate messages, and tracker-ready records for China-focused hiring workflows.

### Deployment Geography for Use:

Global, with Mainland China recruiting context

## Known Risks and Mitigations:

Risk: Sensitive recruiting records may be written to disk in generated DOCX, CSV, and JSON files.

Mitigation: Use the skill only with recruiting data the operator is authorized to process, choose a controlled output directory, and redact salary or interview details when they are not needed.

Risk: Generated CSV files may preserve spreadsheet formulas from candidate data.

Mitigation: Sanitize CSV output or add formula-injection hardening before opening generated CSV files in spreadsheet tools.

Risk: Recruiting recommendations may affect hiring decisions when inputs are incomplete or inconsistent.

Mitigation: Review the recommendation, missing-information fields, and candidate-facing drafts before using them in a live recruiting workflow.

## Reference(s):

- [Real User Scenario](references/real-user-scenario.md)
- [Recruiting Fields Reference](references/recruiting-fields.md)
- [ClawHub skill page](https://clawhub.ai/ashley-aihr/skills/cn-recruiting-workflow)
- [Project homepage](https://github.com/Ashley-AIHR/hrskill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Structured Markdown or text, plus optional DOCX, CSV, and JSON files generated from local JSON inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The packaged scripts can produce interview debrief memos, candidate messages, tracker CSV rows, resume-screening notes, and JSON workflow summaries.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
