## Description: <br>
Eventbrite API integration with managed OAuth for managing events, venues, ticket classes, orders, attendees, and reference data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with Eventbrite accounts through Maton-managed OAuth, including creating and managing events, venues, ticket classes, orders, attendees, and reference data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Maton API key can authorize proxied access to the connected Eventbrite account. <br>
Mitigation: Keep MATON_API_KEY private, store it only in trusted environments, and rotate it if exposure is suspected. <br>
Risk: Requests can affect the wrong Eventbrite account when multiple connections are active. <br>
Mitigation: Use the Maton-Connection header and confirm the target account before executing account-specific actions. <br>
Risk: Create, update, publish, cancel, or delete operations can change live Eventbrite resources. <br>
Mitigation: Require explicit user approval after checking the exact account, resource, and intended change. <br>
Risk: Eventbrite and proxy API calls can hit documented rate limits. <br>
Mitigation: Handle HTTP 429 responses with retry and backoff, and avoid unnecessary polling. <br>


## Reference(s): <br>
- [Eventbrite ClawHub Release](https://clawhub.ai/byungkyu/eventbrite) <br>
- [Eventbrite API Documentation](https://www.eventbrite.com/platform/api) <br>
- [Eventbrite API Basics](https://www.eventbrite.com/platform/docs/api-basics) <br>
- [Eventbrite API Explorer](https://www.eventbrite.com/platform/docs/api-explorer) <br>
- [Maton API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, HTTP, and shell snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Eventbrite OAuth account.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
