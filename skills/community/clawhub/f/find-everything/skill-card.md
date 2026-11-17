## Description:

Cross-platform resource search orchestrator for finding agent skills, MCP servers, prompt templates, and open source projects across ClawHub, Skills.sh, GitHub, prompts.chat, MCPServers.org, and other aggregators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zadanthony](https://clawhub.ai/user/zadanthony)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find, compare, and vet skills, MCP servers, prompt templates, and open source repositories from multiple sources before viewing details or installing a selected resource.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local shell commands while searching or inspecting resources.

Mitigation: Use a sandboxed environment, avoid untrusted search text, and review commands before execution.

Risk: The skill can install or configure third-party resources and modify its registry.

Mitigation: Require explicit confirmation before installs or registry edits, and review source artifacts before allowing setup changes.

Risk: The skill may execute unpinned package tools while interacting with external search sources.

Mitigation: Prefer pinned package versions and reviewed source artifacts before allowing external tools to modify the environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zadanthony/skills/find-everything)
- [Source Registry](artifact/references/registry.json)
- [Known Skills List](artifact/references/known_skills.txt)
- [Security Checklist](artifact/references/security-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown search results with inline shell commands, source notes, and risk labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skipped-source notes, install hints, safety labels, and confirmation guidance before installation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
