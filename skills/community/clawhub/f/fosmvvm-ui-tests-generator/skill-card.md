## Description: <br>
Generate UI tests for FOSMVVM SwiftUI views using XCTest and FOSTestingUI. Covers accessibility identifiers, ViewModelOperations, and test data transport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foscomputerservices](https://clawhub.ai/user/foscomputerservices) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to create XCTest UI test scaffolding and per-view test patterns for FOSMVVM SwiftUI ViewModelViews, including accessibility identifiers, ViewModelOperations verification, and test data transport. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Swift test scaffolding or ViewModelOperations templates may not match the target app's view, operations type, bundle identifier, or business logic. <br>
Mitigation: Review generated diffs before committing and make the target view, operations type, and bundle identifier explicit before generation. <br>
Risk: Broad templates may include placeholders or assumptions that are unsuitable for a specific FOSMVVM project. <br>
Mitigation: Replace placeholders with project-specific values and verify generated tests against the app's actual UI flows. <br>


## Reference(s): <br>
- [FOSUtilities repository](https://github.com/foscomputerservices/FOSUtilities) <br>
- [ClawHub skill page](https://clawhub.ai/foscomputerservices/fosmvvm-ui-tests-generator) <br>
- [Reference templates](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Swift code templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces XCTest and FOSTestingUI scaffolding patterns for SwiftUI ViewModelViews.] <br>

## Skill Version(s): <br>
2.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
