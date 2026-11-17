## Description:

Install and onboard FitAgent for Intervals.icu fitness coaching: install the CLI, initialise a workspace, configure credentials securely, fetch initial data, and verify readiness. Use when the user wants to set up, install, connect, or troubleshoot FitAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jogvan-k](https://clawhub.ai/user/jogvan-k)

### License/Terms of Use:

MIT-0

## Use Case:

Athletes and their coaching agents use this skill to install and configure FitAgent, connect an Intervals.icu account securely, fetch training context, and verify a coaching workspace is ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Intervals.icu credentials and personal fitness data may be exposed during setup or coaching.

Mitigation: Enter the API key only through FitAgent's interactive prompt, keep it out of chat and logs, and protect the coaching workspace containing personal data.

Risk: A workout sync can make changes to the athlete's remote calendar.

Mitigation: Preview changes with a dry run and sync only after the athlete approves the reported changes or has an explicit standing preference.

## Reference(s):

- [FitAgent project](https://github.com/jogvan-k/fit-agent)
- [Intervals.icu](https://intervals.icu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step setup and verification instructions with credential and personal-data safeguards.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
