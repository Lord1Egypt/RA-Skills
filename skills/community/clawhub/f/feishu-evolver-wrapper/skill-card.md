## Description:

Feishu Evolver Wrapper manages capability-evolver lifecycle tasks, Feishu card reporting, dashboard visualization, history export, and watchdog checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autogame-17](https://clawhub.ai/user/autogame-17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running capability-evolver use this skill to start, stop, monitor, and report evolution cycles through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact automatic actions may affect repositories or long-running workspace state.

Mitigation: Use only in a sandboxed or dedicated repository, disable automatic Git pushes, and make watchdog persistence explicit and removable before installation.

Risk: Dynamic evaluation and shell execution can broaden execution risk.

Mitigation: Remove dynamic eval and validate OpenClaw CLI paths without shell execution.

Risk: Automatic npm healing may change dependencies without an explicit operator decision.

Mitigation: Make npm auto-healing opt-in and review dependency changes before use.

Risk: Feishu-bound reports and exports may expose sensitive workspace content or reach unintended destinations.

Mitigation: Limit and redact all Feishu-bound content and restrict configured destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autogame-17/skills/feishu-evolver-wrapper)
- [ClawHub publisher profile](https://clawhub.ai/user/autogame-17)
- [Feishu IM messages API](https://open.feishu.cn/open-apis/im/v1/messages)
- [Feishu Docx documents API](https://open.feishu.cn/open-apis/docx/v1/documents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, CLI status text, Feishu interactive cards, dashboard markdown, and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send reports, dashboard content, or history exports to Feishu when credentials and target IDs are configured.]

## Skill Version(s):

1.8.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
