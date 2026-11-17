## Description:

Convert Figma designs to mobile UI code (Compose/XML/SwiftUI/UIKit/Flutter) via the Figma REST API with local resource scanning, multi-frame comparison, and feedback-log corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timeaground](https://clawhub.ai/user/timeaground)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to convert selected Figma frames into platform-idiomatic mobile UI code for Android Compose, Android XML, SwiftUI, UIKit, or Flutter. It can also scan local project resources with user approval so generated code can reuse existing colors, strings, images, and components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVG export can fetch unvalidated URLs outside the declared Figma API scope.

Mitigation: Review the skill before installing and prefer a version that validates SVG download hosts.

Risk: Installation pulls an unpinned Python dependency.

Mitigation: Install in an isolated environment and pin or review the requests dependency before production use.

Risk: Figma tokens, project scans, and feedback logs can expose sensitive design or source information.

Mitigation: Use a least-privilege Figma token, never paste it into chat, approve scans only for acceptable repositories, and decline feedback logging for sensitive corrections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timeaground/skills/figma-to-mobile)
- [Publisher profile](https://clawhub.ai/user/timeaground)
- [Figma API host](https://api.figma.com)
- [Figma community demo file](https://www.figma.com/community/file/1169726503071187057/)
- [GitHub issues](https://github.com/TimeAground/figma-to-mobile/issues)
- [Compose patterns](references/compose-patterns.md)
- [Android XML patterns](references/xml-patterns.md)
- [SwiftUI patterns](references/swiftui-patterns.md)
- [UIKit patterns](references/uikit-patterns.md)
- [Figma interpretation](references/figma-interpretation.md)
- [Project scan usage](references/scan-usage.md)
- [Multi-frame handling](references/multi-frame.md)
- [Error handling](references/error-handling.md)
- [Feedback logging](references/feedback-log.md)
- [Generation rules](references/generation-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with filename-labeled code blocks, shell commands, JSON scan reports, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated UI code files, scan-report.json after approved project scans, and feedback-log.md only after user consent.]

## Skill Version(s):

2.3.0 (source: frontmatter, changelog, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
