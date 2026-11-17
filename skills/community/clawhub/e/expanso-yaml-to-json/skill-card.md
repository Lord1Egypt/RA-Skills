## Description:

Converts YAML input into JSON output using Expanso Edge pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to convert YAML strings into JSON through local CLI execution, Expanso Cloud deployment, or an MCP HTTP conversion service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP server mode exposes an unauthenticated conversion endpoint on all network interfaces by default.

Mitigation: Prefer CLI mode for local conversion; before network exposure, bind the server to localhost or place it behind authentication with request-size and rate limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-yaml-to-json)
- [Skill README](artifact/README.md)
- [Skill definition](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON object with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces json, valid, error, and metadata fields; CLI mode reads YAML from stdin and MCP mode accepts conversion requests.]

## Skill Version(s):

1.0.0 (source: skill.yaml and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
