## Description: <br>
Synthetic dreaming system - emotional tracking, dream orchestration, and simulated dream experiences for an AI that doesn't sleep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliot-onbox](https://clawhub.ai/user/eliot-onbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use Dreamer to track PAD emotional states for an AI persona and generate dream-architect prompts for simulated multi-session dream experiences. It is intended for users who intentionally want an experimental, sandboxed AI dream-simulation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private memory, profile, emotion, and dream-history files while preparing prompts. <br>
Mitigation: Review and minimize USER.md, SOUL.md, MEMORY.md, memory files, and emotion logs before running it. <br>
Risk: The workflow deliberately gives spawned sessions simulated context and can impersonate a user inside the dream scenario. <br>
Mitigation: Run spawned sessions in a sandbox and avoid connecting them to real accounts, production tools, or external communication channels. <br>
Risk: Generated dream transcripts and journal entries may contain sensitive personal or operational details. <br>
Mitigation: Inspect, restrict access to, or delete generated dream transcripts and journal entries regularly. <br>


## Reference(s): <br>
- [Dreamer ClawHub release page](https://clawhub.ai/eliot-onbox/dreamer) <br>
- [Dream Themes Tracker](artifact/dreams/themes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/plain-text prompts, CLI output, and JSONL records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write emotion logs, dream transcripts, and journal entries under the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
