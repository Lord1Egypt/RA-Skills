## Description:

This skill helps users review Evite events and invitations and manage guest lists, RSVPs, messages, and event details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Evite users can review invitations, events, guest lists, RSVPs, and messages, then manage event details or send invitations and messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because two local references could not be resolved.

Mitigation: Review the skill and its dependencies before installing or running it.

Risk: Event changes and messages can affect invitations, guests, and RSVPs.

Mitigation: Review the proposed action and its preview, then approve it before the skill performs the write.

## Reference(s):

- [Evite](https://www.evite.com)
- [evite-mcp package](https://www.npmjs.com/package/evite-mcp)

## Skill Output:

**Output Type(s):** [Text, Event and RSVP information, Guidance]

**Output Format:** [Natural-language responses with event, guest, RSVP, and message details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read event information and perform event actions; write actions use a preview and user confirmation flow.]

## Skill Version(s):

1.5.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
