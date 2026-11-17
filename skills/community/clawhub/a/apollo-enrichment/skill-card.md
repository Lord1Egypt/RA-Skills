## Description:

Apollo.io contact and company enrichment API. Enrich people with email, phone, title, company data. Enrich organizations with industry, revenue, employee count, funding. Search for prospects. Use when the user needs to enrich contacts, find emails, lookup company info, or search for leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

Developers, sales operators, and go-to-market teams use this skill to enrich contact and company records, find prospects by criteria, and retrieve Apollo.io-sourced business data through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Names, emails, domains, LinkedIn URLs, and bulk contact files submitted to the skill are sent to Apollo.io.

Mitigation: Use the skill only when Apollo.io processing is intended and appropriate for the data being submitted.

Risk: Reveal options can request personal emails or phone numbers.

Mitigation: Use reveal options only when there is a proper basis to request and handle personal contact information.

Risk: Apollo enrichment and search operations may consume Apollo credits.

Mitigation: Check Apollo credit usage before running bulk enrichment or broad searches.

## Reference(s):

- [Apollo.io](https://apollo.io)
- [Apollo API Settings](https://app.apollo.io/#/settings/integrations/api)
- [Apollo Credits](https://app.apollo.io/#/settings/credits)
- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/skills/apollo-enrichment)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Plain text or JSON returned from Apollo.io enrichment and search commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an APOLLO_API_KEY environment variable and may consume Apollo credits.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
