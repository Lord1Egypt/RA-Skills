## Description:

Anti-detection browser automation MCP skill for OpenClaw agents with 41 tools for navigation, interaction, extraction, downloads, profiles, sessions, and stealth web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redf0x1](https://clawhub.ai/user/redf0x1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give OpenClaw agents browser automation over MCP HTTP transport for navigation, interaction, extraction, downloads, session handling, profiles, and stealth web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill provides powerful stealth browser automation capabilities.

Mitigation: Install only when the intended use requires stealth browser control, and run it in a constrained environment.

Risk: Authenticated-session, cookie import, saved profile, download, deletion, JavaScript execution, and external package execution capabilities can expose sensitive data or affect local files.

Mitigation: Use only accounts and cookies the operator is authorized to access, review the upstream npm package before use, avoid casual import of sensitive cookies, and understand where downloads and saved profiles are stored and deleted.

## Reference(s):

- [CamoFox MCP GitHub README](https://github.com/redf0x1/camofox-mcp#readme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser interaction results, accessibility snapshots, screenshots as base64 PNG, downloaded file metadata/content, profile/session metadata, and extracted links or resources.]

## Skill Version(s):

1.10.0 (source: frontmatter, manifest.yaml, changelog released 2026-02-25, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
