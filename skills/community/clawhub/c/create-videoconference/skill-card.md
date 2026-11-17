## Description:

Creates secure Meetling videoconference links and produces invite or share text for instant and scheduled calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bavxhack](https://clawhub.ai/user/bavxhack)

### License/Terms of Use:

MIT

## Use Case:

Employees, external collaborators, developers, and agents use this skill to create Meetling video conference links, generate invite text, and prepare recipient share payloads without automatically sending messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated share payloads could be sent to unintended recipients if participant text or contact mappings are wrong.

Mitigation: Review the generated recipients and unresolved recipients before any Claw sending path uses the share payload.

Risk: Participant names without a future start time are treated as an instant call.

Mitigation: Provide an explicit future start_time for scheduled calls or review the returned mode before sharing the link.

Risk: Missing or invalid contacts.json leaves recipients unresolved.

Mitigation: Check unresolved_recipients and update ./contacts.json before sending invitations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bavxhack/skills/create-videoconference)
- [Meetling application](https://app.meetling.de)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [JSON object containing a Meetling URL, invite or share text, recipient resolution details, and optional scheduling limitations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instant calls return a share payload; scheduled calls return an email invite template and fallback limitations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
