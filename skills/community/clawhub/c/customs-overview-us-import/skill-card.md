## Description:

Query US import transaction statistics grouped by state or city, including import records, container counts, last-90-day activity, and cursor-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External export teams, logistics analysts, and trade professionals use this skill to monitor US import activity and compare state-level or city-level distribution patterns for market analysis and logistics planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an UpKuaJing API key and may store it in a local ~/.upkuajing/.env file.

Mitigation: Prefer an environment variable or protected secret store, verify local file permissions, and do not print the local key file contents.

Risk: US import queries incur fees and account top-up flows can return payment URLs.

Mitigation: Confirm pricing through the provided price information flow and require explicit user approval before any fee-incurring query or payment action.

Risk: Error reports can include request context or response details.

Mitigation: Run error reporting only after user confirmation and remove sensitive query or response details before submission.

## Reference(s):

- [US Import API Reference](references/customs-overview-us-import-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid API calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: server evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
