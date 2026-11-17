## Description:

Turn a written credit-card benefits table into one credit-rights voice clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External finance and credit-content teams use this skill to convert an already-written credit-card benefits table into a labeled pack of 8 to 20 spoken clips. It supports catalog voices or an authorized cloned staff voice, with separate approval before paid clone or speech generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package requests a shared Beatra account token with broad media, artifact, task, and spending capabilities.

Mitigation: Install only when those account powers are acceptable, and revoke or disconnect the device when Beatra access is no longer needed.

Risk: The bundled client silently checks for and installs package updates by default, which can change reviewed code after installation.

Mitigation: Disable automatic updates before use when reviewed code must remain fixed.

Risk: Staff voice samples can be uploaded for cloning, creating likeness and consent risk.

Mitigation: Use only samples with explicit likeness and voice rights, inspect the sample before upload, and keep clone and speech approval steps separate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/credit-rights-voice)
- [Beatra Skill Homepage](https://beatra.ai/skills/credit-rights-voice)
- [Credit rights voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown with JSON and shell command snippets, plus returned audio artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans 8 to 20 labeled clips and may return generated MP3 audio artifacts with actual usage and billing details.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
