## Description: <br>
Secure MCP bridge enabling Claude on your phone to browse and edit local repos with real-time, human-approved file access and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to connect Claude clients to local repositories through an approval-gated MCP bridge, so the agent can browse files and request human-approved reads or writes while activity is audited. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval, audit, WebSocket, and MCP surfaces can be reachable without uniform authentication if the bridge is exposed over LAN or a public tunnel. <br>
Mitigation: Run it on localhost or behind strong private access controls, and add authentication before exposing it through a LAN or public tunnel. <br>
Risk: Printed or shared bearer tokens and exposed workspace roots can allow unintended local file access. <br>
Mitigation: Rotate shared tokens and treat configured workspace roots as writable by anyone who can reach the service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/claude-local-bridge) <br>
- [README](artifact/README.md) <br>
- [Tunnel setup guide](artifact/tunnel.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [MCP tool responses and Markdown guidance with inline shell and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured workspace roots and human approval before file reads or writes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
