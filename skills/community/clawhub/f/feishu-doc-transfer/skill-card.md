## Description:

Feishu Doc Transfer helps an agent transfer ownership of Feishu documents, sheets, bitables, or files to a specified user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill when an agent needs to prepare or run a Feishu document ownership transfer for documents, sheets, bitables, or files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mistaken file token or target owner can transfer Feishu document ownership to the wrong user.

Mitigation: Verify the file token, document type, target owner ID, and member type before execution, and prefer a confirmation or dry-run step for operational use.

Risk: Tenant tokens passed through commands can be exposed in command history or shared transcripts.

Mitigation: Use a least-privilege Feishu app and avoid placing real tenant tokens in command history, logs, or shared agent transcripts.

## Reference(s):

- [Feishu Open Platform App Console](https://open.feishu.cn/app)
- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/feishu-doc-transfer)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked script returns a JSON status object from the Feishu ownership-transfer request.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
