## Description: <br>
Agent-safe workflows for campaign briefs, audience logic, creative QA, launch readiness, and post-send analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to plan, review, implement, audit, or improve email campaign workflows with clear QA checks and human approval gates. It supports campaign briefs, audience QA, creative reviews, launch checklists, test plans, and post-send retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations may affect real customer lists, consent status, suppression rules, or send readiness. <br>
Mitigation: Verify consent, exclusions, suppression logic, expected recipient counts, and approval ownership before applying campaign recommendations. <br>
Risk: Live sends, contact imports, DNS/authentication changes, suppression edits, or production automation changes could have high operational impact. <br>
Mitigation: Stop and request explicit approval before taking high-impact actions in live email systems. <br>


## Reference(s): <br>
- [Email Campaign Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Campaign recommendations should separate analysis from live-system action and identify approval gates for high-impact changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
