## Description:

A meta-learning skill that directs an agent to build structured expertise maps from high-authority sources, including core mental models, expert debates, and diagnostic questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawliet-ai](https://clawhub.ai/user/lawliet-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compress a new domain into a structured learning artifact with authority sources, five mental models, expert conflict points, and diagnostic probes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated learning outputs are saved to a local handoff file that may be read by later audit skills.

Mitigation: Avoid private or sensitive topics unless local persistence is acceptable, and remove the handoff file after use when retention is not needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lawliet-ai/skills/48h-expert)
- [README](artifact/README.md)
- [Output Schema](artifact/schema.json)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Files]

**Output Format:** [JSON conforming to artifact/schema.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the structured learning output to ~/.openclaw/swarm_tmp/expert_output.json for local handoff.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
