## Description:

Inventories local agent skills, estimates their context footprint, identifies possible duplicates, and recommends which skills to keep or review before disabling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can review installed skill libraries, estimated context costs, usage signals, possible duplicates, and automation dependencies before deciding whether to disable any skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete usage records or undiscovered automation dependencies may make a needed skill appear safe to disable.

Mitigation: Review each candidate and its impact, include relevant dependency roots, and protect critical skills before making changes.

Risk: Applying close recommendations changes persistent WorkBuddy skill settings and can affect agent behavior.

Mitigation: Inspect the dry run and backup, then use --apply --yes only after explicitly choosing which skills to disable; restore settings if needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/elisabeth15501/skills/agent-skill-inventory)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text inventory and recommendations, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; optional, user-approved settings changes and saved language preference.]

## Skill Version(s):

1.5.3 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
