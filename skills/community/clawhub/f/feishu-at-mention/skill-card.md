## Description: <br>
Feishu At Mention helps agents format Feishu @ mentions correctly for text, rich text, and interactive card messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vision-qiu](https://clawhub.ai/user/vision-qiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill when composing Feishu messages that need to mention a specific group member or all members. It provides the correct mention syntax for text, rich text, and interactive card message payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using @all may notify an entire Feishu group. <br>
Mitigation: Use @all only when broad notification is intended and the group permissions allow it. <br>
Risk: open_id values or member lookup results may expose identifiers outside the intended workflow. <br>
Mitigation: Limit member lookups and share open_id values only within the relevant Feishu automation flow. <br>
Risk: Mixing mention formats across text, rich text, and card messages can prevent the mention notification from working. <br>
Mitigation: Choose the mention tag format that matches the Feishu message type before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vision-qiu/feishu-at-mention) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable behavior is included in the artifact.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
