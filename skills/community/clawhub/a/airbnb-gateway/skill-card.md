## Description:

A skill for safe, coherent Airbnb operations in OpenClaw-style agent environments, including inbox and reservation reads, guest reply drafting, verified message sending, calendar inspection, and operator-approved calendar mutations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-vaughan](https://clawhub.ai/user/jason-vaughan)

### License/Terms of Use:

MIT

## Use Case:

External rental operators and developers use this skill to make agents handle Airbnb host operations consistently: reading inboxes and reservations, drafting and verifying guest messages, inspecting calendars, and performing explicitly approved calendar changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar or price changes affect live production inventory for a revenue-bearing Airbnb account.

Mitigation: Require explicit per-operation operator approval, perform exactly the approved change, independently verify the after-state, and report the inverse operation.

Risk: Guest messages may be duplicated or falsely reported as sent if endpoint acknowledgments are treated as final confirmation.

Mitigation: Treat send acknowledgments as attempted, re-read the live thread before claiming success, and never auto-resend from failed or unconfirmed state.

Risk: Production use involves broad authenticated browser control and sensitive local token or temporary-file handling.

Mitigation: Use only a trusted local bridge, an account the operator owns, short-lived or scoped tokens where possible, private unique temporary paths, and human approval for every guest send or calendar or price change.

## Reference(s):

- [Airbnb Tool Priority](references/airbnb-tool-priority.md)
- [Airbnb Message State Machine](references/airbnb-message-state-machine.md)
- [Airbnb Safety Rules](references/airbnb-safety-rules.md)
- [Calendar Mutation Procedure](references/calendar-mutation-procedure.md)
- [Future Adapter Interface](references/future-adapter-interface.md)
- [ClawHub Skill Page](https://clawhub.ai/jason-vaughan/skills/airbnb-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured operation states, command examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce guest reply drafts, send or mutation status reports, refusals, escalation guidance, and verification steps.]

## Skill Version(s):

0.2.1 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
