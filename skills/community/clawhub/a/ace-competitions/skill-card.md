## Description:

Ace competitions agent workflow - search, enter, track competitions. Uses browser automation for form filling, email verification, and competition entry. Integrates with competitions dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find online competitions, prepare automated entries, handle verification steps, and track outcomes in a competition dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes unattended competition entry and verification across third-party sites.

Mitigation: Require user approval before submitting each entry and avoid enabling scheduled jobs by default.

Risk: The artifact includes hardcoded contact details and dashboard/API endpoints.

Mitigation: Replace personal contact details with user-provided values and protect or disable dashboard/API outputs unless access control and retention are configured.

Risk: The workflow depends on referenced scripts and automation components that are not included in the artifact.

Mitigation: Confirm referenced scripts are trusted, pinned, and reviewed before execution.

## Reference(s):

- [Ace Competitions ClawHub skill page](https://clawhub.ai/stefanferreira/skills/ace-competitions)
- [stefanferreira ClawHub publisher profile](https://clawhub.ai/user/stefanferreira)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, SQL, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions for browser automation, email verification, dashboard tracking, scheduled jobs, and error recovery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
