## Description:

Provides guidance for combining a FastAPI API backend with a Flask frontend proxy, including route registration, API proxying, imports, cascade deletion, startup scripts, and Docker Compose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunwenpinghao](https://clawhub.ai/user/hunwenpinghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or review a hybrid FastAPI API and Flask frontend setup. It is most useful when resolving route registration, proxy routing, import, cascade deletion, startup, and Docker Compose issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide presents the FastAPI backend as publicly exposed in sample deployment commands and Docker Compose.

Mitigation: Bind the backend privately, avoid publishing the FastAPI port, and expose access through the Flask proxy or another controlled edge service.

Risk: The proxy examples include state-changing HTTP methods without authentication or authorization controls.

Mitigation: Add authentication, authorization, request validation, and error handling before using the pattern outside local development.

Risk: The source includes a real internal user, host, and path reference.

Mitigation: Remove the internal project reference from published copies and review the skill for environment-specific identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunwenpinghao/skills/fastapi-flask-proxy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, and YAML code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
