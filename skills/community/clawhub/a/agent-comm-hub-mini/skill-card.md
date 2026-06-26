## Description: <br>
Agent Comm Hub Mini helps MCP-compatible agents communicate through real-time messages, task dispatch, shared memory, file attachments, and strategy-sharing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect multiple MCP-compatible agents for messaging, task coordination, shared memory, file exchange, and operational status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an external hub server that is not pinned by server-resolved provenance. <br>
Mitigation: Audit and pin the external server repository and dependencies before use, then deploy from a reviewed revision. <br>
Risk: The hub can persist and share messages, tasks, memories, and files across agents. <br>
Mitigation: Limit the hub to trusted agents, restrict tool access by role, and verify retention and deletion behavior before sending sensitive content. <br>
Risk: Agent API tokens act as bearer credentials for hub access. <br>
Mitigation: Store tokens securely, rotate or revoke them when access changes, and avoid exposing them in logs, prompts, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuboacean/agent-comm-hub-mini) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [External hub repository referenced by artifact](https://github.com/liuboacean/agent-comm-hub.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP connection examples and SDK usage patterns for Python and TypeScript agents.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
