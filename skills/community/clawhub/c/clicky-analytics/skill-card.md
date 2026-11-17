## Description:

Fetch website analytics from Clicky (clicky.com) via their REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djedi](https://clawhub.ai/user/djedi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and analytics users use this skill to retrieve Clicky traffic metrics such as visitors, pageviews, top pages, bounce rate, traffic sources, countries, and search rankings for scheduled reports or date-range comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published documentation contains realistic Clicky site IDs and site keys.

Mitigation: Replace those values with placeholders before use, rotate them if they were ever real, and store only the user's own Clicky credentials in protected environment variables.

Risk: Each invocation sends the configured Clicky site key and requested analytics parameters to Clicky's API.

Mitigation: Use the skill only for intended Clicky analytics requests and avoid exposing command output, URLs, or logs that may contain credentials or sensitive analytics parameters.

## Reference(s):

- [Clicky API Data Types](references/api-types.md)
- [Clicky Stats API endpoint](https://api.clicky.com/api/stats/4)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands; Clicky API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and Clicky credentials in environment variables.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
