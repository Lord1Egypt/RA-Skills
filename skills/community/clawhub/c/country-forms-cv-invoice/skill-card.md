## Description:

Fill country-specific CVs and invoices/estimates with the user's own details — US résumé, German Lebenslauf and Rechnung, Japanese 履歴書・職務経歴書・請求書 (源泉徴収), Spanish/Colombian currículum, Europass, Brazilian currículo and nota fiscal withholding. Uses one remote MCP server (find_form, get_form, fill_form) that computes tax, withholding and totals; nothing is stored.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmshinhwa](https://clawhub.ai/user/jmshinhwa)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals preparing country-specific CVs or résumés use the skill to organize their details in local formats. Freelancers and others preparing invoices, estimates, or expense statements use it to calculate country-specific taxes, withholding, totals, and due dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CV and invoice details may include sensitive personal or financial information sent to the remote forms service.

Mitigation: Share only necessary details, avoid sending sensitive identifiers unless requested by the form and chosen by the user, and verify the provider's retention practices first.

Risk: Tax, withholding, or other consequential invoice calculations may be unsuitable for a user's specific circumstances.

Mitigation: Have an adviser check consequential tax calculations before relying on them.

## Reference(s):

- [ReadyStack homepage](https://getreadystack.com/)
- [ClawHub skill page](https://clawhub.ai/jmshinhwa/skills/country-forms-cv-invoice)
- [Remote forms MCP service](https://mcp.getreadystack.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Country-specific CV content and invoice or estimate calculations presented as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CV results follow the selected form's section order and identify missing fields; invoice results include calculated amounts and due dates.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
