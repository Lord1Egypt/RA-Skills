## Description: <br>
Find, shortlist, vet, and enrich US real-world engineering firms, including civil, structural, MEP, mechanical, electrical, geotechnical, transportation, environmental, and manufacturing firms, using the ServiceGraph pro_services dataset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and procurement-focused agents use this skill to identify US engineering services firms, validate ServiceGraph filters, compare brief firm results, and enrich selected firms when the user approves paid unlocks. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill requires a ServiceGraph API key. <br>
Mitigation: Keep the key out of chat and load it from the local shell environment or ServiceGraph MCP server. <br>
Risk: Unlocking firm details can spend ServiceGraph credits. <br>
Mitigation: Confirm the number of firms and credit cost with the user before calling the unlock endpoint. <br>
Risk: The skill is scoped to US real-world engineering firms and can be misapplied to software engineering or non-US requests. <br>
Mitigation: Confirm the request is for real-world engineering procurement in the United States and defer software engineering requests to a software-focused skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-engineering-firm) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown] <br>
**Output Format:** [Markdown with inline shell commands, ServiceGraph API requests, and firm shortlist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a ServiceGraph API key and explicit user approval before paid detail unlocks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
