## Description:

claw-code is a TypeScript runtime port of Claude Code's agent harness for routing prompts, managing sessions, querying tool and command registries, and auditing parity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dae-xiaoe](https://clawhub.ai/user/dae-xiaoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to inspect and exercise a TypeScript port of an agent harness, including command and tool registry queries, prompt routing, session bootstrap, turn-loop simulation, and parity auditing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake prototype or simulator behavior for a full secure runtime.

Mitigation: Treat the release as a harness prototype and review persistence, remote modes, and prefetch hooks before using it with private prompts or production systems.

Risk: Session and prompt-routing commands may expose sensitive context if future implementations add real persistence or remote behavior.

Mitigation: Use non-sensitive prompts in controlled workspaces until storage paths, remote-mode behavior, and data handling have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dae-xiaoe/skills/claw-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include registry summaries, manifest data, command graphs, tool listings, prompt-routing results, setup reports, and session-related text.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
