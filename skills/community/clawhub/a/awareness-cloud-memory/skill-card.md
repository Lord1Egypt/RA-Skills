## Description:

Persistent cloud memory across sessions that automatically recalls prior context before each request, captures session checkpoints, and provides manual Bash tools for searching, recording, and querying memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everest-an](https://clawhub.ai/user/everest-an)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve project decisions, tasks, knowledge, and handoff context across sessions. It can automatically inject relevant memory into prompts and expose manual commands for recall, lookup, recording, setup, and agent prompt retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on recall can send prompt text and memory summaries to the configured memory service.

Mitigation: Use the skill only for work where cloud memory processing is acceptable, and avoid entering secrets or regulated data while it is active.

Risk: Remote memory content can influence prompt context before each request.

Mitigation: Review injected memory context for relevance and treat it as untrusted context when making security-sensitive decisions.

Risk: Setup can persist API credentials in local files and shell profile exports.

Mitigation: Protect the API key, revoke it or run logout when access is no longer needed, and manually remove shell profile exports during uninstall.

Risk: Project-local configuration can alter the endpoint or memory used by the skill.

Mitigation: Inspect project-local openclaw.json before use and prefer a trusted, tightly scoped endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/everest-an/skills/awareness-cloud-memory)
- [Publisher Profile](https://clawhub.ai/user/everest-an)
- [Awareness Service](https://awareness.market)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Bash command examples, XML memory context from hooks, and JSON responses from command scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and AWARENESS_API_KEY plus AWARENESS_MEMORY_ID for cloud use; supports a local endpoint through AWARENESS_LOCAL_URL.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
