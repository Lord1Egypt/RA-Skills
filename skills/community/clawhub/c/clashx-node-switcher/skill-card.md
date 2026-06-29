## Description: <br>
Control ClashX VPN via Peekaboo to test latency and switch to the US proxy node with the lowest latency using menu bar automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifengwang333-ai](https://clawhub.ai/user/shifengwang333-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide ClashX menu bar automation with Peekaboo, run latency tests, and select a lower-latency US proxy node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshot steps can capture sensitive screen content. <br>
Mitigation: Close or hide sensitive windows before use and delete /tmp/clash_nodes.png or /tmp/screen.png after screenshots are no longer needed. <br>
Risk: Coordinate-based menu automation may click the wrong UI element on displays or ClashX layouts that differ from the documented setup. <br>
Mitigation: Review the Peekaboo commands and adjust coordinates for the active display before executing clicks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shifengwang333-ai/skills/clashx-node-switcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes UI coordinate references for a 1920x1080 display and temporary screenshot paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
