## Description:

Creates Feishu documents as the user Han Bo so the document owner is set directly without a later transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized employees or operators use this skill to create Feishu documents under Han Bo's user context and capture the returned document_id for later content operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates Feishu documents under a named user's account without clear authorization or confirmation guardrails.

Mitigation: Install and run it only where users are authorized to create documents as Han Bo; confirm the account context and document title before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/feishu-user-doc)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with shell command guidance and returned document_id]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a Feishu document_id/doc_token for subsequent content operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
