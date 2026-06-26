## Description: <br>
AI-powered email subject line generator. Create subject lines that get opened. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icepopma](https://clawhub.ai/user/icepopma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing teams, founders, and developers use this skill to generate multiple email subject line options for launches, newsletters, sales outreach, and announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal runs may trigger automatic 0.001 USDT SkillPay billing. <br>
Mitigation: Use --test when a charge is not intended and only expose SKILLPAY_MERCHANT_KEY in environments where paid usage is approved. <br>
Risk: Dependency lockfile entries reference HTTP mirror URLs. <br>
Mitigation: Verify dependency provenance and integrity before installing or deploying the skill in controlled environments. <br>
Risk: Generated subject lines may be unsuitable, misleading, or off-brand for a campaign. <br>
Mitigation: Review generated subject lines before sending and apply campaign, legal, and deliverability checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icepopma/email-subject-generator) <br>
- [Publisher profile](https://clawhub.ai/user/icepopma) <br>
- [Project support repository](https://github.com/icepopma/email-subject-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text subject line list from a command-line agent run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 10 subject line options and supports a purpose parameter plus test mode.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
