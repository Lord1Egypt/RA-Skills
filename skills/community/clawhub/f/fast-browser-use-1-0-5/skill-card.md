## Description:

Rust-based Chrome automation for fast, token-efficient DOM extraction, session management, screenshots, infinite scroll harvesting, and sitemap analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makforce](https://clawhub.ai/user/makforce)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use this skill to control Chrome through CDP for stateful web navigation, interaction, content extraction, screenshot capture, and page-structure analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chrome session control can expose sensitive browsing data or authenticated accounts.

Mitigation: Use isolated browser profiles, avoid sensitive accounts, and run the skill only in authorized environments.

Risk: Cookie export, session files, and local storage access can expose private state.

Mitigation: Protect generated session files, restrict filesystem access, and delete exported browser state after use.

Risk: Loopback MCP HTTP or SSE transports can provide browser control if exposed without authentication.

Mitigation: Prefer local stdio transport, keep network transports bound to loopback, and require authentication before remote access.

Risk: Scraping and bot-detection evasion guidance can be misused on sites without permission.

Mitigation: Restrict use to authorized testing and remove or clearly limit evasion-oriented workflows.

Risk: Disabling Chrome sandboxing would increase the impact of browser compromise.

Mitigation: Keep Chrome sandboxing enabled by default and require human review for any sandbox changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/makforce/skills/fast-browser-use-1-0-5)
- [Skill definition](artifact/SKILL.md)
- [Project README](artifact/README.md)
- [Cargo package metadata](artifact/Cargo.toml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the agent to create browser-derived files such as screenshots, session JSON, page snapshots, and extracted content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
