## Description: <br>
Reference tool for devtools \u2014 covers intro, quickstart, patterns and more. Quick lookup for Certcheck concepts, best practices, and implementation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security practitioners use this skill as a quick reference for Certcheck concepts, quickstart steps, patterns, debugging, performance, security, migration, and cheatsheet guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags a nested review helper that may bypass sandbox and approval controls. <br>
Mitigation: Review the helper before installation and run with `--no-yolo` or `AUTOREVIEW_YOLO=0` when sandbox and approval controls should remain active. <br>
Risk: Security evidence notes that code diffs may be sent to fallback local AI CLIs. <br>
Mitigation: Set fallback reviewers to `none` when code diffs should not be shared with other local AI tools. <br>
Risk: Security evidence warns that moderation actions require appropriate ClawHub staff authorization. <br>
Mitigation: Use any moderation capability only from an account authorized to perform ClawHub staff actions. <br>


## Reference(s): <br>
- [Certcheck on ClawHub](https://clawhub.ai/bytesagain-lab/certcheck) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text reference documentation with Markdown-style headings and lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API calls, credentials, or network access are described by the artifact.] <br>

## Skill Version(s): <br>
4.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
