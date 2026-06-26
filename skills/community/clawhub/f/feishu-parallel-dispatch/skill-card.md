## Description: <br>
Spawn one background child task per substantial Feishu prompt so the foreground chat stays responsive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Feishu users and workspace assistants use this skill to keep chats responsive while substantial requests continue in independent background tasks. It is intended for workflows where users may send more prompts before earlier long-running work is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic async task spawning may conflict with workspace expectations for foreground-only replies. <br>
Mitigation: Install only in Feishu workspaces that want background task handling, and honor explicit user requests for synchronous answers. <br>
Risk: Background tasks can make status harder to follow if progress reporting is absent. <br>
Mitigation: Pair the dispatch pattern with heartbeat or status checks, and report each task's completion or failure independently. <br>


## Reference(s): <br>
- [OpenClaw Session Tool Documentation](https://docs.openclaw.ai/session-tool) <br>
- [ClawHub Skill Page](https://clawhub.ai/wd041216-bit/feishu-parallel-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown guidance and short chat responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate one background task per substantial Feishu prompt when the hosting agent supports that workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
