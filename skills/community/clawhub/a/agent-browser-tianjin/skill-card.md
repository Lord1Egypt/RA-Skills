## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianjin-ren](https://clawhub.ai/user/tianjin-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through browser automation tasks such as opening pages, taking snapshots, interacting with elements, filling forms, managing sessions, and capturing screenshots or recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved sessions, cookies, localStorage exports, screenshots, recordings, traces, and state files can contain sensitive data.

Mitigation: Treat generated browser artifacts like secrets, keep them out of repositories, restrict access, and delete them when no longer needed.

Risk: Installing a global browser automation CLI can introduce supply-chain exposure if the upstream package changes or is untrusted.

Mitigation: Install only from a trusted upstream agent-browser release and prefer a reviewed, pinned version or commit.

Risk: Automating sensitive authenticated sites may expose credentials or session state through captured output.

Mitigation: Avoid sensitive authenticated sites unless needed and review outputs before sharing or storing them.

## Reference(s):

- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill Issues](https://github.com/TheSethRose/Agent-Browser-CLI)
- [ClawHub Skill Page](https://clawhub.ai/tianjin-ren/skills/agent-browser-tianjin)
- [Publisher Profile](https://clawhub.ai/user/tianjin-ren)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, videos, traces, cookies, localStorage exports, and saved browser state files when the documented CLI commands are used.]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
