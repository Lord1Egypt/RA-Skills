## Description:

Clawtrix Skill Advisor helps agents audit installed skills for unused or risky entries and recommend mission-relevant additions using ClawHub search and optional peer signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicope](https://clawhub.ai/user/nicope)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to review installed agent skills, identify dead weight, check for updates, and receive advisory recommendations for skills that match the agent mission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mission-derived search terms may reveal sensitive client, project, or business context to public APIs.

Mitigation: Review the agent mission and redact sensitive terms before using the skill, or disable recurring audits when sensitive context is present.

Risk: Automatic heartbeat use can create recurring audits that may be broader than the user intended.

Mitigation: Run the skill on demand or require explicit user approval before scheduled skill-stack reviews.

Risk: Skill recommendations and promotional footer text may be mistaken for neutral system guidance.

Mitigation: Treat all recommendations as advisory and require owner review before installing, removing, or changing skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicope/skills/clawtrix-skill-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefing with inline shell commands and recommendation lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are advisory; the skill instructs the agent not to install or remove skills without owner approval.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
