## Description:

Stream coding agent sessions to a Discord channel in real time via webhook, formatting agent events such as tool calls, file changes, shell commands, command output, and completion summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allanjeng](https://clawhub.ai/user/allanjeng)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use Codecast to make coding-agent sessions observable in Discord, including live command output, file activity, status updates, and completion summaries. It also supports PR review, parallel task, replay, and interactive bridge workflows when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Streaming coding-agent sessions to Discord can expose secrets, source code, local paths, prompts, command output, and other sensitive work.

Mitigation: Use only private, trusted Discord destinations; review streamed content expectations before use; avoid sessions involving secrets or confidential repositories unless the destination is approved.

Risk: Broad permission bypass can allow an inner agent to take actions without normal confirmation prompts.

Mitigation: Avoid global permission bypass by default, run with the least privileges that support the task, and review scripts and commands before starting a relay session.

Risk: Interactive bridge controls can forward Discord messages to local agent sessions or affect local processes if channel and user scope are too broad.

Mitigation: Disable the bridge unless needed, require explicit channel and user allowlists, and protect Discord bot tokens and webhook URLs.

Risk: PR review and parallel task modes can process untrusted repositories, pull requests, or task files.

Mitigation: Do not run PR review or parallel task mode on untrusted input until eval usage is fixed; inspect inputs and use isolated working directories when these modes are enabled.

## Reference(s):

- [Setup guide](references/setup.md)
- [Advanced modes](references/advanced-modes.md)
- [Discord output](references/discord-output.md)
- [ClawHub skill page](https://clawhub.ai/allanjeng/skills/codecast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; scripts relay JSONL or raw CLI streams into Discord messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime relay output may include file activity, command output, tool usage, token usage, cost, and completion summaries; Discord posts are rate-limited and may be batched.]

## Skill Version(s):

4.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
