## Description:

Ai Reviewer produces structured quality review reports for e-commerce image outputs against configurable checklist criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhihai123](https://clawhub.ai/user/duzhihai123)

### License/Terms of Use:

MIT-0

## Use Case:

Creative operations teams and agents use this skill to summarize e-commerce image quality checks, classify pass/revision outcomes, and provide improvement suggestions for generated product imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as an image quality gate, but the authoritative security review says it does not actually inspect images and deterministically approves them.

Mitigation: Treat it as a prototype or workflow stub; do not rely on it to approve e-commerce images until real image analysis is implemented and independently verified.

Risk: Review metadata may be appended to a local history file, which can expose review activity if the metadata is sensitive.

Mitigation: Review the local history logging behavior before using the skill with sensitive projects, products, or customer material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhihai123/skills/ai-reviewer)
- [Publisher profile](https://clawhub.ai/user/duzhihai123)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [JSON quality report with summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verdict, average score, image-level reports, issues, suggestions, and checklist details.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
