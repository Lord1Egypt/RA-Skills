## Description:

Choose or compare backend profiles based on required capabilities, project state, and quality target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to choose or compare backend profiles for browser or engine-based game projects. It helps produce an evidence-based backend decision note that accounts for project state, required capabilities, tradeoffs, and companion specialist follow-through.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project context and write a backend decision note under docs/game-studio/.

Mitigation: Review the proposed decision document before relying on it for project planning.

Risk: The skill references companion specialists that are not bundled with this release.

Mitigation: Install or invoke companion specialist skills only when follow-up implementation guidance is desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mike007jd/skills/game-backend-selector)
- [Backend Profiles](shared/reference/backend-profiles.md)
- [Usage Examples](examples/usage.md)
- [Smoke Test](tests/smoke.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown decision document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally writes docs/game-studio/backend-decision.md and may recommend separate companion specialist skills for follow-up.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
