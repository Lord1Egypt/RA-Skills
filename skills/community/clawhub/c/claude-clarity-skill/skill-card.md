## Description:

Clarity is a Node.js MCP cognitive engine that provides existence awareness, three-layer persistent memory, PAD emotion analysis, and truth-goodness-beauty evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Clarity to add an MCP-based cognitive support layer for structured reasoning, memory continuity, self-verification, emotional analysis, and decision checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent integration and broad memory behavior may be under-disclosed.

Mitigation: Treat installation as review-required, inspect local state and memory behavior, and avoid sensitive environments until the persistence model is accepted.

Risk: External LLM forwarding may occur when related environment variables are configured.

Mitigation: Require explicit opt-in for external calls and audit environment variables before enabling the skill.

Risk: Installer or MCP setup can change local agent configuration and enable host code execution paths.

Mitigation: Do not run install.sh or enable MCP integration until commands and configuration changes are reviewed; test first in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/claude-clarity-skill)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [SYSTEM_REQUIREMENTS.md](artifact/SYSTEM_REQUIREMENTS.md)
- [Security audit report](artifact/docs/security-audit-report-2026-06-13.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local memory/state and register MCP tooling when installed; review security guidance before enabling.]

## Skill Version(s):

1.1.5 (source: evidence.release.version, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
