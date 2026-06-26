## Description: <br>
LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send one-shot prompts to SkillBoss API Hub for question answering, summarization, text generation, and JSON-style responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and text are sent to the external SkillBoss API Hub. <br>
Mitigation: Use the skill only when external processing is approved, avoid sending secrets or regulated personal data, and review SkillBoss privacy and billing terms. <br>
Risk: The skill requires a sensitive API key. <br>
Mitigation: Store SkillBoss_API_KEY in the agent environment, prefer a limited key where possible, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-gemini-v2) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>
- [SkillBoss pilot API endpoint](https://api.SkillBoss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and curl examples; API responses are text or JSON-like content from the external LLM service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and sends prompts to the SkillBoss API Hub.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
