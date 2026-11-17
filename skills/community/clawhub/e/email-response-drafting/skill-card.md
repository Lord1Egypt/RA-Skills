## Description:

Draft email replies with tone matching, proper threading, and formatting that survives email clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to draft concise, tone-matched email replies that preserve thread context and are ready for human review before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill on general response-writing prompts.

Mitigation: Confirm the user wants an email draft and review the generated recipients, subject, and body before approving any send action.

Risk: An email could be sent or saved with incorrect content, recipients, or threading if the draft is not reviewed.

Mitigation: Follow the draft-first workflow: present the draft for review, preserve thread context when available, and wait for explicit send approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/skills/email-response-drafting)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text email drafts with recipient, subject, body, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first workflow; the user must explicitly approve before any email is sent.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
