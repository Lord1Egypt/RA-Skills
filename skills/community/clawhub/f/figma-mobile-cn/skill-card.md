## Description:

Converts Figma designs into mobile UI code for Android Jetpack Compose, Android XML, iOS SwiftUI, and iOS UIKit after fetching and interpreting Figma design structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn Figma links into native mobile UI implementation guidance and code. It helps analyze design hierarchy, clarify platform and layout ambiguity, optionally scan existing project resources, and generate Android or iOS UI code that can be iterated from user feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Figma personal access token, and insecure handling could expose design access credentials.

Mitigation: Configure FIGMA_TOKEN outside the chat through a trusted secret mechanism; do not paste tokens into conversation, avoid plaintext .env storage when possible, ensure any .env file is gitignored, and rotate tokens that were pasted, committed, logged, or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike47512/skills/figma-mobile-cn)
- [Figma community Material Design 3 Messaging App](https://www.figma.com/community/file/1169726503071187057/)
- [Figma interpretation rules](references/figma-interpretation.md)
- [Figma project scan usage](references/figma-scan-usage.md)
- [Code generation rules](references/code-generation.md)
- [Jetpack Compose mapping](references/platform-compose.md)
- [Android XML mapping](references/platform-xml.md)
- [SwiftUI mapping](references/platform-swiftui.md)
- [UIKit mapping](references/platform-uikit.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, shell commands, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform-specific mobile UI code for Jetpack Compose, Android XML, SwiftUI, or UIKit, plus optional project-scan and feedback-log guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
