## Description: <br>
Enables OpenClaw to check Revit status, list available tools, and send Revit commands through a configured Revit MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanchan720](https://clawhub.ai/user/ryanchan720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Revit users and automation developers use this skill to control a live Revit session from OpenClaw chat workflows, including status checks, tool discovery, element queries, annotations, sheets, views, and project edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send commands that change a live Revit project without default command confirmation. <br>
Mitigation: Use first on test or backed-up models, restrict the Revit MCP service to trusted local networks, and enable command confirmation before allowing mutating or bulk Revit commands. <br>


## Reference(s): <br>
- [Copilot for Revit quickstart](https://github.com/ryanchan720/copilot-for-revit/blob/main/QUICKSTART.md) <br>
- [Copilot for Revit](https://github.com/ryanchan720/copilot-for-revit) <br>
- [OpenClaw bridge](https://github.com/ryanchan720/openclaw-bridge) <br>
- [General Copilot add-ins for Revit](https://github.com/ryanchan720/general-copilot-addins-for-revit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVIT_MCP_URL and an optional OPENCLAW_BRIDGE_DIR pointing to the OpenClaw bridge checkout.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
