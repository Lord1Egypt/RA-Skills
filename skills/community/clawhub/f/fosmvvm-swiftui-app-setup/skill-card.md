## Description: <br>
Set up the @main App struct for FOSMVVM SwiftUI apps. Configures MVVMEnvironment, deployment URLs, and test infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foscomputerservices](https://clawhub.ai/user/foscomputerservices) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill when starting or migrating SwiftUI applications to FOSMVVM. It helps generate the main App struct, MVVMEnvironment setup, deployment URL configuration, environment injection, and optional DEBUG-only UI test infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Swift files may contain placeholder production or debug URLs. <br>
Mitigation: Replace placeholder URLs with reviewed project endpoints before using the generated App struct. <br>
Risk: DEBUG-only test hooks and Info.plist deployment settings may not match the target project's release process. <br>
Mitigation: Confirm test infrastructure, deployment keys, and build configuration behavior against the app's CI and release settings. <br>
Risk: Template output can introduce incorrect assumptions about app bundles, resource bundles, or deployment environments. <br>
Mitigation: Review generated Swift and configuration changes before committing or shipping them. <br>


## Reference(s): <br>
- [FOSMVVM SwiftUI App Setup Reference Templates](reference.md) <br>
- [FOSUtilities](https://github.com/foscomputerservices/FOSUtilities) <br>
- [ClawHub Release Page](https://clawhub.ai/foscomputerservices/fosmvvm-swiftui-app-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Swift code templates and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-specific SwiftUI App setup guidance using conversation and codebase context.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
