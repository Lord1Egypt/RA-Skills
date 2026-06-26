## Description: <br>
Create a new topic in a Feishu topic-group and optionally add the first in-thread reply, including an @mention, by sending as the user after explicit intent checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxxbb](https://clawhub.ai/user/dxxbb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators who use Feishu topic-groups use this skill to create a fresh topic, optionally seed a first thread reply, carry over concise context, and include an @mention only when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post Feishu messages as the user to a shared topic-group. <br>
Mitigation: Require explicit send intent and have the user verify the destination group, message text, mentions, and any carried-over context before posting. <br>
Risk: A non-topic target group will receive a normal group message instead of creating a topic. <br>
Mitigation: Resolve and confirm that the target chat is a Feishu topic-group before sending, and stop or explain the fallback behavior if it is not. <br>
Risk: Mentions or carried-over context may notify the wrong person or expose unnecessary prior conversation details. <br>
Mitigation: Keep carried-over summaries minimal and confirm @mention markup and sensitive context before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxxbb/feishu-new-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Concise text or Markdown status updates with Feishu messaging tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu text mention markup and JSON message content for send and reply calls.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence, created 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
