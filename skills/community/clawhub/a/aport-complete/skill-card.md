## Description:

Verify a completed task against an APort passport's deliverable contract before marking it done, including acceptance criteria, summaries, test status, and reviewer checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uchibeke](https://clawhub.ai/user/uchibeke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill as a completion gate before closing tasks, tickets, issues, pull requests, or handoffs. It guides the agent to collect evidence, attest acceptance criteria, submit the verification request, and respond to allow or deny outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details, summaries, attestations, and optional output content may be sent to an external APort service.

Mitigation: Use only when APort is approved for the data involved, and avoid confidential code, customer data, regulated content, and secrets unless that processing is explicitly authorized.

Risk: The skill makes APort a remote gate for whether an agent may call work complete.

Mitigation: Adopt it only where that governance model is intended, and review deny reasons before retrying or changing task status.

Risk: The setup guidance includes an unpinned npx command.

Mitigation: Prefer a pinned and verified setup method when installing or provisioning APort tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uchibeke/skills/aport-complete)
- [APort passport](https://aport.id)
- [APort agent skill](https://aport.id/skill)
- [APort API documentation](https://aport.io/api/documentation)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with JSON examples, endpoint details, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include completion summaries, test status, criterion attestations, verification decision IDs, and retry guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
