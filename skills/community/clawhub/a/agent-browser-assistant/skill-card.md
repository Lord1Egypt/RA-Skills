## Description: <br>
Agent Browser Assistant supports browser automation tasks, web data scraping, form filling, page screenshots, UI testing, and related browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and operations teams use this skill to automate browser workflows such as navigating pages, filling forms, capturing screenshots, exporting pages, scraping page data, and running UI or regression checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to control logged-in browser sessions, submit forms, accept dialogs, upload files, export private pages, scrape data, post content, make purchases, or change account settings. <br>
Mitigation: Use the default sandbox profile, avoid profile="user" on sensitive accounts, and require explicit confirmation before high-impact browser actions. <br>
Risk: Large-scale scraping or batch browser operations can expose private data or exceed site expectations. <br>
Mitigation: Limit scraping scope, review extracted data before use, and confirm authorization before collecting or exporting site content. <br>


## Reference(s): <br>
- [Agent Browser Assistant on ClawHub](https://clawhub.ai/openlark/agent-browser-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline browser automation examples and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser actions for page navigation, element interaction, screenshots, uploads, PDF export, scraping, and testing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
