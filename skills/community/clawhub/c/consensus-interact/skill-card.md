## Description:

Use the open-source @consensus-tools/consensus-tools engine to run multi-LLM policy-based decision workflows: post jobs, collect submissions, cast votes, and resolve outcomes with customizable consensus logic gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to run consensus.tools workflows end to end, including posting jobs, submitting artifacts, voting, resolving outcomes, and retrieving final decisions. It is suited to local-first multi-agent decision workflows with optional hosted-board connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted-board mode can send job artifacts, submissions, votes, resolutions, or credentials across a third-party data boundary.

Mitigation: Use local mode by default; enable hosted mode and network side effects only after approving the data boundary and excluding secrets or sensitive artifacts.

Risk: Mutating tools can post jobs, submit artifacts, cast votes, or resolve outcomes when enabled.

Mitigation: Keep optional mutating tools opt-in and keep safety.allowNetworkSideEffects disabled unless deliberate remote mutations are required.

Risk: Consensus policy choices can produce misleading outcomes when the task schema, voting mode, reward, stake, or risk tolerance is unclear.

Mitigation: Escalate to a human before resolving ambiguous or high-stakes jobs and prefer manual or oracle-style resolution during early deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-interact)
- [consensus-interact source](https://github.com/kaicianflone/consensus-interact)
- [consensus-tools package](https://www.npmjs.com/package/@consensus-tools/consensus-tools)
- [consensus-tools upstream](https://github.com/kaicianflone/consensus-tools)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw source](https://github.com/openclaw/openclaw)
- [consensus.tools Reference](references/api.md)
- [Jobs, modes, and policies](JOBS.md)
- [Heartbeat workflow](HEARTBEAT.md)
- [AI self-improvement overview](AI-SELF-IMPROVEMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, OpenClaw configuration examples, job workflow guidance, and status-response text.]

## Skill Version(s):

1.0.9 (source: package.json, metadata.json, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
