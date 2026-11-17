## Description:

Bridges OpenClaw to the local Claude Code CLI so an OpenClaw agent can delegate tasks to Claude Code and return results to the user's channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[is-xins-xiaobai](https://clawhub.ai/user/is-xins-xiaobai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route multi-step work from OpenClaw into local Claude Code sessions, then receive summarized results back in their chat channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated Claude runs without interactive permission prompts under the user's account.

Mitigation: Use only in trusted, single-user OpenClaw setups and trusted project directories; review delegated tasks before launch.

Risk: Cross-session messaging and broad message-tool access can be unsafe in shared deployments.

Mitigation: Avoid enabling global session visibility on shared deployments and restrict gateway message access to trusted local use.

Risk: Generated session files and logs may retain task context or sensitive output.

Mitigation: Avoid sending secrets in prompts, and inspect or clear generated logs and session files after use.

## Reference(s):

- [Claw2Claude ClawHub skill page](https://clawhub.ai/is-xins-xiaobai/skills/claw2claude)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown chat summaries with optional code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated Claude output is summarized and chunked for chat delivery; project session state and logs may be written locally.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
