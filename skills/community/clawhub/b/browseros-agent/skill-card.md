## Description: <br>
BrowserOS CLI helps agents control a real Chromium browser for website interactions such as clicking elements, filling forms, navigating multi-step flows, taking screenshots, and managing tabs, bookmarks, or history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseros-ai](https://clawhub.ai/user/browseros-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and agent operators use this skill when an agent needs to interact with live websites through BrowserOS rather than only read static page content. Typical tasks include browser-based research, web app testing, form workflows, screenshot capture, and browser resource management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can submit forms, make purchases, post content, change account settings, and operate on logged-in or sensitive sites. <br>
Mitigation: Require user confirmation before sensitive actions and supervise workflows on logged-in, financial, admin, or other high-impact sites. <br>
Risk: Running eval-style JavaScript can execute arbitrary page code in the active browser context. <br>
Mitigation: Prefer lower-risk BrowserOS commands such as snap, text, links, and screenshots; use eval only when no simpler command works and after confirmation. <br>
Risk: The skill can alter browser resources such as bookmarks, history, tabs, downloads, screenshots, and PDFs. <br>
Mitigation: Use read-only commands first, confirm destructive or persistent changes, and save files only to user-specified or workspace paths. <br>


## Reference(s): <br>
- [browseros-cli Command Reference](references/cli-commands.md) <br>
- [BrowserOS](https://browseros.com) <br>
- [BrowserOS CLI Source](https://github.com/browseros-ai/BrowserOS/tree/main/packages/browseros-agent/apps/cli) <br>
- [BrowserOS MCP Setup Guide](https://docs.browseros.com/features/use-with-claude-code) <br>
- [BrowserOS Skills Repository](https://github.com/browseros-ai/skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/browseros-ai/browseros-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots, PDFs, or downloads to user-specified or workspace paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
