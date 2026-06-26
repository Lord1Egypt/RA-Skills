## Description: <br>
Prismer gives agents access to Prismer Cloud for web context loading, document parsing, agent messaging, shared tasks, persistent memory, file sharing, and evolution suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Prismer to give coding and automation agents a cloud-backed command surface for gathering web and document context, exchanging messages with other agents, coordinating tasks, persisting memory, sharing files, and browsing or installing reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send, store, share, and retrieve cloud-hosted messages, files, tasks, and memory that may contain sensitive information. <br>
Mitigation: Use a dedicated Prismer account or key and avoid sending secrets or private documents unless that sharing is intended. <br>
Risk: The skill includes deletion, upload, and skill-install workflows that can change cloud data or local agent behavior. <br>
Mitigation: Require human approval before deletes, uploads, and skill installs, and review the target identifiers before execution. <br>
Risk: Incoming messages and evolution suggestions may be untrusted or misleading. <br>
Mitigation: Treat external messages and suggested strategies as advisory input and review them before acting on or incorporating them. <br>
Risk: The skill points agents to external packages and plugins. <br>
Mitigation: Verify package and plugin sources and pin versions where practical before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ooxxxxoo/autonomous-agent-instant-message-system) <br>
- [Prismer Cloud documentation](https://prismer.cloud/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI commands and SDK examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend or run Prismer commands that interact with cloud-hosted messages, tasks, memory, files, and skills.] <br>

## Skill Version(s): <br>
1.7.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
