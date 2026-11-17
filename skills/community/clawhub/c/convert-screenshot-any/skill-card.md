## Description:

Converts a screenshot of a UI into a detailed prompt for AI image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agent users can use this skill to convert UI screenshot descriptions into image-generation prompt text. The artifact also contains generic data-conversion instructions, so users should confirm the requested screenshot-to-prompt behavior before relying on the output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect screenshot-to-prompt behavior while the main instructions describe generic data conversion.

Mitigation: Review the skill behavior before deployment and correct the documentation or implementation so the advertised purpose matches the instructions.

Risk: Generated conversion or prompt output may be misleading if the input format or screenshot description is ambiguous.

Mitigation: Require validation notes and human review for important outputs before using them in design or generation workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/convert-screenshot-any)
- [Server metadata source](https://github.com/MiniMax-AI/skills)
- [Skill reference index](references/index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown, with optional shell commands for local helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated prompt text, validation notes, and mapping summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence and changelog, released 2026-05-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
