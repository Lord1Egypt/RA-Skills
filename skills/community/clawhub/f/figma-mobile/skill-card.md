## Description:

Figma Mobile converts Figma designs into mobile UI code for Android Jetpack Compose/XML and iOS SwiftUI/UIKit, using the Figma REST API to inspect design structure before generating code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn Figma design links into mobile UI implementation guidance and code for Android and iOS. It fetches and summarizes Figma node structure, asks focused clarification questions when needed, and produces platform-specific UI code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask a user to paste a Figma access token into chat or save it to a local .env file.

Mitigation: Do not share the token in chat; configure FIGMA_TOKEN through a trusted environment or secret manager, keep .env files out of version control, and rotate any token that was exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/figma-mobile)
- [Figma community Material Design 3 Messaging App example](https://www.figma.com/community/file/1169726503071187057/)
- [Figma interpretation rules](artifact/references/figma-interpretation.md)
- [Figma scan usage](artifact/references/figma-scan-usage.md)
- [Code generation rules](artifact/references/code-generation.md)
- [Android Compose mapping](artifact/references/platform-compose.md)
- [Android XML mapping](artifact/references/platform-xml.md)
- [SwiftUI mapping](artifact/references/platform-swiftui.md)
- [UIKit mapping](artifact/references/platform-uikit.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with platform-specific code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated mobile UI files, resource suggestions, Figma structure summaries, clarification questions, SVG export commands, and feedback summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
