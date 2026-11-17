## Description:

Provides a weekly AI large language model report for May 2026 with related Bilibili video links and study summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to load a May 2026 AI large language model weekly report and related Bilibili study links into a local knowledge base for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs persistent knowledge-base writes when run.

Mitigation: Install only when these Bilibili AI-report entries are intended, and ensure records can be reviewed and deleted.

Risk: The skill loads local Python code from a hard-coded D:\\coze-local\\db path.

Mitigation: Review and control the local learn module before enabling the skill.

Risk: Broad trigger phrases may activate the skill unexpectedly.

Mitigation: Narrow the trigger before deployment when accidental activation would create unwanted knowledge-base records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/auto-llm-1644)
- [Source Bilibili video BV1d2Vh6EE1t](https://www.bilibili.com/video/BV1d2Vh6EE1t)
- [Bilibili study link BV1smVu6uEZk](https://www.bilibili.com/video/BV1smVu6uEZk)
- [Bilibili study link BV1Kg1TYJEDg](https://www.bilibili.com/video/BV1Kg1TYJEDg)
- [Bilibili study link BV1iTV965EV7](https://www.bilibili.com/video/BV1iTV965EV7)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown-style study summary and links with a Python-triggered status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an AI-report entry to a local knowledge base when run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
