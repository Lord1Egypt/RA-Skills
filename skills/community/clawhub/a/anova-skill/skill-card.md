## Description: <br>
Control Anova Precision Ovens and Precision Cookers (sous vide) via WiFi WebSocket API. Start cooking modes (sous vide, roasting, steam), set temperatures, monitor status, and stop cooking remotely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodeja](https://clawhub.ai/user/dodeja) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent list, monitor, start, and stop supported Anova WiFi cooking devices from natural-language requests. It is intended for users who already have an Anova device, an Anova personal access token, and a configured Python environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can remotely start or stop a real heating appliance. <br>
Mitigation: Require explicit user confirmation before start, stop, or temperature-changing commands. <br>
Risk: Commands may target the first discovered device rather than the intended appliance. <br>
Mitigation: Verify the Anova device identity before running cooking or stop commands. <br>
Risk: Temperature, humidity, fan speed, and duration inputs may lack sufficient guardrails for regular use. <br>
Mitigation: Add operational range limits and review requested settings before execution. <br>
Risk: The Python dependency is declared with an open lower bound. <br>
Mitigation: Pin and review dependencies before regular or automated use. <br>


## Reference(s): <br>
- [Anova Developer Portal](https://developer.anovaculinary.com) <br>
- [Anova WiFi Device Controller Reference](https://github.com/anova-culinary/developer-project-wifi) <br>
- [Skill Repository](https://github.com/dodeja/anova-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/dodeja/anova-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may start, stop, or monitor real heating appliances through the Anova cloud API.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
