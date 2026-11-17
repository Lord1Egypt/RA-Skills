## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luuray](https://clawhub.ai/user/luuray)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate browser navigation, page inspection, form filling, data extraction, and UI testing through structured shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on authenticated web pages and inspect page content broadly.

Mitigation: Use it only with trusted sites and accounts, and run it in a sandboxed or disposable environment when possible.

Risk: Saved state files, screenshots, recordings, traces, cookies, storage dumps, and network logs can contain sensitive information.

Mitigation: Treat generated browser artifacts as secrets, restrict file permissions, avoid high-value accounts, and delete artifacts when work is complete.

Risk: Installing the global latest npm package can introduce unreviewed upstream changes.

Mitigation: Prefer a pinned and reviewed package version before using the skill in routine workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luuray/skills/agent-browser-disabled)
- [Agent Browser CLI repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that create screenshots, PDFs, recordings, traces, saved state files, and JSON output when the agent-browser CLI is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
