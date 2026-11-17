## Description:

Family Health Tracker helps an assistant log, retrieve, summarize, and prepare household health records, including visits, allergies, medications, immunizations, insurance basics, growth logs, providers, and reminders, in a local JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and household caregivers use this skill to keep family health records organized, look up key details quickly, prepare for appointments, and receive simple reminders for checkups, refills, dental cleanings, and immunizations. The skill is for recordkeeping and scheduling context, not diagnosis, treatment decisions, or medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Family health records are stored in a local plaintext health-data.json file and should be treated as sensitive.

Mitigation: Keep the file in a private, non-shared, non-synced, non-version-controlled location and avoid entering full policy numbers, financial account details, SSNs, or detailed therapy notes.

Risk: The skill tracks health information but is not a medical advisor.

Mitigation: Use it for recordkeeping and preparation only; questions about symptoms, safety, diagnosis, or treatment should be redirected to the user's healthcare provider.

Risk: Printable summaries, emergency cards, or school forms may expose sensitive records if shared without review.

Mitigation: Generate exports locally or in chat for user review first, and do not send full tracker contents to third parties unless the user explicitly approves the reviewed output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris/skills/family-health-tracker)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)
- [Privacy boundary evaluation](artifact/evals/eval-07-privacy-handling.md)
- [Medical advice boundary evaluation](artifact/evals/eval-08-no-medical-advice.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text and Markdown summaries, with local JSON record updates when the assistant has filesystem access]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise health-record confirmations, lookups, family summaries, appointment prep notes, reminders, and safe local-file updates; it should avoid medical advice and refuse highly sensitive identifiers.]

## Skill Version(s):

1.0.2 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
