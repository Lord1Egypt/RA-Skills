## Description: <br>
Cost Guardian monitors OpenClaw API costs by estimating spend from session token usage, reporting model and session breakdowns, alerting against budgets, and recommending lower-cost routing for routine tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tso1079](https://clawhub.ai/user/tso1079) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw API spend, identify high-cost sessions or models, set budget alerts, and prepare daily or weekly cost reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost estimates depend on local session records and static model pricing, so reports can be inaccurate if provider prices or session formats change. <br>
Mitigation: Review the pricing table before relying on budget decisions and update the model pricing values when provider rates change. <br>
Risk: The reporting script reads local OpenClaw session data from the user's home directory. <br>
Mitigation: Run it only in trusted environments and avoid sharing generated reports if session labels or usage details may be sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tso1079/dex-cost-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include budget alerts, model cost breakdowns, top sessions, and routing recommendations based on local OpenClaw session data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
