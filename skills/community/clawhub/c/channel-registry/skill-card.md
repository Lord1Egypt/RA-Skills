## Description:

Registers and queries brand-owned social channel state, cadence, governance, voice-adaptation, UGC-permission, and advocacy facts through append-only registry records and derived views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, social, and governance operators use this skill to record or query authoritative facts for brand-owned channels, UGC permissions, advocate opt-ins, cadence commitments, and proposal decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent channel events or proposal decisions may be written in a full root-runtime install.

Mitigation: Confirm explicit user authorization and review intended registry changes before using write or proposal-decision paths.

Risk: Channel exports, public posts, tags, or hashtags can be mistaken for permission or canonical state evidence.

Mitigation: Require source, date, scope, expiry, and current revision evidence before accepting permissions or channel-state changes.

## Reference(s):

- [Channel Registry on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/channel-registry)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with handoff summaries, registry event instructions, and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit authorization before persistent registry writes; standalone installs may prepare proposals only.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
