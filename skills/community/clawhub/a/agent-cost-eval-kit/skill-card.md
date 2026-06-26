## Description: <br>
Agent Token Cost Signal Kit - Find token waste, repeated calls, and risky routing changes before they become real cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review agent token usage, repeated calls, and routing changes before treating them as cost regressions. It supports read-only evaluation of before/after evidence and produces a status, risk level, and recommended next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive logs may be pasted while gathering token and session evidence. <br>
Mitigation: Redact sensitive data before sharing logs or session excerpts. <br>
Risk: Global or force installation can affect the wider OpenClaw installation. <br>
Mitigation: Use global or force install commands only when the skill is intended to apply beyond the current scope. <br>
Risk: Incomplete, mixed, or under-sampled evidence can make a cost recommendation misleading. <br>
Mitigation: Collect comparable before/after samples and perform read-only verification before changing routes, models, schedules, or production configuration. <br>


## Reference(s): <br>
- [Agent Cost Eval Kit public listing](https://clawhub.ai/choosenobody/agent-cost-eval-kit) <br>
- [Before/After Input Examples](references/before-after-examples.md) <br>
- [Evidence-First Skill Design](references/evidence-first-skill-design.md) <br>
- [OpenClaw Session Inspection Pattern](references/openclaw-session-inspection-pattern.md) <br>
- [ops_cat Quick Check Case Study](references/ops-cat-quick-check-case-study.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown status report with evidence, risk level, and recommended next action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance; does not edit configs, switch models, disable jobs, or delete cron tasks.] <br>

## Skill Version(s): <br>
2.4.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
