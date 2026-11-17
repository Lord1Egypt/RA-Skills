## Description:

Convert apparel sketches into ecommerce-ready colorized shell-jacket renders. Use when users provide garment line art and ask for realistic colorized outputs (especially womens outdoor shell/hardshell), structure-preserving edits, or iterative visual refinements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bananooo-zhang](https://clawhub.ai/user/bananooo-zhang)

### License/Terms of Use:


## Use Case:

External users and design teams use this skill to turn garment line art into ecommerce-style shell jacket renders while preserving key sketch structure. It supports initial colorization and focused revisions using optional style reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's API key and design images to a hard-coded third-party endpoint.

Mitigation: Use it only with design assets approved for upload to models.kapon.cloud, and use a restricted or disposable API key.

Risk: The runtime installs remote Python dependencies and calls an external image generation service.

Mitigation: Review the skill before installation, avoid running it in an environment with unrelated secrets, and pin dependencies before use.

## Reference(s):

- [Prompt Structure](references/prompt-structure.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Guidance]

**Output Format:** [PNG image files with text file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates 1 to 6 PNG variants; default count is 3.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
