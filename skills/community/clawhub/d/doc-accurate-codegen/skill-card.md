## Description:

Guides agents to generate code from actual documentation, validate API signatures, and track references to reduce hallucinated APIs and configuration errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when generating code, API calls, or configuration so an agent first locates documentation, extracts signatures, validates generated output, and records sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares an unexplained BRAVE_API_KEY credential requirement.

Mitigation: Remove the credential requirement unless it is necessary, document why it is needed, and scope its use to explicit documentation lookup actions.

Risk: The skill installs an apparently unnecessary unpinned axios npm package.

Mitigation: Remove the dependency if unused, or pin the package version and review it before installation.

Risk: The skill uses broad always-use language that can over-trigger during normal coding work.

Mitigation: Narrow activation criteria to code generation, API usage, or configuration tasks where documentation lookup is relevant.

Risk: Broad cross-skill documentation reads or skill updates could expose unrelated local context or alter behavior without review.

Mitigation: Require explicit user approval before reading broad cross-skill documentation or proposing skill updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobisamaa/skills/doc-accurate-codegen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include documentation sources, validation notes, generated code, and configuration snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
