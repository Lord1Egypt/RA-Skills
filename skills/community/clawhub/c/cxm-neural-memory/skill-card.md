## Description:

CXM helps agents understand a codebase through local semantic search, dependency mapping, and architecture or documentation ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeavaib](https://clawhub.ai/user/joeavaib)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give coding agents local semantic retrieval, dependency analysis, and architecture-aware context before code search, refactoring, or documentation ingestion tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill reads sensitive local history and AI-session data.

Mitigation: Review before installing and disable ask/ctx collection of shell and AI-session history for sensitive repositories.

Risk: The security review reports unsafe write and install behavior.

Mitigation: Use an isolated virtual environment, avoid the bundled requirements.txt until reduced and cleaned, and set patching.mode to false or require deny-by-default write allowlists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeavaib/skills/cxm-neural-memory)
- [CXM Neural Memory Skill](SKILL.md)
- [CXM README Skill Guide](docs/README_SKILL.md)
- [CXM Agent Skill Documentation](docs/agent_skill.md)
- [CXM CLI Reference](docs/cli-reference.md)
- [CXM Installation Guide](docs/install.md)
- [CXM Agent Tool Schema](docs/agent_skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON for agent-mode commands, plus Markdown and plain-text guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for local codebase context retrieval; outputs may include file paths, code snippets, dependency edges, hotspots, and generated prompts.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
