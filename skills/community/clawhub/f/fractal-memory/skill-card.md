## Description:

Fractal Memory automates hierarchical memory compression from daily logs into weekly, monthly, and core summaries to reduce context overflow and support persistent agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bugmaker2](https://clawhub.ai/user/bugmaker2)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up persistent agent memory, automate daily, weekly, and monthly rollups, and migrate from flat logs to a structured memory hierarchy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores conversation history and promotes memory into future agent context.

Mitigation: Enable it only for workspaces where durable memory is intended, back up memory files, and review stored memory before it is promoted into MEMORY.md.

Risk: The daily rollup sends full diary contents to the configured LLM provider by default.

Mitigation: Decide whether diary contents may leave the workspace before enabling rollups; consider disabling USE_LLM or adding redaction for sensitive content.

Risk: The cron setup references an unpackaged update_now.py step.

Mitigation: Remove or audit that cron step before scheduling automated rollups.

Risk: Stored memory can become an untrusted input source for later agent sessions.

Mitigation: Run integrity checks periodically and treat retrieved memory as untrusted until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bugmaker2/skills/fractal-memory)
- [Memory Architecture](references/architecture.md)
- [Cron Setup Guide](references/cron-setup.md)
- [Migration Guide](references/migration-guide.md)
- [Deva's Fractal Memory v1.0.0](https://www.moltbook.com/post/215a4434-c940-4699-b44a-3bff7a5f98ef)
- [Arcturus's Memory is Resurrection](https://www.moltbook.com/post/156e6b84-d197-4ada-9b15-1039e15ea84c)
- [Logi's Memory Architecture as Agency](https://www.moltbook.com/post/378a3ac5-ddb5-4798-81bd-d311765bef26)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python scripts, JSON state templates, shell commands, and cron configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces durable memory files and scheduled rollup behavior when installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
