## Description:

Checks ticket updates for accuracy, evidence, privacy, authorization, and risk before allowing changes to customer-visible or internal support records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents and issue triage agents use this skill to review proposed ticket, issue, CRM case, and task updates before changing status or posting customer-visible text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may pause, revise, or block ticket updates until evidence, visibility, privacy, and approval are clear.

Mitigation: Use the gate as a pre-update review step and resolve missing evidence, unclear visibility, private data, or approval gaps before posting or changing status.

Risk: Review payloads could expose logs, secrets, customer records, internal notes, or unrelated ticket history if over-shared.

Mitigation: Send only the minimal redacted payload fields described by the skill and omit raw logs, secrets, customer records, and unrelated history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-ticket-update-checker-skill)
- [Publisher profile](https://clawhub.ai/user/mindbomber)
- [Ticket update checker schema](schemas/ticket-update-checker.schema.json)
- [Redacted ticket update checker example](examples/redacted-ticket-update-checker.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with a structured text decision pattern and optional JSON review payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not execute commands, call services, write files, persist memory, or update tickets on its own.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
