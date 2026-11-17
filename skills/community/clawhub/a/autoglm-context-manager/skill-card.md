## Description:

Manages long-term memory and files for multiple AI agents, using vector search and timeline filtering to retrieve relevant context with fewer LLM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janussilence](https://clawhub.ai/user/janussilence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create agent-specific workspaces, save files, search stored context semantically, filter by timeline signals, and optionally request LLM-assisted detail retrieval across long-running projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on unaudited Python code loaded from an external, user-writable context-manager directory.

Mitigation: Install and run it only after reviewing that directory and its dependencies in an isolated environment with pinned versions.

Risk: Persistent agent files may be indexed, cached, logged, and searched over time.

Mitigation: Avoid storing secrets or sensitive private files unless that persistence and retrieval behavior is acceptable for the deployment.

Risk: Optional LLM analysis can send retrieved context to configured model services.

Mitigation: Configure model access deliberately and disable or avoid LLM-assisted detail retrieval for data that should not leave the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janussilence/skills/autoglm-context-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with optional shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include agent IDs, file IDs, search scores, cache status, timing, and optional LLM-generated details.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
