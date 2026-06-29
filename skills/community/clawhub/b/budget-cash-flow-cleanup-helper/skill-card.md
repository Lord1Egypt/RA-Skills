## Description: <br>
Helps individuals, freelancers, family finance organizers, bookkeepers, and small business owners turn messy bank or card exports into categorized transactions, subscription reviews, budget plans, and cash-flow decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to clean up transaction exports, categorize spending, spot recurring subscriptions, and produce practical budget or cash-flow planning artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to trigger for adjacent budgeting or operations requests where it is not intended. <br>
Mitigation: Review invocation behavior during deployment and disable or narrow activation if it appears in unrelated workflows. <br>
Risk: Budgeting and transaction-cleanup tasks may involve sensitive financial records. <br>
Mitigation: Share only the records needed for the task, remove unnecessary account identifiers, and verify outputs before making financial decisions. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/budget-cash-flow-cleanup-helper) <br>
- [Publisher Profile](https://clawhub.ai/user/kyro-ma) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional code blocks, shell commands, checklists, templates, and analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no installed code, command execution, credential use, persistence, or external data transfer is reported in release security evidence.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
