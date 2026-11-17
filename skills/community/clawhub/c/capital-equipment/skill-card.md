## Description:

Search, book, and manage scientific research equipment across 500+ facilities, track usage, submit service requests, and find collaborators securely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cesco345](https://clawhub.ai/user/cesco345)

### License/Terms of Use:


## Use Case:

Researchers and lab operations teams use this skill to find shared scientific equipment, check availability, book instruments, monitor marketplace changes, request service quotes, and manage equipment-related reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a remote development MCP service that may be able to make bookings or submit service requests.

Mitigation: Confirm the server operator, production status, OAuth scopes, and whether bookings or service requests require explicit user confirmation before installing.

Risk: The automations rely on persistent memory for research interests, institution, equipment watchlists, and notification preferences.

Mitigation: Store only preferences that are acceptable to retain, and confirm that users can review, update, or delete saved preferences.

Risk: Marketplace, availability, compliance, and pricing outputs may affect purchasing or facility access decisions.

Mitigation: Review prices, booking details, institutional requirements, and safety or IP obligations before committing to a reservation or transaction.

## Reference(s):

- [Capital Equipment skill page](https://clawhub.ai/cesco345/skills/capital-equipment)
- [Capital Equipment MCP server endpoint](https://us-central1-capital-equipment-dev.cloudfunctions.net/mcpServer/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, and short notification-style text where appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce equipment search summaries, booking reminders, marketplace alerts, service request guidance, and configuration snippets.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
