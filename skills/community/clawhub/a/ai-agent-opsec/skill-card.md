## Description: <br>
Prevents AI agents from leaking classified terms to external APIs, subagents, or logs by using a local term registry, runtime redaction, and pre-publish audit support with zero dependencies and no network calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local runtime redaction before web searches, external LLM or API calls, subagent tasks, and logs. It supports a workspace term registry, sanitized outbound payloads, and a local redaction audit log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The term registry and audit-log directory can contain sensitive operational data if committed or exposed. <br>
Mitigation: Add classified/ and memory/security/ to .gitignore and protect both paths, matching the server security guidance and artifact documentation. <br>
Risk: Outbound protection depends on callers using the sanitized value returned by the helper. <br>
Mitigation: Call sanitizeOutbound before web searches or third-party API calls and pass result.sanitized instead of the original input or outdated payload examples. <br>
Risk: Subagent blocking depends on the external-agent list being configured for the local agent environment. <br>
Mitigation: Configure externalAgents for agents that can make network calls and use redactTaskBeforeSpawn before spawning agent tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/ai-agent-opsec) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sanitized text values, redaction counts, access decisions, and local audit-log entries when used by an agent.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
