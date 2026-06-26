## Description: <br>
Manage disposable email addresses using GuerrillaMail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cprite](https://clawhub.ai/user/cprite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create temporary email addresses, refresh disposable inboxes, read received messages, and remove locally tracked disposable mail when finished. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disposable inbox traffic and message contents are handled by GuerrillaMail and cached locally. <br>
Mitigation: Use the skill only for low-sensitivity temporary flows and remove tracked addresses and cached messages when they are no longer needed. <br>
Risk: Mailbox sessions and message contents are stored under the user's home directory. <br>
Mitigation: Avoid sensitive account recovery, financial, medical, or long-lived login workflows unless local storage controls meet the user's requirements. <br>
Risk: HTTPS validation may be weakened when certificate support is unavailable. <br>
Mitigation: Install or configure certificate support before using the skill in workflows where transport integrity matters. <br>


## Reference(s): <br>
- [GuerrillaMail API Reference](references/api.md) <br>
- [GuerrillaMail API endpoint](https://api.guerrillamail.com/ajax.php) <br>
- [ClawHub skill page](https://clawhub.ai/cprite/dropmail) <br>
- [Publisher profile](https://clawhub.ai/user/cprite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include disposable email addresses, inbox metadata, message bodies, and local cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
