## Description:

Ask questions and read documentation about any GitHub repository using DeepWiki MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to query DeepWiki for repository documentation, codebase context, APIs, architecture explanations, and code review background.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may involve running an unpinned third-party shell installer.

Mitigation: Review the installer before running it, prefer a pinned and verified package distribution, and avoid sudo unless required and understood.

Risk: Repository names, proprietary code context, or confidential questions may be sent to DeepWiki.

Mitigation: Do not send secrets, private repository names, proprietary code, or confidential questions unless that sharing is approved.

## Reference(s):

- [DeepWiki](https://deepwiki.com)
- [usage-patterns.md](references/usage-patterns.md)
- [uxc install script](https://raw.githubusercontent.com/holon-run/uxc/main/scripts/install.sh)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/deepwiki-mcp-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DeepWiki responses are returned in an MCP JSON envelope; extract answer text from .data.content[].text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
