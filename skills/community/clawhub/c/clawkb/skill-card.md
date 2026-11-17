## Description:

Use this skill when an agent needs to work with a ClawKB server over HTTP: register itself, obtain or use a Bearer token, upload images, create or update entries, search entries, read entry detail, or inspect plugin-backed API flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hata1234](https://clawhub.ai/user/hata1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to interact with ClawKB deployments over HTTP for authentication, image uploads, entry creation and editing, search, reading, comments, and internal entry links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional auto-recall plugin may send conversation content to configured ClawKB servers and place returned entries into privileged prompt context.

Mitigation: Use manual API access by default; enable auto-recall only for trusted plugin versions and trusted ClawKB backends, and avoid it for sensitive conversations.

Risk: Bearer tokens grant the agent the ClawKB permissions configured for that token.

Mitigation: Provide least-privilege tokens, map users to appropriate server-side access controls, and revoke or rotate tokens when access is no longer needed.

## Reference(s):

- [ClawKB Skill Page](https://clawhub.ai/hata1234/skills/clawkb)
- [Publisher Profile](https://clawhub.ai/user/hata1234)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP API request examples, response fields to retain, and operational guidance for Bearer token based ClawKB workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
