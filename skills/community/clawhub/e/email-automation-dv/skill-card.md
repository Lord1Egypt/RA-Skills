## Description: <br>
Send and automate emails using ConvertKit or Mailchimp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing operators use this skill to create draft welcome, launch, and nurture email sequences, manage ConvertKit subscribers, and generate sequence performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real marketing-platform credentials and affect subscriber or campaign data. <br>
Mitigation: Use a test account or test audience first, verify every recipient, sequence ID, and subscriber action before running commands, and keep API secrets out of shell history and logs. <br>
Risk: Contact enrollment can create compliance and consent issues. <br>
Mitigation: Enroll only contacts with valid consent and confirm unsubscribe or preference-management handling before sending campaigns. <br>
Risk: The release describes Mailchimp support, but the reviewed artifact behavior is ConvertKit-focused. <br>
Mitigation: Treat the skill as ConvertKit-only unless Mailchimp support is reviewed and validated separately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/email-automation-dv) <br>
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai) <br>
- [ConvertKit API base](https://api.convertkit.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus generated JSON sequence and report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit API credentials for live ConvertKit actions; generated email templates require review before subscriber enrollment.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
