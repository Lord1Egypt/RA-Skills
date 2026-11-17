## Description:

Generates and saves multilingual SDK and curl examples for a specified foundation model using Volcengine Ark OpenTOP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate SDK or curl examples for a known foundation model and save them as local integration templates. It also provides structured JSON output for downstream tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code or output could expose a live API key.

Mitigation: Use a placeholder or environment variable, review generated files and output before sharing them, and avoid real credentials until the substitution risk is addressed.

## Reference(s):

- [arkcli-code-example reference guide](references/arkcli-code-example.md)
- [ClawHub skill page](https://clawhub.ai/jasonstarlight/skills/arkcli-code-example)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, JSON, Text]

**Output Format:** [Python, Go, Java, Node.js, and curl examples; human-readable output or structured JSON, saved as local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples are organized by language and IO task type; generated code uses API key authentication.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
