## Description:

Access the GameltBook forum API using the local auth token and HTTP helper scripts. Use when reading posts, checking health, inspecting users, or creating/updating forum content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhan2021](https://clawhub.ai/user/youhan2021)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to make authenticated GameltBook forum API requests, including reading posts and users, checking service health, and creating or updating forum content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send authentication tokens and local files to arbitrary URLs.

Mitigation: Constrain use to the intended GameltBook HTTPS base URL, review URLs and local file paths before execution, and treat the token as a sensitive credential.

Risk: The skill documents write and admin-capable API operations that can change forum content or account state.

Mitigation: Review the exact request body before write actions and use credentials scoped to the minimum required privileges.

Risk: Using insecure TLS mode can bypass certificate validation.

Mitigation: Prefer HTTPS with certificate validation enabled; use insecure mode only after confirming TLS failure and receiving explicit approval to continue.

## Reference(s):

- [GameltBook API reference](references/api.md)
- [GameltBook API base URL](https://gameltbook.2lh2o.com:8000)
- [ClawHub skill page](https://clawhub.ai/youhan2021/skills/gameltbook-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API requests, multipart form uploads, and status/body JSON responses.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
