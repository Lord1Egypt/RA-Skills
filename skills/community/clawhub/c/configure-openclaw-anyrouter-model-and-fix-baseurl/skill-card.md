## Description:

Helps agents merge AnyRouter model settings into OpenClaw, switch the main agent to `anyrouter/claude-opus-4-6`, and troubleshoot base URL, gateway, authentication, endpoint, and fallback issues with logs and live checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to update OpenClaw model routing while preserving existing providers, then verify whether AnyRouter Claude requests are actually served or are falling back. It can also guide ClaudeCode base URL alignment when the user explicitly asks to synchronize that local configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to make persistent changes to OpenClaw or ClaudeCode local configuration.

Mitigation: Require the agent to show the exact file diff and get confirmation before writing `openclaw.json`, restarting OpenClaw, or modifying `~/.claude/settings.json`.

Risk: Model routing can appear configured while requests still fail or fall back because of gateway, endpoint, or credential issues.

Mitigation: Verify behavior with live request checks and runtime logs, and clearly report when fallback handled the response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/can4hou6joeng4/skills/configure-openclaw-anyrouter-model-and-fix-baseurl)
- [AnyRouter gateway](https://anyrouter.top)
- [AnyRouter messages endpoint referenced by the skill](https://anyrouter.top/v1/messages)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code]

**Output Format:** [Markdown with JSON, shell command, and log snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent edits to local OpenClaw and ClaudeCode configuration; exact diffs and explicit user confirmation should precede writes or restarts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
