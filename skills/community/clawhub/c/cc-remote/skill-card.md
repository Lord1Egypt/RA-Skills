## Description:

Routes prompts to Claude Code on a remote host through FastAPI, Redis, or SSH Screen with retry and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzz123hash](https://clawhub.ai/user/zzz123hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to dispatch Claude Code tasks to configured remote machines and collect execution results through FastAPI, Redis, or SSH Screen channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose unauthenticated remote execution paths through FastAPI and Redis.

Mitigation: Use only on trusted private networks and trusted hosts after adding authentication and access controls to FastAPI and Redis.

Risk: Claude Code permission checks are disabled in the generated worker execution path.

Mitigation: Remove permission bypass before operational use and require review of remote prompts and target directories.

Risk: The SSH Screen fallback runs prompt text through a remote shell and disables strict host-key checking in the executor.

Mitigation: Disable shell-based prompt execution or strictly constrain prompts, and restore SSH host-key verification before use.

Risk: Background worker and API services may keep running after deployment.

Mitigation: Define stop, uninstall, logging, and monitoring procedures for all deployed background services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzz123hash/skills/cc-remote)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may include task identifiers, execution status, selected channel, truncated stdout, and truncated error text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
