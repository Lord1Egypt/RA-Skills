## Description:

Find nearby ATMs when the user asks for cash withdrawal near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find nearby ATMs from an authorized current location, with optional filtering for deposit support, fee-free access, search radius, and result limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses current location data to find nearby ATMs.

Mitigation: Only share precise location after an explicit ATM-finding request and keep location handling aligned with the disclosed consent and anonymization guidance.

Risk: Broad trigger wording could activate the skill during general financial or cash-withdrawal discussions.

Mitigation: Narrow activation text to nearby-ATM lookup requests before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/atms)
- [Publisher profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance describing ATM lookup inputs, response fields, errors, and privacy handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses standardized point-of-interest response fields and supports location, radius, result limit, and optional filters.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
