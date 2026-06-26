## Description: <br>
Finds, shortlists, vets, and enriches US marketing agencies using ServiceGraph's pro_services catalog, with filters for services, location, size, ratings, and third-party listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sales and marketing operators, and agents use this skill to build shortlists of US marketing agencies and enrich selected agency domains with contact and profile details after credentialed access. <br>

### Deployment Geography for Use: <br>
United States for agency results; usage otherwise Global. <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated ServiceGraph calls require a sensitive API key, and exposing the key in chat or logs could compromise the account. <br>
Mitigation: Use the documented MCP server or a shell wrapper that sources SERVICEGRAPH_API_KEY from local environment files; prompt the user to store the key locally and not paste it into chat. <br>
Risk: Unlocking agency detail records can spend credits, even though discovery, validation, search, and brief reads are free. <br>
Mitigation: Search and validate filters first, present brief results to the user, and confirm the selected apexes and credit cost before calling the unlock endpoint. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nostrband/find-marketing-agency) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with REST endpoint examples, curl commands, filter DSL snippets, and shortlist/enrichment recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated calls require a ServiceGraph bearer token; detail unlocks may consume credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter declares 0.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
