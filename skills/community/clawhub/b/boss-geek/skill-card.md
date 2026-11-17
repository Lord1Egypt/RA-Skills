## Description:

Boss Geek helps an agent guide BOSS Zhipin job seekers through OpenCLI commands for job search, job detail lookup, recruiter greetings, chat listing, chat history, and sending messages through a logged-in Chrome session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyqwer1](https://clawhub.ai/user/spyqwer1)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to operate BOSS Zhipin workflows through OpenCLI, including searching for roles, checking job details, greeting recruiters, reading chats, and sending replies. It is intended for users who already have Chrome logged in to zhipin.com and the OpenCLI Chrome extension installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenCLI tooling and plugin can act through a logged-in Chrome session, including reading chats and sending messages.

Mitigation: Use a dedicated Chrome profile logged in only to BOSS Zhipin, and avoid profiles that contain unrelated accounts or sensitive sessions.

Risk: Mutable third-party tooling or plugin revisions may change behavior after installation.

Mitigation: Inspect or pin the OpenCLI package and plugin revision before use.

Risk: Greeting or send commands may contact the wrong recipient or send unintended message text.

Mitigation: Manually confirm recipients, security IDs, encrypted user IDs, and message text before running greet or send commands.

## Reference(s):

- [OpenCLI repository](https://github.com/jackwener/opencli)
- [City, experience, education, and salary codes](references/codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples that reference BOSS Zhipin security IDs and encrypted user IDs supplied by OpenCLI results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
