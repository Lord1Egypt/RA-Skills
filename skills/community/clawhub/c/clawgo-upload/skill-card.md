## Description:

Zip local files or folders, upload them to clawgo.me, and return a shareable clone link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjunyeee](https://clawhub.ai/user/chenjunyeee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to package selected local files or folders into a zip archive, upload it to clawgo.me, and share the resulting clone link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files or whole folders may be zipped and uploaded to an external sharing service.

Mitigation: Manually choose upload contents and avoid persona, policy, user-profile, .env, credential, key, token, cookie, backup, and source-control files.

Risk: The returned clone link and key may provide access to uploaded content while retention and access controls are unclear.

Mitigation: Treat the clone link and key as sensitive and share them only with intended recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjunyeee/skills/clawgo-upload)
- [clawgo.me upload service](https://clawgo.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the clone link, 12-character key, uploaded file name, file size, and upload time after availability is confirmed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
