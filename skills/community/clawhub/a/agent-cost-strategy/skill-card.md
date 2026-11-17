## Description:

Tiered model selection and cost optimization guidance for multi-agent AI workflows across AI providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose cost-appropriate models, route sub-agent and scheduled work, and apply prompt caching and batch processing patterns without losing sight of accuracy, safety, or privacy needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cost-focused defaults may route work to models that are too weak for accuracy, safety, or privacy-sensitive tasks.

Mitigation: Treat the tier rules as guidance and escalate model choice when task complexity, user impact, or safety sensitivity requires it.

Risk: Cached context can include workspace files, memory, secrets, or sensitive personal data.

Mitigation: Avoid caching sessions that contain secrets or sensitive personal data, and end those sessions when the privacy boundary matters more than cost savings.

Risk: Provider prices, cache behavior, batch discounts, TTLs, and model names can change.

Mitigation: Confirm current provider pricing and cache behavior before relying on the skill's example numbers in production workflows.

## Reference(s):

- [Cache Optimization Patterns](artifact/references/cache-optimization.md)
- [ClawHub skill page](https://clawhub.ai/djc00p/skills/agent-cost-strategy)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with routing tables, rules, and inline examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider pricing, model names, cache TTLs, and discounts should be checked against current provider documentation before operational use.]

## Skill Version(s):

1.3.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
