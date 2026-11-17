## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janeaaaa](https://clawhub.ai/user/janeaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows such as navigation, page inspection, form filling, data extraction, UI testing, screenshots, PDFs, and session state management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state and generated artifacts may contain cookies, tokens, credentials, or private page data.

Mitigation: Keep auth.json, screenshots, PDFs, videos, and traces out of repositories and shared folders, and review them before sharing.

Risk: Global installation of an unpinned browser automation CLI can introduce unexpected behavior as dependencies change.

Mitigation: Install from a pinned, trusted agent-browser version when possible and avoid running installation as root or administrator.

## Reference(s):

- [Agent Browser ClawHub Skill Page](https://clawhub.ai/janeaaaa/skills/agent-browser-v2)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown with inline shell commands and structured command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser artifacts such as screenshots, PDFs, videos, traces, cookies, and saved storage state when the documented commands are used.]

## Skill Version(s):

1.0.0 (source: evidence.release and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
