## Description: <br>
Converts Figma designs into mobile UI code for Android Jetpack Compose, Android XML, iOS SwiftUI, and iOS UIKit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to fetch Figma design structure, clarify layout choices, and generate native mobile UI code for Android or iOS. It is intended for workflows where a Figma access token and local project context are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Figma access token and may access proprietary design data. <br>
Mitigation: Use a least-privilege Figma token, configure it through a secure local secret mechanism, and avoid pasting tokens into chat. <br>
Risk: Token or project details could be exposed if stored in a repository .env file or feedback log. <br>
Mitigation: Ensure secret files are ignored by version control, and delete or sanitize feedback logs that contain proprietary code or design details. <br>
Risk: Generated UI code may not fully match project conventions or design intent. <br>
Mitigation: Review generated code before use and validate it against the target app's component, resource, and security standards. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mike47512/figma-mobile-cn) <br>
- [Figma interpretation reference](artifact/references/figma-interpretation.md) <br>
- [Code generation reference](artifact/references/code-generation.md) <br>
- [Figma scan usage reference](artifact/references/figma-scan-usage.md) <br>
- [Android Compose mapping reference](artifact/references/platform-compose.md) <br>
- [Android XML mapping reference](artifact/references/platform-xml.md) <br>
- [SwiftUI mapping reference](artifact/references/platform-swiftui.md) <br>
- [UIKit mapping reference](artifact/references/platform-uikit.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated native mobile UI code blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on Figma API data, user clarification, and optional local project scans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
