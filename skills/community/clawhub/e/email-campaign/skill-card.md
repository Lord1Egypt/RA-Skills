## Description: <br>
PayLessTax email automation system - 4x daily, 250 emails each. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wespeakallday](https://clawhub.ai/user/wespeakallday) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Business operators and campaign administrators use this skill to send scheduled PayLessTax email batches through Google Workspace Gmail, track failed sends, and monitor bounce and unsubscribe signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful Gmail access for scheduled bulk email and inbox handling. <br>
Mitigation: Install only for a Google Workspace domain you control, use a dedicated sending mailbox, and reduce Gmail permissions where possible. <br>
Risk: Mass sending and contact scraping can create compliance and consent risks. <br>
Mitigation: Use only consented mailing lists, disable or tightly scope inbox contact scraping, and maintain a durable unsubscribe suppression list. <br>
Risk: Automated batches may exceed acceptable operational or policy limits if run without review. <br>
Mitigation: Add a dry-run or approval step, enforce durable daily limits, and review campaign results before continued scheduling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wespeakallday/email-campaign) <br>
- [Gmail modify OAuth scope](https://www.googleapis.com/auth/gmail.modify) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON batch result with sent counts, failures, bounces, unsubscribe status, and optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Google Workspace Gmail credentials, a mailing-list file, batch-size settings, and scheduled campaign configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
