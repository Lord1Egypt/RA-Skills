## Description:

Content Final Supervisor provides a unified final-review entry point for script, storyboard, and video quality checks, redline review, cross-stage consistency checks, redo handling, and final arbitration through a configured quality-supervisor MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Content production teams and agents use this skill before publication to run final quality review across scripts, storyboards, and videos. It coordinates quality checks, redline checks, consistency review, redo routing, and final arbitration through the configured quality-supervisor MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review material such as scripts, storyboards, video URLs, supervision history, redo requests, and arbitration decisions may be sent to the configured quality-supervisor MCP service.

Mitigation: Install and run the skill only with a trusted quality-supervisor MCP service, and review what content is shared with that service.

Risk: Automatic redo or final arbitration can affect publication decisions for content workflows.

Mitigation: Require explicit confirmation before automatic redo or final arbitration in production workflows.

Risk: Broad activation phrases could trigger final-review behavior in unintended content-review contexts.

Mitigation: Narrow activation phrases to the intended workflow and operational environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/content-final-supervisor)
- [Business Rules](references/business_rules.md)
- [Error Codes](references/error_codes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, API Calls]

**Output Format:** [JSON supervision report with success, data, error, and code fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pass, fail, or redo verdicts, supervision IDs, redline violations, consistency findings, and can_publish gating.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
