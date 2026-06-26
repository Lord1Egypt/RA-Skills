## Description: <br>
Finds, shortlists, vets, and enriches US SEO agencies through the ServiceGraph API using SEO-specific filters and firm-detail unlocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help business users find, compare, and enrich US SEO agency candidates for needs such as technical SEO, local SEO, link-building, ecommerce SEO, B2B SEO, and SEO audits. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: ServiceGraph API keys are sensitive credentials and could be exposed if pasted into chat or read from local environment files. <br>
Mitigation: Keep the API key in the shell environment or .env.local and do not paste it into the conversation. <br>
Risk: Full enrichment unlocks spend ServiceGraph credits for selected firms. <br>
Mitigation: Review brief search results and confirm the selected firms before approving any unlock request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-seo-agency) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with filter examples, curl commands, API request outlines, and shortlist summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ServiceGraph API key for authenticated calls; full detail enrichment uses paid unlocks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
