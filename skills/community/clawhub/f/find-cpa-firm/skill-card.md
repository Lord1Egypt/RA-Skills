## Description: <br>
Find, shortlist, vet, and enrich U.S. business accounting and tax firms using the ServiceGraph pro_services dataset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users procure U.S. B2B CPA, accounting, audit, tax, bookkeeping, advisory, and valuation firms. It guides ServiceGraph searches, presents shortlist results, and asks for confirmation before paid firm-detail unlocks. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ServiceGraph API key, which could expose sensitive credentials if pasted into chat or read from environment files. <br>
Mitigation: Keep SERVICEGRAPH_API_KEY in the local environment, avoid sharing it in chat, and use shell dispatch without printing secrets. <br>
Risk: Unlocking firm details spends ServiceGraph credits. <br>
Mitigation: Show the credit cost before unlock calls and get user confirmation before any paid request. <br>
Risk: Using the workflow outside its intended scope can return irrelevant or misleading firm recommendations. <br>
Mitigation: Limit use to U.S. B2B accounting and tax firm procurement, pin industry:accounting_tax, and decline personal tax, in-house hiring, software comparison, and non-U.S. requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-cpa-firm) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with ServiceGraph filter examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include filter DSL queries, brief firm shortlists, and optional paid unlock requests that require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
