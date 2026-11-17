## Description:

Checks whether an important prior tool action actually took effect by comparing the tool's reported outcome with observed wire evidence, then returns a verdict such as CONFIRMED, SILENT_FAILURE, UNVERIFIED, or FAILED.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after consequential tool calls to decide whether to build on the result, treat it as not done, verify the effect directly, or fix and retry. It is intended for actions such as command execution, file writes, POST/PUT/DELETE requests, message sends, and fetches that later work depends on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Most checks depend on the external ClawPhylax plugin and its local ledger; without it, some actions may be UNVERIFIED.

Mitigation: Install and enable the ClawPhylax plugin when available, or verify important effects directly before reporting success.

Risk: The security review notes that the plugin dependency is not bundled in this artifact.

Mitigation: Review and install the plugin separately, and rely on the artifact security verdict only for this skill text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/did-that-actually-work)
- [ClawPhylax project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like text with a first-line ACTION verdict and evidence, caution, next-step, and scope sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts are limited to CONFIRMED, SILENT_FAILURE, UNVERIFIED, or FAILED, with a corresponding action recommendation.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
