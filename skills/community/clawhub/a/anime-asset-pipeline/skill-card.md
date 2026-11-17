## Description:

Pipeline for producing anime/2D character art with an AI image model, focused on identity locking, per-region defect checking, and 8-bit quantization budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and artists use this skill to produce consistent anime and 2D character art across sprite sheets, key visuals, and music-video frames. It guides identity anchoring, per-region defect checks, and decisions that avoid spending on visually negligible changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image generation can incur provider costs, and a provider may be unavailable in a session.

Mitigation: Check provider availability and the expected balance or cost before starting a generation run.

Risk: Mechanical checklist results can be mistaken for visual approval of generated art.

Mitigation: Use checklists to catch defects, then obtain separate human visual approval.

## Reference(s):

- [Identity lock](references/identity-lock.md)
- [Per-region defect checklist](references/defect-checklist.md)
- [8-bit quantisation budget](references/8bit-budget.md)
- [Channel preflight](references/channel-preflight.md)
- [Review report template](assets/review-report-template.md)
- [ClawHub release page](https://clawhub.ai/catsmansion/skills/anime-asset-pipeline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance and review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
