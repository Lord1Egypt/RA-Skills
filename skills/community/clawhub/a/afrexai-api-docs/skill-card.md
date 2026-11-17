## Description:

Generate comprehensive OpenAPI 3.0 specs, markdown reference docs, and SDK quickstarts from API endpoint descriptions with examples and error codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to turn API endpoint descriptions, route files, or controller snippets into OpenAPI specifications, human-readable API references, and SDK quickstart guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API examples can accidentally include secrets, credentials, or private production data if those details are pasted into endpoint descriptions or source snippets.

Mitigation: Avoid providing secrets or private production data as input, and review generated examples before publishing documentation.

Risk: Generated documentation may contain inaccurate examples, missing edge cases, or misleading endpoint behavior.

Mitigation: Review the generated OpenAPI spec, examples, authentication notes, and error responses against the implemented API before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-api-docs)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [OpenAPI 3.0 YAML, Markdown reference documentation, and SDK quickstart guides]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes request and response examples, error code references, authentication notes, rate limiting notes, and language-specific quickstart snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
