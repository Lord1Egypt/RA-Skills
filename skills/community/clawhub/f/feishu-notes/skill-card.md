## Description:

Read, write, and manage Feishu (\u98de\u4e66) documents via the Open API, including document creation, content reading, text appending, and OAuth token refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windsjj20](https://clawhub.ai/user/windsjj20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, read, append, and format Feishu notes in a user's personal cloud drive after Feishu Open Platform and OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Feishu drive access, which can expose or modify more documents than intended.

Mitigation: Use a dedicated Feishu app and account where broad drive access is acceptable, and avoid granting access to sensitive drives.

Risk: The claimed folder-only boundary is not enforced by the evidence security summary.

Mitigation: Treat the folder token as an organization aid, and validate document IDs and folder membership before allowing read, write, move, or delete actions.

Risk: Image insertion can fetch arbitrary URLs supplied to the tool.

Mitigation: Only allow trusted image URLs or vetted image data, and do not pass untrusted prompt-supplied URLs directly to the skill.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/windsjj20/skills/feishu-notes)
- [Publisher profile](https://clawhub.ai/user/windsjj20)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and Feishu document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Feishu documents through authenticated Open API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
