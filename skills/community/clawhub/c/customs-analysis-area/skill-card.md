## Description:

Queries trade area distribution data by country or region for a specified HS code, including exporter or importer focus and recent-month filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, market researchers, and import-export professionals use this skill to compare country-level trade distribution for a product HS code and plan geographic market strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API integration can incur costs for area distribution queries and billing-related operations.

Mitigation: Confirm the user's intent before any fee-bearing call, check current pricing through the documented pricing page or price_info command, and show returned fee and balance details after execution.

Risk: The skill can store and read an UpKuaJing API key from the local ~/.upkuajing/.env file.

Mitigation: Avoid printing or pasting the local API key into chats or logs, and restrict local file permissions before using the skill in shared environments.

Risk: Error reporting can send request context, request parameters, and response data to the platform.

Mitigation: Run error reporting only after explicit user confirmation and review the context for sensitive data before submission.

Risk: The skill performs maintenance-oriented version checks against the provider API.

Mitigation: Review the network behavior before installation and account for the version check when approving outbound API access.

## Reference(s):

- [Area Distribution API Reference](references/customs-analysis-area-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-analysis-area)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing Open API Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [JSON, text, shell commands, configuration, guidance]

**Output Format:** [JSON responses and concise human-facing Markdown guidance with inline shell commands when setup or billing actions are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY; API calls may incur fees and return paginated results.]

## Skill Version(s):

1.0.3 (source: frontmatter metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
