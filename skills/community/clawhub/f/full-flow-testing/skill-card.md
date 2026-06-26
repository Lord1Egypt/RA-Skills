## Description: <br>
Enterprise API testing assistant that supports developer self-tests, single API deep tests, business flow tests, security audits, defect diagnosis, and report generation with user confirmation before each step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaosiming](https://clawhub.ai/user/zhaosiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and API teams use this skill to plan and run user-confirmed API self-tests, deep tests, business-flow tests, security audits, defect diagnosis, and consolidated reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local workspaces and generated reports may contain credentials, request payloads, tokens, or customer data. <br>
Mitigation: Use dedicated test accounts and non-production tokens, keep workspace paths controlled, and review generated reports before sharing them. <br>
Risk: Shared knowledge-base updates may preserve sensitive or inaccurate API details if users confirm unsafe changes. <br>
Mitigation: Avoid confirming updates that include secrets, raw tokens, customer data, or unreviewed internal payloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaosiming/full-flow-testing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Files, Guidance] <br>
**Output Format:** [Markdown reports and structured testing guidance with API request and response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local user workspaces, session state, knowledge-base notes, and test report files when the user confirms each step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
