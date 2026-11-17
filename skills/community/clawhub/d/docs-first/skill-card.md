## Description:

Docs-first directs an agent to consult official documentation before answering questions about specific third-party libraries, frameworks, packages, SDKs, CLIs, APIs, or programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itoldis](https://clawhub.ai/user/itoldis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make software-specific answers check current official documentation or repositories before responding. It is intended for API, configuration, installation, compatibility, CLI, SDK, and error-resolution questions where stale knowledge can mislead users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add source links to otherwise straightforward answers.

Mitigation: Use the compact footer format required by the skill so citations remain visible but unobtrusive.

Risk: A response can still be wrong if it relies on unofficial, outdated, or version-mismatched documentation.

Mitigation: Search official documentation or the official repository first, prefer the user's stated version, and state when no official source was found.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answer with a compact documentation link footer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should identify the relevant official source and version when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
