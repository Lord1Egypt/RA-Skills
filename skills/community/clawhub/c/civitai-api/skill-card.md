## Description:

Query the Civitai public REST API to search models, inspect creators, fetch model or version details, reverse-lookup models by hash, list images or tags, and build authenticated download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to query Civitai assets from an agent workflow, inspect model metadata, identify model versions by hash, and create authenticated download URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Civitai API token may be stored in the workspace or passed to the helper script.

Mitigation: Keep the token in a local .env file or environment variable, avoid committing it, and keep the .env file limited to the Civitai token when possible.

Risk: Generated download URLs may include a token in the query string.

Mitigation: Treat generated download URLs as credentials and avoid echoing, logging, or sharing them unless explicitly required.

## Reference(s):

- [Civitai Public REST API notes](references/api-notes.md)
- [Civitai Public REST API documentation](https://developer.civitai.com/docs/api/public-rest)
- [Civitai](https://civitai.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the bundled helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated download URLs that contain a Civitai API token and should be treated as secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
