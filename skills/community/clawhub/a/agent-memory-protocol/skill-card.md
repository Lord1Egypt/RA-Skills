## Description: <br>
Agent memory management protocol. Activate for any memory read, write, or update operation. Defines six-category write spec, L0 sync rules, and dedup strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ottoprua](https://clawhub.ai/user/ottoprua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents a consistent protocol for deciding what memory to persist, where to store it, how to deduplicate updates, and when to flush context before information is lost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may persist personal, project, or conversation data across sessions without clear consent or sensitivity boundaries. <br>
Mitigation: Define data that must never be stored, require confirmation before saving personal or sensitive details, and document how users can inspect, edit, exclude, and delete memories. <br>
Risk: Optional qmd and LosslessClaw integrations can expand where retained memory and conversation data is indexed or recovered. <br>
Mitigation: Review those integrations before enabling them, limit indexed paths to intended memory stores, and confirm retention expectations with users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ottoprua/agent-memory-protocol) <br>
- [Memory Stack Guide](MEMORY-STACK.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [qmd](https://github.com/tobilen/qmd) <br>
- [LosslessClaw](https://github.com/martian-engineering/lossless-claw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with file-path conventions, directory layouts, and inline shell/configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to create and update memory files, indexes, summaries, and related configuration according to the protocol.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
