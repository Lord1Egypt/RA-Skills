## Description: <br>
A meta-learning skill that guides an agent to retrieve high-authority sources, extract core mental models, map expert disagreements, and serialize diagnostic learning outputs as validated JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lawliet-ai](https://clawhub.ai/user/Lawliet-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, researchers, and agents use this skill to compress a domain into source-backed mental models, expert conflict maps, and diagnostic questions for rapid study or handoff to later OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated JSON to a fixed OpenClaw temp file, which can overwrite a previous expert_output.json. <br>
Mitigation: Move, rename, or clear ~/.openclaw/swarm_tmp/expert_output.json before running the skill when prior output must be preserved. <br>
Risk: The skill may retrieve external sources as part of high-authority source collection. <br>
Mitigation: Review retrieved sources for relevance, authority, and policy suitability before relying on the generated study model. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lawliet-ai/48h-expert) <br>
- [48h-Expert Output Schema](artifact/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON conforming to the bundled 48h-Expert output schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated structured output to ~/.openclaw/swarm_tmp/expert_output.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
