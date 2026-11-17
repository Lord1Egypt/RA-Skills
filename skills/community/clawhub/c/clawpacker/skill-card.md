## Description:

Use when exporting, importing, packaging, cloning, restoring, or moving an OpenClaw agent between machines or instances, especially when the user mentions clawpacker, .ocpkg packages, agent portability, or reusable agent templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lc708](https://clawhub.ai/user/lc708)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to move OpenClaw agents between machines or instances by fetching the current canonical clawpacker instructions before running package operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to fetch and follow live remote instructions that can change after review.

Mitigation: Vendor the full reviewed instructions locally, or pin the remote content by commit and verify it by hash before use.

Risk: Canonical instruction URLs may become unavailable during a packaging or restore task.

Mitigation: Stop and ask for an updated repository path or current local copy instead of guessing clawpacker commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lc708/skills/clawpacker)
- [Canonical clawpacker instructions URL from artifact](https://raw.githubusercontent.com/cogine-ai/clawpack/master/skills/clawpacker/SKILL.md)
- [Canonical clawpacker fallback URL from artifact](https://raw.githubusercontent.com/cogine-ai/clawpack/main/skills/clawpacker/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline URLs and command-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current remote canonical instructions at task time; stops and asks for an updated source if both listed URLs are unavailable.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
