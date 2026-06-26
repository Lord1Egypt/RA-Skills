## Description: <br>
REST API reference for 147 services. Authentication patterns, endpoints, rate limits, and common gotchas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a broad API reference when integrating third-party services, checking authentication patterns, endpoint examples, rate limits, pagination, resilience, and common implementation gotchas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Curl examples may contact external services or trigger side effects such as sending messages, changing data, deleting resources, or performing financial and trading actions. <br>
Mitigation: Treat examples as templates, use sandbox or test credentials first, and require explicit user confirmation before running side-effecting requests. <br>
Risk: Secrets or personal data could be exposed if placeholders are replaced carelessly or credentials are pasted into logs, URLs, or shared transcripts. <br>
Mitigation: Use environment variables, avoid query-string credentials, redact command output, and verify placeholders before execution. <br>
Risk: API endpoint details, models, versions, and rate limits can drift from provider behavior after publication. <br>
Mitigation: Check the provider's current documentation before production use and validate responses instead of assuming HTTP 200 always means success. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivangdavila/api) <br>
- [Skill homepage](https://clawic.com/skills/api) <br>
- [Setup](setup.md) <br>
- [Authentication patterns](auth.md) <br>
- [Credential naming convention](credentials.md) <br>
- [Pagination patterns](pagination.md) <br>
- [Resilience patterns](resilience.md) <br>
- [Webhook patterns](webhooks.md) <br>
- [AI/ML API references](apis/ai-ml.md) <br>
- [Payments API references](apis/payments.md) <br>
- [Developer API references](apis/developer.md) <br>
- [Productivity API references](apis/productivity.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline curl examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples are templates for user-reviewed API calls.] <br>

## Skill Version(s): <br>
1.3.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
