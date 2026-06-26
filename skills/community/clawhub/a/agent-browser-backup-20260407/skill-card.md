## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejianjun000](https://clawhub.ai/user/xiejianjun000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate browser navigation, UI interaction, form filling, page scraping, session reuse, screenshots, PDFs, recordings, and web UI checks through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser automation can submit forms, upload files, change accounts, or act inside authenticated sessions. <br>
Mitigation: Use only on sites the user is authorized to automate and require explicit confirmation before submissions, uploads, account changes, or reuse of saved login state. <br>
Risk: Saved browser state and generated artifacts can contain credentials, private page content, or extracted secrets. <br>
Mitigation: Protect auth.json, screenshots, recordings, traces, PDFs, logs, and scraped data; store them in approved locations and delete them when no longer needed. <br>
Risk: The skill depends on the upstream agent-browser CLI and local node/npm tooling. <br>
Mitigation: Install only when browser automation is needed, keep the CLI current, and verify commands in a terminal when behavior is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejianjun000/agent-browser-backup-20260407) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-producing CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm. The wrapped CLI can create local artifacts such as screenshots, recordings, traces, PDFs, logs, extracted page data, and saved browser state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
