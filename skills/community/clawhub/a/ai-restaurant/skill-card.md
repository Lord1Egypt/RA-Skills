## Description:

智慧餐饮 helps agents provide restaurant information, menu lookup, ordering, delivery, reservations, queueing, order lookup, member lookup, and feedback workflows through natural-language chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawangda](https://clawhub.ai/user/dawangda)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant customers and service agents use this skill to complete common restaurant workflows such as checking menus, placing orders, arranging delivery, reserving tables, taking queue numbers, and checking member or order information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says this skill handles contact, delivery, order, and member data while endpoint, authorization, retention, and supported-channel disclosures are inconsistent.

Mitigation: Before customer use, align the MCP URL with the documented TLS hostname, resolve retention and channel disclosures, and document authorization for order and member actions.

Risk: The security verdict is suspicious and the guidance says installation should depend on trust in the publisher and deployment operator.

Mitigation: Deploy only after operator review, with trusted publisher approval, TLS verification, access controls, and privacy disclosures confirmed for the target restaurant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dawangda/skills/ai-restaurant)
- [Privacy policy](https://clawhub.ai/dawangda/ai-restaurant/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Natural-language responses with structured MCP tool calls when restaurant actions are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle customer contact, delivery, order, reservation, queue, and member data through configured restaurant tools.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
