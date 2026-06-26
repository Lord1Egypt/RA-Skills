## Description: <br>
Manages Clash proxy nodes by listing current node status, available nodes in groups, and switching to specified nodes by name or index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YonghaoZhao722](https://clawhub.ai/user/YonghaoZhao722) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect a local Clash proxy controller, list available proxy nodes, and switch the active node when managing proxy routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local Clash proxy details and switch the active proxy node. <br>
Mitigation: Install it only when that behavior is desired, keep the Clash control API bound to localhost, and verify node and group names before switching. <br>
Risk: A Clash API secret, if configured, protects proxy controller access. <br>
Mitigation: Protect the API secret and avoid exposing the controller beyond the local machine. <br>
Risk: Unusual proxy or group names can be misread when passed through a shell. <br>
Mitigation: Quote unusual node and group names when invoking the script from a shell. <br>


## Reference(s): <br>
- [Clash Node Manager on ClawHub](https://clawhub.ai/YonghaoZhao722/clash-node-manager) <br>
- [check_clash.py](artifact/check_clash.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Clash proxy group names, node names, connection counts, and switch results returned by the local controller.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
