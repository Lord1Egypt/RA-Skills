## Description:

Helps teams deploy an agent that replies to leads from a workspace mailbox and checks unanswered email threads for a limited follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales-development teams and developers adapt this skill to deploy a lead-engagement agent that continues email threads, handles replies and opt-outs, and checks quiet threads for at most one follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent agent can send unintended or repeated email replies from a real workspace mailbox.

Mitigation: Before deployment, enforce recipient and thread limits, one send per wake, and safe memory handling; test replies and opt-outs, including adversarial messages.

Risk: A mailbox incurs recurring charges, and registering a new domain can incur a non-refundable charge.

Mitigation: Review the deployment plan and current prices, and obtain explicit approval before creating billable resources.

Risk: A reply sent from the wrong mailbox or without complete threading headers can break the conversation loop.

Mitigation: Keep the sending mailbox fixed and verify test replies stay in the same thread before production use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/agentic-engagement)
- [Cargo skill repository](https://github.com/getcargohq/gtm-skills)
- [Conversation loop reference](references/loop.md)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration guidance]

**Output Format:** [Threaded email replies and TypeScript resource definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for one send per wake, at most one unanswered follow-up, and no sends after an opt-out.]

## Skill Version(s):

0.1.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
