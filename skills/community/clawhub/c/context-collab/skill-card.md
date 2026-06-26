## Description: <br>
Multi-agent collaboration protocol engine for OpenClaw that creates shared spaces, injects shared context into agent conversations, and provides tools for shared files, tasks, members, and annotations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luojingwei123](https://clawhub.ai/user/luojingwei123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use this plugin to coordinate multiple agents through shared project context, task state, team metadata, and human annotations. It is intended for group or channel workflows where agents need a common workspace instead of isolated local context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote shared content can be automatically injected into agent prompts. <br>
Mitigation: Install only if you trust the configured Context server and the people who can edit the shared space; disable autoInject unless it is explicitly needed. <br>
Risk: Shared-space tools can write, delete, modify task state, change members, and send notifications. <br>
Mitigation: Require human confirmation before agents write or delete files, delete spaces, modify members, or send notifications. <br>
Risk: Private workspace data or secrets placed in shared Context files may be exposed to other space participants. <br>
Mitigation: Do not place secrets or private workspace data in shared Context files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luojingwei123/context-collab) <br>
- [Publisher profile](https://clawhub.ai/user/luojingwei123) <br>
- [Context server URL](https://context-server-mj6f.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown and JSON responses from shared-space tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, write, delete, and search shared-space files through a configured Context server.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
