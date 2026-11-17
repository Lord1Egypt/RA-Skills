## Description:

Diagnoses and fixes OpenClaw cron job model override issues by identifying rejected model selections and adding permitted models to the agent allowlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mklue](https://clawhub.ai/user/mklue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to diagnose cron jobs that reject configured model overrides, fall back to default cloud models, run slowly, or consume unexpected tokens. It guides them through log checks, allowlist validation, configuration updates, and gateway restart verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify the OpenClaw agent model allowlist configuration.

Mitigation: Confirm the model name is intentional, run the helper with --dry-run when possible, and create or keep a backup of ~/.openclaw/openclaw.json before applying changes.

Risk: A model format mismatch or missing provider definition can keep cron jobs falling back to defaults after the allowlist is changed.

Mitigation: Verify the model appears in the provider configuration and the agent allowlist using the same provider-prefixed format, then restart the gateway and inspect cron run history.

## Reference(s):

- [OpenClaw Model Configuration Layers](references/model-config-layers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and an optional Python helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may propose edits to ~/.openclaw/openclaw.json and requires gateway restart verification.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
