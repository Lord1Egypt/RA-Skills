## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luuray](https://clawhub.ai/user/luuray) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to drive browser workflows from an agent, including page navigation, element interaction, form filling, page-state extraction, screenshots, PDFs, and UI testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to cookies, local storage, saved sessions, screenshots, PDFs, video captures, and other browser artifacts. <br>
Mitigation: Use isolated browser sessions or test accounts for sensitive sites, and protect or delete auth.json, captures, cookies, and storage exports after use. <br>
Risk: Browser automation can submit data, change account state, upload files, post content, or make purchases if directed at live sites. <br>
Mitigation: Require explicit confirmation before state-changing actions and limit use to trusted sites, accounts, and test environments where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luuray/agent-browser-disabled) <br>
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce JSON, screenshots, PDFs, videos, cookies, storage data, and network request information when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
