## Description:

Step-by-step wizard for connecting an owner's Google Calendar to their OpenClaw PA agent, including granting write permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw PA agent owners and operators use this skill to connect an owner's Google Calendar, grant calendar write access, re-authenticate after permission failures, and troubleshoot multi-account calendar setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup may grant broad Google Workspace authority beyond calendar-only access.

Mitigation: Use the narrowest OAuth scopes that satisfy the task, preferably calendar-only scopes when email, Drive, contacts, Sheets, or Docs are not required.

Risk: The direct credential-file workaround can expose owner refresh tokens or client secrets to an agent context.

Mitigation: Avoid the workaround when possible, do not print or paste credential-file contents, and keep refresh tokens and client secrets outside agent-visible context.

Risk: Deployment-specific account names and credential paths may be reused in the wrong environment.

Mitigation: Replace host-specific accounts, emails, and credential paths with environment-specific values before operational use.

## Reference(s):

- [Calendar Setup ClawHub release](https://clawhub.ai/netanel-abergel/skills/calendar-setup)
- [Google Calendar](https://calendar.google.com)
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token)
- [Google Calendar API calendar list endpoint](https://www.googleapis.com/calendar/v3/users/me/calendarList)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural setup checklist with account-specific placeholders for Google Calendar and OAuth configuration.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
