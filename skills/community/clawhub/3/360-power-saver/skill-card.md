## Description: <br>
360 Power Saver helps agents guide local power, battery, CPU, memory, and energy diagnostics, including battery reports, energy analysis, and power-plan switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttqftech](https://clawhub.ai/user/ttqftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to inspect local power state, battery health, CPU and memory load, energy reports, and available power plans before suggesting or applying power-saving actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request elevated permissions for Windows powercfg actions such as energy reports or power-plan changes. <br>
Mitigation: Proceed with elevation only when the user intentionally wants that diagnostic or power-plan action. <br>
Risk: The skill may create diagnostic reports or context files under TEMP/360-power-saver. <br>
Mitigation: Clear the TEMP/360-power-saver folder if retained local diagnostic history is not desired. <br>
Risk: The skill may optionally retrieve remote power-strategy advice. <br>
Mitigation: Use the remote advice only as guidance and review it before acting on any recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttqftech/360-power-saver) <br>
- [Remote power strategy document](https://clawhub.virustotal.com/trustedApi/360power/v1/devicePower.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Analysis, Files] <br>
**Output Format:** [Markdown with inline PowerShell and shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local TEMP reports and diagnostic context files when the user permits those actions.] <br>

## Skill Version(s): <br>
0.0.15-dazhanhongtu (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
