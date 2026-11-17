## Description:

Run a narrow compare between two or three backend profiles when architecture uncertainty is real.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers and engineers use this skill to compare two or three plausible backend profiles for a game project and record the decision, criteria, rationale, and cost note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compare mode can spend extra agent time and tokens when the backend choice is already obvious.

Mitigation: Use the skill only when architecture uncertainty is real and include the requested token or cost note in the decision record.

Risk: The workflow may update project documentation with an incorrect or weakly supported backend decision.

Mitigation: Review the compared options, criteria, and rationale before accepting changes to docs/game-studio/backend-decision.md.

## Reference(s):

- [README](artifact/README.md)
- [Usage Examples](artifact/examples/usage.md)
- [Smoke Test](artifact/tests/smoke.md)
- [ClawHub Skill Page](https://clawhub.ai/mike007jd/skills/game-compare-backends)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown decision note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an evidence-based backend comparison and cost note for docs/game-studio/backend-decision.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
