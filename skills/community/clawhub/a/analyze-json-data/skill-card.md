## Description:

Analyze JSON data and generate a structured API design document or OpenAPI specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect JSON structures and draft API designs or OpenAPI 3.0 specifications from the fields they provide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input JSON files may contain sensitive or proprietary data.

Mitigation: Use only JSON files that the user explicitly chooses to process and avoid providing confidential data unless approved for this workflow.

Risk: Generated OpenAPI output may be incomplete or misleading because endpoint suggestions are inferred from JSON field names and the README contains placeholder content.

Mitigation: Review and adjust the generated specification before using it for implementation, documentation, or automation.

## Reference(s):

- [MiniMax-AI skills source listed in metadata](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON OpenAPI 3.0 content, optionally written to a local .json file by the bundled helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API paths are inferred from top-level JSON fields and should be reviewed before downstream use.]

## Skill Version(s):

1.0.1 (source: server release evidence and CHANGELOG, released 2026-05-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
