## Description:

CoolSkill Builder converts natural-language requirements, API documents, GitHub repositories, and code snippets into standardized zero-dependency skill packages with generated implementation files, tests, manifests, registry metadata, and security-check guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredtai](https://clawhub.ai/user/fredtai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert source material into reusable skill modules with a fixed Python run interface, cross-agent manifests, local registry entries, tests, and security scan guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can write generated files and local registry entries.

Mitigation: Use it in a disposable or version-controlled workspace and review generated files before keeping or publishing them.

Risk: Generated Python implementations and tests may be untrusted code.

Mitigation: Review and scan generated code, then run tests in a sandbox or container before deployment.

Risk: Optional GitHub sync can use environment credentials.

Mitigation: Use least-privilege tokens, avoid exposing broad credentials in the environment, and require explicit confirmation before registry or GitHub writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fredtai/skills/coolskill-builder)
- [ZeroSkill-Forge specification](artifact/references/spec.md)
- [File templates](artifact/references/file-templates.md)
- [Security rules](artifact/references/security-rules.md)
- [Registry format](artifact/references/registry-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with generated file contents and inline command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated skill package files and registry entries when used as directed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
