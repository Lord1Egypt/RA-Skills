## Description:

Displays API credit balances for 5 core providers (Anthropic, OpenAI, OpenRouter, Mistral, Groq) with video game style health bars, API auto-checks, and manual sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franciscobuiltdat](https://clawhub.ai/user/franciscobuiltdat)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to check, display, manually update, and record top-ups for API credit balances across supported AI providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenAI auto-check may require an organization-admin API key, which is broader access than users may expect.

Mitigation: Prefer manual sync or narrowly scoped billing/read-only credentials where available, and avoid exposing an organization-admin key.

Risk: Auto-check mode makes network requests to provider APIs using credentials from environment variables.

Mitigation: Use manual sync for zero-network operation, keep keys out of files, and rotate or revoke keys after testing.

Risk: The skill writes local balance data to config.json.

Mitigation: Store only non-sensitive balance values and restrict config.json permissions to the local user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franciscobuiltdat/skills/api-credits-lite)
- [README](artifact/README.md)
- [Security Policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style text with health-bar status output and optional shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local balance configuration and optionally call provider APIs when environment variables are set.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
