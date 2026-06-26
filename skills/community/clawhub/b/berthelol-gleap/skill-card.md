## Description: <br>
Gleap REST API integration for customer support analytics and ticket management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berthelol](https://clawhub.ai/user/berthelol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support, operations, and developer teams use this skill to query Gleap ticket data, build support reports, analyze team performance, and prepare reporting automation with curl and jq. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose support ticket data and customer details through raw exports, API responses, or downstream tools. <br>
Mitigation: Use least-privilege Gleap service-account tokens, avoid raw ticket exports unless necessary, and redact customer names, emails, comments, and ticket titles before using LLMs or external services. <br>
Risk: Scheduled reports or integrations can send support data to unintended Slack, Notion, or other destinations. <br>
Mitigation: Verify destinations before enabling automation, monitor scheduled jobs, and rotate or disable credentials when no longer needed. <br>


## Reference(s): <br>
- [Gleap skill page](https://clawhub.ai/berthelol/berthelol-gleap) <br>
- [Gleap API base URL](https://api.gleap.io/v3) <br>
- [Endpoint reference](references/endpoints.md) <br>
- [Use cases and patterns](references/use-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash curl and jq examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GLEAP_TOKEN, GLEAP_PROJECT, curl, and jq; API responses are JSON and may include support-ticket content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
