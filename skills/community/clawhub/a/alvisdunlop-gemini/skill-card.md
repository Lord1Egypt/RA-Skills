## Description: <br>
LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to send one-shot prompts to SkillBoss API Hub for question answering, summarization, and text generation. It is suited for workflows where an agent should provide Python or curl examples for calling the hosted LLM endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and provided content are sent to the external SkillBoss hosted API. <br>
Mitigation: Use only with data you are allowed to share with SkillBoss, and avoid submitting secrets, credentials, private documents, personal data, or regulated data unless approved. <br>
Risk: The skill requires a sensitive API key for SkillBoss access. <br>
Mitigation: Store SkillBoss_API_KEY in a secure environment variable or secret store and do not embed it in prompts, code snippets, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvisdunlop-gemini) <br>
- [SkillBoss API endpoint](https://api.SkillBoss.co/v1/pilot) <br>
- [SkillBoss setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and curl examples; API responses may be text or JSON depending on the prompt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillBoss_API_KEY and sends prompts to the SkillBoss hosted API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
