## Description: <br>
Submits websites to the DomainRank.app AI directory through the DomainRank submission API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[domainrankhq](https://clawhub.ai/user/domainrankhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and submit one or more website listings to DomainRank.app with a selected price plan. It is intended for workflows where the user has a DomainRank API key and must review website details and expected credit cost before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends website names, URLs, selected price plans, and bearer-token authenticated requests to an external DomainRank service. <br>
Mitigation: Use a dedicated API key if available, provide credentials only at execution time, and verify the destination API endpoint before sending requests. <br>
Risk: Single or batch submissions can spend DomainRank credits according to the chosen price plan. <br>
Mitigation: Review the website list, URL, price plan, and expected total credit cost, and require explicit confirmation before each single or batch submission. <br>


## Reference(s): <br>
- [DomainRank submission API endpoint](https://domainrank.app/api/submit-item) <br>
- [DomainRank AI SEO skills](https://domainrank.app/ai-seo-skills) <br>
- [ClawHub release page](https://clawhub.ai/domainrankhq/domainrank-submit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided DomainRank bearer token and explicit user confirmation before batch submissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
