## Description:

Manages regression test planning, test case execution, defect fix verification, and regression reporting for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiciferyi](https://clawhub.ai/user/luiciferyi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, release managers, and agent operators use this skill to define regression scope, select test cases, verify defect fixes, record execution results, and produce release-oriented regression reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regression plans, defect verification records, and release recommendations may contain confidential defects, customer details, incident information, credentials, or production secrets if users include them in reports.

Mitigation: Confirm the target Feishu knowledge base is approved for that information, and omit credentials, customer data, production secrets, and confidential incident details unless the space is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luiciferyi/skills/agent-regression-testing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style plans, checklists, execution records, defect verification tables, and regression reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Feishu documents when the configured Feishu tools are available.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
