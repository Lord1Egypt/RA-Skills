## Description: <br>
Agent Notify helps AI coding agent users configure local sound alerts and visual attention cues for confirmation requests and task completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Miluer-tcq](https://clawhub.ai/user/Miluer-tcq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using AI coding agents use this skill to set up local notification hooks so they can step away and still notice confirmation prompts or completed tasks. It supports quick defaults and custom sound, trigger, and flash settings where the target agent's hook format is compatible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes local agent configuration to run notification hooks. <br>
Mitigation: Review the generated settings.json hook entries and notify-config.json before accepting changes, and use the uninstall flow to remove notification hooks and files when no longer needed. <br>
Risk: Windows support is described, but the release artifact does not include the referenced Windows notification script. <br>
Mitigation: Verify or provide the Windows script before relying on Windows setup; otherwise use the included macOS or Linux notification scripts or integrate manually. <br>
Risk: Broad notification trigger phrases may activate setup during general discussion about sounds or alerts. <br>
Mitigation: Confirm the intended setup mode, target agent, and configuration directory before writing files or updating hooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Miluer-tcq/agent-notify) <br>
- [Publisher profile](https://clawhub.ai/user/Miluer-tcq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and local configuration commands for agent notification hooks; no external service calls are required.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
