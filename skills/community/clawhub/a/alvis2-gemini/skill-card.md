## Description: <br>
LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send one-shot prompts for Q&A, summarization, and text generation through the SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and supplied text are sent to SkillBoss API Hub and may be routed to downstream model providers. <br>
Mitigation: Do not use the skill with secrets, private records, regulated data, or confidential business content unless that vendor data flow has been approved. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Provide SkillBoss_API_KEY through a managed environment secret and avoid exposing it in prompts, logs, shell history, or checked-in files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis2-gemini) <br>
- [SkillBoss API endpoint](https://api.SkillBoss.co/v1/pilot) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, markdown, JSON-shaped text, or code snippets returned from a remote LLM API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and sends prompts to SkillBoss API Hub, which may route requests to downstream model providers.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
