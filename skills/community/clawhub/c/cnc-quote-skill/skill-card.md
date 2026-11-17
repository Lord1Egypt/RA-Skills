## Description:

AI-powered CNC machining quote system with risk detection, material optimization, and multi-channel integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT

## Use Case:

Manufacturers, machine shops, procurement teams, and developers use this skill to generate CNC machining quotes, flag order risks, suggest material or cost optimizations, and connect quoting workflows to QQ Bot, email, or API channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read or write local files while processing quote history, materials, configuration, or imports.

Mitigation: Install only after reviewing requested file permissions, and run it with the narrowest workspace and data access needed for quoting.

Risk: QQ, email, API, and DashScope integrations may expose proprietary drawings, customer contacts, quote history, or pricing data.

Mitigation: Do not connect sensitive production data until retention, self-learning behavior, and opt-out controls are documented and approved.

Risk: Installation-source details are unclear because server-resolved GitHub import provenance is unavailable.

Mitigation: Confirm the canonical publisher and repository, then prefer a pinned release or verified ClawHub package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/cnc-quote-skill)
- [Publisher profile](https://clawhub.ai/user/timo2026)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe quote totals, confidence scores, risk flags, optimization suggestions, integration snippets, and configuration settings.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact metadata, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
