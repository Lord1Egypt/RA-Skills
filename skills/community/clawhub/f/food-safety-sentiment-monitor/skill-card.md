## Description: <br>
Monitors food safety sentiment on Chinese social platforms, detects negative events, grades risks, and generates PR response plans and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stylemonster](https://clawhub.ai/user/stylemonster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External communications, operations, and food-safety response teams use this skill to monitor public food-safety discussion, triage negative events, and draft response or recap materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraped public social-platform text or incident details may be sent to a configured AI provider. <br>
Mitigation: Avoid adding API credentials until provider data-sharing implications are understood, and redact sensitive data before analysis. <br>
Risk: The prototype can return simulated results when scraping or API access fails. <br>
Mitigation: Verify any claimed food-safety incident independently before acting on generated risk ratings or PR plans. <br>
Risk: Browser automation dependencies may become outdated. <br>
Mitigation: Update and pin Playwright and browser dependencies before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stylemonster/food-safety-sentiment-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown-style response plans, and JSON-style risk analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include simulated fallback analysis when scraping or API access fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact package.json.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
