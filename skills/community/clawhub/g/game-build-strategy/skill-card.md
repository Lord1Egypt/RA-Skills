## Description:

Decide the AI-native development mode, quality target, task granularity, and refactor policy based on project state and user intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose an evidence-based game build mode, quality target, task size, and refactor policy for greenfield, product-facing, or live-risk game projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated planning documents could steer broad changes in shipped or live-risk game projects.

Mitigation: Review docs/game-studio/build-strategy.md and docs/game-studio/quality-target.md before acting on them, especially when the selected mode is surgical-live or the project is already shipped.

Risk: The skill writes project planning files as part of normal use.

Mitigation: Confirm generated documentation changes before committing or applying the resulting strategy to implementation work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mike007jd/skills/game-build-strategy)
- [Publisher Profile](https://clawhub.ai/user/mike007jd)
- [Development Modes](artifact/shared/reference/development-modes.md)
- [Quality Targets](artifact/shared/reference/quality-targets.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown planning documents and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update docs/game-studio/build-strategy.md and docs/game-studio/quality-target.md in the user's project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
