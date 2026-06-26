## Description: <br>
Helps agents operate Aicoo group chats by creating and managing groups, sending messages, inviting members, generating join links, and using the relevant Aicoo APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to manage multi-party Aicoo conversations, send group messages, search group conversation history, invite or remove members, and adjust group settings through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, session cookies, and join links can expose or alter access to group conversations. <br>
Mitigation: Treat these values as secrets, avoid logging or sharing them, and rotate or revoke them if exposed. <br>
Risk: Group administration commands can invite or remove members and change settings. <br>
Mitigation: Confirm the target group ID, member identity, and intended setting before executing administrative commands. <br>
Risk: Group messages and search results can disclose conversation content to unintended recipients. <br>
Mitigation: Review message content and scope searches or responses to the intended group before sending or sharing results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xisen-w/aicoo-group-chat) <br>
- [Aicoo Agent Message API](https://www.aicoo.io/api/v1/agent/message) <br>
- [Aicoo Group Conversations API](https://www.aicoo.io/api/v1/conversations?view=group) <br>
- [Aicoo Group Management API](https://www.aicoo.io/api/groups) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API requests that require AICOO_API_KEY or session cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
