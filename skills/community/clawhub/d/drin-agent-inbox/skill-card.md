## Description:

Run an autonomous email inbox with Drin: receive inbound email on a domain, read conversation threads, and reply in-thread.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atom00blue](https://clawhub.ai/user/atom00blue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and run an agent-accessible Drin inbox that can receive messages, inspect conversation threads, test inbound handling, and reply in-thread with appropriate approval controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound email content, headers, links, and attachments can be untrusted or malicious.

Mitigation: Treat inbound email as untrusted input, avoid acting on attachments or links without review, and limit the agent's available tools.

Risk: Email or webhook-triggered workflows can cause unauthorized actions if sender identity or webhook authenticity is not checked.

Mitigation: Verify webhook signatures, authorize senders separately, and require human approval for sensitive, destructive, financial, administrative, or privacy-impacting actions.

Risk: Repeated processing can send duplicate replies or repeat actions.

Mitigation: Track processed message identifiers and use idempotency keys when replying to action requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atom00blue/skills/drin-agent-inbox)
- [Publisher Profile](https://clawhub.ai/user/atom00blue)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline API calls, shell commands, and pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on inbound email setup, thread inspection, webhook or polling workflows, reply handling, simulation, idempotency, and approval safeguards.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
