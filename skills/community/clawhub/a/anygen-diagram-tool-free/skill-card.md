## Description:

AnyGen图表生成-免费版 helps agents generate flowcharts, architecture diagrams, organization charts, and other visual structures from natural-language prompts through the AnyGen CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to turn natural-language diagram descriptions into rendered visual assets through the AnyGen CLI. It is suited for documentation, study notes, architecture sketches, and workflow diagrams, but not for real-time stream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram descriptions may be sent to AnyGen's remote service and could expose secrets, regulated data, or confidential architecture details.

Mitigation: Do not include sensitive or regulated information unless organizational policy approves that service for the data.

Risk: The skill requires AnyGen authentication through an API key or browser login.

Mitigation: Use environment variables or the AnyGen CLI login flow for credentials, avoid hardcoding keys, and rotate any exposed key.

Risk: The workflow uses command-line execution to call the AnyGen CLI.

Mitigation: Review commands before execution and limit execution to expected AnyGen CLI invocations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/anygen-diagram-tool-free)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return diagram URLs or local file paths from the AnyGen CLI; requires authentication and remote service access.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
