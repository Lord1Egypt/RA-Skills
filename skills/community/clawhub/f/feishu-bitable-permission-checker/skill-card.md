## Description:

Checks links from a Feishu Bitable and reports which linked Feishu docx or wiki documents are readable by the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganguagua](https://clawhub.ai/user/ganguagua)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or workspace administrators use this skill to audit whether links listed in a Feishu Bitable are readable, separating accessible and inaccessible documents in a final Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks access by fetching full document contents, which may expose readable document bodies to the agent context, logs, or traces.

Mitigation: Run it only when the operator is authorized to audit the Bitable and every linked document, and prefer metadata-only permission checks when available.

Risk: Permission results can reveal which documents a user or agent can access.

Mitigation: Share the report only with the authorized requester and avoid posting results in broad group chats.

## Reference(s):

- [Feishu API Notes for Bitable Permission Checker](references/api_notes.md)
- [ClawHub skill page](https://clawhub.ai/ganguagua/skills/feishu-bitable-permission-checker)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown permission report with tables of readable and unreadable documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report should avoid exposing document contents and should only summarize permission status and links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
