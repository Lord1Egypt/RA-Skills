## Description:

Desktop Agent Ops guides agents through verified, window-scoped desktop automation on macOS, Windows, and Linux, including setup, screenshots, OCR targeting, input actions, validation, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[appergb](https://clawhub.ai/user/appergb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to perform GUI tasks in native desktop apps when direct APIs are unavailable or unsuitable. It emphasizes scoped screenshots, OCR or template targeting, one-action-at-a-time execution, result verification, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires desktop screen-capture and input-control privileges.

Mitigation: Install only in environments where those permissions are acceptable, and keep actions scoped to the intended app window with screenshot verification before and after input.

Risk: Automatic setup can install packages, open permission settings, and run diagnostic screenshots or mouse movement.

Mitigation: Require explicit user approval before setup and review the setup steps before granting operating-system permissions.

Risk: The Windows clipboard command path was called out by security guidance for review.

Mitigation: Review or fix the Windows clipboard implementation before Windows use, then verify text input in a non-sensitive test window.

Risk: Unpinned dependencies or OCR assets can change desktop automation behavior over time.

Mitigation: Pin Python dependencies and OCR assets for release deployments, and rerun smoke tests after environment changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/appergb/skills/desktop-agent-ops)
- [Workflow](references/workflow.md)
- [Platform macOS](references/platform-macos.md)
- [Platform Windows](references/platform-windows.md)
- [Platform Linux](references/platform-linux.md)
- [Precise Targeting](references/precise-targeting.md)
- [Target Providers](references/target-providers.md)
- [Validation Patterns](references/validation-patterns.md)
- [Cleanup Rules](references/cleanup-rules.md)
- [Collaboration Rules](references/collaboration-rules.md)
- [Eval Scenarios](references/eval-scenarios.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for desktop control and may direct helper scripts that capture screens, move the pointer, click, type, inspect windows, run OCR, and clean task context.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
