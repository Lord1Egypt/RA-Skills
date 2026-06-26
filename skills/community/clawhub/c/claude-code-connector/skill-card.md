## Description: <br>
Claude Code Connector lets an agent send prompts to Claude Code through an ACP bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[partigle](https://clawhub.ai/user/partigle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route analysis or coding prompts to Claude Code through a local ACP bridge when that integration is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's behavior depends on a local bridge shell script that is outside the submitted package. <br>
Mitigation: Install only where you control and have inspected the referenced bridge script before use. <br>
Risk: Prompts and referenced content may be forwarded to Claude Code through the bridge. <br>
Mitigation: Avoid sending secrets, private files, or sensitive project data unless that data flow is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/partigle/claude-code-connector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Prompt-dependent Claude Code response, typically Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local ACP bridge script configured outside the submitted skill package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
