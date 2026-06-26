## Description: <br>
Auto Qa runs browser-based web QA flows in OpenClaw, captures failure evidence, generates decision reports, and prepares repair guidance for follow-up work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxvchaos](https://clawhub.ai/user/zxvchaos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and QA engineers use this skill to run web regression, smoke, demonstration, and release-gate checks, then review screenshots, console logs, network evidence, trace alignment, reports, and repair prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser screenshots, console logs, network logs, traces, and generated reports may include sensitive page data. <br>
Mitigation: Run against test or staging accounts when possible and avoid sensitive authenticated pages unless the destination and data-sharing expectations are clear. <br>
Risk: Report screenshots can be sent to an inferred recent chat channel by default. <br>
Mitigation: Disable automatic current-channel notification or provide an explicit notification target when report screenshots should not be shared automatically. <br>
Risk: Generated scenario JSON drives browser actions and assertions. <br>
Mitigation: Review generated scenario JSON before execution, especially when testing pages with account state, forms, or side effects. <br>


## Reference(s): <br>
- [AutoQA state snapshot](references/state_snapshot_20260220.md) <br>
- [ClawHub Auto Qa listing](https://clawhub.ai/zxvchaos/auto-qa) <br>
- [Publisher profile](https://clawhub.ai/user/zxvchaos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown, JSON reports, HTML reports, screenshots, trace artifacts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces QA evidence bundles, release decisions, fix plans, next-window prompts, standby prompts, and optional report screenshot notifications.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
