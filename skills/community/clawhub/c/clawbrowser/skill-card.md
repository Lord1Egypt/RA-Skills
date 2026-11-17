## Description:

Use when the agent needs to drive a browser through the Microsoft Playwright CLI (`playwright-cli`) for navigation, form interactions, screenshots, recordings, data extraction, session management, or debugging without loading a full MCP browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tezatezaz](https://clawhub.ai/user/tezatezaz)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to control browser sessions with Playwright CLI for navigation, form interactions, debugging, screenshots, recordings, and extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser sessions can retain cookies, storage, history, authentication state, and tabs between commands.

Mitigation: Use isolated sessions for sensitive sites and delete named sessions after authenticated work.

Risk: Screenshots, PDFs, traces, videos, snapshots, console output, and network logs may contain sensitive data.

Mitigation: Treat captured browser artifacts as sensitive files and review them before sharing or retaining them.

Risk: Installing the Playwright CLI from an untrusted or floating npm source can introduce supply-chain uncertainty.

Mitigation: Install only from a trusted npm registry and prefer a pinned Playwright CLI version.

## Reference(s):

- [Clawbrowser ClawHub listing](https://clawhub.ai/tezatezaz/skills/clawbrowser)
- [ClawAudit report f4d4fb45-ed25-4659-8235-2459d0dc8189](https://clawaudit.duckdns.org/audit/f4d4fb45-ed25-4659-8235-2459d0dc8189)
- [ClawAudit report a55cb413-b111-4f1a-9f39-a5c857090ebf](https://clawaudit.duckdns.org/audit/a55cb413-b111-4f1a-9f39-a5c857090ebf)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of screenshots, PDFs, traces, videos, snapshots, console logs, and network logs as browser automation artifacts.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
