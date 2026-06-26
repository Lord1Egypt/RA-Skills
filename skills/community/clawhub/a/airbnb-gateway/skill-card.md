## Description: <br>
Airbnb Gateway standardizes safe Airbnb host operations for agents, including inbox checks, reservation and calendar reads, reply drafting, single-attempt guest message sends, and post-send verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-vaughan](https://clawhub.ai/user/jason-vaughan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External rental operators and developers use this skill to give agents a consistent operating contract for Airbnb inbox, reservation, calendar, drafting, and verified guest-message workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Airbnb tool-role mappings could point agents at tools the operator did not intend to authorize. <br>
Mitigation: Before installation, review the role map and bind only approved Airbnb, browser, DevTools, and fallback tools. <br>
Risk: Guest-facing sends can create duplicate or incorrect messages if retried from ambiguous state. <br>
Mitigation: Use per-message approval where required, send each draft once, verify by re-reading the live thread, and escalate unconfirmed sends instead of resending automatically. <br>
Risk: A persistent send ledger may contain guest, thread, and reservation metadata. <br>
Mitigation: Store the ledger only in an approved location with access controls and retention appropriate for guest and reservation data. <br>


## Reference(s): <br>
- [Airbnb Gateway ClawHub listing](https://clawhub.ai/jason-vaughan/airbnb-gateway) <br>
- [Airbnb tool priority and role mapping](references/airbnb-tool-priority.md) <br>
- [Airbnb message send state machine](references/airbnb-message-state-machine.md) <br>
- [Airbnb safety rules](references/airbnb-safety-rules.md) <br>
- [Future adapter interface](references/future-adapter-interface.md) <br>
- [Send log schema](state/send-log.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with structured status examples and JSON schema references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational procedures, escalation guidance, draft-review workflows, and deployment-specific tool-role mapping instructions.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
