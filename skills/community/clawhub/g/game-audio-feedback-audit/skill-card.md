## Description:

Audit the project's audio layer as UX feedback: UI sounds, success/failure signals, danger cues, layering, and semantic sound priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to audit an existing game's audio as part of the UX feedback system, including confirmation sounds, reward cues, danger signals, layering conflicts, and evidence quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit documentation can be incomplete or inaccurate when runtime audio behavior is not inspected.

Mitigation: Review generated audit files before committing them, and grant shell or build access only when runtime evidence is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mike007jd/skills/game-audio-feedback-audit)
- [Audio Feedback Audit Checklist](artifact/shared/checklists/audio-feedback-audit-checklist.md)
- [Audit Confidence and Evidence](artifact/shared/reference/audit-confidence-and-evidence.md)
- [Usage Examples](artifact/examples/usage.md)

## Skill Output:

**Output Type(s):** [markdown, json, guidance]

**Output Format:** [Markdown audit findings and JSON scorecard updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based findings should include confidence levels and evidence categories.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact bundle metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
