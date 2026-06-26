## Description: <br>
Guides an agent through cross-platform desktop GUI workflows using screenshots, OCR, focused windows, helper scripts, verification loops, setup, and cleanup on macOS, Windows, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[appergb](https://clawhub.ai/user/appergb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need a main agent to operate desktop applications through visible GUI state, window focus, screenshots, OCR targeting, click/type actions, and post-action verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can set up dependencies and operate the user's live desktop with broad authority. <br>
Mitigation: Install only when live desktop automation is intended, review first-run setup, clear sensitive windows and clipboard contents, and require explicit confirmation before sending messages, changing settings, entering credentials, or performing irreversible actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/appergb/desktop-agent-ops) <br>
- [Workflow](references/workflow.md) <br>
- [Reproducible Setup](references/reproducible-setup.md) <br>
- [Platform macOS](references/platform-macos.md) <br>
- [Platform Windows](references/platform-windows.md) <br>
- [Platform Linux](references/platform-linux.md) <br>
- [Target Providers](references/target-providers.md) <br>
- [Validation Patterns](references/validation-patterns.md) <br>
- [Precise Targeting](references/precise-targeting.md) <br>
- [Evaluation Scenarios](references/eval-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command outputs, and file-oriented setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to guide an agent step by step and may include helper-script commands, screenshots or OCR result paths, validation notes, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
