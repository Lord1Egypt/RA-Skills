## Description: <br>
LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other external users use this skill to send one-shot prompts for Q&A, summarization, JSON generation, and general text generation through the hosted SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and included text are sent to SkillBoss's hosted service. <br>
Mitigation: Avoid secrets, regulated data, or proprietary content unless the organization has approved SkillBoss and the API-key scope. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store SkillBoss_API_KEY in the runtime environment or an approved secret manager, and rotate or scope the key according to organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-gemini-model) <br>
- [SkillBoss API Hub endpoint](https://api.SkillBoss.co/v1/pilot) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and curl examples, plus generated text or JSON responses from the API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the SkillBoss_API_KEY environment variable and sends prompts to SkillBoss's hosted service.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
