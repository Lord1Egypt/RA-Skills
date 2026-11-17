## Description:

AI window switching skill for locating and activating target Windows windows, with fuzzy matching, process and handle activation, JSON results, and tab-switch fallback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddmy](https://clawhub.ai/user/ddmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find, disambiguate, and activate running Windows application windows or browser/editor tabs from natural-language requests. It is intended for workflows where an agent should list candidate windows, confirm ambiguous matches, and execute focus changes through the provided command surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enumerate visible window titles, which may expose sensitive application or document names.

Mitigation: Use explicit app names where possible, avoid listing windows in sensitive sessions, and review returned candidates before sharing or storing output.

Risk: The skill can automatically change the active window or tab, which may disrupt user context or target the wrong application when aliases are ambiguous.

Mitigation: Require confirmation for short or ambiguous aliases and follow the documented find-window before activate-window workflow.

Risk: The security guidance notes missing d-switch.ps1 and d-switch.cmd files in the package, while the shell wrapper expects the PowerShell script.

Mitigation: Verify the Windows entry scripts are present and tested before relying on the package for automation.

## Reference(s):

- [Dkey Switch ClawHub Page](https://clawhub.ai/ddmy/skills/dkey-switch)
- [Usage Patterns](artifact/references/usage-patterns.md)
- [AI E2E Cases](artifact/references/ai-e2e-cases.md)
- [Onboarding Flow](artifact/references/onboarding-flow.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON result handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused; prefers --json outputs for agent parsing and confirmation before ambiguous activation.]

## Skill Version(s):

1.1.4 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
