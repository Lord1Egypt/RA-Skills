## Description:

Guides developers and AI agents through building, debugging, packaging, and publishing DSH (DeepSeek Harness / Cordis) plugins, with a version gate for the pre-stable upstream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liupengyang-1008](https://clawhub.ai/user/liupengyang-1008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to choose a DSH plugin form, implement and troubleshoot plugin features, and verify packaging and installation. It provides templates, API guidance, version checks, and release workflows for DSH and Cordis plugins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some package examples are unpinned.

Mitigation: Pin dependency versions and verify package sources before installing them.

Risk: Some testing guidance uses real profiles and live sources.

Mitigation: Use a disposable test profile and non-production data or credentials for live tests.

Risk: The skill includes persistent-memory guidance.

Mitigation: Review what will be retained and exclude secrets and sensitive user data.

## Reference(s):

- [Version gate](artifact/references/00-version-gate.md)
- [Plugin templates](artifact/references/02-templates.md)
- [API cookbook](artifact/references/03-api-cookbook.md)
- [Workflow and packaging](artifact/references/06-workflow.md)
- [Common pitfalls](artifact/references/05-pitfalls.md)
- [Version history](artifact/references/13-version-history.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code examples, shell commands, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.11.0 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
