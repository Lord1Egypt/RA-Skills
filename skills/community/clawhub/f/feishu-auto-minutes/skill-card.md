## Description:

飞书会议纪要AI helps an agent extract meeting content from Feishu documents, group chats, and Bitable records, then produce structured meeting minutes with decisions, action items, and follow-up dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[young-joey](https://clawhub.ai/user/young-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external collaborators use this skill to turn Feishu meeting sources, chat discussions, and tabular meeting records into concise meeting minutes, decisions, action items, and distribution-ready Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access meeting content from Feishu sources provided by the user.

Mitigation: Grant access only to the specific documents, chats, or records needed for the minutes task.

Risk: Automatically distributed minutes could expose confidential meeting details to unintended recipients.

Mitigation: Before distribution, confirm the target Feishu document, group chat, and recipient list.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/young-joey/skills/feishu-auto-minutes)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, API Calls]

**Output Format:** [Markdown meeting minutes with structured sections for attendees, discussion, decisions, action items, and next meeting details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Feishu documents, group chat discussions, and Bitable records, and may prepare or send generated minutes to Feishu destinations selected by the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
