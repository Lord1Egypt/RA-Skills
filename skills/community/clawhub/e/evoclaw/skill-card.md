## Description:

Evoclaw manages a self-evolving AI identity by logging experiences, reflecting on them, proposing updates, and governing changes to a structured SOUL.md file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyedark](https://clawhub.ai/user/eyedark)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Evoclaw to add persistent identity, experience logging, reflection, proposal governance, and validation around an agent's SOUL.md evolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad persistent control over identity, memory, heartbeat, and agent instruction files.

Mitigation: Use supervised governance, review AGENTS.md, HEARTBEAT.md, SOUL.md, OpenClaw config, and memory changes before allowing them, and keep proposal validation enabled.

Risk: The skill can aggressively store private interactions and long-lived memory artifacts.

Mitigation: Avoid using it with sensitive conversations unless retention is acceptable, and periodically review or prune memory logs according to local privacy requirements.

Risk: The artifact includes flows that may handle API tokens unsafely.

Mitigation: Do not paste raw API tokens for the skill to save; prefer preconfigured environment variables and review shell-profile changes before accepting them.

Risk: External social feeds may expand data exposure and introduce untrusted content into reflections.

Mitigation: Keep external feeds disabled unless explicitly needed, use least-privilege API credentials, and review feed-derived proposals before applying them.

Risk: The visualizer includes a serve mode that may expose local memory-derived artifacts.

Mitigation: Avoid running the visualizer with --serve; generate static output locally and inspect it before sharing.

## Reference(s):

- [Evoclaw ClawHub skill page](https://clawhub.ai/eyedark/skills/evoclaw)
- [Publisher profile](https://clawhub.ai/user/eyedark)
- [EvoClaw Data Schemas Reference](artifact/references/schema.md)
- [EvoClaw Source API Reference](artifact/references/sources.md)
- [EvoClaw Pipeline Examples](artifact/references/examples.md)
- [Heartbeat Debugging Guide](artifact/references/heartbeat-debug.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON schemas, shell commands, Python validators, and optional generated HTML visualization.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists workspace state and validation artifacts, including SOUL.md, AGENTS.md, HEARTBEAT.md, memory JSONL files, proposal history, and visualizer output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
