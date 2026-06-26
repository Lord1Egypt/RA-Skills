## Description: <br>
Analyze email inbox health with weather metaphors, spam and signal classification, email debt scoring, and ghost detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents with a configured Himalaya IMAP account use this skill to summarize inbox health, prioritize human replies, estimate email processing time, and produce text or JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inbox reports may expose private sender details, email addresses, subjects, and reply status. <br>
Mitigation: Run only against email accounts intended for analysis and redact terminal logs or JSON output before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pfrederiksen/email-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally configured Himalaya CLI with IMAP access; analysis may include sender names, email addresses, subjects, and reply-waiting status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
