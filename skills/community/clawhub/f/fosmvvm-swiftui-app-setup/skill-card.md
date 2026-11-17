## Description:

Set up the @main App struct for FOSMVVM SwiftUI apps, including MVVMEnvironment, deployment URLs, environment injection, and DEBUG test infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when starting or migrating SwiftUI applications that follow FOSMVVM architecture. It helps generate the main App struct, MVVMEnvironment configuration, deployment URL setup, resource bundle wiring, and optional UI test infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated app configuration can point at incorrect production, staging, or debug URLs.

Mitigation: Review deployment URL values before using generated App struct code in an application target.

Risk: Generated resource bundle or test view registrations can be incomplete for the target project.

Mitigation: Compare generated resourceBundles and registerTestingViews entries against the app's actual modules and ViewModelViews.

Risk: Optional UI choices such as forced dark mode may not match product requirements.

Mitigation: Review optional environment and color scheme settings before adopting the full template.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/foscomputerservices/skills/fosmvvm-swiftui-app-setup)
- [FOSUtilities Homepage](https://github.com/foscomputerservices/FOSUtilities)
- [Reference Templates](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with Swift code templates and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SwiftUI App struct templates and setup guidance for FOSMVVM applications.]

## Skill Version(s):

2.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
