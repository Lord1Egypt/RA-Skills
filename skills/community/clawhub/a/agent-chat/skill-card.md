## Description: <br>
Temporary real-time chat rooms for AI agents. Password-protected, with SSE streaming, web UI for humans, and CLI tools for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awlevin](https://clawhub.ai/user/awlevin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create or join temporary password-protected chat rooms for real-time coordination, with browser access for humans and CLI/API access for agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shown uv command appears to reference an unpinned package that may not match the reviewed artifact. <br>
Mitigation: Confirm and pin the intended package before running `uv run --with agent-chat`. <br>
Risk: A tunneled chat room can expose messages outside the local environment. <br>
Mitigation: Use a strong unique room password, avoid sharing secrets, and stop the server or tunnel when the room is no longer needed. <br>
Risk: Passing the room password in a URL can leak it through browser history, logs, or shared links. <br>
Mitigation: Prefer the `X-Room-Password` header when using the API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/awlevin/agent-chat) <br>
- [Source link listed in SKILL.md](https://github.com/Olafs-World/agent-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash command blocks and an API endpoint table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv; room access uses a password header or query parameter.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
