## Description:

Use this skill to query the Elfa API for social and web market data, get sourced explanations and claim checks, and configure monitors and automated alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nero-sensei](https://clawhub.ai/user/nero-sensei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the Elfa API to retrieve crypto and equity market signals, get sourced explanations and claim checks, and set up monitoring or automated alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review warns that the build script may delete unrelated files in a shared output folder.

Mitigation: Before using the build script, review its target output folder and run it in an isolated directory containing only its intended outputs.

Risk: The security review warns that the update path can install unpinned, changing content; the scan was partial and some static checks were degraded.

Mitigation: Review the exact release and its changes before installing or updating, and treat scan results as incomplete.

## Reference(s):

- [Elfa API documentation](https://docs.elfa.ai)
- [Elfa API](https://api.elfa.ai)
- [Elfa Auto documentation](https://docs.elfa.ai/auto/overview)
- [Elfa Verify documentation](https://docs.elfa.ai/verify/overview)
- [Elfa skill package and updates](https://go.elfa.ai/claude-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code examples, JSON data, and alert/query configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured API results and streaming responses.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
