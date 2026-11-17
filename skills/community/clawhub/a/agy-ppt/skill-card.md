## Description:

Orchestrates image-based PowerPoint presentations, with AGY directing the workflow, Kiro handling engineering, and Codex generating or editing slide images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sujunmin](https://clawhub.ai/user/sujunmin)

### License/Terms of Use:

MIT-0

## Use Case:

Presentation creators and developers use this skill to plan, review, generate, and assemble image-based slide decks with speaker notes and optional source-grounding checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image-artifact path handling may copy unintended local images into the project output.

Mitigation: Review before installing; require reported artifacts to resolve within the current generated-images thread directory before copying. Until fixed, avoid untrusted slide or source prompts and environments containing sensitive local images.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sujunmin/skills/agy-ppt)
- [Presentation workflow and approval gates](artifact/docs/workflow-gates-and-progress.md)
- [Image generation runtime](artifact/docs/codex-image-runtime.md)
- [Project assembly and reporting](artifact/docs/project-assembly-and-reporting.md)

## Skill Output:

**Output Type(s):** [Presentation files, Images, Markdown]

**Output Format:** [PPTX with slide images and Markdown speaker notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outline, visual style, and sample slide require approval before full-deck generation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
