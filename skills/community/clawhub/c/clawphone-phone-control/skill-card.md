## Description: <br>
Guides an agent to perceive and operate a connected phone through MCP tools for screen reading, app launching, control tapping, text input, and phone automation troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Be1Human](https://clawhub.ai/user/Be1Human) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide phone UI automation with a perception-first workflow, current-screen verification, and fallback handling for fragile mobile app flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad phone control, including actions inside logged-in apps. <br>
Mitigation: Require explicit user approval before sending messages, making purchases, deleting data, changing settings, or acting inside logged-in apps. <br>
Risk: Clipboard-based input can expose secrets or place sensitive content where other apps may read it. <br>
Mitigation: Avoid clipboard-based input for passwords, tokens, payment data, and other secrets. <br>
Risk: Fragile mobile flows can lead to unintended taps or sends when the visible screen changes. <br>
Mitigation: Use the skill's perception-first workflow: inspect the current screen, prefer text or node-based controls, and re-check the interface after each action. <br>


## Reference(s): <br>
- [MCP Tool Reference](tools-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Be1Human/clawphone-phone-control) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, configuration] <br>
**Output Format:** [Markdown guidance with inline MCP tool names and stepwise operating rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes current-screen verification before and after sensitive phone actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
