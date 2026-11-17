## Description:

Generate SwiftUI views that render FOSMVVM ViewModels and scaffold the ViewModelView pattern with bindings, loading states, validation, operations, and previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers use this skill to create SwiftUI view files for FOSMVVM applications after the corresponding ViewModel structure and interaction requirements are known. It helps produce display-only, interactive, form, async loading, list, and container views that follow FOSMVVM conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated action methods and form fields can affect application behavior when they call ViewModel operations or submit user data.

Mitigation: Review generated action methods, async submission flows, validation handling, and operation calls as normal application code before merging.

Risk: Incorrect ViewModel identity or binding choices can cause SwiftUI views to render stale data or fail to update as intended.

Mitigation: Check generated ViewModelView bindings, child app state mapping, and ViewModelId usage against the existing ViewModel definitions.

## Reference(s):

- [FOSMVVM SwiftUI View Generator on ClawHub](https://clawhub.ai/foscomputerservices/skills/fosmvvm-swiftui-view-generator)
- [Reference Templates](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with Swift code blocks and generated SwiftUI source patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated views depend on existing FOSMVVM ViewModels, operations, targets, and feature names supplied by the user or project context.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
