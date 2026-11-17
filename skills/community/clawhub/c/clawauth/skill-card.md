## Description:

Let agents request OAuth access from end users via short links, continue working asynchronously, and later claim reusable third-party API tokens from local keychain storage instead of a centralized SaaS token vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to request user-delegated OAuth access through short links, continue working asynchronously, and later claim provider tokens from local keychain storage for operator-controlled API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may handle reusable OAuth token payloads in command output.

Mitigation: Route token-bearing output through operator-controlled secret handling and redact it from chat, logs, traces, and telemetry.

Risk: An unpinned global CLI install can create supply-chain and version-drift risk.

Mitigation: Use an operator-approved, pinned `clawauth` build in a trusted runtime image instead of ad-hoc global npm installs.

## Reference(s):

- [Clawauth commands reference](references/commands.md)
- [Clawauth hosted service](https://auth.clawauth.app)
- [OpenClaw skill docs](https://docs.openclaw.ai/tools/skills)
- [OpenClaw macOS skill docs](https://docs.openclaw.ai/platforms/mac/skills)
- [Clawauth source code](https://github.com/claw-auth/clawauth)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON field names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output should preserve secret boundaries by avoiding raw token disclosure in chat, logs, traces, telemetry, or shell environment variables.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
