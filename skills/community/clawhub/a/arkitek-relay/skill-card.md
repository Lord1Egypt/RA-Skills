## Description: <br>
Connect this agent to ArkiTek for secure remote chat via SSE without tunnels or open ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raleighgardner16-source](https://clawhub.ai/user/raleighgardner16-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use ArkiTek Relay to connect an OpenClaw agent to ArkiTek for remote chat while keeping the agent behind outbound-only connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The relay uses an API key to connect an agent to a remote chat service. <br>
Mitigation: Treat ARKITEK_API_KEY as a secret, avoid logging or sharing it, and revoke or rotate the key when access is no longer needed. <br>
Risk: Running the relay keeps remote chat access active through a background connection. <br>
Mitigation: Run the relay only when remote access is intended and stop the process when the session should end. <br>
Risk: The relay runs an npm package as part of the connection workflow. <br>
Mitigation: Install and run it only when you trust ArkiTek and the arkitek-relay-skill package. <br>


## Reference(s): <br>
- [ArkiTek homepage](https://arkitekai.com) <br>
- [ClawHub skill page](https://clawhub.ai/raleighgardner16-source/arkitek-relay) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, and an ARKITEK_API_KEY secret to run the relay.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
