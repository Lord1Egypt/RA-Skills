## Description: <br>
LinkedIn API integration with a single agntdata API key (Bearer token). Fetch company profiles, jobs, people, posts, and professional network insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to call agntdata's LinkedIn endpoints for sales research, recruiting workflows, account enrichment, job and company research, and professional network intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AGNTDATA_API_KEY, a sensitive bearer token for a third-party API. <br>
Mitigation: Store the key in the environment only, avoid committing it, and prefer scoped or revocable credentials when available. <br>
Risk: LinkedIn-derived profile, company, job, and post data can include personal or professional information. <br>
Mitigation: Query and retain only the data needed for the user's task, and confirm that the planned use meets legal, platform, and privacy obligations. <br>


## Reference(s): <br>
- [agntdata LinkedIn API Reference](https://agnt.mintlify.app/apis/social/linkedin) <br>
- [agntdata Documentation](https://agnt.mintlify.app) <br>
- [ClawHub Skill Listing](https://clawhub.ai/jaencarrodine/agntdata-linkedin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and AGNTDATA_API_KEY; API responses are structured JSON from agntdata LinkedIn endpoints.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
