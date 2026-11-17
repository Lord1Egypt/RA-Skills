## Description:

Generates UUID v1, UUID v4, UUID v5, and shortened UUID-style identifiers locally using the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate local UUIDs and GUIDs for application data, tests, scripts, or documentation without external dependencies or API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UUID v1 identifiers can expose timestamp semantics and may be unsuitable for public or privacy-sensitive identifiers.

Mitigation: Prefer UUID v4 for public or privacy-sensitive use unless UUID v1 timestamp behavior is required.

Risk: Extremely large batch requests can create excessive local output or avoidable resource use.

Mitigation: Request bounded batches and review generated output size before using it downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-uuid-generator)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text UUID strings or JSON output, with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch generation, UUID versions 1, 4, and 5, and shortened Base62-style UUID output.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
