## Description:

Cclaw helps agents create comedy writing, generate FFmpeg-based video edits, and prepare comedy poster briefs for canvas-design workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kreator666](https://clawhub.ai/user/kreator666)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, performers, and developers use Cclaw to draft standup, sketch, manzai, scripts, satire, parody, and absurdist pieces, then turn selected material into FFmpeg video edits or poster design briefs for event and social assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg actions can modify or overwrite local media when commands or output paths are not reviewed.

Mitigation: Inspect each generated command and output path before running it, and keep original media files unchanged.

Risk: Bundled poster output scripts contain hard-coded personal file paths.

Mitigation: Do not run those scripts until paths have been replaced with explicit local inputs and destinations chosen by the user.

Risk: The server security verdict is suspicious because local command execution is under-scoped.

Mitigation: Review the skill before installation and limit execution to commands needed for the intended creative or media-production task.

## Reference(s):

- [Cclaw on ClawHub](https://clawhub.ai/kreator666/skills/cclaw)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Command Routing](commands.md)
- [Video Tool Workflow](modules/tools/video/README.md)
- [Poster Tool Workflow](modules/tools/poster/README.md)
- [Comedy Theory Reference](references/comedy-theory.md)
- [Comedy Template Reference](references/comedy-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional shell commands, generated creative text, design briefs, and code-oriented instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute FFmpeg workflows and may prepare poster briefs for another design skill; users should inspect commands and file paths before execution.]

## Skill Version(s):

1.10.0 (source: frontmatter, release evidence, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
