## Description: <br>
Agent Governance Auditor evaluates agent specifications for governance risks, scores six dimensions, and produces actionable gap findings and improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and governance reviewers use this skill to audit SOUL.md files, system prompts, configurations, or agent descriptions before deployment. It identifies missing scope, oversight, memory, security, decision-making, and accountability controls and returns prioritized remediation language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Governance scores and recommendations may be treated as final approval for deployment. <br>
Mitigation: Use the report as advisory input and require human review before production rollout, especially for high-stakes or autonomous agents. <br>
Risk: Users may paste secrets, private credentials, or unreleased sensitive prompts into the audit session. <br>
Mitigation: Remove secrets and confidential material before analysis unless the agent session is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/filipbl4gojevic/agent-governance-auditor) <br>
- [Scoring rubric](artifact/references/scoring-rubric.md) <br>
- [Common governance gaps](artifact/references/common-gaps.md) <br>
- [Audit report template](artifact/templates/audit-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown governance audit report with score tables, findings, risk profile, and paste-ready remediation language] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores six governance dimensions on a 0-100 scale and may add special handling for short, low-stakes, high-stakes, or multi-agent specifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
