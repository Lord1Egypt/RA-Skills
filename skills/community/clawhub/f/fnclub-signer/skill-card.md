## Description:

Automatically signs in to the FN Club forum at club.fnnas.com, including CAPTCHA handling through Baidu OCR when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onetian1211](https://clawhub.ai/user/onetian1211)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation agents use this skill to perform daily FN Club forum sign-ins, check sign-in status, and set up scheduled sign-in tasks with OpenClaw cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a forum password and Baidu OCR credentials.

Mitigation: Provide credentials through protected environment variables or a private config file, and do not commit secrets to source control.

Risk: CAPTCHA images may be uploaded to Baidu OCR during sign-in.

Mitigation: Install only when this data flow is acceptable for the account and forum content being accessed.

Risk: Reusable cookies and OCR tokens may be stored on disk.

Mitigation: Set FNCLUB_DATA_DIR to a private directory with restrictive permissions and delete cached files when the skill is no longer used.

Risk: A scheduled cron job can keep using credentials after initial setup.

Mitigation: Remove the OpenClaw cron job and cached files when stopping or rotating the forum account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onetian1211/skills/fnclub-signer)
- [FN Club forum](https://club.fnnas.com/)
- [Baidu AI Open Platform](https://ai.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires forum credentials and Baidu OCR credentials before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
