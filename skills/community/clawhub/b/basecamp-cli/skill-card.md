## Description:

Manage Basecamp (via bc3 API / 37signals Launchpad) projects, to-dos, messages, and campfires via a TypeScript CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emredoganer](https://clawhub.ai/user/emredoganer)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to configure and run Basecamp CLI workflows for authentication, project management, to-do management, messages, campfires, and people lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI handles Basecamp OAuth secrets, access tokens, and live account data.

Mitigation: Use a non-production Basecamp account first, keep BASECAMP_CLIENT_SECRET and tokens out of shared terminals and logs, and revoke tokens if exposed.

Risk: Authenticated commands can change live Basecamp content, including archiving projects, creating messages, sending chat lines, and modifying to-dos.

Mitigation: Review command targets and options before execution and limit use to accounts where those changes are authorized.

Risk: People and profile commands can print personal or sensitive business data.

Mitigation: Run these commands only for authorized Basecamp accounts and avoid sharing raw output in public or untrusted channels.

## Reference(s):

- [Basecamp bc3 API](https://github.com/basecamp/bc3-api)
- [37signals Launchpad Integrations](https://launchpad.37signals.com/integrations)
- [Basecamp CLI on ClawHub](https://clawhub.ai/emredoganer/skills/basecamp-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Text]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or tabular CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read from or write to live Basecamp accounts after OAuth authentication.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
