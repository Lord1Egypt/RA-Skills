## Description:

Distill colleagues' work styles, thinking patterns, and institutional knowledge into local profiles that deepen with each user-provided observation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn their own observations about colleagues into structured work-style profiles, collaboration guidance, and institutional-memory notes. It supports active collaboration, onboarding, team-dynamics questions, and continuity after colleagues leave.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent profiles about coworkers.

Mitigation: Record only work-relevant observations with reasonable consent, follow workplace policy, and delete stale profiles periodically.

Risk: Profiles may capture sensitive or speculative personal information.

Mitigation: Avoid health, stress, financial, relationship, rumor, and HR-like judgments; use confidence levels and factual observations.

Risk: Local profile files may expose colleague information if shared or synced unintentionally.

Mitigation: Use safe profile identifiers instead of raw names when appropriate and keep the ~/.colleague-skill directory out of shared or synced locations.

## Reference(s):

- [Colleague.skill ClawHub listing](https://clawhub.ai/realteamprinz/skills/colleague)
- [README](artifact/README.md)
- [Work Style Dimensions Reference Guide](artifact/references/work-style-dimensions.md)
- [Colleague Profile Template](artifact/templates/COLLEAGUE-PROFILE.md)
- [Interaction Log Template](artifact/templates/INTERACTION-LOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown profiles, JSONL interaction logs, and natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores human-readable colleague profiles and observation logs locally under ~/.colleague-skill/.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
