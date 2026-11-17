## Description:

Codex Auth is a deprecated OpenClaw/Codex OAuth helper that starts an OpenAI login flow and applies callback tokens to local auth profile files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlysilent](https://clawhub.ai/user/deadlysilent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining legacy OpenClaw Codex profile authentication use this skill to run the deprecated /codex_auth flow, generate an OAuth login URL, and apply returned callback credentials to local auth profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived OAuth access and refresh tokens and stores pending OAuth state under /tmp.

Mitigation: Install only if comfortable with local token writes; avoid queue mode until token staging is moved out of /tmp, permissions are forced to 0600, queued payloads are deleted after use, and callback URLs are not passed through shell command arguments.

Risk: Queued apply mode can restart the local gateway in the background.

Mitigation: Use queued apply only during planned maintenance windows and review the emitted revert command and backups before relying on the updated profile.

Risk: The standalone codex-auth path is deprecated and no longer maintained as the primary workflow.

Mitigation: Prefer the maintained codex-profiler path for ongoing /codex_auth and /codex_usage operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadlysilent/skills/codex-auth)
- [Artifact security notes](artifact/SECURITY.md)
- [Artifact risk policy](artifact/RISK.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile-targeted OAuth start, finish, queued apply, and status flows for local OpenClaw auth profiles.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
