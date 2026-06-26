## Description: <br>
Automated web task execution service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide authorized web automation tasks such as form filling, scraping, testing, website monitoring, and submissions while applying guardrails for credentials, site controls, and scraped data handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web automation and scraping can affect sites or accounts where the user lacks authorization. <br>
Mitigation: Run the skill only for sites and accounts where you have authorization, check robots.txt where applicable, and do not use it to bypass CAPTCHAs, rate limits, IP bans, two-factor authentication, or other site protections. <br>
Risk: OAuth tokens or sensitive credentials can be exposed through prompts, command arguments, URLs, logs, shell history, or process listings. <br>
Mitigation: Pass credentials through environment variables or credential stores, keep them out of URLs and command-line data fields, and treat base64-encoded credentials as plaintext. <br>
Risk: Scraped data, credentials, or session tokens could be sent to the wrong external endpoint. <br>
Mitigation: Confirm destinations before forwarding scraped data and do not send credentials or session tokens through email or webhooks. <br>
Risk: The documentation mentions scheduled or cron-style tasks, but the included code only implements direct scraping. <br>
Mitigation: Verify any scheduling behavior before relying on it, and do not assume cron automation is implemented by the bundled script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/ai-web-automation-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Artifact safety evaluation](artifact/SAFETY.md) <br>
- [Faberlens](https://faberlens.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and plain-text guidance with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require OAuth tokens or sensitive credentials; generated scrape reports are written as Markdown files by the bundled script.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
