## Description:

Orchestrates configured OpenClaw agents by classifying tasks, resolving ambiguity, selecting specialist agents, planning execution, and aggregating results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staok](https://clawhub.ai/user/staok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route complex prompts to installed specialist agents, choose single or multi-agent execution plans, and aggregate the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup relies on unpinned third-party install scripts.

Mitigation: Review the external agency-agents-zh repository before installation, pin to a reviewed commit when possible, and install in a restricted environment.

Risk: Routine use can share task content with sub-agent sessions and web searches.

Mitigation: Avoid routing sensitive prompts unless sharing that content with selected agents and live research tools is acceptable.

## Reference(s):

- [Agency Agents Router on ClawHub](https://clawhub.ai/staok/skills/agency-agents-router)
- [agency-agents-zh setup guide](https://github.com/jnMetaCode/agency-agents-zh#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
- [agency-agents upstream](https://github.com/msitarzewski/agency-agents)
- [Agency Orchestrator](https://github.com/jnMetaCode/agency-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands and structured orchestration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May delegate task content to sub-agent sessions and recommend live web research for factual or time-sensitive work.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
