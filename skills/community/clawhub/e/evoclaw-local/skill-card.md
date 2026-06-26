## Description: <br>
EvoClaw Local helps an AI agent maintain and evolve its SOUL.md identity through logged experiences, reflections, governed proposals, validation scripts, and optional social feed inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink-kai](https://clawhub.ai/user/ink-kai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced agent users install EvoClaw Local into a workspace so an agent can record experiences, reflect on them, propose identity updates, and validate changes to SOUL.md under a chosen governance mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records conversations and agent memory in workspace files. <br>
Mitigation: Install only in workspaces where persistent agent memory is intended, and review the memory directory contents before sharing or committing the workspace. <br>
Risk: The skill can change agent behavior files such as SOUL.md, AGENTS.md, and HEARTBEAT.md through its installation and proposal workflow. <br>
Mitigation: Use supervised or approval governance, inspect every proposed diff, and keep immutable CORE identity rules protected from direct edits. <br>
Risk: Optional external sources can use API credentials and fetch social feed content. <br>
Mitigation: Keep external sources disabled unless needed, store only environment variable names in configuration, avoid pasting raw tokens into prompts, and revoke tokens if they are exposed. <br>
Risk: The soul visualizer includes save behavior for SOUL.md and should not be treated as read-only. <br>
Mitigation: Use the visualizer only in a trusted local workspace and review SOUL.md after saving. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ink-kai/evoclaw-local) <br>
- [EvoClaw Configuration Guide](configure.md) <br>
- [EvoClaw Data Schemas Reference](references/schema.md) <br>
- [EvoClaw Pipeline Examples](references/examples.md) <br>
- [EvoClaw Source API Reference](references/sources.md) <br>
- [Heartbeat Debugging Guide](references/heartbeat-debug.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON/JSONL schemas, shell commands, configuration files, validator outputs, and generated local HTML visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and validates local memory, proposal, state, and SOUL.md files when installed and run by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
