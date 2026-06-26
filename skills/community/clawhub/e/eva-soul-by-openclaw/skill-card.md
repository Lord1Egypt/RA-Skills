## Description: <br>
Eva Soul is an OpenClaw cognitive plugin that adds personality, emotion, memory, character, concept extraction, pattern recognition, decision support, and knowledge graph tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catfei0518](https://clawhub.ai/user/catfei0518) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use Eva Soul to give an assistant persistent memory, emotion and personality state, decision support, active inquiry, dialogue compression, and knowledge graph utilities during assistant sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can retain raw conversation and memory data under ~/.openclaw/workspace/memory. <br>
Mitigation: Install only where long-term local memory is acceptable, avoid shared machines, narrow or review the configured memory path, and manually inspect or delete stored memory files as needed. <br>
Risk: Prompts and memory text may be sent to SiliconFlow when SILICONFLOW_API_KEY is configured. <br>
Mitigation: Do not configure SILICONFLOW_API_KEY unless external processing is intended and acceptable for the data being handled. <br>
Risk: Automatic memory behavior and migration cleanup can preserve or remove user data in ways users may not expect. <br>
Mitigation: Review autoMemory behavior, inspect stored files directly, and back up memory data before running migration or cleanup commands. <br>


## Reference(s): <br>
- [ClawHub Eva Soul release page](https://clawhub.ai/catfei0518/eva-soul-by-openclaw) <br>
- [Eva Soul documentation](https://eva.catx.ltd) <br>
- [English README](README_EN.md) <br>
- [Chinese README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Structured tool results, persisted JSON state, and plain-language assistant guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memory, emotion, personality, concept, pattern, and knowledge graph data under the configured OpenClaw memory path.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
