## Description:

Audit interaction feedback quality: input acknowledgment, hit/collect/reward/failure signaling, danger telegraphing, and state-transition clarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers and designers use this skill to audit whether a game clearly responds to player actions and communicates rewards, denials, danger, failures, and state transitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to write audit files under docs/game-studio/audit, which may be inappropriate in some workspaces.

Mitigation: Use it only where those audit-path writes are acceptable, and review generated audit files before committing or sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mike007jd/skills/game-feedback-audit)
- [Feedback Audit Checklist](shared/checklists/feedback-audit-checklist.md)
- [Game Feel Pillars](shared/checklists/game-feel-pillars.md)
- [Audit Confidence and Evidence](shared/reference/audit-confidence-and-evidence.md)
- [Usage Examples](examples/usage.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown audit files, JSON scorecard, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs are audit notes and a scorecard under docs/game-studio/audit when the skill is applied to a project.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
