## Description: <br>
Send and manage iMessages via BlueBubbles self-hosted macOS server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users with a self-hosted BlueBubbles macOS server use this skill to send and manage iMessage conversations, including text messages, attachments, reactions, edits, unsend actions, and iMessage effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send, attach, react to, edit, or unsend live iMessages through the configured BlueBubbles server. <br>
Mitigation: Require explicit confirmation before any send, attachment, reaction, edit, or unsend action. <br>
Risk: Broad sender access or exposed server credentials could allow unintended messaging. <br>
Mitigation: Use only a BlueBubbles server you control and trust, prefer HTTPS or a private network, protect the server password, and replace allowed_senders = ["*"] with trusted contacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/auto-bluebubbles) <br>
- [BlueBubbles](https://bluebubbles.app) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [JSON tool call payloads and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured BlueBubbles server URL and password.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
