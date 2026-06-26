## Description: <br>
Semantic search over 3,200+ 3GPP technical specifications (TS/TR series, Rel-15 and Rel-19). Search text, diagrams, and figures across 904K+ vectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chriscarrotlabs](https://clawhub.ai/user/chriscarrotlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, standards researchers, and telecom engineers use this skill to search 3GPP TS and TR documents, inspect sections, retrieve figures, and compare information across releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key for authenticated 3GPP Scout endpoints. <br>
Mitigation: Store SCOUT_API_KEY in the environment or OpenClaw configuration and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: The service is paid, so repeated API calls can consume account credits. <br>
Mitigation: Use filters, document lookups, and focused search parameters before broad searches to control usage. <br>
Risk: Search results can omit relevant standards context or produce incomplete comparisons across releases. <br>
Mitigation: Cite document number, section number, and release, and use section text or table-of-contents endpoints to verify important claims. <br>


## Reference(s): <br>
- [ClawHub 3GPP Scout package page](https://clawhub.ai/chriscarrotlabs/3gpp-scout) <br>
- [3GPP Scout homepage](https://3gppscout.com) <br>
- [3GPP Scout API documentation](https://api.3gppscout.com/docs) <br>
- [3GPP Scout dashboard](https://dashboard.3gppscout.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API request and response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCOUT_API_KEY for authenticated search and document endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
