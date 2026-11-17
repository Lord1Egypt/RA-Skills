## Description:

Route tasks to sub-agents with optimal model selection, error recovery, and result verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to decide when to delegate work to sub-agents, choose an appropriate model tier, provide scoped task context, recover from failed delegations, and verify returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated tasks may expose sensitive context to sub-agents when broad history or unnecessary files are included.

Mitigation: Keep delegated context minimal and send only the files or details needed for the sub-agent's task.

Risk: Timeout recovery can interrupt unfinished sub-agent work and logged state may contain private details.

Mitigation: Ping for status before terminating a sub-agent, retry only when the task remains necessary, and avoid placing sensitive details in recovery notes.

Risk: Sub-agent outputs can be incomplete, incorrectly formatted, or hallucinate files and sources.

Mitigation: Verify returned work by running tests or syntax checks, confirming files exist, spot-checking data, and confirming cited sources.

## Reference(s):

- [Delegate Skill Page](https://clawhub.ai/ivangdavila/skills/delegate)
- [Error Recovery Patterns](artifact/errors.md)
- [Spawn Templates](artifact/templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with structured checklists, tables, and task templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides delegation prompts, model-tier guidance, error recovery steps, and verification checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
