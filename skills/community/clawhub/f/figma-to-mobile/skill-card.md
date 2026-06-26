## Description: <br>
Converts Figma designs into production-ready mobile UI code for Android Jetpack Compose/XML and iOS SwiftUI/UIKit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timeaground](https://clawhub.ai/user/timeaground) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and mobile engineers use this skill to convert selected Figma frames into copy-pasteable Android or iOS UI code, with clarifying questions for platform, repeated content, and component choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Figma personal access token and can access design data through the Figma API. <br>
Mitigation: Set FIGMA_TOKEN in the local environment or a secrets manager; do not paste tokens into chat and keep any .env file ignored by git. <br>
Risk: Project scanning can inspect broad local app resources, including private strings or assets outside the intended target. <br>
Mitigation: Run project_scan.py only against the intended project and module, review the scan report before use, and avoid scanning unrelated private repositories. <br>
Risk: Generated mobile UI code may approximate complex Figma visuals or use placeholders for photos and bitmaps. <br>
Mitigation: Review generated code and rendered UI before merging; replace placeholders and manually verify complex gradients, shadows, resources, and component behavior. <br>


## Reference(s): <br>
- [Figma Interpretation](references/figma-interpretation.md) <br>
- [Generation Rules](references/generation-rules.md) <br>
- [Project Scan Usage Guide](references/scan-usage.md) <br>
- [Compose Patterns](references/compose-patterns.md) <br>
- [Android XML Patterns](references/xml-patterns.md) <br>
- [SwiftUI Patterns](references/swiftui-patterns.md) <br>
- [UIKit Patterns](references/uikit-patterns.md) <br>
- [Material Design 3 Messaging App Demo Source](https://www.figma.com/community/file/1169726503071187057/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file headers, code blocks, short analysis, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIGMA_TOKEN for Figma API access and can optionally inspect local mobile project resources when project scanning is requested.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
