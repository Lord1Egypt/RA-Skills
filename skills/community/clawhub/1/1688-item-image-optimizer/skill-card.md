## Description:

Routes 1688 sellers to product image workflows for main image optimization, carousel images, detail images, background replacement, and digital model generation through permission checks and tool-page URL construction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 sellers use this skill to choose and open the correct product-image creation tool for main images, carousels, detail images, background replacement, or digital model generation. The skill can also configure access credentials and verify digital model permission before routing restricted workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist a 1688 access key in local OpenClaw configuration.

Mitigation: Install only where local credential persistence is permitted; use scoped credentials where available and rotate or remove the key when the skill is no longer needed.

Risk: The skill sends authenticated usage telemetry through the 1688 gateway after CLI commands.

Mitigation: Review telemetry acceptability before installation and deploy only in environments where this reporting is allowed.

Risk: Opened tool URLs may include a session identifier and image or offer parameters.

Mitigation: Avoid sharing generated tool URLs or logs that contain them, and confirm that session handling matches the account's data-handling policy.

Risk: Workflow instructions can limit what the parent agent says after execution.

Mitigation: Review and test workflow behavior before deployment so suppressed responses do not hide errors or unexpected outcomes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-item-image-optimizer)
- [Interaction specs](references/interaction-specs.md)
- [1688 image tool entrypoint](https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command results, Markdown messages, and OpenClaw interaction payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open 1688 tool pages, show image-type or image-selection cards, and return fail-closed guidance when permission checks fail.]

## Skill Version(s):

0.51.0 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
