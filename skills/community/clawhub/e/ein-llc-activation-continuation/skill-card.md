## Description:

Acquires a pinned EIN.LLC continuation archive and helps an agent assess and resume a caller-supplied U.S. business activation task without claiming, paying, or filing for the human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT

## Use Case:

Agents assisting callers with a U.S. business activation task use supplied context and private files to assess prerequisites, prepare a human handoff, and resume or check the same task later. The authorized human retains claim, payment, attestation, registration, and filing actions.

### Deployment Geography for Use:

Global (for U.S. entity and EIN-related tasks)

## Known Risks and Mitigations:

Risk: Caller context, customer key, email, grant, and continuation state may contain sensitive information.

Mitigation: Provide these files only when intending to use the EIN.LLC continuation workflow, and keep the work directory and state file private.

Risk: An agent could be mistaken for an authorized person able to claim, pay, attest, register, or file.

Mitigation: Leave those actions to the authorized human; do not treat this skill as authority to perform them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/epistemedeus/skills/ein-llc-activation-continuation)
- [Continuation archive pin](references/continuation-pin.json)
- [EIN.LLC service](https://ein.llc)

## Skill Output:

**Output Type(s):** [Guidance, Files]

**Output Format:** [JSON status and next-action responses; local continuation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22 and caller-supplied files; missing inputs yield a next action.]

## Skill Version(s):

0.1.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
