## Description: <br>
LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to ask one-shot questions, summarize text, and generate content through SkillBoss API Hub with a configured API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and supplied text are sent to a third-party LLM API service. <br>
Mitigation: Avoid sending secrets, regulated data, or internal-only material unless policy allows it. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Use a dedicated, least-privilege API key and rotate it according to local credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alv-gemini) <br>
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and curl examples plus generated text responses from an API call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends prompts and supplied text to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
