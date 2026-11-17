## Description:

Check transaction status on AO bridge

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpd](https://clawhub.ai/user/charles-lpd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AO bridge users use this skill to look up an AO bridge transaction by hash and report its status, asset flow, fee, confirmation, and related transaction metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction hashes submitted to the skill are sent to the external AOX API.

Mitigation: Avoid using the skill for hashes that should not be disclosed to the AOX service; review the outgoing lookup before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charles-lpd/skills/check-ao-transaction)
- [AOX transaction API](https://api.aox.xyz/tx/)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [JSON transaction lookup result with status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided transaction hash and sends that hash to the AOX API for lookup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
