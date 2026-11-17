## Description:

Use when encountering any bug, test failure, or unexpected behavior before proposing fixes, enforcing a four-phase root-cause investigation before any code change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolz1](https://clawhub.ai/user/carolz1)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to debug technical failures systematically by reproducing issues, gathering evidence, identifying patterns, testing one hypothesis at a time, and applying a single verified root-cause fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic steps may expose environment values, signing identities, certificate-store details, or GPG key information in shared logs.

Mitigation: Prefer presence checks and redacted diagnostics, and require explicit approval before credential-store diagnostics or publishing diagnostic output.

Risk: Broad activation language may trigger the full debugging workflow for routine technical questions.

Mitigation: Apply the workflow when the user reports a bug, test failure, or unexpected behavior, and keep unrelated exploratory questions out of scope.

## Reference(s):

- [Server-resolved GitHub source import](https://github.com/CarolZ1/debugging)
- [ClawHub skill page](https://clawhub.ai/carolz1/skills/debugging-2)
- [Publisher profile](https://clawhub.ai/user/carolz1)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured debugging process; it does not require external services or dependencies.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
