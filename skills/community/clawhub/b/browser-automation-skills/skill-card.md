## Description: <br>
Browser automation skills for AI models to navigate, screenshot, interact with, scrape, debug, test, and record local Google Chrome sessions through CDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaerye23](https://clawhub.ai/user/huaerye23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding assistant users use this skill pack to control a local Chrome browser for navigation, screenshots, interaction, scraping, debugging, automated QA, and session recording. It is suited to browser-based inspection and workflow execution where actions can be observed and verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over an existing Chrome session, including pages that may contain sensitive accounts or private content. <br>
Mitigation: Use a separate Chrome profile with no sensitive accounts, close private tabs before use, and keep the remote debugging endpoint local. <br>
Risk: Browser automation can perform consequential actions such as login, form submission, purchases, posts, deletions, or account changes. <br>
Mitigation: Require explicit user confirmation before any consequential browser action and verify state with screenshots before proceeding. <br>
Risk: Screenshots, recordings, DOM output, network logs, or console logs may include sensitive page data. <br>
Mitigation: Review screenshots, recordings, and extracted page data before sharing or storing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaerye23/browser-automation-skills) <br>
- [README](artifact/README.md) <br>
- [Browser Automation API Reference](artifact/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data, file paths, screenshots, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, recordings, DOM summaries, network and console summaries, and PASS/FAIL QA reports depending on the invoked browser workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
