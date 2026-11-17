## Description:

Generates personalized BOSS Zhipin greeting messages by using boss-cli to retrieve job details, compare them with a user's resume, and draft two concise message variants under 200 Chinese characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bifang988](https://clawhub.ai/user/bifang988)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and recruiting assistants use this skill to turn a target BOSS Zhipin job and a user's resume details into a focused job-fit analysis and two human-sounding outreach greetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install and run an unpinned third-party CLI.

Mitigation: Verify the kabi-boss-cli source and version before installation, and pin or record the reviewed version where possible.

Risk: Login through the CLI may access browser cookies.

Mitigation: Prefer QR-code login over browser-cookie access when authenticating to BOSS Zhipin.

Risk: Resume content can include sensitive personal data.

Mitigation: Provide only the resume fields needed to generate the greeting instead of a complete sensitive resume file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bifang988/skills/boss-greeting-message)
- [ClawHub publisher profile](https://clawhub.ai/user/bifang988)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with job analysis, two greeting-message variants, word counts, and inline shell commands when setup or job lookup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Greeting messages are constrained to no more than 200 Chinese characters each.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
