## Description:

focusAI helps an agent guide local FocusAI use for screen activity monitoring, focus scoring, and same-day visual history queries after user consent and setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hr2ay](https://clawhub.ai/user/hr2ay)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill with an agent to start, stop, check, and query a local FocusAI installation for focus monitoring and work-session history. The skill is intended for user-controlled local workflows where screenshots, CSV reports, and cloud vision API use are disclosed before monitoring begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local FocusAI program can capture screen contents and send screenshots to a configured cloud vision provider.

Mitigation: Use it only after explicit user consent, confirm the chosen provider and API cost implications, and stop monitoring when it is no longer needed.

Risk: The release directs users toward external FocusAI code that is not pinned by server-resolved provenance.

Mitigation: Review or pin the FocusAI code before running it, and avoid administrator privileges.

Risk: API keys and retained screenshots or reports can expose sensitive information if mishandled.

Mitigation: Keep credentials in the local config file, do not read or transmit credential contents through the agent, and delete retained screenshots or reports when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hr2ay/skills/focus-ai)
- [Publisher profile](https://clawhub.ai/user/hr2ay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide API calls to a local FocusAI service and summarize local activity records when available.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
