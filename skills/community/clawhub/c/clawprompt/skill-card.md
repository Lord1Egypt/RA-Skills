## Description: <br>
ClawPrompt launches a browser-based teleprompter with mobile remote control for video recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Creators, presenters, and video teams use this skill to run a local teleprompter while recording video, with a phone on the same Wi-Fi network acting as a remote for page turns and text upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The teleprompter runs as a local web server intended for access from devices on the same Wi-Fi network. <br>
Mitigation: Use it only on trusted Wi-Fi networks and stop the server when recording is complete. <br>
Risk: Script text may be shared with paired browser sessions and may remain in browser site data. <br>
Mitigation: Avoid highly confidential scripts on shared networks and clear browser site data when persistence is not desired. <br>
Risk: The security review notes an external QR fallback that may be worth removing or disclosing in a future version. <br>
Mitigation: Review the QR behavior before deployment and disclose or remove the fallback when stricter privacy controls are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiafar/clawprompt) <br>
- [Publisher profile](https://clawhub.ai/user/jiafar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and local browser URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts a local Node.js teleprompter server and provides browser-based controls for desktop and phone use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
