## Description: <br>
Send push notifications to iOS devices via Bark app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanbo92](https://clawhub.ai/user/yanbo92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send Bark push notifications to iOS devices from an agent workflow, including optional title, subtitle, URL, sound, group, urgency level, and critical alert settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification titles, bodies, URLs, and the Bark key may be sent to the configured Bark server. <br>
Mitigation: Avoid sending secrets or sensitive content, prefer POST requests, and consider a self-hosted Bark server for more control. <br>
Risk: The Bark key may be stored locally in plaintext at ~/.bark/key. <br>
Mitigation: Restrict file permissions for ~/.bark/key and delete or rotate the key when it is no longer needed. <br>


## Reference(s): <br>
- [Bark project](https://github.com/Finb/Bark) <br>
- [Bark default API endpoint](https://api.day.app/) <br>
- [ClawHub skill page](https://clawhub.ai/yanbo92/bark) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write a plaintext Bark key at ~/.bark/key and send notification content to the configured Bark server.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
