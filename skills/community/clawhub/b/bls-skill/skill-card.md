## Description:

The skill helps agents query and operate Baidu Intelligent Cloud Log Service (BLS), including Project and LogStore discovery, index inspection, query generation, and log retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoming23333](https://clawhub.ai/user/xiaoming23333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect BLS resources, generate BLS match or SQL queries, and retrieve or analyze logs through authenticated BLS API calls.

### Deployment Geography for Use:

China and Hong Kong SAR BLS regions supported by the skill.

## Known Risks and Mitigations:

Risk: BLS access keys can be exposed if secret keys are passed directly on the command line.

Mitigation: Prefer environment variables or a locked-down credential file for credentials instead of the --sk command-line option.

Risk: The skill can query Baidu Log Service projects and logstores using the supplied credentials.

Mitigation: Use a least-privilege BLS identity limited to the projects and logstores the agent is intended to query.

## Reference(s):

- [BLS API Reference](references/api_reference.md)
- [BLS SQL Syntax](references/sql_syntax.md)
- [BLS Match Syntax](references/match_syntax.md)
- [Baidu Cloud BCE Authentication Reference](https://cloud.baidu.com/doc/Reference/s/Njwvz1wot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query execution requires a supported BLS region and BLS credentials; API responses may include raw log records or tabular SQL results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
