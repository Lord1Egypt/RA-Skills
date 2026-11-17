## Description:

Create and maintain a Teams management page for OpenClaw Control UI, including named agent teams, parent/child nesting, indented tree rendering, collapsible team groups, parent selectors, and file-backed team registry persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, extend, fix, or document the OpenClaw Teams page, including team hierarchy UX, gateway methods, UI state, and file-backed team registry persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide changes to OpenClaw Teams UI, gateway code, runtime artifacts, and persistent team registry data.

Mitigation: Require source changes to be rebuilt, tested, deployed with backup and rollback, and verified against nested team save/load behavior before use.

Risk: The troubleshooting guidance can lead an operator toward direct patching of a live gateway runtime bundle.

Mitigation: Prefer source-level fixes and rebuilt runtime artifacts; allow direct live bundle patching only under explicit emergency operator control.

## Reference(s):

- [Teams Page UI Structure](references/ui-structure.md)
- [Teams Runtime Troubleshooting](references/runtime-troubleshooting.md)
- [Agent Team Organization on ClawHub](https://clawhub.ai/maverick-software/skills/agent-team-organization)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code, command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide edits to OpenClaw Teams UI, gateway handlers, runtime artifacts, and persistent team registry data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
