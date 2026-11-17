## Description:

Deprecated skill that directs users to install the consolidated `auth0` skill for Auth0 React SPA login, logout, protected routes, and user sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining React SPAs use this deprecated skill as a redirect notice and should install the consolidated `auth0` skill for Auth0 authentication work, including login, logout, protected routes, and user sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This deprecated skill redirects users to install a replacement skill through an unpinned ClawHub install command.

Mitigation: Review the replacement auth0 skill, prefer a pinned or otherwise trusted ClawHub installer invocation when available, and run installation from a least-privilege shell without production secrets.

Risk: Users may expect maintained Auth0 React implementation guidance from a retired skill.

Mitigation: Use this skill only as a deprecation notice and install the consolidated auth0 skill for current Auth0 authentication guidance.

## Reference(s):

- [Auth0 React skill page](https://clawhub.ai/auth0/skills/auth0-react)
- [Auth0 agent skills repository](https://github.com/auth0/agent-skills)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redirects users to install the consolidated auth0 skill; no maintained Auth0 React implementation guidance is provided.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
