## Description:

Personal travel assistant for Atlas - dream destinations, planning, history, documents, budget, checklists and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donmeusi](https://clawhub.ai/user/donmeusi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan personal travel, organize destination wishlists, build trip folders, manage packing and document checklists, track budgets, and maintain travel reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to store travel, identity, medical, financial, booking, policy, card, and device details in persistent plaintext markdown files.

Mitigation: Use redacted values where possible, avoid storing full sensitive identifiers unless strictly necessary, and keep high-risk document copies or personal data in an encrypted vault.

Risk: Travel document and visa examples may not match a user's nationality or current destination requirements.

Mitigation: Verify visa, entry, passport-validity, and insurance requirements with official sources before booking or travel.

## Reference(s):

- [Atlas Travel Extras on ClawHub](https://clawhub.ai/donmeusi/skills/atlas-travel-extras)
- [Memory Structure - Detailed Overview](references/memory-structure.md)
- [Trip Kanban Tracker](references/trip-kanban-template.md)
- [Packliste - Template](references/packing-template.md)
- [Beach Packing List](references/packing-beach.md)
- [Hiking Packing List](references/packing-hiking.md)
- [Business Travel Packing List](references/packing-business.md)
- [Winter/Ski Packing List](references/packing-winter.md)
- [Budget Template - Reise](references/budget-template.md)
- [Dokumenten-Checkliste - Vor jeder Reise](references/document-checklist.md)
- [Wochenendtrip Template](references/weekend-trip-template.md)
- [Flight Price Tracker](references/flight-price-template.md)
- [Travel Statistics Dashboard](references/statistics-template.md)
- [Emergency Access Card](references/emergency-card-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown templates, checklists, folder structures, reminders, and travel-planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and maintains local markdown travel records under an Atlas Travel Extras folder.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
