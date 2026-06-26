## Description: <br>
Control cmux terminal multiplexer via its Unix socket API to manage workspaces, surfaces, terminal input, notifications, sidebar metadata, and system state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnwangjie](https://clawhub.ai/user/cnwangjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect and control a local cmux terminal multiplexer session, including workspace navigation, pane management, terminal input, notifications, and status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send text or key presses into terminal surfaces. <br>
Mitigation: Require confirmation before terminal input is sent, and target explicit workspace and surface identifiers. <br>
Risk: The skill can close cmux workspaces. <br>
Mitigation: Require confirmation before closing workspaces and verify the target workspace before executing the action. <br>
Risk: The skill controls whichever cmux socket it is pointed at. <br>
Mitigation: Keep CMUX_SOCKET_PATH pointed at the intended socket and avoid using ambiguous default sessions when multiple cmux instances are active. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnwangjie/cmux) <br>
- [Publisher profile](https://clawhub.ai/user/cnwangjie) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands, JSON-RPC examples, and Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cmux CLI or a Unix socket at /tmp/cmux.sock, with CMUX_SOCKET_PATH available for alternate socket paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
