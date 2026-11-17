## Description:

Analyzes local Claude Code and Codex session transcripts to explain token use and suggest a next step when one appears in the report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merchantguardops](https://clawhub.ai/user/merchantguardops)

### License/Terms of Use:

MIT-0

## Use Case:

Claude Code and Codex users can examine a local session's token use and understand the report's recommended next step. When sub-agent limits are relevant, the skill can offer an optional plugin installation with user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned npm package may expose sensitive local agent transcripts to untrusted code.

Mitigation: Review and trust the package and its version before running it; avoid sensitive workspaces unless using a validated or pinned install.

Risk: The optional plugin installs persistent agent-control hooks.

Mitigation: Explain the plugin's effects, review its source, and obtain the user's consent before installation.

## Reference(s):

- [AgentGuard Burn homepage](https://agentguard.run/burn)
- [AgentGuard Burn on ClawHub](https://clawhub.ai/merchantguardops/skills/agentguard-burn)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with session summary and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes API list equivalents from actual charges; quotes the report's next step when present.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
