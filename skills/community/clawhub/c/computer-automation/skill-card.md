## Description:

Run and create reusable browser and Windows desktop automations from an AI agent with AIVane (MCP): web scraping and data extraction to CSV, Excel or Google Sheets, form filling, signing in to portals and downloading reports or invoices, repeated price and stock checks, and Windows app steps. Use when the user wants to automate a repetitive computer task once and rerun it, run a saved AIVane automation, check or stop a run, read its outputs and files, or connect AIVane to Claude Code, Codex, Cursor, Hermes or OpenClaw. Do not use for writing Playwright, Selenium or Puppeteer code by hand, for one-off browsing you can do with your own browser tools, or for Android phone control over LAN (use the agent-android skill).

This skill is ready for commercial/non-commercial use.

## Publisher:

[aivane-labs](https://clawhub.ai/user/aivane-labs)

### License/Terms of Use:

MIT-0

## Use Case:

AI agent users and developers use this skill to connect AIVane and run or create reusable browser and Windows desktop automations. They can collect results and files from recurring tasks such as form filling, portal downloads, and price checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automations can interact with portals and may submit forms, buy, send, or delete items; setup and access-token handling also require care.

Mitigation: Review the setup guidance and grant only intended access. Confirm the automation and inputs before consequential runs, keep credentials out of chat, and show only the outputs needed for the task.

## Reference(s):

- [AIVane AI tools documentation](https://aivane.net/docs/ai-tools/)
- [AIVane setup instructions](references/setup.md)
- [Project repository (metadata link)](https://github.com/aivanelabs/ai-rpa)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API calls, Files]

**Output Format:** [Text guidance and automation results or files, including reports, spreadsheets, and screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automation outputs may contain private data; show only what the task needs and save files only when asked.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
