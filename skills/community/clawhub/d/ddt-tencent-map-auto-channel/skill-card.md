## Description:

Analyzes automotive after-market brand coverage, service mix, location profiles, and competitive context from DDT published store snapshots, with Tencent Map copied address text usable as optional location input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Market, channel-planning, and sales users use this skill to assess automotive after-market brand networks by national scale, regional concentration, service categories, surrounding context, and local competitive signals. It is scoped to published DDT data snapshots and stops when brand, coverage, credential, or API response evidence is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends relevant brand, location, and store-query data to the DDT service using a user-provided DDT API key.

Mitigation: Use it only when that data sharing is acceptable, keep the API key out of chats, logs, and repositories, and configure credentials only in a controlled local or runtime environment.

Risk: Changing the API base can route requests to an endpoint outside the trusted default.

Mitigation: Use the default DDT API base unless you intentionally control and trust the alternate endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-auto-channel)
- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with concise conclusions, key metrics, coverage notes, and limited requested store details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl examples and API setup guidance; does not output API keys, supplier fields, storage IDs, or unsupported internal fields.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
