## Description: <br>
Helps agents design SaaS churn prevention strategies, including cancel flows, save offers, failed-payment recovery, and retention interventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External SaaS founders, product teams, and growth or retention teams use this skill to diagnose churn, design cancellation experiences, map save offers to cancellation reasons, and plan dunning workflows for failed payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read a local product-marketing context file that contains secrets or unrelated confidential business information. <br>
Mitigation: Review that context file before use and remove secrets or unrelated confidential material. <br>
Risk: Cancel-flow and dunning recommendations can create legal or compliance risk if they make cancellation difficult or apply high-friction retention handling inappropriately. <br>
Mitigation: Review recommendations with legal or compliance judgment and keep cancellation paths clear, especially for larger accounts or regulated markets. <br>


## Reference(s): <br>
- [Cancel Flow Patterns](references/cancel-flow-patterns.md) <br>
- [Dunning Playbook](references/dunning-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with tables, checklists, sample UX copy, and campaign timing recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May adapt recommendations from local product-marketing context when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
