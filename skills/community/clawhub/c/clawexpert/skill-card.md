## Description:

EverClaw turns OpenClaw into a persistent domain expert that researches topics, builds a local indexed knowledge base, and answers future questions with citations from collected sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edgepro001](https://clawhub.ai/user/edgepro001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use EverClaw to run long-running topic research, maintain a local knowledge base, and answer domain questions from stored source-backed notes instead of relying only on model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently affect future answers by reading and writing a local knowledge base and session state.

Mitigation: Install only when persistent research memory is desired, keep proactive mode off unless topic tracking is acceptable, and periodically review or delete local knowledge and state files.

Risk: Autonomous research, inherited subagents, cron or auto modes can consume time and resources.

Mitigation: Avoid cron and auto modes until resource use is understood, constrain runtime with documented options, and restrict the sandbox and knowledge directory.

Risk: Path-based forget and cleanup workflows can remove local files if paths resolve outside the intended knowledge base.

Mitigation: Before using deletion workflows, confirm the resolved path is inside the intended knowledge base.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edgepro001/skills/clawexpert)
- [Metadata Homepage](https://github.com/EdgePro001/ClawExpert)
- [Subagent Prompt Reference](references/subagent-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, status summaries, citations, and generated knowledge-base files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local knowledge-base content, topic indexes, progress files, and source-backed answer summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
