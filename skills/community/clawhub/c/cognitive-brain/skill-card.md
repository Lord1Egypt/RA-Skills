## Description:

Cognitive Brain provides cross-session memory storage, recall, association, and context injection for OpenClaw agents using a PostgreSQL-backed memory system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aboutyao](https://clawhub.ai/user/aboutyao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an OpenClaw agent persistent memory across sessions, including recall of prior user context, memory encoding, association, and prediction workflows. It is intended for environments where chat history storage and reuse have been explicitly accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores, recalls, and injects chat history across sessions.

Mitigation: Use only with explicit user consent, narrow retention rules, and regular review of stored memories before they are reused by an agent.

Risk: Memory and API access can expose sensitive conversation data if the database, Redis cache, or service port is broadly reachable.

Mitigation: Run in an isolated environment with no exposed API port and a dedicated least-privileged database role.

Risk: Installation behavior includes automatic dependency installation and a privileged curl-to-shell path in artifact documentation.

Mitigation: Avoid privileged curl-to-shell installation, review dependencies before installing, and disable runtime npm installs unless explicitly accepted.

Risk: Default and example database settings may encourage weak scoping of credentials and stored memory.

Mitigation: Replace defaults with environment-specific credentials, restrict database permissions, and keep configuration files out of shared locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aboutyao/skills/cognitive-brain)
- [Cognitive Brain Documentation](docs/README.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Install Guide](docs/INSTALL_GUIDE.md)
- [Cognitive Recall Hook](hooks/cognitive-recall/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown context snippets, JSON-like memory records, JavaScript API examples, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on a local Node.js runtime, PostgreSQL memory store, optional Redis cache, and configured OpenClaw hook events.]

## Skill Version(s):

7.0.1 (source: server release metadata and target metadata; artifact manifests also contain 5.x versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
