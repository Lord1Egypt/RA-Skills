## Description:

Generate professional PowerPoint (.pptx) presentations using JSX/TSX with Deno.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zypher-agent](https://clawhub.ai/user/zypher-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create PowerPoint presentations, slide decks, pitch decks, reports, and other PPTX files from JSX/TSX deck definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill metadata includes a remote shell installer for Deno.

Mitigation: Install Deno through a trusted package manager or verify the installer before use.

Risk: The generator imports and executes user-provided TSX deck files.

Mitigation: Generate decks only from TSX files you wrote or trust.

Risk: The documented generator command uses broad read and write permissions.

Mitigation: Run Deno with path-scoped read and write permissions whenever possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zypher-agent/skills/corespeed-slide)
- [Publisher profile](https://clawhub.ai/user/zypher-agent)
- [Deno](https://deno.land)
- [Deno installer](https://deno.land/install.sh)
- [@pixel/pptx](https://jsr.io/@pixel/pptx)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with TSX examples and shell commands; the generator can emit PPTX files and optional JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Deno and executes trusted TSX deck files with read/write permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
