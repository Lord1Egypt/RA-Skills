## Description:

Spawn and orchestrate multiple coordinated AI sub-agents to work in parallel on complex tasks such as research, content generation, code review, data processing, and decision councils.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decompose large tasks, assign focused work to multiple sub-agents, collect results, and synthesize a single response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sub-agents can write shared workspace files or return outputs that are incorrect, stale, or inconsistent.

Mitigation: Review workspace writes and synthesized outputs before relying on them.

Risk: Persistent sub-agent sessions can accumulate context and increase token cost.

Mitigation: Prefer one-shot runs and use persistent sessions only when ongoing collaboration is needed.

Risk: Spawning too many sub-agents at once can make the environment unresponsive.

Mitigation: Batch work into small waves and use clear, focused prompts for each sub-agent.

## Reference(s):

- [Fuzzy Multi Agent Team on ClawHub](https://clawhub.ai/fuzzyb33s/skills/fuzzy-multi-agent-team)
- [fuzzyb33s publisher profile](https://clawhub.ai/user/fuzzyb33s)
- [Multi-Agent Team Templates](references/team-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and structured task instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sub-agent prompts, coordination plans, progress summaries, synthesized findings, and workspace file guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
