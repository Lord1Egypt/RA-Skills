## Description: <br>
Apollo.io Enrichment enriches contacts and companies with Apollo.io data and supports prospect searches for leads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to enrich individual contacts, bulk contact lists, and organizations with Apollo.io data, or to search for prospects by title, company, location, and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contact, company, and bulk enrichment inputs are sent to Apollo.io and may include personal data. <br>
Mitigation: Submit only data the user is authorized to process and share with Apollo.io. <br>
Risk: The reveal-email and reveal-phone options can return personal contact information. <br>
Mitigation: Use reveal options only when there is a clear business need and appropriate permission to handle the returned data. <br>
Risk: Apollo enrichment and reveal operations may consume Apollo credits. <br>
Mitigation: Check Apollo credit usage and use limits or bulk files deliberately before running enrichment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/capt-marbles/apollo-enrichment) <br>
- [Apollo.io](https://apollo.io) <br>
- [Apollo API key settings](https://app.apollo.io/#/settings/integrations/api) <br>
- [Apollo credits settings](https://app.apollo.io/#/settings/credits) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Formatted text summaries or JSON API responses from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APOLLO_API_KEY and may consume Apollo credits.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
