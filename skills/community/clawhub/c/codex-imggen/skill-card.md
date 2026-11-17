## Description:

Generates images through Codex CLI with size controls, optional reference images, and batch game UI asset prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate single images, targeted size or aspect-ratio images, and batch game UI image sheets through Codex CLI. It is useful when an agent needs repeatable shell-command guidance for image generation and copying PNG outputs to a requested directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference images may be sent outside the local machine through Codex CLI.

Mitigation: Use only approved Codex accounts, proxy settings, sandboxes, and data-handling policies; avoid confidential prompts, private artwork, internal screenshots, regulated data, and sensitive local image files unless approved.

Risk: The copy step can select the newest shared Codex generated-image directory rather than a guaranteed current-session result.

Mitigation: Run the skill in a restricted, disposable workspace and visually verify the copied output before using or publishing it.

Risk: Requested pixel dimensions may not be exact because the documented Codex CLI image output is constrained to about 1.57 megapixels.

Mitigation: Use the documented safe size keys when possible, and post-process with an image tool when exact final dimensions are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/codex-imggen)
- [ClawHub publisher profile](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are copied from ~/.codex/generated_images/ to the requested output directory; batch mode writes a combined PNG image.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
