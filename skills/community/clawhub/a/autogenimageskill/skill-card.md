## Description:

Use when the user wants GPT-Image-2 image generation or image-to-image through an official OpenAI permission code/API key, a custom Responses-compatible proxy, or a reserved purchased-capacity relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherstrings](https://clawhub.ai/user/etherstrings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or transform PNG images from prompts through an official OpenAI path, a configured Responses-compatible proxy, or a reserved-capacity relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source images, and credentials may be sent to configurable services, including custom proxies or reserved relay services.

Mitigation: Install only when the configured image backend is trusted; prefer official mode without overriding OPENAI_BASE_URL, and treat proxy or relay modes as third-party data sharing.

Risk: API keys, permission codes, purchase keys, or provider tokens can be exposed if handled carelessly at runtime.

Mitigation: Pass secrets through environment variables or a secret manager, avoid command-line arguments for sensitive values when possible, and keep generated summaries redacted.

## Reference(s):

- [Access Modes](references/access-modes.md)
- [Runtime Notes](references/runtime.md)
- [ClawHub Skill Page](https://clawhub.ai/etherstrings/skills/autogenimageskill)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration guidance, Text]

**Output Format:** [PNG image file plus concise text metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the absolute output path, access mode, endpoint or relay job ID, provider name when available, byte size, and revised prompt while keeping credentials redacted.]

## Skill Version(s):

0.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
