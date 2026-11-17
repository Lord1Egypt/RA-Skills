## Description:

Enables agents to automate real browser sessions through a CLI or Python SDK for JS-rendered, authenticated, and interactive web workflows, including snapshots, form filling, scraping, CDP sessions, and CLI-to-SDK code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tielei](https://clawhub.ai/user/tielei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to control websites that require JavaScript execution, login state, UI interaction, screenshots, browser storage, or CLI-to-SDK automation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can execute mutable remote code through dependency setup.

Mitigation: Review the install script before running it, preinstall uv through a trusted package manager, pin bridgic-browser to a reviewed version, and run it in an isolated project, user account, or container.

Risk: Browser automation can retain or access sensitive session data, screenshots, storage files, and network captures.

Mitigation: Use --clear-user-data or a separate BRIDGIC_HOME for sensitive browsing, avoid CDP against an everyday Chrome profile unless needed, and treat captured browser artifacts as sensitive.

## Reference(s):

- [CDP Mode](artifact/references/cdp-mode.md)
- [CLI Guide](artifact/references/cli-guide.md)
- [CLI and SDK API Mapping Guide](artifact/references/cli-sdk-api-mapping.md)
- [Environment Variables and Login State](artifact/references/env-vars.md)
- [SDK Guide](artifact/references/sdk-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation steps, SDK snippets, environment configuration, screenshots or file paths when requested by the user.]

## Skill Version(s):

0.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
