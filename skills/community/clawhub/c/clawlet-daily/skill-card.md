## Description:

Clawlet Daily generates a personalized Markdown daily report by aggregating learning notes, task logs, and AI briefing records from the memory directory with summaries and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzszsp](https://clawhub.ai/user/zzszsp)

### License/Terms of Use:

MIT-0

## Use Case:

Clawlet users use this skill to answer daily-summary prompts by scanning matching memory records and producing a sourced daily activity report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad daily-summary triggers may cause the agent to read and summarize memory files that contain private or sensitive information.

Mitigation: Use the skill only in trusted single-user contexts, narrow requests to explicit dates, and review memory contents for secrets before generating reports.

Risk: A daily report can expose or overstate activity records if source files are incomplete, stale, or unrelated to the requested date.

Mitigation: Keep source links in the report and review summarized claims against the referenced memory files.

## Reference(s):

- [Clawlet Daily on ClawHub](https://clawhub.ai/zzszsp/skills/clawlet-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown daily report with linked source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are grounded in matching memory files when those files are available to the agent.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
