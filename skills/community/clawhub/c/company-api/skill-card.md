## Description:

Integrates with the Tuoluojiang company platform API to query daily reports, projects, finances, customers, contracts, products, and related business data with automatic token refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-j-j](https://clawhub.ai/user/mr-j-j)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operations staff, and developers who use the Tuoluojiang backend can retrieve and create company records such as daily reports, projects, tasks, bills, customers, contracts, and products through shell-driven API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores company API credentials and cached tokens in local files.

Mitigation: Use least-privilege credentials, protect the configuration and token files, avoid shared machines, and rotate credentials if exposure is possible.

Risk: The skill can run mutating company API operations such as creating projects, tasks, and products.

Mitigation: Review commands and inputs before execution and avoid mutating commands until input handling and confirmation gates are fixed.

Risk: The skill sends credentials and business data to a configured API endpoint.

Mitigation: Use only trusted HTTPS endpoints controlled by the intended company platform.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mr-j-j/skills/company-api)
- [ClawHub Publisher Profile](https://clawhub.ai/user/mr-j-j)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided company API endpoint and credentials; writes local configuration and token cache files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
