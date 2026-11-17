## Description:

Run Dievio lead search and LinkedIn lookup workflows through the public API with correct authentication, filters, pagination, and credit-aware handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT

## Use Case:

External growth teams, sales development teams, agencies, and developers use this skill to run Dievio B2B lead searches, enrich LinkedIn profile URLs, handle pagination, and return API results for downstream automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if passed on the command line, printed, or stored in logs.

Mitigation: Use the DIEVIO_API_KEY environment variable, avoid printing secrets, and install only from a trusted or pinned source.

Risk: Raw or enriched Dievio results can contain sensitive lead contact data such as emails and phone numbers.

Mitigation: Use the default summary output for logs and only request raw output when collection, storage, and use of the contact data are authorized.

Risk: Large paginated searches may consume API credits and return fewer rows than requested when credits are low.

Mitigation: Set explicit max_results and pagination limits, monitor returned count fields, and stop pagination when has_more is false.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hundevmode/skills/dievio-lead-search-api)
- [Dievio Website](https://dievio.com)
- [Dievio API Overview](https://docs.dievio.com/api-reference/overview)
- [Dievio Authentication](https://docs.dievio.com/api-reference/authentication)
- [Dievio Lead Search](https://docs.dievio.com/api-reference/search)
- [Dievio LinkedIn Lookup](https://docs.dievio.com/api-reference/linkedin-lookup)
- [API contracts](references/api-reference.md)
- [Filter fields and allowed values](references/filters-cheatsheet.md)
- [Pagination behavior](references/pagination.md)
- [Error handling guidance](references/errors.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default CLI output is summary-only; raw output may include emails, phone numbers, and other lead contact data.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
