## Description:

Engram helps AI agents build, query, and maintain persistent local knowledge graphs for code, organization, infrastructure, and concept relationships across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use Engram to persist architecture, dependency, ownership, and concept relationships, then query paths, blast radius, stale nodes, branch overlays, and cross-model links during future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent knowledge graphs may capture sensitive workspace, organizational, infrastructure, or people metadata.

Mitigation: Limit use to non-sensitive architecture and relationship facts by default; avoid storing secrets, credential paths, SSH configuration details, email contents, personal trust rankings, or private organizational data.

Risk: The skill installs and uses a third-party npm package that persists local data.

Mitigation: Pin and audit the package version before use, and restrict access to the local database file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morpheis/skills/clawdactual-engram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI command examples and optional structured CLI output such as JSON, JSON-LD, DOT, or batch commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a durable local SQLite knowledge graph; CLI commands can emit structured JSON with the --json flag.]

## Skill Version(s):

0.1.12 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
