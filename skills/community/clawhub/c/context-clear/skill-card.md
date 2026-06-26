## Description: <br>
Memory management system with automated tiered storage (hot/warm/gist/forgotten), time-decay organization, promotion engine, layer-search protocol, and session-injection plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slientrain-new](https://clawhub.ai/user/slientrain-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to manage local conversation memory across sessions, run /refresh to organize stored memories, and retrieve prior context through a hot/warm/gist/forgotten workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored conversation history can be automatically added into future prompts. <br>
Mitigation: Install only when persistent local memory is intended, and avoid storing secrets in ~/.openclaw/memory_fs. <br>
Risk: The /refresh workflow can organize memory files and old forgotten files may be permanently deleted after the retention window. <br>
Mitigation: Review or back up ~/.openclaw/memory_fs before running /refresh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/slientrain-new/context-clear) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [OpenClaw plugin manifest](artifact/plugin/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and OpenClaw plugin command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reuses local memory files under ~/.openclaw, including hot, warm, gist, and forgotten tiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and plugin/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
