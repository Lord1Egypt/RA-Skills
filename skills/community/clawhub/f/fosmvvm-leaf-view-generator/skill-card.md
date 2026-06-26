## Description: <br>
Generate Leaf templates for FOSMVVM WebApps. Create full-page views and HTML-over-the-wire fragments that render ViewModels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foscomputerservices](https://clawhub.ai/user/foscomputerservices) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate Vapor Leaf full-page and fragment templates aligned with FOSMVVM ViewModels, including localized display values and HTML-over-the-wire update patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Leaf fragments can expose identifiers or state through data attributes that are visible to clients. <br>
Mitigation: Review generated HTML before use and include only identifiers and state values that are safe to expose client-side. <br>
Risk: Template proposals may be incorrect if the conversation context does not accurately describe the ViewModel, localization, or fragment type. <br>
Mitigation: Keep the request focused on the target ViewModel and verify generated templates against the actual server and ViewModel code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foscomputerservices/fosmvvm-leaf-view-generator) <br>
- [FOSUtilities homepage](https://github.com/foscomputerservices/FOSUtilities) <br>
- [Reference templates](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown with Leaf, HTML, Swift, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates template proposals from conversation context for user review before use.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
