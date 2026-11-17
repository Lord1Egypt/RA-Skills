## Description:

ExpertLens is a platform-agnostic reasoning skill that helps an agent diagnose the real task, adapt its reasoning to the domain, self-audit its output, and optionally coordinate multi-model review for complex work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashutosh2m](https://clawhub.ai/user/ashutosh2m)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use ExpertLens to make an LLM produce structured, domain-adapted analysis, recommendations, self-critique, and task-specific guidance instead of generic responses. It is intended for complex, creative, strategic, architectural, publishable, or high-stakes tasks rather than simple factual lookups or one-step edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous Swarm Mode can send broad task context to third-party AI services.

Mitigation: Disable or avoid Autonomous Swarm Mode for confidential work unless each external send shows the minimized prompt, destination, and account first.

Risk: The skill can activate a broad reasoning persona on many complex tasks.

Mitigation: Install it only where that broad reasoning posture is desired, and reserve simple factual or one-step tasks for normal agent behavior.

Risk: Memory, file, or feedback sends may store or transmit user context if approved.

Mitigation: Approve those actions only after reviewing exactly what will be written, stored, or sent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ashutosh2m/skills/expertlens)
- [Project homepage from ClawHub metadata](https://github.com/Ashutosh2M/ExpertLens)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted prose, lists, tables, and recommendations matched to the user's task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed schema; output shape follows the task and may include analysis, recommendations, self-critique, relay prompts, or implementation guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
