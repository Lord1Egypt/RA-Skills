## Description:

Analyzes ActivityWatch computer activity data to summarize time distribution and provide actionable productivity advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qew21](https://clawhub.ai/user/qew21)

### License/Terms of Use:


## Use Case:

Individuals and productivity-focused users run this skill to review recent ActivityWatch application and window activity, understand time distribution, identify patterns such as context switching, and receive concise improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ActivityWatch application names and raw window titles may reveal sensitive document names, URLs, email subjects, or other private work context to the configured AI model.

Mitigation: Run the skill only with user consent, limit collection to the needed time range, and aggregate or redact window titles before sending activity summaries for analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown narrative with command output summaries and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses recent local ActivityWatch records and should minimize or redact raw window titles before model analysis.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
