## Description:

Runs Expanso Edge pipelines that process nested JSON input and return JSON metadata such as the original object, top-level keys, key counts, and trace information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation agents use this skill to process nested JSON through Expanso Edge in either a local CLI pipeline or an HTTP/MCP-style pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP mode exposes an unauthenticated HTTP endpoint on all network interfaces.

Mitigation: Prefer the CLI pipeline, or bind the HTTP server to localhost and add authentication plus request-size and rate limits before using it on any reachable host.

Risk: Deploying the pipeline from a remote URL depends on trusting that source at run time.

Mitigation: Review and pin trusted pipeline content before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-json-flatten)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON objects and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI pipeline reads standard input with a 1 MiB buffer; the MCP pipeline exposes a POST /flatten HTTP endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
