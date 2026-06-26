## Description: <br>
Smooth Browser helps AI agents use Smooth CLI to navigate websites, fill forms, extract data, test web apps, and automate browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoniocirclemind](https://clawhub.ai/user/antoniocirclemind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to drive Smooth CLI browser sessions for web navigation, authenticated workflows, scraping, structured extraction, form filling, app testing, file-assisted tasks, and JavaScript evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated browser profiles can reuse cookies and account sessions for broad web or account actions. <br>
Mitigation: Use separate profiles per site or account, prefer anonymous or read-only profiles for scraping, and require explicit approval before login reuse, posting, purchases, settings changes, or billing access. <br>
Risk: Passwords, MFA codes, or sensitive account data can be exposed if placed in prompts or metadata for the external browser automation service. <br>
Mitigation: Avoid putting passwords or MFA codes in prompts or metadata, and use live-view manual intervention for authentication challenges. <br>
Risk: Open-ended browsing or scraping tasks can reach unintended pages or collect unintended data. <br>
Mitigation: Use allowed URL restrictions, keep tasks goal-oriented and bounded, and review extracted output before using it downstream. <br>
Risk: Downloads, JavaScript execution on authenticated pages, profile deletion, and file deletion can have persistent or hard-to-review effects. <br>
Mitigation: Require explicit approval before downloads, JavaScript execution on authenticated pages, or deleting profiles and files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/antoniocirclemind/browser-smooth) <br>
- [Smooth app and API key portal](https://app.smooth.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Smooth CLI session IDs, profile IDs, response schemas, and commands for browser navigation, extraction, file handling, downloads, or JavaScript evaluation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
