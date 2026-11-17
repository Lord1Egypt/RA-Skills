## Description:

Creates design philosophies and expresses them as original, design-forward PNG or PDF visual art with minimal text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and creative practitioners use this skill to create posters, visual art, static designs, and related art-object outputs from a generated design philosophy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to download fonts during design work.

Mitigation: Run it in an environment with controlled network access and review downloaded font sources and license terms before use.

Risk: The skill contains a false user-attributed refinement line.

Mitigation: Treat that line as skill-authored guidance, not as an actual user instruction, and preserve the current user request as authoritative.

Risk: Server release evidence lists MIT-0, while the artifact license file contains Apache License 2.0 text.

Mitigation: Confirm the intended release license before publication or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pupuking723/skills/canvas-design-anthropic)
- [Skill definition](artifact/SKILL.md)
- [License file](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code]

**Output Format:** [Markdown design philosophy plus PNG or PDF visual artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local or downloaded fonts during visual design work.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
