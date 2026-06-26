## Description: <br>
Helps an agent find, shortlist, vet, and enrich US management consulting firms across strategy, operations, executive coaching, leadership development, organizational change, PMO, and sales or revenue operations using the ServiceGraph pro_services dataset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to search for US management consulting firms, validate filter intent, compare brief firm cards, and optionally enrich selected company records after confirming unlock costs. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ServiceGraph bearer token for API calls. <br>
Mitigation: Keep SERVICEGRAPH_API_KEY in the shell environment or local env file and avoid pasting secrets into chat or model context. <br>
Risk: Detailed firm enrichment can spend credits when records are unlocked. <br>
Mitigation: Present the number of firms and credit cost before unlock requests, and proceed only after user confirmation. <br>
Risk: Overbroad filters can return firms outside the intended management consulting scope. <br>
Mitigation: Pin industry:management_consulting and validate filters before search or enrichment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-management-consultant) <br>
- [ServiceGraph API base](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline API requests and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return brief firm summaries for free searches and enriched firm details after user-approved credit unlocks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
