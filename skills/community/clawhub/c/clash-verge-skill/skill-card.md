## Description: <br>
Control Clash Verge Rev via the mihomo API to query proxy status, switch nodes, test delays, manage connections, DNS, and maintenance tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianping7](https://clawhub.ai/user/brianping7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage a local Clash Verge Rev or mihomo proxy, including proxy mode, node selection, latency checks, active connections, DNS queries, and maintenance actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform disruptive local proxy operations such as switching nodes, closing connections, flushing DNS, restarting the mihomo core, and updating GeoIP or GeoSite data. <br>
Mitigation: Require an explicit user request or confirmation before running commands that change proxy state, close traffic, restart services, or update databases. <br>
Risk: The broad activation scope around Clash, proxy, VPN, nodes, and network proxy management may bring the skill into sensitive network troubleshooting workflows. <br>
Mitigation: Review the intended command, target group or node, and expected effect before executing proxy-management actions. <br>
Risk: Status, connection, DNS, and rule commands can expose local network configuration or active connection details. <br>
Mitigation: Limit use to the local Clash or mihomo endpoint and avoid sharing connection metadata unless it is needed for the user's request. <br>


## Reference(s): <br>
- [Clash Verge Skill on ClawHub](https://clawhub.ai/brianping7/clash-verge-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
