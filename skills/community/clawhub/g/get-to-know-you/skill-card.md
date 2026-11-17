## Description:

Get To Know You helps an agent collect a user's work context and preferences through guided Q&A, then apply a confirmation-first workflow for handling negative feedback and skill optimization requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzanezhou0829](https://clawhub.ai/user/zzzanezhou0829)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and agent operators use this skill to build a personalized working profile and require clearer requirement alignment before changes are made after feedback. It is intended for agents that should adapt communication, output, and workflow behavior based on user-confirmed preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects broad personal and workplace preference information that can shape future agent behavior.

Mitigation: Collect only information the user explicitly chooses to share, avoid sensitive personal or workplace details, and review the resulting profile before it is reused.

Risk: The collector can append raw collected text to persistent agent configuration files.

Mitigation: Review proposed writes before running the script and prefer explicit invocation over automatic or passive collection.

## Reference(s):

- [Information Collection Question Bank](references/question_bank.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell command examples and configuration-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist collected answers into local agent configuration files when the user approves or runs the collector script.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
