## Description: <br>
Fusion 360 Bridge helps agents inspect and control Autodesk Fusion 360 over HTTP through the Fusion Bridge add-in, including health checks, state inspection, logs, and raw Python execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smicbee](https://clawhub.ai/user/smicbee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CAD automation users use this skill to connect an agent to a trusted Fusion Bridge environment, inspect Fusion runtime state, review logs, and generate Python or HTTP requests for Fusion 360 modeling tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge exposes raw Python execution through a network-reachable HTTP service. <br>
Mitigation: Run it only in a trusted environment, prefer localhost-only binding or firewall restrictions, and do not expose TCP port 8765 to untrusted networks. <br>
Risk: Agent-generated Python can modify open Fusion 360 projects or affect the host running Fusion. <br>
Mitigation: Review raw Python before execution, checkpoint important designs, and use small helper-style snippets before larger scripts. <br>
Risk: Long-running or UI-blocking Fusion code can stall bridge work until timeout. <br>
Mitigation: Use concise snippets, reserve blocking UI popups for deliberate checkpoints, inspect logs, and keep execution time within the bridge timeout. <br>


## Reference(s): <br>
- [Fusion 360 Bridge ClawHub page](https://clawhub.ai/smicbee/fusion-bridge) <br>
- [Fusion 360 Bridge source repository](https://github.com/smicbee/fusion-360-bridge) <br>
- [Fusion Bridge API Reference](references/api.md) <br>
- [Fusion Bridge Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw Python snippets and HTTP request examples for a local Fusion Bridge instance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
