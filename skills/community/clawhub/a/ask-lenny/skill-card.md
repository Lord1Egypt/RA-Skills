## Description: <br>
Ask Lenny helps agents answer product, growth, GTM, pricing, AI product, and leadership questions by searching Lenny Rachitsky podcast and newsletter archive material and synthesizing responses from cited passages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MyClaw-AI](https://clawhub.ai/user/MyClaw-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve and synthesize product and growth guidance from a local searchable archive of Lenny Rachitsky podcast and newsletter content. It is intended for questions that need grounded quotes, source attribution, and cross-guest synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script downloads public archive data from GitHub and stores a local searchable index. <br>
Mitigation: Review or pin the data source before setup in stricter environments. <br>
Risk: Broad trigger phrases can activate the skill unintentionally. <br>
Mitigation: Use explicit invocations such as '@lenny' when intentional activation matters. <br>
Risk: Answers may be incomplete or misleading if retrieved passages do not fully support the question. <br>
Mitigation: Require direct quotes and source attribution, and state when the archive does not contain a well-supported answer. <br>


## Reference(s): <br>
- [Ask Lenny on ClawHub](https://clawhub.ai/MyClaw-AI/ask-lenny) <br>
- [Guest Index](references/guest-index.md) <br>
- [MyClaw.ai](https://myclaw.ai) <br>
- [Lenny's Data](https://lennysdata.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON search results and Markdown answers with quoted source passages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns ranked archive chunks with guest, title, date, score, source, and text; default previews cap each chunk at about 2000 characters unless full output is requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
