## Description:

boss-job helps job seekers use OpenCLI to search or recommend BOSS直聘 jobs, view job details, greet HR contacts, inspect chat lists and history, and send messages through a logged-in Chrome session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyqwer1](https://clawhub.ai/user/spyqwer1)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to operate the BOSS直聘 OpenCLI plugin for job discovery and recruiter messaging from an authenticated Chrome browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable external components that operate through a logged-in Chrome session and can read or send recruiter messages.

Mitigation: Install only if the OpenCLI package, GitHub plugin repository, and Chrome extension source are trusted; verify recipients and message text before using greet or send, and avoid automatic or bulk messaging.

## Reference(s):

- [OpenCLI](https://github.com/jackwener/opencli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenCLI commands that act through a logged-in Chrome session.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
