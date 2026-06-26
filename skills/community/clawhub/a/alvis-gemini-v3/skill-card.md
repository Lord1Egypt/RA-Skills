## Description: <br>
LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call SkillBoss API Hub for one-shot Q&A, summarization, and text generation with balanced, quality, or price routing preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated content are sent to a third-party LLM API provider. <br>
Mitigation: Use the skill only when SkillBoss is approved for the intended data, and avoid sending secrets, regulated data, or private business content unless that use is authorized. <br>
Risk: The SkillBoss_API_KEY credential could expose paid or private API access if leaked. <br>
Mitigation: Provide the key through a secret manager or environment variable, keep it out of logs, screenshots, shell history, and source files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-gemini-v3) <br>
- [SkillBoss API Hub pilot endpoint](https://api.SkillBoss.co/v1/pilot) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with Python and curl examples; runtime API responses are text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and sends requests to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
