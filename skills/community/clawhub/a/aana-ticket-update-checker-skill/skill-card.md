## Description: <br>
Checks ticket updates for accuracy, evidence, privacy, authorization, and risk before allowing changes to customer-visible or internal support records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents, issue triagers, CRM operators, and customer-facing teams use this skill to check proposed ticket updates before posting comments, changing status, transferring ownership, adjusting priority, closing, reopening, or replying to customers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsupported or misleading ticket updates could be posted when facts, scope, or status are unclear. <br>
Mitigation: Require evidence for claims and retrieve missing support before posting or mark the update as tentative. <br>
Risk: Customer-visible replies or public issue comments could expose private data, internal notes, or unrelated ticket history. <br>
Mitigation: Use a minimal redacted review payload and redact private or sensitive details before external visibility. <br>
Risk: Status, priority, ownership, SLA, escalation, closure, or reopening changes may be unauthorized or irreversible. <br>
Mitigation: Require approval for higher-risk or irreversible changes and block unauthorized updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-ticket-update-checker-skill) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Ticket update checker schema](artifact/schemas/ticket-update-checker.schema.json) <br>
- [Redacted review payload example](artifact/examples/redacted-ticket-update-checker.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, configuration] <br>
**Output Format:** [Markdown and structured text checklist with optional JSON review payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute code, call ticket systems, write files, persist memory, or install dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
