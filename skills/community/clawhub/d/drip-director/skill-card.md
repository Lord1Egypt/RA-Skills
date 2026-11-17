## Description:

Drip Director guides agents through a confirmed, multi-stage streetwear and fashion image generation pipeline using Nano Banana Pro for generation and Gemini for critique.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoneislandartur](https://clawhub.ai/user/stoneislandartur)

### License/Terms of Use:


## Use Case:

External users and image-production agents use this skill to turn a rough streetwear or fashion image request into a governed workflow with structured intake, constraint tracking, generation, critique, and regeneration from original references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images, briefs, and constraints may be sent to Google Gemini during critique.

Mitigation: Install only when that data sharing is acceptable, and avoid sensitive images or briefs unless Google API use is approved for the deployment.

Risk: Local file handling may process or delete the wrong files.

Mitigation: Use trusted session metadata for attachment paths, private temporary directories, and cleanup-path validation before deletion.

Risk: The workflow invokes local image-generation scripts whose source and version may vary by installation.

Mitigation: Pin or verify the generator before use and scan the installed skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stoneislandartur/skills/drip-director)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style conversational prompts, status blocks, structured reports, and bash commands for image generation and critique steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation between stages; may invoke local image-generation scripts and Google Gemini API calls.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
