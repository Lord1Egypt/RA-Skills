## Description: <br>
Provides agent guidance for using the 泛微 e-office IM Socket.IO/WebSocket API for private chat, group chat, online status, offline messages, and group management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanruxiaohong](https://clawhub.ai/user/quanruxiaohong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent prepare Socket.IO calls and workflows for e-office IM, including sending messages, managing groups, checking online status, and handling offline messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad live messaging, status changes, and group-management actions through an e-office IM account. <br>
Mitigation: Use a least-privileged token and require explicit user confirmation before sending messages, withdrawing or deleting messages, changing status, or modifying groups. <br>
Risk: Credentials and message contents may be exposed if tokens or payloads are logged, shared, or sent over an insecure endpoint. <br>
Mitigation: Do not log or share tokens, avoid administrator credentials, and prefer wss/https endpoints. <br>


## Reference(s): <br>
- [e-office IM API documentation](references/im-api.md) <br>
- [Project homepage](https://github.com/yourname/eoffice-im-skill) <br>
- [ClawHub skill page](https://clawhub.ai/quanruxiaohong/eoffice-im) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, JSON, shell, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EOFFICE_IM_BASE_URL and EOFFICE_IM_TOKEN configuration before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
