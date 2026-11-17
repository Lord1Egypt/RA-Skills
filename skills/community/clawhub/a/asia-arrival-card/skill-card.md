## Description:

Guides travelers through arrival card, visa, and travel declaration preparation for Malaysia, Thailand, Singapore, Indonesia, Vietnam, the Philippines, Japan, Korea, and other destinations via current official-source lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivy-ting](https://clawhub.ai/user/ivy-ting)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel assistants use this skill to prepare required materials, extract passport, flight, and hotel details from provided documents, and generate step-by-step guidance for official arrival-card or entry declaration forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive passport, itinerary, hotel, and contact details may be exposed while preparing entry forms.

Mitigation: Share only fields needed for the task, redact unnecessary scans, avoid passwords, payment details, and email codes, and verify extracted fields before use.

Risk: Automation guidance for official government forms could cause incorrect entries or actions outside the user's control.

Mitigation: Keep official submissions manual, treat automation snippets as examples, and review every field on the government website before submitting.

Risk: Entry requirements, timing windows, fees, and official URLs may change.

Mitigation: Confirm requirements on current official government websites before travel and before relying on generated guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivy-ting/skills/asia-arrival-card)
- [Materials checklist](reference/materials-checklist.md)
- [Country guides](reference/country-guides.md)
- [Country comparison](reference/country-comparison.md)
- [Smart document recognition](reference/smart-document-recognition.md)
- [Automation framework](reference/automation-framework.md)
- [Malaysia Digital Arrival Card](https://imigresen-online.imi.gov.my/mdac/main)
- [Singapore SG Arrival Card](https://eservices.ica.gov.sg/sgarrivalcard/)
- [Philippines eTravel](https://etravel.gov.ph/)
- [Visit Japan Web](https://www.vjw.digital.go.jp/)
- [Korea K-ETA](https://www.k-eta.go.kr/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with tables, checklists, extracted-field summaries, and pseudocode when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions and require user confirmation before using extracted document data.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
