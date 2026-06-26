## Description: <br>
ABM Outbound helps agents turn LinkedIn prospect URLs into coordinated outbound campaigns by scraping profiles, enriching contact data, finding mailing addresses, and preparing email, LinkedIn, and Scribeless handwritten-letter workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dru-ca](https://clawhub.ai/user/dru-ca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and growth teams use this skill to plan account-based outbound campaigns from LinkedIn prospect lists, enrich contact records, and coordinate email, LinkedIn, and handwritten-letter touchpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive prospect contact data, including residential mailing addresses. <br>
Mitigation: Use only with a clear lawful basis, prefer business contact data, avoid home-address outreach unless explicitly authorized, and confirm retention and vendor-processing requirements before use. <br>
Risk: The workflow can add prospects to outbound systems without enough campaign guardrails. <br>
Mitigation: Start with a small reviewed list and confirm suppression, opt-out, and approval requirements before adding anyone to email, LinkedIn, or letter campaigns. <br>
Risk: The workflow depends on third-party API keys for enrichment, scraping, email, and mail services. <br>
Mitigation: Use restricted API keys, keep secrets out of shared files and prompts, and rotate keys if they are exposed. <br>


## Reference(s): <br>
- [ABM Outbound on ClawHub](https://clawhub.ai/dru-ca/abm-outbound) <br>
- [Enrichment Reference](references/enrichment.md) <br>
- [Scribeless API Reference](references/scribeless-api.md) <br>
- [Apify](https://apify.com) <br>
- [Apollo](https://apollo.io) <br>
- [Scribeless Platform](https://platform.scribeless.co) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, csv] <br>
**Output Format:** [Markdown with bash, Python, JSON, and CSV examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided prospect data, third-party API keys, campaign identifiers, and review before campaign execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
