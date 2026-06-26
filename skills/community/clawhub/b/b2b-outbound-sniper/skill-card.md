## Description: <br>
Autonomous B2B outbound skill that turns job-board hiring signals into qualified pipeline using Apify scraping, Hunter.io email verification, and Hunter campaign loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlemnos32](https://clawhub.ai/user/getlemnos32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and operations users use this skill to identify companies with recent hiring signals, verify business email contacts, and add qualified leads to a Hunter.io outbound campaign. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically add scraped contacts to a live outbound email campaign. <br>
Mitigation: Use a dedicated Hunter campaign, set strict send and scrape quotas, and review leads before enrollment where possible. <br>
Risk: Automated commercial outreach may create legal or compliance exposure. <br>
Mitigation: Confirm CAN-SPAM, GDPR, unsubscribe, consent, and jurisdiction-specific anti-spam requirements before running campaigns. <br>
Risk: API keys and local tracking files may expose account access or contact data. <br>
Mitigation: Use limited-scope keys where available, keep credentials out of source files, and protect or delete generated contact-tracking files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/getlemnos32/b2b-outbound-sniper) <br>
- [Apify console](https://console.apify.com) <br>
- [Hunter.io API key settings](https://app.hunter.io/api-key) <br>
- [Hunter.io campaigns](https://app.hunter.io/campaigns) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can write local JSON and JSONL tracking files and can add recipients to a configured Hunter.io campaign.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
