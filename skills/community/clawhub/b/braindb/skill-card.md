## Description:

Persistent, semantic memory for AI agents. Gives your AI long-term recall that survives compaction and session resets - 98% accuracy, 20ms latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chair4ce](https://clawhub.ai/user/chair4ce)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use BrainDB to add persistent semantic memory to OpenClaw agents so relevant facts, preferences, decisions, and workflows can be stored and recalled across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store personal, business, and conversation context.

Mitigation: Use the skill only when long-term local memory is appropriate, review what is captured, and export or remove stored memories when they are no longer needed.

Risk: Installation can modify OpenClaw configuration and run persistent Docker services.

Mitigation: Review install scripts before execution, verify the release artifact hash, and confirm the OpenClaw config changes and running containers after installation.

Risk: Optional swarm migration may send file contents to Google's Gemini API.

Mitigation: Use local-only migration options such as --no-swarm, --scan, and --dry-run unless external processing is explicitly acceptable.

Risk: Local services may expose or alter memories if left weakly protected.

Mitigation: Keep the gateway bound to localhost, enable BRAINDB_API_KEY authentication, and avoid exposing BrainDB ports beyond the local machine.

Risk: Execution-awareness encoding can add broad tool and environment memories.

Mitigation: Inspect proposed memories before running the execution-awareness encoder and avoid encoding sensitive environment details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chair4ce/skills/braindb)
- [BrainDB Documentation](https://github.com/Chair4ce/braindb#readme)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime memory recall is text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and Node. Normal operation is local, while optional migration with swarm may send file contents to Gemini.]

## Skill Version(s):

0.5.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
