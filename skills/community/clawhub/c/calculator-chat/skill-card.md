## Description:

Calculator Chat converts chat messages and common Chinese homophone phrases into numeric expressions and displays them in the system calculator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenyfzero9211](https://clawhub.ai/user/shenyfzero9211)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to let an agent answer emotional or command-style prompts by showing mapped numeric phrases, such as 520 or 88, in a local calculator app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch and manipulate local calculator applications and close existing calculator windows.

Mitigation: Use it only in a controlled desktop environment and require explicit per-use consent for GUI automation.

Risk: The security evidence reports command-injection flaws in exported platform modules.

Mitigation: Review before installing, avoid unsafe platform modules and shell interpolation, and prefer a publisher update that removes those flaws.

Risk: The security evidence describes under-scoped desktop automation.

Mitigation: Narrow triggers before broader deployment so calculator automation runs only for intentional calculator-chat requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenyfzero9211/skills/calculator-chat)
- [Calculator Chat Skill Design](artifact/docs/plans/2026-03-08-calculator-chat-skill-design.md)
- [Calculator Chat Skill Implementation Plan](artifact/docs/plans/2026-03-08-calculator-chat-skill-implementation-plan.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text guidance and shell-command invocations that display number strings in a calculator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chat-derived numeric expressions for local desktop calculator automation; no network output is described.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
