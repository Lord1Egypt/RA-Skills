## Description:

Generate professional PowerPoint (.pptx) presentations using JSX/TSX with Deno, including slides, text, shapes, tables, charts, images, gradients, shadows, and flexible layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-bot](https://clawhub.ai/user/claw-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create slide decks, pitch decks, reports, and other PowerPoint files from JSX/TSX presentation source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs generated slide code with broad local file read/write access and references a remote Deno installer.

Mitigation: Use only trusted TSX slide files, avoid running in directories containing secrets, install Deno through a trusted package manager, and prefer a lockfile with narrowly scoped Deno permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claw-bot/skills/corespeed-pptx)
- [claw-bot publisher profile](https://clawhub.ai/user/claw-bot)
- [@pixel/pptx package](https://jsr.io/@pixel/pptx)
- [Deno](https://deno.land)
- [Corespeed](https://corespeed.io)
- [Corespeed skills issues](https://github.com/corespeed-io/skills/issues)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Configuration instructions]

**Output Format:** [TSX presentation source, shell command output, optional JSON status, and generated .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Deno and runs TSX slide files with local read/write permissions.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
