## Description: <br>
Control Brave Browser via CDP for web browsing, content extraction, screenshots, and JavaScript execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to attach to a user-managed Brave Browser instance for page inspection, web automation, content extraction, screenshots, and controlled JavaScript execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in Brave profile and may interact with personal sessions, form submissions, or private page data. <br>
Mitigation: Use a separate Brave profile or test browser with no personal sessions, and avoid accounts or pages where unintended actions or data capture would be harmful. <br>
Risk: Browser automation commands can click, type, publish, execute JavaScript, read cookies, or read storage in the attached browser. <br>
Mitigation: Review every interaction, publish-related command, and cookie or storage access before running it. <br>
Risk: Anti-detection and multi-framework click strategies may cause actions that are difficult to distinguish from direct user interaction. <br>
Mitigation: Prefer read-only content extraction first, and use interaction commands only when the intended target and effect are clear. <br>


## Reference(s): <br>
- [Brave Browser Agent on ClawHub](https://clawhub.ai/mayf3/brave-browser-agent) <br>
- [Common Patterns](references/PATTERNS.md) <br>
- [Framework-Aware Click Strategies](references/framework-publish.md) <br>
- [Site-Specific Patterns](references/site-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots or files when browser automation commands request them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
