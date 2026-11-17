## Description:

Hybrid reload mode auto-restarts for gateway/plugins changes. Config patching requires baseHash from config.get first. Minimax cron auth uses system-level tokens, not session OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabbykst](https://clawhub.ai/user/rabbykst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw gateway exec denials and apply narrowly scoped, hash-verified configuration changes for allowlist, reload, and Minimax authentication issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad gateway security-profile changes can expose more exec capability than intended.

Mitigation: Prefer a narrowly scoped exec allowlist fix over switching to a full tools profile, then verify the resulting configuration.

Risk: Gateway configuration changes can fail or affect restart-required and protected paths.

Mitigation: Capture the baseHash with config.get before config.patch, respect protected paths, and confirm a rollback or restart path before applying changes.

Risk: Credential fallback steps can lead to plaintext API key handling.

Mitigation: Avoid plaintext API keys where possible and use approved secret handling for Minimax provider credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rabbykst/skills/fix-exec-allowlist-miss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with inline gateway and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes config patch workflow, restart guidance, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
