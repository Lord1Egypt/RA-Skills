## Description:

Query and analyze Claude Code session data from a remote server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myakove](https://clawhub.ai/user/myakove)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect Claude Code session history, messages, tool calls, tasks, project activity, and usage statistics through a configured ccsinfo server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ccsinfo server can expose Claude Code conversations, prompts, tool outputs, project paths, and possibly secrets over the network.

Mitigation: Install only for trusted servers, prefer 127.0.0.1 with SSH tunneling or VPN for remote access, avoid plaintext LAN exposure unless protected by strong network controls and authentication, and pin the CLI/server version.

## Reference(s):

- [ccsinfo CLI Commands Reference](references/cli-commands.md)
- [ClawHub skill page](https://clawhub.ai/myakove/skills/ccsinfo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CCSINFO_SERVER_URL and the ccsinfo CLI; many commands can return JSON with --json.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
