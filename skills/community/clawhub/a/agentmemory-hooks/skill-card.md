## Description:

The agentmemory plugin hooks capture observations automatically across the agent session lifecycle for memory recall, recap, handoff, and session history workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to understand and configure automatic memory capture hooks that record prompts, tool activity, and session events without manual saves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable third-party hooks record prompts and tool activity by default, which may capture secrets, proprietary code, customer data, or private prompts.

Mitigation: Review what the plugin stores, where the localhost service persists data, how to delete records, how to disable hooks, and whether a pinned reviewed version can be installed before using it in sensitive workspaces.

Risk: Optional LLM summarization and context injection can spend tokens and reintroduce stored observations into later agent context.

Mitigation: Keep AGENTMEMORY_AUTO_COMPRESS and AGENTMEMORY_INJECT_CONTEXT disabled unless the workspace owner has reviewed the data flow and approved the token and privacy tradeoffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/agentmemory-hooks)
- [Server-resolved GitHub source](https://github.com/rohitg00/agentmemory/tree/main/plugin/skills/agentmemory-hooks)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes default automatic capture behavior and opt-in summarization or context injection settings.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
