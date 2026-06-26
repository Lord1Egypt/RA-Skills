## Description: <br>
CrabPet turns OpenClaw usage logs into a virtual pixel lobster pet with levels, moods, achievements, and shareable pet cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liqiwa](https://clawhub.ai/user/liqiwa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use this skill to view a persistent pet companion that reflects their activity history, generate status summaries, list achievements, and create shareable pet cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw memory logs to infer activity habits and personality traits. <br>
Mitigation: Install only when that local activity analysis is acceptable, and review the generated status or card content before sharing it. <br>
Risk: Shareable pet cards can contain derived activity data such as level, streak, achievements, mood, and personality labels. <br>
Mitigation: Treat generated cards as public-facing summaries and avoid sharing them when those derived signals reveal sensitive work patterns. <br>
Risk: PNG card generation can use local Chrome/Chromium execution and a web template that may request Google Fonts. <br>
Mitigation: Use text or Markdown card output when avoiding browser execution or external font requests is required. <br>


## Reference(s): <br>
- [CrabPet ClawHub listing](https://clawhub.ai/liqiwa/crabpet) <br>
- [CrabPet README](README.md) <br>
- [CrabPet Personality System](references/personality.md) <br>
- [CrabPet Design Notes](openclaw-ai-pet-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output, Markdown/text pet cards, optional PNG pet card files, and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw memory logs and writes persistent pet state and generated card files under the skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
