## Description:

Helps agents guide character consistency work for AI-generated images using reference sheets, detailed prompt anchors, LoRA techniques, color palettes, and inference.sh commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Artists, game developers, illustrators, animators, and visual-novel or comics creators use this skill to create repeatable character reference material and prompts for consistent AI-generated character images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start asks users to run a mutable remote shell installer and then authenticate with the CLI.

Mitigation: Review the installer source first, prefer a pinned and separately verified manual install, and avoid using sensitive environments unless the distribution path and token storage are trusted.

Risk: The related skill installation commands are optional and may install unpinned dependencies.

Mitigation: Skip those commands unless their sources and versions have been verified or pinned.

## Reference(s):

- [Character Design Sheet on ClawHub](https://clawhub.ai/okaris/skills/character-design-sheet)
- [Publisher profile](https://clawhub.ai/user/okaris)
- [inference.sh](https://inference.sh)
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON command inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt templates, reference-sheet layouts, color palette values, and LoRA setup guidance.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
