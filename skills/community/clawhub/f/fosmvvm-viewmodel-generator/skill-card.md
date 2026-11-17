## Description:

Generate FOSMVVM ViewModels for SwiftUI screens, pages, and components, including RequestableViewModel scaffolding, localization bindings, and stub factories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers use this skill to create SwiftUI ViewModel scaffolding for FOSMVVM applications, choosing server-hosted, client-hosted, or child ViewModel patterns based on the screen or component being built.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Swift source or localization YAML may use filenames, targets, or locales that do not match the receiving application.

Mitigation: Review generated filenames, module targets, resource paths, and locale keys before adding the output to a project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foscomputerservices/skills/fosmvvm-viewmodel-generator)
- [FOSUtilities repository](https://github.com/foscomputerservices/FOSUtilities)
- [ViewModel reference templates](artifact/reference.md)

## Skill Output:

**Output Type(s):** [code, configuration, markdown, guidance]

**Output Format:** [Markdown guidance with Swift and YAML code templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Swift source files, localization YAML, request types, and factory scaffolding depending on the selected ViewModel pattern.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
