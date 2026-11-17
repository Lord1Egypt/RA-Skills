## Description:

A-share paper-trading automation workflow for MX APIs. Use when user asks to run scheduled A-share mock trading, enforce risk limits (single position cap, total exposure cap, stale-order cancellation), generate daily review, or maintain Day/Balance/Daily Return tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youjunzhao](https://clawhub.ai/user/youjunzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-workflow operators use this skill to set up and run scheduled A-share paper-trading automation with MX APIs, including risk limits, stale-order cancellation, daily review JSON, and Day/Balance/Daily Return tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled paper-trading jobs may run at configured times without the operator noticing.

Mitigation: Confirm where scheduled jobs will be created and how to disable them before installing or running the workflow.

Risk: Workspace files such as runtime scripts, review JSON, and README tracking may be created or updated.

Mitigation: Review generated workspace scripts and confirm README updates should be allowed before execution.

Risk: The workflow requires MX API credentials.

Mitigation: Use an MX API key intended for paper trading only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youjunzhao/skills/a-share-claw)
- [MX API endpoint](https://mkapi2.dfcfs.com/finskillshub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration details, Python runtime file expectations, and JSON review-file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update workspace runtime files, create scheduled paper-trading runs, produce review JSON, and update a README day table.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
