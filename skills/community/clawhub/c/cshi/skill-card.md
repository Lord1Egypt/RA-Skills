## Description:

Extracts query parameters from a provided URL and saves them into a MySQL database for later processing or analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lin-shiwu](https://clawhub.ai/user/lin-shiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to parse URL query strings and persist the extracted parameters in MySQL for later processing or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL parameter names are used to build dynamic SQL for table creation and inserts.

Mitigation: Use a fixed schema or validate parameter names before processing untrusted URLs.

Risk: Default MySQL credentials use root/root.

Mitigation: Override defaults with a least-privileged MySQL account and do not use root credentials.

Risk: Stored URLs or query parameters may contain sensitive data.

Mitigation: Avoid sensitive URLs and use a dedicated database with appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lin-shiwu/skills/cshi)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline shell commands and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes parsed URL parameters to a MySQL table named url_parameters.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
