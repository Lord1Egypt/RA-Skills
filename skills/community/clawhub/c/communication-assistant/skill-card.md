## Description: <br>
Send formatted notifications via email (himalaya) and iMessage (BlueBubbles). Use when you need to broadcast markdown-formatted messages to email recipients and phone numbers in a single step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to draft a markdown notification and send it through configured email and iMessage channels in one workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be sent to unintended email recipients or phone numbers. <br>
Mitigation: Before each send, inspect the markdown content and recipient lists. <br>
Risk: The workflow depends on a local send-notification.sh script that was not included in the reviewed package. <br>
Mitigation: Review the local script before using it to send messages. <br>
Risk: The skill sends messages through configured email and BlueBubbles accounts. <br>
Mitigation: Install and use it only when those configured accounts are intended for the notification workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/communication-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to send user-provided markdown through locally configured email and BlueBubbles tooling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
