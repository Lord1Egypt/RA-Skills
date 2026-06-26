## Description: <br>
Routes messages from specified Feishu group chats to corresponding agents for processing and relays their replies back to the original group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunitaly](https://clawhub.ai/user/sunitaly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route messages from four configured Feishu group chats to designated agents and relay completed replies back to the originating chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages from configured Feishu chats are forwarded to designated agents and their replies may be relayed automatically. <br>
Mitigation: Install only for trusted chats and trusted mapped agents; add redaction, consent, and review controls before using it with secrets or sensitive internal content. <br>
Risk: The routing behavior depends on fixed chat ID to agent mappings. <br>
Mitigation: Verify the four configured chat IDs and agent identifiers before deployment and update the mappings when chat ownership or agent responsibilities change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunitaly/feishu-routing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown instructions with inline Python example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes configured Feishu chat IDs to named agents and relays the selected agent's reply.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
