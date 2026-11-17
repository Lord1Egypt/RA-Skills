## Description:

Generates complete Android app projects for CodeAssist using Kotlin, Jetpack Compose, Material 3, native module.toml configuration, Android resources, and package-ready project structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonio338854](https://clawhub.ai/user/antonio338854)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scaffold Android applications that can be imported into CodeAssist and built on-device. It is intended for requests to create Kotlin, Compose, Material 3, or CodeAssist-format Android app projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scaffolding and packaging workflows can write project files outside the intended folder when names or output paths are not constrained.

Mitigation: Use trusted app and package names, generate output in a dedicated workspace folder, and review generated paths before packaging or sharing files.

Risk: Documented shell commands may execute unintended operations if copied with raw or crafted user input.

Mitigation: Review commands before execution, quote or validate user-provided values, and avoid passing untrusted input directly into shell commands.

Risk: Generated Android manifests may include unnecessary network permissions or cleartext HTTP settings.

Mitigation: Remove unused Android permissions and avoid android:usesCleartextTraffic unless it is required and tightly scoped.

## Reference(s):

- [Dependencies and APIs](artifact/references/dependencies.md)
- [Config File Templates](artifact/references/config-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/antonio338854/skills/codeassist-kotlin-compose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance plus generated Android project files in Kotlin, XML, TOML, JSON, and ZIP packaging commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CodeAssist native Android project structure with module.toml, manifest.json, bundled dependency metadata, resource files, Kotlin sources, and packaging instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
