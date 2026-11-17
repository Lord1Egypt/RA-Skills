## Description:

Generates API documentation from code comments with OpenAPI/Swagger support and JSON or YAML output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and API maintainers can use this skill to draft API documentation artifacts for web services and route-based applications. Review is needed before relying on the output as complete generated documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its automatic API documentation generation capability because the bundled script writes a fixed OpenAPI sample.

Mitigation: Review generated documentation against the source application routes and comments before publishing or integrating it.

Risk: The output path may overwrite an existing file.

Mitigation: Choose a new output path or back up existing documentation files before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/api-docs-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON/YAML API documentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled shell script writes a fixed OpenAPI JSON sample to the requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
