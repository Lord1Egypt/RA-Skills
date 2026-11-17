## Description:

Generate UI tests for FOSMVVM SwiftUI views using XCTest and FOSTestingUI. Covers accessibility identifiers, ViewModelOperations, and test data transport.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate XCTest/FOSTestingUI scaffolding for FOSMVVM SwiftUI ViewModelViews, including UI state tests, operation-verification tests, helper extensions, and test support for interactive or display-only views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SwiftUI view and operations templates may be adopted as production architecture without sufficient review.

Mitigation: Review generated UI tests, SwiftUI view changes, operations protocols, and any real API or data-loading implementation before integrating them.

Risk: Sensitive values may be exposed if secrets are included in conversation or loaded code context used to generate tests.

Mitigation: Avoid providing secrets in prompts or source context, and scrub generated test data before committing generated files.

## Reference(s):

- [FOSMVVM UI Tests Generator on ClawHub](https://clawhub.ai/foscomputerservices/skills/fosmvvm-ui-tests-generator)
- [FOSUtilities homepage](https://github.com/foscomputerservices/FOSUtilities)
- [Reference Templates](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Swift code templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project setup, per-view UI test, ViewModelOperations, and SwiftUI test-support patterns that should be reviewed before adoption.]

## Skill Version(s):

2.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
