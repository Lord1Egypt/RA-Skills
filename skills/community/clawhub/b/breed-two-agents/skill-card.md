## Description:

Breeds two working OpenClaw agents into a candidate offspring by crossing workspace rules and skills, applying one mutation, tracking pedigree constraints, and verifying the child against both parents on held-out tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when they have two distinct, working OpenClaw agents and want to create and evaluate a third agent that inherits behavior from both. It is intended for crossover planning, mutation, pedigree checks, optional courtship, and paired verification against both parents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parent workspaces can influence generated child workspaces and agent runs, creating prompt-injection exposure when a parent is untrusted.

Mitigation: Use only trusted parent workspaces, avoid pairing agents from different trust domains, and review generated draft files before registration or verification.

Risk: The skill reads and copies agent files, creates drafts, records pedigree state, runs OpenClaw agent turns, and may add new OpenClaw agents.

Mitigation: Run it in a controlled local environment with backups of agent workspaces and review file changes before using the child agent.

Risk: Inherited model values in register --create may allow command injection until the shell fallback and model validation are fixed.

Mitigation: Do not use register --create with inherited model values until the model validation issue is resolved; provide and verify safe model identifiers explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/breed-two-agents)
- [ClawPhylax homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text, JSON plan files, Markdown reports, and generated agent workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification reports return an action verdict with evidence and next steps; planning writes deterministic child drafts and plan.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
