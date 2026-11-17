## Description:

Author a new HyperFrames registry block (caption style, VFX block, transition, lower third) or component (text effect, overlay, snippet) and ship it as an upstream PR to the hyperframes repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-kay8](https://clawhub.ai/user/lucas-kay8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to create, validate, preview, and submit new HyperFrames catalog blocks or components as upstream pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to run contribution and publishing commands that may affect a checkout or remote project.

Mitigation: Review each command before execution and run the workflow in a clean checkout or container.

Risk: Generated templates load third-party scripts from public CDNs.

Mitigation: Vendor dependencies or add integrity controls before using generated templates in stricter environments.

Risk: Unpinned external tooling can change behavior over time.

Mitigation: Use locked or pinned project dependencies for hyperframes, oxfmt, and tsx.

## Reference(s):

- [Contribute Templates](templates.md)
- [HyperFrames registry item schema](https://hyperframes.heygen.com/schema/registry-item.json)
- [ClawHub skill page](https://clawhub.ai/lucas-kay8/skills/contribute-catalog)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, HTML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scaffold patterns, validation steps, preview guidance, and pull request instructions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
