## Description: <br>
Query and analyze Claude Code session data from a remote server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myakove](https://clawhub.ai/user/myakove) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Claude Code sessions, view conversation history and tool calls, search prompts, track tasks, and review usage statistics through a configured ccsinfo server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ccsinfo server can expose private Claude Code session history on the network. <br>
Mitigation: Use only a server you control, prefer binding it to 127.0.0.1 or a private VPN, and add firewall or authentication controls where available. <br>
Risk: Plain HTTP traffic on shared networks may expose sensitive session text. <br>
Mitigation: Avoid plain HTTP on shared networks and route access through trusted local or protected network paths. <br>
Risk: Retrieved session text may contain prompts, tool outputs, code, secrets, or old instructions. <br>
Mitigation: Treat retrieved session content as sensitive and untrusted, and review it before reuse or disclosure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myakove/ccsinfo) <br>
- [CLI commands reference](references/cli-commands.md) <br>
- [ccsinfo server repository](https://github.com/myk-org/ccsinfo) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON from the ccsinfo CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CCSINFO_SERVER_URL, the ccsinfo CLI, and network access to a ccsinfo server.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
