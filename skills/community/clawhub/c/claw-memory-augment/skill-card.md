## Description: <br>
Long-term memory system for OpenClaw agents. Store, retrieve, and query conversation history and learned information across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist preferences, decisions, learnings, and session context across OpenClaw sessions, then retrieve those memories through search, listing, summaries, export, and import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories persist locally and may contain private user, project, or business context. <br>
Mitigation: Avoid storing passwords, API keys, personal identifiers, or sensitive business data, and periodically review ~/.memory-augment/storage.yaml. <br>
Risk: Automatic context injection can surface stored memories in later agent turns where they may be irrelevant or sensitive. <br>
Mitigation: Disable auto_inject or narrow its triggers when using the skill in sensitive workflows. <br>
Risk: Delete and import commands can remove or overwrite useful local memory data. <br>
Mitigation: Back up the memory file before bulk deletion or import operations. <br>


## Reference(s): <br>
- [Memory Types Reference](references/memory-types.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/indigas/claw-memory-augment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON command output with YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local YAML memory records and can export memories as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
