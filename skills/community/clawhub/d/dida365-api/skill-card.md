## Description:

滴答清单 (Dida365) API integration that helps an agent guide OAuth setup and manage Dida365 tasks and projects through the Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imchongliu](https://clawhub.ai/user/imchongliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure Dida365 OAuth credentials, obtain an access token, and create, update, complete, delete, or organize tasks and projects in a Dida365 account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a long-lived Dida365 task API token and uses client credentials for OAuth setup.

Mitigation: Protect the client secret and token file, keep restrictive token-file permissions, and avoid committing credentials or tokens to version control.

Risk: The documented API actions can write, complete, or delete tasks and projects in a Dida365 account.

Mitigation: Require explicit user confirmation before completing or deleting tasks or projects, especially when an agent is acting on behalf of the user.

Risk: The OAuth flow uses a local callback and a static example state value.

Mitigation: Use per-run OAuth state validation when adapting the example flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imchongliu/skills/dida365-api)
- [Dida365 Developer Platform](https://developer.dida365.com)
- [Dida365 Open API Base URL](https://api.dida365.com/open/v1/)
- [Dida365 Website](https://dida365.com)
- [Dida365 Help Center](https://help.dida365.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, JavaScript, curl, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDA365_CLIENT_ID and DIDA365_CLIENT_SECRET environment variables and a locally stored Dida365 OAuth access token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
