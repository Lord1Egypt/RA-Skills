## Description: <br>
Read a local Apple Health export and expose activity, sleep, heart, HRV, workouts, and long-term trends to agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, and troubleshoot Apple Health MCP for MCP-compatible clients while keeping local health export data handling explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps agents access a local Apple Health export, which can contain sensitive health data. <br>
Mitigation: Keep the export local, request explicit user consent before access, and avoid printing private user data or secrets. <br>
Risk: The setup flow uses an npm package through npx, which can change unless the package version is pinned. <br>
Mitigation: Verify the referenced repository and npm package before running commands, and consider pinning a package version. <br>
Risk: Health data summaries can be mistaken for medical advice. <br>
Mitigation: Present outputs as informational and avoid medical, legal, financial, or platform-policy advice. <br>


## Reference(s): <br>
- [Apple Health MCP repository](https://github.com/davidmosiah/apple-health-mcp) <br>
- [Apple Health connector docs](https://wellness.delx.ai/connectors/apple-health) <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/apple-health-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup guidance, MCP client configuration, safety boundaries, and troubleshooting steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
