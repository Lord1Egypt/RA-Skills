## Description:

Build multi-agent systems and swarms on AINative for dispatching OpenClaw agents, implementing agent communication, building autonomous handoffs, and collecting RLHF feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route coding, deployment, security, testing, documentation, data, and performance tasks across AINative/OpenClaw agents. It also provides patterns for agent-to-agent communication, custom API-backed agents, memory recall, and feedback collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples send prompts, conversation history, memory contents, recall queries, and feedback to AINative-hosted services.

Mitigation: Use only data approved for that provider, and avoid secrets, regulated data, customer data, proprietary code, and security findings unless the organization has approved the data flow.

Risk: The memory examples can persist user-derived content in cloud memory without clear consent or retention controls.

Mitigation: Establish consent, retention, deletion, and review procedures before enabling memory or feedback collection workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/ainative-agent-framework)
- [AINative chat completions API](https://api.ainative.studio/v1/public/chat/completions)
- [AINative memory remember API](https://api.ainative.studio/api/v1/public/memory/v2/remember)
- [AINative memory recall API](https://api.ainative.studio/api/v1/public/memory/v2/recall)
- [AINative RLHF feedback API](https://api.ainative.studio/api/v1/public/zerodb/rlhf/feedback)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, command examples, routing patterns, and operational guidance for agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
