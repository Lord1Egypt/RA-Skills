## Description:

Parse SQLite databases into structured JSON data. Use when exploring unknown database schemas, understanding table relationships, and extracting map data as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect unfamiliar SQLite schemas, understand table relationships, and extract selected database content, including map or grid data, into structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQLite databases provided for parsing may contain private records or other sensitive data.

Mitigation: Provide only databases the user is authorized to inspect and comfortable having analyzed in the agent session.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, JSON]

**Output Format:** [Markdown with SQL, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces schema-inspection queries, extraction patterns, and structured JSON examples; database contents should be reviewed for sensitive records before analysis.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
