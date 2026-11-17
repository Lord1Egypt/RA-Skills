## Description:

Find verified professional email addresses with the FinalScout API by LinkedIn profile URL, full name plus company domain, or news article URL, with single and bulk lookup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davis-lee](https://clawhub.ai/user/davis-lee)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, partnerships, and operations users can ask an agent to find professional email addresses and contact enrichment details from LinkedIn URLs, names with company domains, article URLs, CSVs, tables, or JSON lead lists. The skill is intended for external API-backed contact lookup workflows where users need result status, confidence, credits, rate limits, and optional CSV export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends names, company domains, LinkedIn URLs, article URLs, and optional metadata to FinalScout.

Mitigation: Use the skill only for contact data that may be shared with FinalScout, and avoid including sensitive metadata that is not needed for lookup or correlation.

Risk: Bulk lead lists and webhook payloads may contain personal contact information.

Mitigation: Review bulk inputs and webhook destinations before execution, and use trusted endpoints for webhook delivery.

Risk: CSV export links may be accessible to anyone with the link until they expire.

Mitigation: Share export links only with intended recipients and prefer inline results when a downloadable file is not necessary.

Risk: Personal-email and generic-email fallback can broaden the kinds of addresses returned.

Mitigation: Enable those options only when the user explicitly requests them and the use case permits that data.

## Reference(s):

- [FinalScout](https://finalscout.com)
- [FinalScout API settings](https://finalscout.com/app/api/settings)
- [ClawHub skill page](https://clawhub.ai/davis-lee/skills/b2b-contact-enrichment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with tables, JSON request examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contact lookup summaries, verification status, deliverability scores, credit usage, remaining credits, task IDs, and CSV export links.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
