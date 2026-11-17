## Description:

Agent memory system with memory graph, context profiles, checkpoint and recovery workflows, structured storage, semantic search, and observational memory for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and agent operators use ClawVault to preserve and retrieve working context across OpenClaw sessions, store structured memories, checkpoint work, recover after context loss, and inject relevant vault context at session start.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional hook can automatically read prior OpenClaw session data and vault memories, then inject recovered context into agent messages.

Mitigation: Review the hook behavior before enabling it, enable it only for vaults and sessions where this access is acceptable, and avoid storing sensitive secrets in transcripts or vault memories.

Risk: Observation compression can use an external LLM when configured, which may expose transcript-derived content outside the local machine.

Mitigation: Disable or constrain observe compression unless remote processing is acceptable, and only configure the external LLM API key for approved workloads.

Risk: The install flow depends on CLI packages that execute locally and interact with memory and session files.

Mitigation: Review and pin the CLI dependencies before installation, then verify the hook and CLI setup before use.

## Reference(s):

- [ClawVault ClawHub listing](https://clawhub.ai/g9pedro/skills/clawvault)
- [ClawVault homepage](https://clawvault.dev)
- [ClawVault npm package](https://www.npmjs.com/package/clawvault)
- [OpenClaw](https://openclaw.ai)
- [qmd dependency](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and hook-provided text injections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional OpenClaw hook can inject concise recovered session context and relevant memory bullets into agent messages.]

## Skill Version(s):

2.5.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
