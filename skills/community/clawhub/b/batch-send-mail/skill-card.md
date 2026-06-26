## Description: <br>
Batch Send Mail helps agents send personalized bulk emails from CSV or Excel tables by substituting template variables, supporting CC recipients, HTML content, shared attachments, SMTP configuration, and dry-run previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyifeng6](https://clawhub.ai/user/wangyifeng6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to prepare and run personalized bulk email sends from CSV or Excel contact tables, including dry-run review before real SMTP delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real bulk email sends can reach unintended recipients or CC recipients if the table, template, subject, or attachments are wrong. <br>
Mitigation: Use dry-run mode first and verify recipients, CCs, template substitutions, subject, and attachments before approving any real send. <br>
Risk: SMTP credentials may be saved in config/config.ini or supplied during execution. <br>
Mitigation: Prefer an app-specific SMTP password or authorization code, protect the configuration file, and delete it after use when credentials should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyifeng6/batch-send-mail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can preview personalized messages in dry-run mode before sending through SMTP.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
