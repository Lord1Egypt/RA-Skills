## Description:

Global E-Invoice Partner Selection helps agents identify, filter, score, and recommend local e-invoicing compliance channel partners for a target country, including POC acceptance criteria and commercial negotiation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangxf0927](https://clawhub.ai/user/tangxf0927)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business, product, compliance, and engineering teams use this skill to evaluate local e-invoicing access-point, service-provider, T-VAN, PJAP, or SDI intermediary partners for international expansion. It produces a traceable partner-selection workflow with named eliminations, tiered recommendations, POC scripts, and negotiation terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on market reference data that can become outdated for current e-invoicing regulations and certified-provider lists.

Mitigation: Verify official regulator and access-point registry sources during each use, and treat bundled country data as starting material only.

Risk: Partner recommendations may influence compliance or production market-entry decisions.

Mitigation: Require legal confirmation for proxy submission, data localization, and local operating obligations before production rollout.

Risk: The workflow is Chinese-first and may not fit teams expecting an English-first partner research process.

Mitigation: Confirm language and review expectations before installation or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangxf0927/skills/e-invoice-partner-selection)
- [Country regulatory reference](reference/country_regulatory_reference.md)
- [Partner scoring matrix](reference/partner_scoring_matrix.md)
- [POC acceptance scripts](reference/poc_acceptance_scripts.md)
- [OpenPeppol Malaysia member directory](https://peppol.org/members/?country=Malaysia)
- [OpenPeppol Singapore and Malaysia authority page](https://peppol.org/peppolauthority/singapore-and-malaysia/)
- [IMDA nationwide e-invoicing framework](https://www.imda.gov.sg/how-we-can-help/nationwide-e-invoicing-framework)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Structured Chinese-language analysis that can be consolidated into a .docx report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include official registry URLs, candidate tables, multi-round filtering, scored recommendations, POC acceptance criteria, and negotiation guidance.]

## Skill Version(s):

1.1.1 (source: server release evidence; skill frontmatter is 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
