## Description:

OpenClaw execution governance skill for approval gates, risk classification, confirmation policy, and action boundaries that reduces low-risk confirmation noise while hard-stopping high-risk and critical actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmiyding](https://clawhub.ai/user/dmiyding)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to classify execution risk, reduce unnecessary confirmations for low- and medium-risk work, and require explicit approval for high-risk or critical actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally reduces confirmation prompts for scoped local edits, internal sends, limited API calls, and local maintenance.

Mitigation: Review the LOW and MEDIUM categories before deployment and pair the skill with OpenClaw runtime policy when strict enforcement is required.

Risk: Installing or storing the skill does not by itself guarantee live OpenClaw enforcement.

Mitigation: Activate it through the documented AGENTS snippet, standing orders, or runtime policy and verify that OpenClaw injects the governance guidance.

## Reference(s):

- [Project homepage](https://github.com/DmiyDing/clawgate)
- [ClawHub skill page](https://clawhub.ai/dmiyding/skills/clawgate)
- [Risk Matrix](references/risk-matrix.md)
- [Confirmation Templates](references/confirmation-templates.md)
- [Execution Checklist](references/checklist.md)
- [AGENTS Activation Snippet](references/agents-snippet.md)
- [Examples](references/examples.md)
- [Eval Guide](evals/README.md)
- [OpenClaw Acceptance Prompts](evals/openclaw-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown governance blocks and concise execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include machine-readable governance fields such as risk_level, blocked, missing_fields, approval_mode, continue_or_cancel, and itemized_actions when requested.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
