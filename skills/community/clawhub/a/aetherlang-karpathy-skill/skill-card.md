## Description:

API connector for AetherLang Omega that sends a user query and AetherLang flow code to the hosted AetherLang API to run Karpathy-inspired agent node types and return results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to compose AetherLang flows for planning, code interpretation, critique, routing, ensemble synthesis, memory, tools, loops, transforms, and parallel execution through a hosted API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected prompts and AetherLang flow code are sent to a third-party hosted API.

Mitigation: Send only the query and flow code needed for the task, and avoid secrets, credentials, private files, sensitive personal data, or system prompts.

Risk: The server-side memory node can persist data across executions.

Mitigation: Use memory only for non-sensitive data and choose namespaces and keys that do not reveal confidential or personal information.

Risk: The tool node can call public REST URLs specified in a flow.

Mitigation: Use trusted public APIs only, avoid private or internal URLs, and confirm unfamiliar URLs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contrario/skills/aetherlang-karpathy-skill)
- [Publisher profile](https://clawhub.ai/user/contrario)
- [AetherLang API endpoint](https://api.neurodoc.app/aetherlang/execute)
- [Publisher homepage](https://clawhub.ai/contrario)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with AetherLang code examples, shell commands, and JSON response parsing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns hosted API results and guidance; no local code execution or local file modification is described.]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
