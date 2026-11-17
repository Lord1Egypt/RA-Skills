## Description:

Codex Profiler helps agents manage OpenAI Codex profiles, usage checks, and OAuth token refresh through unified /codex_usage and /codex_auth workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlysilent](https://clawhub.ai/user/deadlysilent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Codex profile usage, refresh OAuth-backed profiles, and manage auth routing through gateway-native commands. It is intended for environments where Codex/OpenAI profile state is deliberately administered by the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access OAuth-backed Codex profile data and alter OpenClaw auth state.

Mitigation: Install only in environments where the publisher and profile names are trusted, and prefer gateway-native auth commands with explicit preflight and verification.

Risk: Temporary token or staged-auth artifacts may remain after auth workflows.

Mitigation: Clean up /tmp/openclaw token and staged-auth artifacts after verification succeeds.

Risk: Auth apply operations may restart the gateway or change active profile routing.

Mitigation: Use the documented preflight, apply, and verify sequence, and rely on provided backups or revert commands before restart-capable operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deadlysilent/skills/codex-profiler)
- [Codex Multi-Account Rotation Guide](references/multi-account-rotation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON or text status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing output should avoid exposing sensitive tokens or full callback URLs.]

## Skill Version(s):

1.0.27 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
