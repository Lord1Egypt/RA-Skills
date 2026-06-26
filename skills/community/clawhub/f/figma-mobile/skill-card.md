## Description: <br>
Converts Figma designs into mobile UI code for Android Jetpack Compose, Android XML, iOS SwiftUI, and UIKit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn Figma design links into mobile UI code. It helps inspect Figma structure, ask targeted clarification questions, and produce platform-specific UI implementation guidance or code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Figma Personal Access Token and the artifact instructions include chat-based token collection and local .env storage. <br>
Mitigation: Configure FIGMA_TOKEN through a secure environment or secret manager, never paste real tokens into chat, keep .env out of version control, and rotate the token if exposure is suspected. <br>
Risk: Generated mobile UI code may not match project conventions or may introduce unsuitable resources, layout choices, or component mappings. <br>
Mitigation: Review generated code before use, run project-specific checks, and inspect feedback-log.md or scan-report.json before committing or sharing changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawkk/figma-mobile) <br>
- [Code Generation Rules](artifact/references/code-generation.md) <br>
- [Figma Interpretation Rules](artifact/references/figma-interpretation.md) <br>
- [Figma Scan Usage](artifact/references/figma-scan-usage.md) <br>
- [Jetpack Compose Mapping](artifact/references/platform-compose.md) <br>
- [Android XML Mapping](artifact/references/platform-xml.md) <br>
- [SwiftUI Mapping](artifact/references/platform-swiftui.md) <br>
- [UIKit Mapping](artifact/references/platform-uikit.md) <br>
- [Figma Material Design 3 Messaging App Demo](https://www.figma.com/community/file/1169726503071187057/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated mobile UI source snippets, Figma structure summaries, clarification questions, scan reports, and token setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
